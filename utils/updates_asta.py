"""
╔══════════════════════════════════════════════════════════════╗
║          ASTA ACADÉMIE — OFFLINE UPDATE SYSTEM               ║
║         Développé par Space | Asta Dev — Promo 2024-2028     ║
╚══════════════════════════════════════════════════════════════╝
"""

import json
import os
import shutil
import hashlib
from pathlib import Path
from datetime import datetime

CURRENT_VERSION = "1.0.0"
UPDATE_EXTENSION = ".astaupdate"
APP_DATA_DIR = Path(os.getenv("APPDATA", ".")) / "AstaAcademie"
VERSION_FILE = APP_DATA_DIR / "version.json"

def get_current_version() -> dict:
    """Lit la version actuelle."""
    if VERSION_FILE.exists():
        try:
            with open(VERSION_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "version": CURRENT_VERSION,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "notes": "Version initiale — Asta Académie"
    }

def save_version(version_info: dict):
    """Sauvegarde les infos de version."""
    APP_DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(VERSION_FILE, "w") as f:
        json.dump(version_info, f, indent=2)

def verify_update_file(filepath: str) -> tuple[bool, str, dict]:
    """
    Vérifie l'intégrité d'un fichier .astaupdate
    Retourne (is_valid, message, update_data)
    """
    try:
        if not filepath.endswith(UPDATE_EXTENSION):
            return False, f"Extension invalide. Attendu: {UPDATE_EXTENSION}", {}
        
        with open(filepath, "r", encoding="utf-8") as f:
            update_data = json.load(f)
        
        required_fields = ["version", "date", "notes", "files", "checksum"]
        for field in required_fields:
            if field not in update_data:
                return False, f"Champ manquant dans le fichier: {field}", {}
        
   
        data_to_check = json.dumps({k: v for k, v in update_data.items() if k != "checksum"}, sort_keys=True)
        computed = hashlib.sha256(f"ASTA_UPDATE_{data_to_check}".encode()).hexdigest()[:16].upper()
        
        if computed != update_data.get("checksum", "").upper():
            return False, "❌ Checksum invalide — Fichier corrompu ou non officiel", {}
        
        current = get_current_version()
        if update_data["version"] <= current["version"]:
            return False, f"Version {update_data['version']} ≤ Version actuelle {current['version']}", {}
        
        return True, f"✅ Mise à jour {update_data['version']} vérifiée", update_data
    
    except json.JSONDecodeError:
        return False, "❌ Fichier .astaupdate corrompu (JSON invalide)", {}
    except FileNotFoundError:
        return False, "❌ Fichier introuvable", {}
    except Exception as e:
        return False, f"❌ Erreur: {str(e)}", {}

def apply_update(update_data: dict, app_dir: str) -> tuple[bool, str]:
    """
    Applique une mise à jour.
    update_data: données du fichier .astaupdate
    app_dir: répertoire de l'application
    """
    try:
    
        backup_dir = APP_DATA_DIR / "backup" / datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        updated_files = []
        for file_info in update_data.get("files", []):
            filename = file_info.get("name", "")
            content = file_info.get("content", "")
            
            target = Path(app_dir) / filename
            
            if target.exists():
                shutil.copy2(target, backup_dir / filename)
            
            target.parent.mkdir(parents=True, exist_ok=True)
            with open(target, "w", encoding="utf-8") as f:
                f.write(content)
            updated_files.append(filename)
    
        save_version({
            "version": update_data["version"],
            "date": update_data["date"],
            "notes": update_data["notes"],
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        return True, f"✅ Mise à jour {update_data['version']} appliquée! ({len(updated_files)} fichier(s) mis à jour)"
    
    except Exception as e:
        return False, f"❌ Erreur lors de la mise à jour: {str(e)}"

def create_update_package(version: str, notes: str, files: list) -> str:
    """
    [OUTIL DÉVELOPPEUR] Crée un fichier .astaupdate
    files: [{"name": "fichier.py", "content": "..."}]
    """
    update_data = {
        "version": version,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "notes": notes,
        "files": files,
        "checksum": ""
    }
    
    data_to_check = json.dumps({k: v for k, v in update_data.items() if k != "checksum"}, sort_keys=True)
    checksum = hashlib.sha256(f"ASTA_UPDATE_{data_to_check}".encode()).hexdigest()[:16].upper()
    update_data["checksum"] = checksum
    
    output_file = f"update_v{version}{UPDATE_EXTENSION}"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(update_data, f, indent=2, ensure_ascii=False)
    
    return output_file