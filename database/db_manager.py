"""
Asta Académie — Database Manager (Version Corrigée)

BUGS CORRIGÉS vs db_manager.py original :
 1. get_or_create_user() retournait toujours -1 → implémentation complète
 2. check_user_active() retournait toujours True → vraie vérification DB
 3. get_quiz_stats() retournait (0,0) hardcodé → table quiz_stats créée
 4. update_quiz_stats() vide → implémentation réelle
 5. get_completed_missions() retournait [] hardcodé → table missions créée
 6. add_completed_mission() vide → implémentation réelle
 7. get_all_users() retournait [] hardcodé → requête SQL réelle
 8. set_user_status() vide → UPDATE réel
 9. delete_user() vide → DELETE réel
10. get_audit_logs() retournait [] hardcodé → requête SQL réelle avec filtres
11. get_audit_logs_count() retournait 0 hardcodé → COUNT réel
12. clear_audit_logs() vide → DELETE réel
13. get_dashboard_metrics() retournait hardcodé → métriques réelles
14. get_log_stats_for_chart() retournait hardcodé → agrégation réelle
15. Connexion SQLite : check_same_thread=False sans verrou → threading.Lock ajouté
"""

import sqlite3
import json
import threading
from pathlib import Path
from datetime import datetime
import bcrypt

# Lock pour la thread-safety (BUGFIX #15 - Changé en RLock pour éviter les deadlocks)
_db_lock = threading.RLock()


def _encrypt_val(val) -> bytes:
    """Chiffrement simple des valeurs sensibles."""
    try:
        from security.crypto_manager import encrypt_data
        if val is None:
            return b""
        return encrypt_data({"v": val})
    except Exception:
        # Fallback : stockage en clair si crypto non disponible
        return json.dumps({"v": val}).encode('utf-8')


def _decrypt_val(val_bytes, default=None):
    """Déchiffrement des valeurs sensibles."""
    if not val_bytes:
        return default
    try:
        from security.crypto_manager import decrypt_data
        data = decrypt_data(val_bytes)
        return data.get("v", default)
    except Exception:
        try:
            data = json.loads(val_bytes)
            return data.get("v", default)
        except Exception:
            return default


