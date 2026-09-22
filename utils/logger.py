import os
from pathlib import Path
from datetime import datetime

DATA_DIR = Path(os.getenv("APPDATA", ".")) / "AstaAcademie"

class AstaLogger:
    """Gestion centralisée des logs pour Asta Académie (SQLite)."""
    
    _user_context = "[GUEST]"
    _user_id = 1 # Default

    @staticmethod
    def setup():
        """(Déprécié) Les dossiers sont gérés par DB Manager."""
        pass

    @staticmethod
    def set_user_context(user_id: int, nom: str, hwid: str = ""):
        AstaLogger._user_id = user_id
        AstaLogger._user_context = f"[UID:{user_id} | {nom} | HWID:{hwid}]"

    @staticmethod
    def _write_db(level: str, msg: str):
        try:
            from core.config import DB_FILE, DATA_DIR
            from database.db_manager import add_audit_log
            action = f"{AstaLogger._user_context} {msg}"
            add_audit_log(DB_FILE, AstaLogger._user_id, level, action)
            
            # Écriture dans un fichier texte lisible
            log_file = DATA_DIR / "Asta_Logs.txt"
            DATA_DIR.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(f"[{timestamp}] [{level}] {action}\n")
        except Exception:
            pass

    @staticmethod
    def info(msg: str):
        AstaLogger._write_db("SYSTEM", msg)

    @staticmethod
    def error(msg: str, exc_info=False):
        # We append exc_info detail in the msg string if needed
        err_msg = msg + (" (Exception captured)" if exc_info else "")
        AstaLogger._write_db("ERROR", err_msg)

    @staticmethod
    def security(msg: str):
        AstaLogger._write_db("SECURITY", msg)

    @staticmethod
    def hacking(msg: str):
        AstaLogger._write_db("HACKING", msg)
