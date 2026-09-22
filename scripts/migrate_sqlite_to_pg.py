import sqlite3
import requests
import json
from pathlib import Path

# Constantes
SQLITE_DB = Path.home() / "Documents" / "AstaAcademie" / "asta_database.db"
API_URL = "http://127.0.0.1:8080/api/v1"

def migrate():
    print(f"Migration depuis {SQLITE_DB} vers le Backend Go (PostgreSQL)")
    
    if not SQLITE_DB.exists():
        print("Erreur: Base de données SQLite introuvable !")
        return
        
    conn = sqlite3.connect(SQLITE_DB)
    cursor = conn.cursor()
    
    # 1. Migrer l'Administrateur (Création d'un token pour l'API)
    print("\n--- 1. Authentification / Création Admin ---")
    resp = requests.post(f"{API_URL}/auth/login", json={"nom": "SuperAdmin", "password": "default_pass"})
    if resp.status_code != 200:
        print(f"Erreur Auth: {resp.text}")
        return
    token = resp.json().get("token")
    headers = {"Authorization": f"Bearer {token}"}
    print("Authentification réussie, Token JWT obtenu.")
    
    # 2. Migrer les Utilisateurs
    print("\n--- 2. Migration des Utilisateurs ---")
    cursor.execute("SELECT id, nom, is_active FROM users")
    users = cursor.fetchall()
    print(f"{len(users)} utilisateurs à migrer (simulation pour l'instant via connexion).")
    
    # Actuellement l'API Go crée un utilisateur lors du Login s'il n'existe pas.
    # Pour migrer proprement, on simule un login pour chaque étudiant pour le créer dans Postgres.
    user_mapping = {} # id_sqlite -> id_postgres
    for u in users:
        u_id, nom, is_active = u
        r = requests.post(f"{API_URL}/auth/login", json={"nom": nom, "password": "default_pass"})
        if r.status_code == 200:
            pg_user = r.json().get("user")
            user_mapping[u_id] = pg_user["id"]
            
            # Mettre à jour le statut
            requests.patch(f"{API_URL}/users/{pg_user['id']}/status", headers=headers, json={"is_active": bool(is_active)})
            print(f"Utilisateur {nom} migré.")
            
    print("\nMigration terminée avec succès. (Seuls les utilisateurs sont migrés pour l'instant pour le test de perf)")
    conn.close()

if __name__ == "__main__":
    migrate()
