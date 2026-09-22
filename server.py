#!/usr/bin/env python3
"""
Serveur local Flask minimal sécurisé pour Asta Académie
- écoute 127.0.0.1:5000
- protection anti-LFI
- route /api/space-ai/chat (RAG local sur .txt)
- route /api/admin/clean pour purge
- route /api/stats
"""

from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from pathlib import Path
import os
import re
import shutil
import time
import sqlite3
import hashlib
import binascii
import hmac
import base64
import json
from datetime import datetime

APP_DIR = Path(__file__).parent.resolve()
NOTES_DIR = APP_DIR / "student_notes"
TMP_DIR = APP_DIR / "tmp"
DATA_DIR = APP_DIR / "data"
DB_FILE = DATA_DIR / "asta_database.db"

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB

# --- Helpers
ALLOWED_EXT = {'.txt'}
KEYWORDS_RE = re.compile(r"\b([a-zA-Z]{3,})\b")


def is_safe_path(base: Path, path: Path) -> bool:
    try:
        base = base.resolve()
        path = path.resolve()
        return str(path).startswith(str(base))
    except Exception:
        return False


def list_local_texts():
    NOTES_DIR.mkdir(exist_ok=True)
    return list(NOTES_DIR.glob('**/*.txt'))


def rag_answer(query: str) -> str:
    """Recherche simple de passages contenant tokens communs et compose une réponse.
    Cette implémentation garde tout local: pas d'appel externe."""
    tokens = set([t.group(1).lower() for t in KEYWORDS_RE.finditer(query)])
    candidates = []
    for p in list_local_texts():
        try:
            text = p.read_text(encoding='utf-8', errors='ignore')
            lowered = text.lower()
            score = sum(1 for tk in tokens if tk in lowered)
            if score > 0:
                candidates.append((score, p, text))
        except Exception:
            continue
    candidates.sort(reverse=True, key=lambda x: x[0])
    if not candidates:
        return "Désolé — je n'ai pas trouvé d'information locale pertinente. Essaie de reformuler ou ajoute des documents de révision dans 'student_notes'."

    best = candidates[0]
    snippet = best[2][:2000]
    return f"Réponse basée sur '{best[1].name}':\n\n{snippet}\n\n(Contexte local fourni)"


# --- Routes
@app.route('/api/space-ai/chat', methods=['POST'])
def space_ai_chat():
    data = request.get_json(silent=True) or {}
    q = data.get('question') or data.get('q') or ''
    if not q or not isinstance(q, str):
        return jsonify({'error': 'question manquante'}), 400
    # simple RAG local
    ans = rag_answer(q)
    return jsonify({'answer': ans})


@app.route('/api/admin/clean', methods=['POST'])
def admin_clean():
    # authentification: accepte clé statique ou token JWT
    if not _is_admin_request(request):
        return jsonify({'error': 'non autorisé'}), 403

    removed = []
    # nettoyer tmp
    if TMP_DIR.exists():
        for p in TMP_DIR.glob('**/*'):
            try:
                if p.is_file():
                    p.unlink()
                    removed.append(str(p))
                elif p.is_dir():
                    shutil.rmtree(p)
                    removed.append(str(p))
            except Exception:
                continue
    # .pyc
    for p in APP_DIR.rglob('*.pyc'):
        try:
            p.unlink()
            removed.append(str(p))
        except Exception:
            continue
    # logs > 30 jours
    for p in APP_DIR.rglob('*.log'):
        try:
            if time.time() - p.stat().st_mtime > 30 * 24 * 3600:
                p.unlink()
                removed.append(str(p))
        except Exception:
            continue

    return jsonify({'removed': removed, 'count': len(removed)})


@app.route('/api/stats', methods=['GET'])
def stats():
    users = 0
    # heuristique: count fichiers de profil si présents
    profiles = list(APP_DIR.glob('profiles/*.json')) if (APP_DIR / 'profiles').exists() else []
    users = len(profiles)
    notes = len(list_local_texts())
    return jsonify({'users': users, 'notes': notes})


@app.route('/api/file/read', methods=['GET'])
def file_read():
    # read only from student_notes and only secure filenames
    name = request.args.get('name', '')
    if not name:
        return jsonify({'error': 'name missing'}), 400
    safe = secure_filename(name)
    path = NOTES_DIR / safe
    if not is_safe_path(NOTES_DIR, path) or path.suffix.lower() not in ALLOWED_EXT or not path.exists():
        return jsonify({'error': 'file inaccessible'}), 403
    try:
        text = path.read_text(encoding='utf-8', errors='ignore')
        return jsonify({'content': text})
    except Exception:
        return jsonify({'error': 'lecture impossible'}), 500


# -----------------------
# Admin user management
# -----------------------
ADMIN_KEY = 'local-admin-key'
ADMIN_JWT_SECRET = os.environ.get('ADMIN_JWT_SECRET', 'dev-secret-change-me')
JWT_TTL = 60 * 60 * 2  # 2 hours


def _base64url_encode(b: bytes) -> str:
    return base64.urlsafe_b64encode(b).rstrip(b"=").decode('ascii')


def _base64url_decode(s: str) -> bytes:
    rem = len(s) % 4
    if rem:
        s += '=' * (4 - rem)
    return base64.urlsafe_b64decode(s.encode('ascii'))


def _sign_jwt(header_b64: str, payload_b64: str) -> str:
    msg = (header_b64 + "." + payload_b64).encode('ascii')
    sig = hmac.new(ADMIN_JWT_SECRET.encode('utf-8'), msg, hashlib.sha256).digest()
    return _base64url_encode(sig)


