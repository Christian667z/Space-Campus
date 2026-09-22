#!/usr/bin/env python3
"""Initialise la base SQLite locale pour Asta Académie.

Usage:
  python scripts/init_db.py      # crée la DB et demande un mot de passe admin
  python scripts/init_db.py --no-admin   # crée la DB sans utilisateur
"""
from __future__ import annotations

import sqlite3
import os
from datetime import datetime
import hashlib
import binascii
import getpass

try:
    from core.config import DB_FILE, DATA_DIR
except Exception:
    DB_FILE = os.path.join(os.getcwd(), "data", "asta_database.db")
    DATA_DIR = os.path.dirname(DB_FILE)


def ensure_dirs():
    d = os.path.dirname(str(DB_FILE))
    if d and not os.path.exists(d):
        os.makedirs(d, exist_ok=True)


def create_schema(conn: sqlite3.Connection):
    cur = conn.cursor()
    cur.executescript("""
    PRAGMA foreign_keys = ON;

    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        salt TEXT NOT NULL,
        is_admin INTEGER NOT NULL DEFAULT 0,
        created_at TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        titre TEXT,
        contenu TEXT,
        date_created TEXT,
        date_modified TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE SET NULL
    );

    CREATE TABLE IF NOT EXISTS sessions (
        id TEXT PRIMARY KEY,
        user_id INTEGER,
        data TEXT,
        created_at TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS licenses (
        key TEXT PRIMARY KEY,
        issued_to TEXT,
        issued_at TEXT
    );

    CREATE INDEX IF NOT EXISTS idx_notes_user ON notes(user_id);
    """)
    conn.commit()


def hash_password(password: str, salt: bytes | None = None) -> tuple[str, str]:
    if salt is None:
        salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 120000)
    return binascii.hexlify(dk).decode('ascii'), binascii.hexlify(salt).decode('ascii')


def create_admin(conn: sqlite3.Connection, username: str, password: str):
    pwd_hash, salt = hash_password(password)
    cur = conn.cursor()
    cur.execute(
        "INSERT OR REPLACE INTO users (username, password_hash, salt, is_admin, created_at) VALUES (?, ?, ?, ?, ?)",
        (username, pwd_hash, salt, 1, datetime.utcnow().isoformat()),
    )
    conn.commit()


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Initialise la base SQLite locale AstaAcademie")
    parser.add_argument('--no-admin', action='store_true', help='Ne pas créer d\'utilisateur admin')
    parser.add_argument('--db', type=str, default=None, help='Chemin vers le fichier sqlite à créer')
    args = parser.parse_args()

    global DB_FILE
    if args.db:
        DB_FILE = args.db

    ensure_dirs()
    conn = sqlite3.connect(str(DB_FILE))
    try:
        create_schema(conn)
        print(f"Base créée/initialisée : {DB_FILE}")

        if not args.no_admin:
            print("Création d'un compte administrateur.")
            user = input("Nom d'utilisateur admin [admin]: ") or "admin"
            pwd = getpass.getpass("Mot de passe: ")
            pwd2 = getpass.getpass("Confirmer mot de passe: ")
            if pwd != pwd2:
                print("Les mots de passe ne correspondent pas — abandon.")
            elif len(pwd) < 6:
                print("Mot de passe trop court (>=6). Abandon.")
            else:
                create_admin(conn, user, pwd)
                print(f"Utilisateur admin '{user}' créé.")

    finally:
        conn.close()


if __name__ == '__main__':
    main()
