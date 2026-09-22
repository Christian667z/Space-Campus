import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_database():
    try:
        # Connect to the default postgres database
        conn = psycopg2.connect(
            user="postgres",
            password="Coucou28",
            host="localhost",
            port="5432"
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'asta_academie'")
        exists = cursor.fetchone()
        
        if not exists:
            cursor.execute("CREATE DATABASE asta_academie")
            print("Base de données 'asta_academie' créée avec succès !")
        else:
            print("La base de données 'asta_academie' existe déjà.")
            
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Erreur lors de la création de la base de données : {e}")
        print("Avez-vous bien installé PostgreSQL avec le mot de passe 'postgres' ?")

if __name__ == "__main__":
    create_database()