def _create_token(username: str, is_admin: bool) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {"sub": username, "is_admin": 1 if is_admin else 0, "exp": int(time.time()) + JWT_TTL}
    h_b = _base64url_encode(json.dumps(header, separators=(',', ':')).encode('utf-8'))
    p_b = _base64url_encode(json.dumps(payload, separators=(',', ':')).encode('utf-8'))
    sig = _sign_jwt(h_b, p_b)
    return f"{h_b}.{p_b}.{sig}"


def _validate_token(token: str) -> dict | None:
    try:
        parts = token.split('.')
        if len(parts) != 3:
            return None
        h_b, p_b, sig = parts
        expected = _sign_jwt(h_b, p_b)
        if not hmac.compare_digest(expected, sig):
            return None
        payload = json.loads(_base64url_decode(p_b).decode('utf-8'))
        if 'exp' in payload and int(time.time()) > int(payload['exp']):
            return None
        return payload
    except Exception:
        return None

def _get_db_conn():
    db_path = str(DB_FILE) if hasattr(DB_FILE, 'as_posix') or isinstance(DB_FILE, (str, Path)) else str(DB_FILE)
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def _ensure_schema():
    conn = _get_db_conn()
    cur = conn.cursor()
    cur.executescript('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        salt TEXT NOT NULL,
        is_admin INTEGER NOT NULL DEFAULT 0,
        created_at TEXT NOT NULL
    );
    ''')
    conn.commit()
    conn.close()

def _hash_password(password: str):
    salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 120000)
    return binascii.hexlify(dk).decode('ascii'), binascii.hexlify(salt).decode('ascii')

def _add_user(username: str, password: str, is_admin: bool = False):
    _ensure_schema()
    pwd_hash, salt = _hash_password(password)
    conn = _get_db_conn()
    cur = conn.cursor()
    cur.execute("INSERT OR REPLACE INTO users (username, password_hash, salt, is_admin, created_at) VALUES (?, ?, ?, ?, ?)",
                (username, pwd_hash, salt, 1 if is_admin else 0, datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()

def _list_users():
    _ensure_schema()
    conn = _get_db_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, username, is_admin, created_at FROM users ORDER BY id")
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows

def _delete_user(username: str):
    _ensure_schema()
    conn = _get_db_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE username = ?", (username,))
    conn.commit()
    affected = cur.rowcount
    conn.close()
    return affected


def _is_admin_request(req):
    # Allow either static admin key or Bearer JWT token
    if req.headers.get('X-ADMIN-KEY', '') == ADMIN_KEY:
        return True
    auth = req.headers.get('Authorization', '')
    if auth.startswith('Bearer '):
        token = auth.split(' ', 1)[1].strip()
        payload = _validate_token(token)
        if payload and payload.get('is_admin'):
            return True
    return False


@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json(silent=True) or {}
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'username/password required'}), 400
    try:
        _ensure_schema()
        conn = _get_db_conn()
        cur = conn.cursor()
        cur.execute("SELECT username, password_hash, salt, is_admin FROM users WHERE username = ?", (username,))
        row = cur.fetchone()
        conn.close()
        if not row:
            return jsonify({'error': 'invalid credentials'}), 401
        stored_hash = row['password_hash']
        salt = binascii.unhexlify(row['salt'])
        dk = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 120000)
        if not hmac.compare_digest(binascii.hexlify(dk).decode('ascii'), stored_hash):
            return jsonify({'error': 'invalid credentials'}), 401
        token = _create_token(username, bool(row['is_admin']))
        return jsonify({'token': token})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/auth/register', methods=['POST'])
def auth_register():
    data = request.get_json(silent=True) or {}
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'username and password required'}), 400
    try:
        # create non-admin user
        _add_user(username, password, is_admin=False)
        return jsonify({'status': 'ok', 'username': username})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/auth/login', methods=['POST'])
def auth_login():
    data = request.get_json(silent=True) or {}
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'username/password required'}), 400
    try:
        _ensure_schema()
        conn = _get_db_conn()
        cur = conn.cursor()
        cur.execute("SELECT username, password_hash, salt, is_admin FROM users WHERE username = ?", (username,))
        row = cur.fetchone()
        conn.close()
        if not row:
            return jsonify({'error': 'invalid credentials'}), 401
        stored_hash = row['password_hash']
        salt = binascii.unhexlify(row['salt'])
        dk = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 120000)
        if not hmac.compare_digest(binascii.hexlify(dk).decode('ascii'), stored_hash):
            return jsonify({'error': 'invalid credentials'}), 401
        token = _create_token(username, bool(row['is_admin']))
        return jsonify({'token': token})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/admin/users', methods=['GET'])
def admin_users_list():
    if not _is_admin_request(request):
        return jsonify({'error': 'non autorisé'}), 403
    try:
        users = _list_users()
        return jsonify({'users': users})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/admin/users', methods=['POST'])
def admin_users_create():
    if not _is_admin_request(request):
        return jsonify({'error': 'non autorisé'}), 403
    data = request.get_json(silent=True) or {}
    username = data.get('username')
    password = data.get('password')
    is_admin = bool(data.get('is_admin', False))
    if not username or not password:
        return jsonify({'error': 'username and password required'}), 400
    try:
        _add_user(username, password, is_admin)
        return jsonify({'status': 'ok', 'username': username})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/admin/users', methods=['DELETE'])
def admin_users_delete():
    if not _is_admin_request(request):
        return jsonify({'error': 'non autorisé'}), 403
    data = request.get_json(silent=True) or {}
    username = data.get('username')
    if not username:
        return jsonify({'error': 'username required'}), 400
    try:
        affected = _delete_user(username)
        return jsonify({'status': 'ok', 'deleted': affected})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    # Démarrer uniquement en local
    app.run(host='127.0.0.1', port=5000, debug=False)
