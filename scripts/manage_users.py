#!/usr/bin/env python3
"""Manage users in the local SQLite DB for AstaAcademie.

Usage:
  python scripts/manage_users.py add username
  python scripts/manage_users.py remove username
  python scripts/manage_users.py list
"""
from __future__ import annotations

import sqlite3
import sys
import os
import getpass
import binascii
import hashlib
from datetime import datetime

try:
    from core.config import DB_FILE
except Exception:
    DB_FILE = os.path.join(os.getcwd(), 'data', 'asta_database.db')


def hash_password(password: str, salt: bytes | None = None) -> tuple[str, str]:
    if salt is None:
        salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 120000)
    return binascii.hexlify(dk).decode('ascii'), binascii.hexlify(salt).decode('ascii')


def add_user(username: str, admin: bool = False):
    pwd = getpass.getpass(f"Mot de passe pour {username}: ")
    pwd2 = getpass.getpass("Confirmer: ")
    if pwd != pwd2:
        print("Les mots de passe ne correspondent pas.")
        return
    pwd_hash, salt = hash_password(pwd)
    conn = sqlite3.connect(str(DB_FILE))
    cur = conn.cursor()
    cur.execute("INSERT OR REPLACE INTO users (username, password_hash, salt, is_admin, created_at) VALUES (?, ?, ?, ?, ?)",
                (username, pwd_hash, salt, 1 if admin else 0, datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()
    print(f"Utilisateur '{username}' ajouté.")


def remove_user(username: str):
    conn = sqlite3.connect(str(DB_FILE))
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE username = ?", (username,))
    conn.commit()
    conn.close()
    print(f"Utilisateur '{username}' supprimé (si existait).")


def list_users():
    conn = sqlite3.connect(str(DB_FILE))
    cur = conn.cursor()
    cur.execute("SELECT id, username, is_admin, created_at FROM users ORDER BY id")
    rows = cur.fetchall()
    conn.close()
    for r in rows:
        print(f"{r[0]:>3} | {r[1]:<20} | admin={bool(r[2])} | created={r[3]}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    cmd = sys.argv[1].lower()
    if cmd == 'add' and len(sys.argv) >= 3:
        add_user(sys.argv[2], admin='--admin' in sys.argv)
    elif cmd == 'remove' and len(sys.argv) >= 3:
        remove_user(sys.argv[2])
    elif cmd == 'list':
        list_users()
    else:
        print(__doc__)


if __name__ == '__main__':
    main()
