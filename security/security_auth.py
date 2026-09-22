import hashlib
import subprocess
import os
import platform
from pathlib import Path
from datetime import datetime

# Import logging
from utils.logger import AstaLogger
from security.crypto_manager import save_encrypted_json, load_encrypted_json

SECRET_SALT = "ASTA_UNASMOH_SPACE_DEV_2024"
SECRET_SALT_HACKING = "ASTA_HACKING_PREMIUM_2024"
ANTI_DEBUG_ACTIVE = True

def check_anti_debug():
    """Détecte si l'app est analysée ou déboguée."""
    if not ANTI_DEBUG_ACTIVE:
        return
    import sys
    if sys.gettrace() is not None:
        sys.exit(0)

def get_raw_uuid() -> str:
    """Récupère l'UUID de la carte mère."""
    return f"{platform.node()}-{os.getenv('USERNAME', 'user')}"

def generate_hwid() -> str:
    """Génère un HWID de 16 caractères en SHA-256."""
    raw = get_raw_uuid()
    salted = f"{raw}{SECRET_SALT}"
    full_hash = hashlib.sha256(salted.encode()).hexdigest().upper()
    hwid = full_hash[:16]
    return f"{hwid[:4]}-{hwid[4:8]}-{hwid[8:12]}-{hwid[12:16]}"

def generate_license_key(hwid: str) -> str:
    """Génère la clé de licence attendue pour un HWID donné."""
    raw_hwid = hwid.replace("-", "")
    combined = f"{raw_hwid}{SECRET_SALT}_LICENSE"
    full_hash = hashlib.sha256(combined.encode()).hexdigest().upper()
    key = full_hash[:20]
    return f"{key[:5]}-{key[5:10]}-{key[10:15]}-{key[15:20]}"

def generate_hacking_key(hwid: str) -> str:
    """Génère la clé premium pour l'onglet Hacking."""
    raw_hwid = hwid.replace("-", "")
    combined = f"{raw_hwid}{SECRET_SALT_HACKING}_HACKING"
    full_hash = hashlib.sha256(combined.encode()).hexdigest().upper()
    key = full_hash[:20]
    return f"{key[:5]}-{key[5:10]}-{key[10:15]}-{key[15:20]}"

def verify_license(hwid: str, entered_key: str) -> bool:
    expected = generate_license_key(hwid)
    is_valid = entered_key.strip().upper() == expected.strip().upper()
    if is_valid:
        AstaLogger.security(f"✅ Tentative de connexion RÉUSSIE avec la clé : {entered_key.strip().upper()}")
    else:
        AstaLogger.security(f"❌ Tentative de connexion ÉCHOUÉE avec la clé : {entered_key.strip().upper()}")
    return is_valid

def verify_hacking_key(hwid: str, entered_key: str) -> bool:
    expected = generate_hacking_key(hwid)
    is_valid = entered_key.strip().upper() == expected.strip().upper()
    if is_valid:
        AstaLogger.security(f"✅ Clé Hacking validée : {entered_key.strip().upper()}")
    else:
        AstaLogger.security(f"❌ Échec validation clé Hacking : {entered_key.strip().upper()}")
    return is_valid

def _get_registry_path() -> Path:
    from core.config import DATA_DIR
    return DATA_DIR / "config" / "registre_licences.enc"

def load_license() -> dict:
    """Charge et déchiffre la licence depuis le registre sécurisé."""
    return load_encrypted_json(_get_registry_path(), {})

def load_hacking_license() -> str:
    saved = load_license()
    return saved.get("cle_hacking", "")

def save_hacking_license(key: str):
    saved = load_license()
    saved["cle_hacking"] = key
    save_encrypted_json(_get_registry_path(), saved)
    AstaLogger.security("Licence hacking mise à jour dans le registre.")

def save_license(hwid: str, key: str, hacking_key: str = "", nom: str = "Étudiant", actif: bool = True):
    """Sauvegarde la licence dans le registre sécurisé."""
    data = {
        "nom": nom,
        "cle": key,
        "cle_hacking": hacking_key,
        "hwid": hwid,
        "date_activation": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "actif": actif
    }
    save_encrypted_json(_get_registry_path(), data)
    
    # Création d'une copie lisible pour l'utilisateur dans ses documents
    try:
        from core.config import DATA_DIR
        licence_backup = DATA_DIR / "Ma_Licence_Asta.txt"
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        with open(licence_backup, "w", encoding="utf-8") as f:
            f.write(f"=== LICENCE ASTA ACADÉMIE ===\n")
            f.write(f"Nom : {nom}\n")
            f.write(f"HWID : {hwid}\n")
            f.write(f"Clé de Licence Principale : {key}\n")
            if hacking_key:
                f.write(f"Clé Hacking : {hacking_key}\n")
            f.write(f"Date d'activation : {data['date_activation']}\n")
            f.write(f"\nGardez ce fichier en sécurité. En cas de réinstallation sur le même PC, utilisez ces clés.\n")
    except Exception as e:
        AstaLogger.error(f"Erreur sauvegarde copie licence txt: {e}")

    AstaLogger.security(f"Licence (Base + Hacking) synchronisée pour HWID: {hwid}")

def check_license_on_startup(event=None) -> tuple[bool, str]:
    """
    Vérifie le HWID matériel, le compare avec le registre sécurisé.
    Bloque immédiatement si HWID mismatch ou actif == false.
    """
    check_anti_debug()
    actual_hwid = generate_hwid()
    saved = load_license()

    if saved:
        saved_hwid = saved.get("hwid", "")
        saved_key  = saved.get("cle", "")
        is_active  = saved.get("actif", False)
        
        # Kill Switch Check
        if not is_active:
            AstaLogger.security("Licence bloquée par l'administrateur (actif=False).")
            return False, actual_hwid
            
        # Hardware Lock Check
        if saved_hwid != actual_hwid:
            AstaLogger.security(f"ALERTE MATÉRIELLE : L'application a été copiée d'un autre PC. HWID attendu: {saved_hwid}, actuel: {actual_hwid}")
            return False, actual_hwid
            
        # Key Check
        if verify_license(actual_hwid, saved_key):
            AstaLogger.security("Licence matérielle validée avec succès.")
            return True, actual_hwid

    return False, actual_hwid

def log_usage(action: str = "startup"):
    """Enregistre les statistiques d'utilisation localement."""
    AstaLogger.info(f"Action: {action}")