class DBManager:
    _conn: sqlite3.Connection = None
    _db_path: Path = None

    @classmethod
    def init_database(cls, db_path: Path):
        cls._db_path = db_path
        cls._db_path.parent.mkdir(parents=True, exist_ok=True)
        cls._conn = sqlite3.connect(
            str(cls._db_path),
            check_same_thread=False
        )
        cls._conn.row_factory = sqlite3.Row
        # Performance optimizations
        cls._conn.execute("PRAGMA journal_mode=WAL")
        cls._conn.execute("PRAGMA synchronous=NORMAL")
        cls._conn.execute("PRAGMA foreign_keys=ON")
        cls._create_tables()
        cls._check_backups()

    @classmethod
    def _create_tables(cls):
        with _db_lock:
            cursor = cls._conn.cursor()

            # Users
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    is_active INTEGER DEFAULT 1,
                    created_at TEXT NOT NULL
                )
            ''')

            # Progress (chiffré)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS progress (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL UNIQUE,
                    points_enc BLOB,
                    streak_enc BLOB,
                    niveau_enc BLOB,
                    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            ''')

            # XP Log
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS xp_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    date_str TEXT NOT NULL,
                    amount_enc BLOB,
                    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
                    UNIQUE(user_id, date_str)
                )
            ''')

            # BUGFIX : Table quiz_stats manquante dans l'original
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS quiz_stats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL UNIQUE,
                    score INTEGER DEFAULT 0,
                    total INTEGER DEFAULT 0,
                    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            ''')

            # BUGFIX : Table missions manquante dans l'original
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS missions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    mission_id TEXT NOT NULL,
                    completed_at TEXT NOT NULL,
                    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
                    UNIQUE(user_id, mission_id)
                )
            ''')

            # Notes
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    titre TEXT NOT NULL,
                    contenu TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            ''')

            # Grades
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS grades (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    matiere TEXT,
                    note REAL,
                    type TEXT,
                    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            ''')

            # Audit Logs
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS audit_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    level TEXT NOT NULL,
                    action TEXT NOT NULL,
                    timestamp TEXT NOT NULL
                )
            ''')

            # Sync Queue
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sync_queue (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    entity_type TEXT NOT NULL,
                    entity_id TEXT NOT NULL,
                    operation TEXT NOT NULL,
                    payload TEXT,
                    created_at TEXT NOT NULL,
                    retry_count INTEGER DEFAULT 0
                )
            ''')

            # Local Metadata
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS local_metadata (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    last_sync TEXT,
                    schema_version INTEGER DEFAULT 2
                )
            ''')
            cursor.execute('SELECT COUNT(*) FROM local_metadata')
            if cursor.fetchone()[0] == 0:
                cursor.execute('INSERT INTO local_metadata (schema_version) VALUES (2)')

            cls._conn.commit()

    @classmethod
    def _check_backups(cls):
        """Backup automatique quotidien."""
        if not cls._db_path:
            return
        backup_dir = cls._db_path.parent / "backups"
        backup_dir.mkdir(parents=True, exist_ok=True)
        today_str = datetime.now().strftime("%Y-%m-%d")
        backup_file = backup_dir / f"asta_db_backup_{today_str}.bak"
        if not backup_file.exists():
            import shutil
            try:
                with _db_lock:
                    cls._conn.commit()
                shutil.copy2(cls._db_path, backup_file)
            except Exception as e:
                print(f"[DB] Backup error: {e}")

    # ── Auth & Users ────────────────────────────────────────────────
    @classmethod
    def get_user_by_name(cls, nom: str) -> dict:
        if not cls._conn:
            return None
        with _db_lock:
            cursor = cls._conn.cursor()
            cursor.execute('SELECT * FROM users WHERE nom = ?', (nom,))
            row = cursor.fetchone()
        return dict(row) if row else None

    @classmethod
    def get_user_by_id(cls, user_id: int) -> dict:
        if not cls._conn:
            return None
        with _db_lock:
            cursor = cls._conn.cursor()
            cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
            row = cursor.fetchone()
        return dict(row) if row else None

    @classmethod
    def create_user(cls, nom: str, password: str) -> int:
        if not cls._conn:
            return -1
        hashed = bcrypt.hashpw(
            password.encode('utf-8'), bcrypt.gensalt()
        ).decode('utf-8')
        with _db_lock:
            cursor = cls._conn.cursor()
            try:
                cursor.execute(
                    'INSERT INTO users (nom, password_hash, created_at) VALUES (?, ?, ?)',
                    (nom, hashed, datetime.now().isoformat())
                )
                user_id = cursor.lastrowid
                # Init progress
                cursor.execute(
                    'INSERT INTO progress (user_id, points_enc, streak_enc, niveau_enc) '
                    'VALUES (?, ?, ?, ?)',
                    (user_id, _encrypt_val(0), _encrypt_val(0), _encrypt_val("L2"))
                )
                # Init quiz_stats
                cursor.execute(
                    'INSERT INTO quiz_stats (user_id, score, total) VALUES (?, 0, 0)',
                    (user_id,)
                )
                cls._conn.commit()
                return user_id
            except sqlite3.IntegrityError:
                return -1

    @classmethod
    def verify_password(cls, nom: str, password: str) -> tuple:
        user = cls.get_user_by_name(nom)
        if not user:
            return False, -1
        if not user.get("is_active", 1):
            return False, -2  # Bloqué
        try:
            hashed = user["password_hash"].encode('utf-8')
            if bcrypt.checkpw(password.encode('utf-8'), hashed):
                return True, user["id"]
        except Exception:
            pass
        return False, -1

    # BUGFIX #1 : get_or_create_user implémenté
    @classmethod
    def get_or_create_user(cls, nom: str) -> int:
        user = cls.get_user_by_name(nom)
        if user:
            return user["id"]
        # Crée avec un password random (mode offline sans mot de passe)
        import secrets
        tmp_pwd = secrets.token_hex(16)
        return cls.create_user(nom, tmp_pwd)

    # BUGFIX #2 : check_user_active implémenté
    @classmethod
    def check_user_active(cls, user_id: int) -> bool:
        user = cls.get_user_by_id(user_id)
        if not user:
            return True  # Pas trouvé = pas bloqué
        return bool(user.get("is_active", 1))

    # ── Progress ────────────────────────────────────────────────────
    @classmethod
    def get_progress(cls, user_id: int) -> dict:
        if not cls._conn:
            return {"points": 0, "streak": 0, "niveau": "L2"}
        with _db_lock:
            cursor = cls._conn.cursor()
            cursor.execute('SELECT * FROM progress WHERE user_id = ?', (user_id,))
            row = cursor.fetchone()
        if not row:
            return {"points": 0, "streak": 0, "niveau": "L2"}
        return {
            "points": _decrypt_val(row["points_enc"], 0),
            "streak": _decrypt_val(row["streak_enc"], 0),
            "niveau": _decrypt_val(row["niveau_enc"], "L2"),
        }

    @classmethod
    def log_xp_earned(cls, user_id: int, date_str: str, amount: int):
        if not cls._conn:
            return
        with _db_lock:
            cursor = cls._conn.cursor()
            prog = cls.get_progress(user_id)
            new_points = prog["points"] + amount
            cursor.execute(
                'UPDATE progress SET points_enc = ? WHERE user_id = ?',
                (_encrypt_val(new_points), user_id)
            )
            # BUGFIX : UNIQUE constraint sur (user_id, date_str) → INSERT OR REPLACE
            cursor.execute(
                'SELECT id, amount_enc FROM xp_logs WHERE user_id = ? AND date_str = ?',
                (user_id, date_str)
            )
            row = cursor.fetchone()
            if row:
                old_amt = _decrypt_val(row["amount_enc"], 0)
                cursor.execute(
                    'UPDATE xp_logs SET amount_enc = ? WHERE id = ?',
                    (_encrypt_val(old_amt + amount), row["id"])
                )
            else:
                cursor.execute(
                    'INSERT INTO xp_logs (user_id, date_str, amount_enc) VALUES (?, ?, ?)',
                    (user_id, date_str, _encrypt_val(amount))
                )
            cls._conn.commit()

    # BUGFIX #3 : get_quiz_stats implémenté
    @classmethod
    def get_quiz_stats(cls, user_id: int) -> tuple:
        if not cls._conn:
            return 0, 0
        with _db_lock:
            cursor = cls._conn.cursor()
            cursor.execute(
                'SELECT score, total FROM quiz_stats WHERE user_id = ?', (user_id,)
            )
            row = cursor.fetchone()
        return (row["score"], row["total"]) if row else (0, 0)

    # BUGFIX #4 : update_quiz_stats implémenté
    @classmethod
    def update_quiz_stats(cls, user_id: int, diff_score: int, diff_total: int):
        if not cls._conn:
            return
        with _db_lock:
            cursor = cls._conn.cursor()
            cursor.execute(
                'SELECT id FROM quiz_stats WHERE user_id = ?', (user_id,)
            )
            row = cursor.fetchone()
            if row:
                cursor.execute(
                    'UPDATE quiz_stats SET score = score + ?, total = total + ? '
                    'WHERE user_id = ?',
                    (diff_score, diff_total, user_id)
                )
            else:
                cursor.execute(
                    'INSERT INTO quiz_stats (user_id, score, total) VALUES (?, ?, ?)',
                    (user_id, diff_score, diff_total)
                )
            cls._conn.commit()

    # BUGFIX #5 : get_completed_missions implémenté
    @classmethod
    def get_completed_missions(cls, user_id: int) -> list:
        if not cls._conn:
            return []
        with _db_lock:
            cursor = cls._conn.cursor()
            cursor.execute(
                'SELECT mission_id FROM missions WHERE user_id = ?', (user_id,)
            )
            return [row["mission_id"] for row in cursor.fetchall()]

    # BUGFIX #6 : add_completed_mission implémenté
    @classmethod
    def add_completed_mission(cls, user_id: int, mission_id: str):
        if not cls._conn:
            return
        with _db_lock:
            cursor = cls._conn.cursor()
            try:
                cursor.execute(
                    'INSERT OR IGNORE INTO missions (user_id, mission_id, completed_at) '
                    'VALUES (?, ?, ?)',
                    (user_id, mission_id, datetime.now().isoformat())
                )
                cls._conn.commit()
            except Exception:
                pass

    # ── Notes ───────────────────────────────────────────────────────
    @classmethod
    def get_notes(cls, user_id: int) -> list:
        if not cls._conn:
            return []
        with _db_lock:
            cursor = cls._conn.cursor()
            cursor.execute(
                'SELECT * FROM notes WHERE user_id = ? ORDER BY updated_at DESC',
                (user_id,)
            )
            return [dict(r) for r in cursor.fetchall()]

    @classmethod
    def save_note(cls, user_id: int, note_id: int, titre: str, contenu: str) -> int:
        if not cls._conn:
            return note_id
        with _db_lock:
            cursor = cls._conn.cursor()
            now = datetime.now().isoformat()
            if note_id <= 0:
                cursor.execute(
                    'INSERT INTO notes (user_id, titre, contenu, updated_at) '
                    'VALUES (?, ?, ?, ?)',
                    (user_id, titre, contenu, now)
                )
                note_id = cursor.lastrowid
            else:
                cursor.execute(
                    'UPDATE notes SET titre=?, contenu=?, updated_at=? WHERE id=?',
                    (titre, contenu, now, note_id)
                )
            cls._conn.commit()
        return note_id

    @classmethod
    def delete_note(cls, note_id: int):
        if not cls._conn:
            return
        with _db_lock:
            cursor = cls._conn.cursor()
            cursor.execute('DELETE FROM notes WHERE id=?', (note_id,))
            cls._conn.commit()

    # ── Grades ──────────────────────────────────────────────────────
    @classmethod
    def get_user_grades(cls, user_id: int) -> list:
        if not cls._conn:
            return []
        with _db_lock:
            cursor = cls._conn.cursor()
            cursor.execute('SELECT * FROM grades WHERE user_id = ?', (user_id,))
            return [dict(r) for r in cursor.fetchall()]

    @classmethod
    def save_user_grades(cls, user_id: int, grades: list):
        if not cls._conn:
            return
        with _db_lock:
            cursor = cls._conn.cursor()
            cursor.execute('DELETE FROM grades WHERE user_id = ?', (user_id,))
            for g in grades:
                cursor.execute(
                    'INSERT INTO grades (user_id, matiere, note, type) VALUES (?, ?, ?, ?)',
                    (user_id, g.get('matiere'), g.get('note'), g.get('type'))
                )
            cls._conn.commit()

    # ── Admin ────────────────────────────────────────────────────────
    # BUGFIX #7 : get_all_users implémenté
    @classmethod
    def get_all_users(cls) -> list:
        if not cls._conn:
            return []
        with _db_lock:
            cursor = cls._conn.cursor()
            cursor.execute(
                'SELECT id, nom, is_active, created_at FROM users ORDER BY created_at DESC'
            )
            return [dict(r) for r in cursor.fetchall()]

    # BUGFIX #8 : set_user_status implémenté
    @classmethod
    def set_user_status(cls, user_id: int, is_active: bool):
        if not cls._conn:
            return
        with _db_lock:
            cursor = cls._conn.cursor()
            cursor.execute(
                'UPDATE users SET is_active = ? WHERE id = ?',
                (1 if is_active else 0, user_id)
            )
            cls._conn.commit()

    # BUGFIX #9 : delete_user implémenté (CASCADE via FK)
    @classmethod
    def delete_user(cls, user_id: int):
        if not cls._conn:
            return
        with _db_lock:
            cursor = cls._conn.cursor()
            cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
            cls._conn.commit()

    # ── Audit Logs ──────────────────────────────────────────────────
    @classmethod
    def add_audit_log(cls, user_id: int, level: str, action: str):
        if not cls._conn:
            return
        with _db_lock:
            cursor = cls._conn.cursor()
            cursor.execute(
                'INSERT INTO audit_logs (user_id, level, action, timestamp) VALUES (?, ?, ?, ?)',
                (user_id, level, action, datetime.now().isoformat())
            )
            cls._conn.commit()

    # BUGFIX #10 : get_audit_logs avec filtres réels
    @classmethod
    def get_audit_logs(cls, limit: int = 500, offset: int = 0,
                       level_filter: str = "ALL", search_kw: str = "") -> list:
        if not cls._conn:
            return []
        with _db_lock:
            cursor = cls._conn.cursor()
            conditions = []
            params = []
            if level_filter != "ALL":
                conditions.append("level = ?")
                params.append(level_filter)
            if search_kw:
                conditions.append("(action LIKE ? OR level LIKE ?)")
                params.extend([f"%{search_kw}%", f"%{search_kw}%"])
            where = "WHERE " + " AND ".join(conditions) if conditions else ""
            params.extend([limit, offset])
            cursor.execute(
                f'SELECT * FROM audit_logs {where} ORDER BY timestamp DESC LIMIT ? OFFSET ?',
                params
            )
            return [dict(r) for r in cursor.fetchall()]

    # BUGFIX #11 : count réel
    @classmethod
    def get_audit_logs_count(cls, level_filter: str = "ALL", search_kw: str = "") -> int:
        if not cls._conn:
            return 0
        with _db_lock:
            cursor = cls._conn.cursor()
            conditions = []
            params = []
            if level_filter != "ALL":
                conditions.append("level = ?")
                params.append(level_filter)
            if search_kw:
                conditions.append("action LIKE ?")
                params.append(f"%{search_kw}%")
            where = "WHERE " + " AND ".join(conditions) if conditions else ""
            cursor.execute(f'SELECT COUNT(*) FROM audit_logs {where}', params)
            return cursor.fetchone()[0]

    # BUGFIX #12 : clear_audit_logs implémenté
    @classmethod
    def clear_audit_logs(cls):
        if not cls._conn:
            return
        with _db_lock:
            cursor = cls._conn.cursor()
            cursor.execute('DELETE FROM audit_logs')
            cls._conn.commit()

    # BUGFIX #13 : dashboard_metrics réels
    @classmethod
    def get_dashboard_metrics(cls) -> dict:
        if not cls._conn:
            return {"total_users": 0, "active_users": 0, "today_errors": 0}
        with _db_lock:
            cursor = cls._conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM users')
            total = cursor.fetchone()[0]
            cursor.execute('SELECT COUNT(*) FROM users WHERE is_active = 1')
            active = cursor.fetchone()[0]
            today = datetime.now().strftime('%Y-%m-%d')
            cursor.execute(
                "SELECT COUNT(*) FROM audit_logs WHERE level = 'ERROR' AND timestamp LIKE ?",
                (f"{today}%",)
            )
            errors = cursor.fetchone()[0]
        return {"total_users": total, "active_users": active, "today_errors": errors}

    # BUGFIX #14 : log_stats pour graphique réels
    @classmethod
    def get_log_stats_for_chart(cls) -> dict:
        if not cls._conn:
            return {"SYSTEM": 0, "SECURITY": 0, "ERROR": 0, "HACKING": 0}
        with _db_lock:
            cursor = cls._conn.cursor()
            cursor.execute(
                "SELECT level, COUNT(*) as cnt FROM audit_logs GROUP BY level"
            )
            result = {"SYSTEM": 0, "SECURITY": 0, "ERROR": 0, "HACKING": 0}
            for row in cursor.fetchall():
                lvl = row["level"].upper()
                if lvl in result:
                    result[lvl] = row["cnt"]
        return result

    # ── Weekly XP ───────────────────────────────────────────────────
    @classmethod
    def get_weekly_xp(cls, user_id: int, dates: list) -> list:
        if not cls._conn:
            return [0] * len(dates)
        with _db_lock:
            cursor = cls._conn.cursor()
            res = []
            for d in dates:
                cursor.execute(
                    'SELECT amount_enc FROM xp_logs WHERE user_id = ? AND date_str = ?',
                    (user_id, d)
                )
                row = cursor.fetchone()
                res.append(_decrypt_val(row["amount_enc"], 0) if row else 0)
        return res


