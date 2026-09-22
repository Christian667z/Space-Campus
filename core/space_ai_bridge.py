"""
Pont entre Asta Académie (onglet Space AI) et le dossier « Space AI » (JARVIS / Gemini).
"""
from __future__ import annotations

import logging
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

_API_PLACEHOLDERS = frozenset({
    "", "VOTRE_CLE_ICI", "votre_cle_ici", "VOTRE_TOKEN_ICI", "votre_token_ici",
})

DEFAULT_MODEL = "gemini-2.0-flash"


def _project_root() -> Path:
    """Racine installée : à côté de l'exe (build) ou racine du dépôt (dev)."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent.parent


def _bundled_assets_dir() -> Path:
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS) / "assets"
    return _project_root() / "assets"


def get_space_ai_dir() -> Path:
    """Dossier « Space AI » à la racine du projet."""
    return _project_root() / "Space AI"


def get_main_script() -> Path:
    """Script principal JARVIS (main5.py)."""
    folder = get_space_ai_dir()
    for name in ("main5.py", "main2.py"):
        path = folder / name
        if path.is_file():
            return path
    return folder / "main5.py"


def get_python_executable() -> Path:
    """Python du venv Space AI, sinon l'interpréteur courant."""
    folder = get_space_ai_dir()
    if sys.platform == "win32":
        venv_py = folder / "venv" / "Scripts" / "python.exe"
    else:
        venv_py = folder / "venv" / "bin" / "python"
    if venv_py.is_file():
        return venv_py
    return Path(sys.executable)


def load_space_ai_env() -> None:
    """Charge la cle Gemini : AppData puis dossier Space AI (optionnel)."""
    candidates = []
    try:
        from core.config import DATA_DIR
        candidates.append(DATA_DIR / "space_ai.env")
    except Exception:
        pass
    candidates.append(get_space_ai_dir() / ".env")

    env_file = next((p for p in candidates if p.is_file()), None)
    if not env_file:
        return
    try:
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key, value = key.strip(), value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value
    except OSError as exc:
        logger.warning("Impossible de lire %s : %s", env_file, exc)


def _key_valid(key: Optional[str]) -> bool:
    return bool(key) and str(key).strip() not in _API_PLACEHOLDERS


def is_cloud_available() -> bool:
    load_space_ai_env()
    return _key_valid(os.environ.get("GEMINI_API_KEY"))


def is_jarvis_installed() -> bool:
    return get_main_script().is_file()


def build_academie_system_prompt(profile: dict, rag_context: str = "") -> str:
    nom = profile.get("nom", "Étudiant")
    memoire = profile.get("ai_memory", "")
    parts = [
        "Tu es Space AI, l'assistant intelligent intégré à Asta Académie (UNASMOH).",
        f"L'étudiant s'appelle {nom}.",
        "Réponds en français, de façon claire, pédagogique et professionnelle.",
        "Priorise les cours, la révision, les quiz et la navigation dans l'application.",
        "Si la question concerne un cours, appuie-toi sur le contexte fourni.",
        "Réponses concises (max ~12 lignes) sauf si l'utilisateur demande plus de détails.",
    ]
    if memoire:
        parts.append(f"Profil mémorisé de l'étudiant : {memoire}")
    if rag_context:
        parts.append(f"\n--- Contexte cours (RAG) ---\n{rag_context}")
    return "\n".join(parts)


def generate_cloud_response(
    user_text: str,
    profile: dict,
    rag_context: str = "",
    model: str = DEFAULT_MODEL,
) -> Optional[str]:
    """
    Appelle Gemini via google.genai (même stack que le dossier Space AI).
    Retourne None si indisponible ou en cas d'erreur.
    """
    load_space_ai_env()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not _key_valid(api_key):
        return None

    try:
        import google.genai as genai
        from google.genai import types
    except ImportError:
        logger.info("google.genai non installé — mode cloud désactivé.")
        return None

    try:
        client = genai.Client(api_key=api_key)
        system = build_academie_system_prompt(profile, rag_context)
        response = client.models.generate_content(
            model=model,
            contents=[types.Content(
                role="user",
                parts=[types.Part(text=user_text)],
            )],
            config=types.GenerateContentConfig(
                system_instruction=system,
                temperature=0.7,
                max_output_tokens=1024,
            ),
        )
        text = getattr(response, "text", None) or ""
        return text.strip() or None
    except Exception as exc:
        logger.warning("Erreur Gemini Space AI : %s", exc)
        return None


def launch_jarvis_app(detached: bool = True) -> tuple[bool, str]:
    """
    Lance l'assistant JARVIS complet (main5.py) dans un processus séparé.
    """
    script = get_main_script()
    if not script.is_file():
        return False, f"Script introuvable : {script}"

    python = get_python_executable()
    cwd = get_space_ai_dir()
    try:
        kwargs = {
            "cwd": str(cwd),
            "env": os.environ.copy(),
        }
        if sys.platform == "win32":
            kwargs["creationflags"] = subprocess.CREATE_NEW_CONSOLE
        if detached:
            subprocess.Popen(
                [str(python), str(script.name)],
                **kwargs,
            )
        else:
            subprocess.run(
                [str(python), str(script.name)],
                cwd=str(cwd),
                check=False,
            )
        return True, "JARVIS Space AI lancé."
    except OSError as exc:
        logger.error("Échec lancement JARVIS : %s", exc)
        return False, str(exc)


def asset_path(name: str) -> Path:
    """Chemin vers un asset (bundlé PyInstaller ou dossier assets/)."""
    root = _bundled_assets_dir()
    primary = root / name
    if primary.is_file():
        return primary
    fallback = root / "Space_logo_256.png"
    if fallback.is_file():
        return fallback
    return primary
