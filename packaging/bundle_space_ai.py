"""
Copie le bundle Space AI minimal vers dist/ (build PyInstaller).
Exclut venv, __pycache__, captures d'écran, etc.
"""
from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "Space AI"
DST = ROOT / "dist" / "Space AI"

INCLUDE_FILES = (
    "main5.py",
    "ha_config.py",
    "SpaceAI_agent.py",
    "DEMARRER_SPACEAI.bat",
    "install.bat",
    "requirements.txt",
    ".env.example",
)

EXCLUDE_DIRS = {"venv", "__pycache__", ".git", "_setup", "node_modules", "frontend"}


def bundle() -> bool:
    if not SRC.is_dir():
        print("[bundle_space_ai] Dossier source introuvable:", SRC)
        return False

    if DST.exists():
        shutil.rmtree(DST)
    DST.mkdir(parents=True)

    copied = 0
    for name in INCLUDE_FILES:
        src = SRC / name
        if src.is_file():
            shutil.copy2(src, DST / name)
            copied += 1

    env_example = DST / ".env.example"
    env_target = DST / ".env"
    if env_example.is_file() and not env_target.is_file():
        shutil.copy2(env_example, env_target)

    print(f"[bundle_space_ai] {copied} fichiers -> {DST}")
    return copied > 0


if __name__ == "__main__":
    ok = bundle()
    raise SystemExit(0 if ok else 1)
