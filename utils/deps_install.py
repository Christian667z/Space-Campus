"""
Installation robuste des dépendances (réseau instable, venv sans pip).
Utilisé par install_red.py et build_red.py.
"""
from __future__ import annotations

import shutil
import socket
import subprocess
import sys
from pathlib import Path
from typing import Callable, Optional

ROOT = Path(__file__).resolve().parent.parent
VENV_DIR = ROOT / ".venv"
PY_WIN = VENV_DIR / "Scripts" / "python.exe"


def _run(cmd: str, log: Callable[[str], None], cwd: Optional[Path] = None) -> int:
    log(f"  > {cmd}")
    proc = subprocess.Popen(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        cwd=str(cwd or ROOT),
    )
    while True:
        line = proc.stdout.readline()
        if not line and proc.poll() is not None:
            break
        if line:
            log(line.rstrip("\r\n"))
    return proc.returncode or 0


def network_ok(host: str = "pypi.org", port: int = 443, timeout: float = 4.0) -> bool:
    try:
        socket.create_connection((host, port), timeout=timeout)
        return True
    except OSError:
        return False


def recreate_venv(log: Callable[[str], None]) -> bool:
    """Recrée .venv avec pip intégré (ensurepip)."""
    if VENV_DIR.exists():
        log("[INFO] Suppression de l'ancien .venv (pip manquant ou corrompu)...")
        try:
            shutil.rmtree(VENV_DIR)
        except OSError as exc:
            log(f"[ATTENTION] Impossible de supprimer .venv : {exc}")

    if shutil.which("uv"):
        for args in ("uv venv --python 3.12", "uv venv"):
            if _run(args, log) == 0 and PY_WIN.is_file():
                _run(f'uv pip install pip setuptools wheel --python "{PY_WIN}"', log)
                if _pip_works(log):
                    return True

    for py_cmd in ("py -3.12", "py -3.11", "py -3", "python"):
        if _run(f'{py_cmd} -m venv "{VENV_DIR}"', log) == 0 and PY_WIN.is_file():
            bootstrap_pip(log)
            if _pip_works(log):
                return True
    return False


def bootstrap_pip(log: Callable[[str], None]) -> None:
    py = f'"{PY_WIN}"'
    _run(f"{py} -m ensurepip --upgrade", log)
    _run(f"{py} -m pip install --upgrade pip setuptools wheel", log)


def _pip_works(log: Callable[[str], None]) -> bool:
    return _run(f'"{PY_WIN}" -m pip --version', log) == 0


def pip_install_file(req_file: Path, log: Callable[[str], None], retries: int = 2) -> bool:
    if not req_file.is_file():
        log(f"[ERREUR] Fichier introuvable : {req_file}")
        return False

    py = f'"{PY_WIN}"'
    timeout = "--default-timeout=180"

    for attempt in range(1, retries + 2):
        log(f"[INFO] Installation {req_file.name} (tentative {attempt})...")
        if _run(f'{py} -m pip install -r "{req_file}" {timeout}', log) == 0:
            return True

    if shutil.which("uv") and PY_WIN.is_file():
        if _run(f'uv pip install -r "{req_file}" --python "{PY_WIN}"', log) == 0:
            return True

    return False


def pip_install_packages(packages: str, log: Callable[[str], None]) -> bool:
    py = f'"{PY_WIN}"'
    return _run(f"{py} -m pip install {packages} --default-timeout=180", log) == 0


def ensure_venv_ready(log: Callable[[str], None]) -> bool:
    if not PY_WIN.is_file():
        log("[INFO] Creation de l'environnement virtuel...")
        return recreate_venv(log)

    if not _pip_works(log):
        log("[INFO] pip absent dans .venv — reparation...")
        bootstrap_pip(log)
        if _pip_works(log):
            return True
        return recreate_venv(log)

    return True


def install_all_requirements(log: Callable[[str], None]) -> bool:
    if not ensure_venv_ready(log):
        log("[ERREUR] Impossible de preparer .venv avec pip.")
        return False

    if not network_ok():
        log("")
        log("[ATTENTION] Reseau : pypi.org injoignable (DNS / Internet).")
        log("  Verifiez Wi-Fi, puis : ipconfig /flushdns")
        log("")

    if not pip_install_file(ROOT / "requirements-core.txt", log):
        log("[ERREUR] Dependances principales (PySide6) non installees.")
        log_network_help(log)
        return False

    opt = ROOT / "requirements-optional.txt"
    if opt.is_file():
        if pip_install_file(opt, log):
            log("[OK] Space AI (Gemini) installe.")
        else:
            log("[ATTENTION] google-genai non installe — Space AI en mode Local seulement.")

    leg = ROOT / "requirements-legacy.txt"
    if leg.is_file() and not pip_install_file(leg, log):
        log("[ATTENTION] customtkinter non installe (ancienne UI main.py).")

    voice = ROOT / "requirements-voice.txt"
    if voice.is_file():
        if pip_install_file(voice, log):
            log("[OK] Module vocal Space AI installe.")
            _try_pyaudio(log)
        else:
            log("[ATTENTION] Voix non installee — chat texte OK, micro desactive.")

    return True


def _try_pyaudio(log: Callable[[str], None]) -> None:
    """PyAudio necessaire au micro (wheel precompile Windows)."""
    py = f'"{PY_WIN}"'
    if _run(f"{py} -m pip install pyaudio --only-binary :all: --default-timeout=180", log) == 0:
        log("[OK] PyAudio installe.")
        return
    log("[ATTENTION] PyAudio absent — pip install pyaudio (micro peut ne pas marcher).")


def install_build_deps(log: Callable[[str], None]) -> bool:
    if not ensure_venv_ready(log):
        return False

    core_build = (
        "pyinstaller PySide6 \"Pillow<10.0.0\" \"cryptography<42.0.0\" "
        "bcrypt python-dotenv"
    )
    log("[INFO] Installation des outils de compilation (sans Gemini d'abord)...")
    if not pip_install_packages(core_build, log):
        log_network_help(log)
        return False

    opt = ROOT / "requirements-optional.txt"
    if opt.is_file():
        if pip_install_file(opt, log):
            log("[OK] google-genai installe pour le build Space AI.")
        else:
            log("[ATTENTION] Build sans google-genai — exe OK, mode Cloud desactive.")

    return True


def log_network_help(log: Callable[[str], None]) -> None:
    log("")
    log("=== AIDE RESEAU (DNS / Hote inconnu) ===")
    log("  1. CMD admin : ipconfig /flushdns")
    log("  2. Test : ping pypi.org")
    log("  3. Relancez install_asta.bat ou build_asta.bat")
    log("  4. Autre reseau (partage 4G) si le Wi-Fi bloque PyPI")
    log("")