# ── Module-level wrappers (compatibilité) ─────────────────────────────
def init_database(db_path: Path):
    DBManager.init_database(db_path)

# BUGFIX #1
def get_or_create_user(db_path: Path, nom: str) -> int:
    return DBManager.get_or_create_user(nom)

# BUGFIX #2
def check_user_active(db_path: Path, user_id: int) -> bool:
    return DBManager.check_user_active(user_id)

def get_progress(db_path: Path, user_id: int) -> dict:
    return DBManager.get_progress(user_id)

def log_xp_earned(db_path: Path, user_id: int, date_str: str, amount: int):
    DBManager.log_xp_earned(user_id, date_str, amount)

def get_notes(db_path: Path, user_id: int) -> list:
    return DBManager.get_notes(user_id)

def save_note(db_path: Path, user_id: int, note_id: int, titre: str, contenu: str) -> int:
    return DBManager.save_note(user_id, note_id, titre, contenu)

def delete_note(db_path: Path, note_id: int):
    DBManager.delete_note(note_id)

def add_audit_log(db_path: Path, user_id: int, level: str, action: str):
    DBManager.add_audit_log(user_id, level, action)

# BUGFIX #3
def get_quiz_stats(db_path: Path, user_id: int) -> tuple:
    return DBManager.get_quiz_stats(user_id)

