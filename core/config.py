import os
import sys
import json
from pathlib import Path
from utils.logger import AstaLogger
from utils.updates_asta import CURRENT_VERSION


def get_base_dir() -> Path:
    """Racine de l'app (sources ou dossier contenant l'exe PyInstaller)."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent.parent


BASE_DIR = get_base_dir()


def asset_file(filename: str) -> Path:
    """Résout un fichier dans assets/ (dev ou exe PyInstaller)."""
    for base in (get_base_dir(),):
        candidate = base / "assets" / filename
        if candidate.is_file():
            return candidate
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        bundled = Path(sys._MEIPASS) / "assets" / filename
        if bundled.is_file():
            return bundled
    return get_base_dir() / "assets" / filename

APP_NAME  = "Asta Académie"
VERSION   = CURRENT_VERSION
UNIVERSITE = "UNASMOH"
FULL_UNI  = "Université Américaine des Sciences Modernes"
OPTION    = "Sciences Informatiques"
DEV_NAME  = "Space | Asta Dev"
DEV_REAL  = "Lucky Luke"
PROMO     = "2024-2028"
WHATSAPP  = "+509 3567-2037"

import os
from pathlib import Path
import json

# Charger dynamiquement le dossier d'installation si configuré
def get_data_dir():
    try:
        from pathlib import Path
        import os
        # Utiliser le dossier "Documents/AstaAcademie" pour que l'utilisateur y ait accès facilement
        documents_path = Path(os.environ['USERPROFILE']) / 'Documents' if os.name == 'nt' else Path.home() / 'Documents'
        appdata = documents_path / "AstaAcademie"
    except Exception:
        appdata = Path(os.getenv("APPDATA", ".")) / "AstaAcademie"
        
    launcher_cfg = appdata / "launcher_path.json"
    if launcher_cfg.exists():
        try:
            cfg = json.loads(launcher_cfg.read_text(encoding="utf-8"))
            if "install_dir" in cfg and Path(cfg["install_dir"]).exists():
                return Path(cfg["install_dir"])
        except Exception:
            pass
    return appdata

DATA_DIR     = get_data_dir()
DATA_DIR.mkdir(parents=True, exist_ok=True)

PROFILE_FILE = DATA_DIR / "profile.enc"
NOTES_FILE   = DATA_DIR / "notes.json"
SCORES_FILE  = DATA_DIR / "scores.json"
DB_FILE      = DATA_DIR / "asta_database.db" # SQLite (deprecated)
SESSION_FILE = DATA_DIR / "session.json"
LICENSE_FILE = DATA_DIR / "license.key"

# Configuration du LLM local (commande CLI). Exemple:
# LOCAL_LLM_CMD = "gpt4all --model ./models/gpt4all-lora.bin --n_predict {max_tokens} --n_keep 64 --context 2048"
# Le placeholder {max_tokens} sera remplacé par la valeur fournie.
LOCAL_LLM_CMD = os.getenv("LOCAL_LLM_CMD", "")
LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "512"))
LLM_TIMEOUT = int(os.getenv("LLM_TIMEOUT", "30"))

COLORS = {
    # ── Thèmes classiques ─────────────────────────────────────────────
    "noir_blanc_1": {
        "bg": "#FFFFFF", "sidebar": "#F0F0F0", "card": "#FFFFFF",
        "accent": "#000000", "accent2": "#333333", "text": "#000000",
        "subtext": "#666666", "border": "#CCCCCC", "success": "#1a7a1a",
        "warning": "#8a6000", "danger": "#cc0000", "hover": "#E0E0E0",
    },
    "noir_blanc_2": {
        "bg": "#0d0d0d", "sidebar": "#151515", "card": "#1a1a1a",
        "accent": "#FFFFFF", "accent2": "#CCCCCC", "text": "#FFFFFF",
        "subtext": "#888888", "border": "#333333", "success": "#00cc44",
        "warning": "#ffaa00", "danger": "#ff4444", "hover": "#252525",
    },
    "noir_vert": {
        "bg": "#0f172a", "sidebar": "#1e293b", "card": "#111827",
        "accent": "#10b981", "accent2": "#0ea5e9", "text": "#f8fafc",
        "subtext": "#94a3b8", "border": "#334155", "success": "#10b981",
        "warning": "#eab308", "danger": "#ef4444", "hover": "#1e293b",
    },
    # ── Nouveaux thèmes ───────────────────────────────────────────────
    "rouge_noir": {
        "bg": "#0a0000", "sidebar": "#130000", "card": "#1a0000",
        "accent": "#ff2222", "accent2": "#cc0000", "text": "#ffcccc",
        "subtext": "#883333", "border": "#440000", "success": "#ff4444",
        "warning": "#ff8800", "danger": "#ff0000", "hover": "#220000",
    },
    "bleu_nuit": {
        "bg": "#00001a", "sidebar": "#000d2e", "card": "#001040",
        "accent": "#4fc3f7", "accent2": "#0288d1", "text": "#e3f2fd",
        "subtext": "#4a7aaa", "border": "#003366", "success": "#00e5ff",
        "warning": "#ffd740", "danger": "#ff5252", "hover": "#001a4d",
    },
    "violet_cyber": {
        "bg": "#0d0010", "sidebar": "#150020", "card": "#1a002a",
        "accent": "#cc44ff", "accent2": "#9900cc", "text": "#f0ccff",
        "subtext": "#7733aa", "border": "#440066", "success": "#44ff99",
        "warning": "#ffcc00", "danger": "#ff3366", "hover": "#220033",
    },
    "orange_feu": {
        "bg": "#0d0500", "sidebar": "#1a0a00", "card": "#221000",
        "accent": "#ff7700", "accent2": "#cc5500", "text": "#ffe0cc",
        "subtext": "#996633", "border": "#553300", "success": "#aaff00",
        "warning": "#ffdd00", "danger": "#ff3300", "hover": "#2a1500",
    },
    "rose_neon": {
        "bg": "#0d0008", "sidebar": "#1a0015", "card": "#220020",
        "accent": "#ff44aa", "accent2": "#cc0077", "text": "#ffe0f0",
        "subtext": "#883366", "border": "#440033", "success": "#44ffbb",
        "warning": "#ffcc44", "danger": "#ff2244", "hover": "#280025",
    },
    "ocean": {
        "bg": "#001520", "sidebar": "#002030", "card": "#002a40",
        "accent": "#00e5cc", "accent2": "#00b3a0", "text": "#ccfff8",
        "subtext": "#336677", "border": "#004455", "success": "#00ff99",
        "warning": "#ffcc00", "danger": "#ff5555", "hover": "#003348",
    },
}

def get_translation(lang_code="fr"):
    locale_file = Path("locales") / f"{lang_code}.json"
    if locale_file.exists():
        try:
            return json.loads(locale_file.read_text(encoding="utf-8"))
        except:
            pass
    # Fallback
    fallback = Path("locales") / "fr.json"
    if fallback.exists():
        return json.loads(fallback.read_text(encoding="utf-8"))
    return {}

def load_json(path, default):
    try:
        if path.exists():
            # If file ends with .enc, try encrypted loader
            if str(path).endswith('.enc'):
                try:
                    from security.crypto_manager import load_encrypted_json
                    return load_encrypted_json(path, default)
                except Exception:
                    pass
            return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        AstaLogger.error(f"Erreur lors du chargement de {path}: {e}", exc_info=True)
    return default

def save_json(path, data):
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        # If path ends with .enc, try encrypted save
        if str(path).endswith('.enc'):
            try:
                from security.crypto_manager import save_encrypted_json
                ok = save_encrypted_json(path, data)
                if ok:
                    return
            except Exception:
                pass
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception as e:
        AstaLogger.error(f"Erreur lors de la sauvegarde de {path}: {e}", exc_info=True)


# Migration automatique depuis l'ancien profile.json vers profile.enc chiffré
def _migrate_plain_profile() -> None:
    try:
        plain = DATA_DIR / "profile.json"
        enc = PROFILE_FILE
        # Si le fichier ancien existe, mais que le fichier chiffré n'existe pas,
        # on migre et on supprime l'ancien.
        if plain.exists():
            try:
                # Lire le JSON en clair
                raw = json.loads(plain.read_text(encoding="utf-8"))
            except Exception:
                raw = {}
            try:
                save_json(enc, raw)
                # Créer une sauvegarde horodatée du fichier en clair avant suppression
                try:
                    import shutil
                    from datetime import datetime
                    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                    backup_file = plain.with_name(f"{plain.name}.{ts}.bak")
                    shutil.copy2(str(plain), str(backup_file))
                    plain.unlink()
                except Exception:
                    # Si la sauvegarde échoue, ne pas supprimer l'original
                    AstaLogger.error("Échec de la création de la sauvegarde du profile.json lors de la migration.")
            except Exception as e:
                AstaLogger.error(f"Échec de migration profile -> profile.enc: {e}", exc_info=True)
    except Exception as e:
        AstaLogger.error(f"Erreur lors de la vérification de migration du profile: {e}", exc_info=True)


# Lancer la migration au chargement du module
_migrate_plain_profile()

