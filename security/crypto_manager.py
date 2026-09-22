import json
from pathlib import Path
import hashlib
import base64
from cryptography.fernet import Fernet
from utils.logger import AstaLogger

# Constante secrète, elle doit rester identique pour pouvoir déchiffrer
SECRET_SALT = "ASTA_UNASMOH_SPACE_DEV_2024_AES256"
# La clé doit faire 32 octets (256 bits)
AES_KEY = hashlib.sha256(SECRET_SALT.encode()).hexdigest()[:32]

HAS_CPP_CORE = False
try:
    import core.core_speed as cs
    HAS_CPP_CORE = True
except ImportError:
    AstaLogger.error("Le module C++ core_speed (AES-256) est introuvable. Utilisation de Fernet en solution de secours.")

def _get_fallback_fernet() -> Fernet:
    key = hashlib.sha256(SECRET_SALT.encode()).digest()
    b64_key = base64.urlsafe_b64encode(key)
    return Fernet(b64_key)

def encrypt_data(data: dict) -> bytes:
    json_data = json.dumps(data, ensure_ascii=False)
    if HAS_CPP_CORE:
        return cs.encrypt_aes256(json_data.encode("utf-8"), AES_KEY)
    else:
        f = _get_fallback_fernet()
        return b"FERNET_FALLBACK|" + f.encrypt(json_data.encode("utf-8"))

def decrypt_data(encrypted_bytes: bytes) -> dict:
    try:
        if encrypted_bytes.startswith(b"FERNET_FALLBACK|"):
            f = _get_fallback_fernet()
            decrypted_json = f.decrypt(encrypted_bytes[16:]).decode("utf-8")
            return json.loads(decrypted_json)
        
        if HAS_CPP_CORE:
            decrypted_bytes = cs.decrypt_aes256(encrypted_bytes, AES_KEY)
            return json.loads(decrypted_bytes.decode("utf-8"))
        else:
            AstaLogger.error("Impossible de déchiffrer un fichier AES-256 sans le module C++.")
            return {}
    except Exception as e:
        AstaLogger.error(f"Erreur de déchiffrement : {e}")
        return {}

def save_encrypted_json(path: Path, data: dict) -> bool:
    """Sauvegarde un dictionnaire dans un fichier chiffré."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        encrypted = encrypt_data(data)
        path.write_bytes(encrypted)
        return True
    except Exception as e:
        AstaLogger.error(f"Erreur d'écriture chiffrée sur {path}: {e}")
        return False

def load_encrypted_json(path: Path, default=None) -> dict:
    """Charge un fichier chiffré et le retourne en dictionnaire."""
    if default is None:
        default = {}
    if not path.exists():
        return default
    try:
        encrypted_bytes = path.read_bytes()
        return decrypt_data(encrypted_bytes)
    except Exception as e:
        AstaLogger.error(f"Erreur de lecture chiffrée sur {path}: {e}")
        return default