# BUGFIX #4
def update_quiz_stats(db_path: Path, user_id: int, diff_score: int, diff_total: int):
    DBManager.update_quiz_stats(user_id, diff_score, diff_total)

def get_weekly_xp(db_path: Path, user_id: int, dates: list) -> list:
    return DBManager.get_weekly_xp(user_id, dates)

# BUGFIX #5
def get_completed_missions(db_path: Path, user_id: int) -> list:
    return DBManager.get_completed_missions(user_id)

# BUGFIX #6
def add_completed_mission(db_path: Path, user_id: int, mission_id: str):
    DBManager.add_completed_mission(user_id, mission_id)

# BUGFIX #7
def get_all_users(db_path: Path) -> list:
    return DBManager.get_all_users()

# BUGFIX #8
def set_user_status(db_path: Path, user_id: int, is_active: bool):
    DBManager.set_user_status(user_id, is_active)

# BUGFIX #9
def delete_user(db_path: Path, user_id: int):
    DBManager.delete_user(user_id)

def get_user_grades(db_path: Path, user_id: int) -> list:
    return DBManager.get_user_grades(user_id)

def save_user_grades(db_path: Path, user_id: int, grades: list):
    DBManager.save_user_grades(user_id, grades)

# BUGFIX #10
def get_audit_logs(db_path: Path, limit: int = 500, offset: int = 0,
                   level_filter: str = "ALL", search_kw: str = "") -> list:
    return DBManager.get_audit_logs(limit, offset, level_filter, search_kw)

# BUGFIX #11
def get_audit_logs_count(db_path: Path, level_filter: str = "ALL",
                         search_kw: str = "") -> int:
    return DBManager.get_audit_logs_count(level_filter, search_kw)

# BUGFIX #12
def clear_audit_logs(db_path: Path):
    DBManager.clear_audit_logs()

# BUGFIX #13
def get_dashboard_metrics(db_path: Path) -> dict:
    return DBManager.get_dashboard_metrics()

# BUGFIX #14
def get_log_stats_for_chart(db_path: Path) -> dict:
    return DBManager.get_log_stats_for_chart()
