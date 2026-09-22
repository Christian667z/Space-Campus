import os
import sys
import subprocess
import re
import shutil
import tempfile
from pathlib import Path

ANSI_ESCAPE = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

ROOT = Path(__file__).resolve().parent
SPACE_AI_DIR = ROOT / "Space AI"


def print_red(text):
    sys.stdout.write(f"\033[91m{text}\033[0m\n")
    sys.stdout.flush()


def run_command_red(cmd_args, cwd=None):
    process = subprocess.Popen(
        cmd_args,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding='utf-8',
        errors='replace',
        cwd=cwd,
    )
    while True:
        line = process.stdout.readline()
        if not line and process.poll() is not None:
            break
        if line:
            clean_line = ANSI_ESCAPE.sub('', line).rstrip('\r\n')
            print_red(clean_line)
    return process.returncode


def setup_space_ai_env():
    """Cree space_ai.env dans AppData (utilise par l'onglet Space AI)."""
    try:
        from core.config import DATA_DIR
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        appdata_env = DATA_DIR / "space_ai.env"
        if appdata_env.is_file():
            print_red(f"[OK] {appdata_env}")
            return
        example = SPACE_AI_DIR / ".env.example"
        if example.is_file():
            shutil.copy2(example, appdata_env)
        else:
            appdata_env.write_text(
                "GEMINI_API_KEY=VOTRE_CLE_ICI\n",
                encoding="utf-8",
            )
        print_red(f"[OK] Fichier cree : {appdata_env}")
    except Exception as exc:
        print_red(f"[ATTENTION] space_ai.env : {exc}")


def bundle_space_ai_dev():
    """S'assure que les fichiers JARVIS essentiels sont presents."""
    if not SPACE_AI_DIR.is_dir():
        print_red("[ATTENTION] Dossier 'Space AI' absent — JARVIS desactive.")
        return
    required = ["main5.py", "DEMARRER_SPACEAI.bat"]
    missing = [f for f in required if not (SPACE_AI_DIR / f).is_file()]
    if missing:
        print_red(f"[ATTENTION] Fichiers manquants dans Space AI : {', '.join(missing)}")
    else:
        print_red("[OK] Dossier Space AI pret (JARVIS).")


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(errors='replace')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(errors='replace')

    if os.name == 'nt':
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-12), 7)

    os.chdir(ROOT)

    print_red("==============================================================")
    print_red("        INSTALLATEUR ASTA ACADEMIE (PySide6 + Space AI)")
    print_red("==============================================================")
    print_red("")

    if not (ROOT / "main_qt.py").is_file():
        print_red("[ERREUR] main_qt.py introuvable.")
        print_red("Lancez install_asta.bat depuis le dossier AstaAcademie.")
        input("\nAppuyez sur une touche pour continuer...")
        sys.exit(1)

    if not (ROOT / "requirements.txt").is_file():
        print_red("[ERREUR] requirements.txt introuvable.")
        input("\nAppuyez sur une touche pour continuer...")
        sys.exit(1)

    # ── 1. uv ────────────────────────────────────────────────────────
    print_red("[1/6] Verification de uv...")
    uv_check = subprocess.run("where uv", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if uv_check.returncode != 0:
        print_red("[INFO] uv absent. Installation...")
        run_command_red(
            'powershell -ExecutionPolicy Bypass -NoProfile -Command '
            '"irm https://astral.sh/uv/install.ps1 | iex"'
        )
        user_path = os.path.expandvars(r"%USERPROFILE%\.local\bin;%LOCALAPPDATA%\uv\bin")
        os.environ["PATH"] = user_path + os.pathsep + os.environ["PATH"]
        if subprocess.run("where uv", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode != 0:
            print_red("[ERREUR] uv introuvable apres installation. Redemarrez le terminal.")
            input("\nAppuyez sur une touche pour continuer...")
            sys.exit(1)
    print_red("[OK] uv disponible.")
    print_red("")

    # ── 2. venv + deps (pip robuste, reseau partiel OK) ─────────────
    print_red("[2/6] Environnement virtuel et dependances (PySide6, Gemini...)...")
    sys.path.insert(0, str(ROOT))
    from utils.deps_install import install_all_requirements, PY_WIN

    if not install_all_requirements(print_red):
        print_red("")
        print_red("Astuce : lancez reparer_venv.bat ou supprimez le dossier .venv puis relancez.")
        input("\nAppuyez sur une touche pour continuer...")
        sys.exit(1)

    if not PY_WIN.is_file():
        print_red("[ERREUR] Python du venv introuvable.")
        input("\nAppuyez sur une touche pour continuer...")
        sys.exit(1)

    print_red("[OK] Dependances principales installees.")
    print_red("")

    # ── 3. Ressources / logos ────────────────────────────────────────
    print_red("[3/6] Verification des ressources et logos...")
    assets = ROOT / "assets"
    checks = [
        assets / "Space_logo.ico",
        assets / "Space_logo_256.png",
        assets / "space_ai_logo.svg",
        assets / "asta_academie_mark.svg",
    ]
    for path in checks:
        if path.is_file():
            print_red(f"  [OK] {path.name}")
        else:
            print_red(f"  [ATTENTION] Manquant : {path}")
    print_red("")

    # ── 4. Space AI ────────────────────────────────────────────────────
    print_red("[4/6] Configuration Space AI (onglet integre)...")
    setup_space_ai_env()
    print_red("  Cle Gemini : %APPDATA%\\AstaAcademie\\space_ai.env")
    print_red("  Lanceur unique : LANCER_ASTA_ACADEMIE.bat")
    print_red("")

    # ── 5. Raccourci Bureau (main_qt.py) ───────────────────────────────
    print_red("[5/6] Raccourci Bureau (LANCER_ASTA_ACADEMIE.bat)...")
    app_dir = str(ROOT)
    shortcut_path = os.path.expandvars(r"%USERPROFILE%\Desktop\Asta Academie.lnk")
    launcher_bat = str(ROOT / "LANCER_ASTA_ACADEMIE.bat")
    icon_candidates = [
        ROOT / "assets" / "Space_logo.ico",
        ROOT / "Space_logo.ico",
    ]
    icon_path = next((str(p) for p in icon_candidates if p.is_file()), launcher_bat)

    vbs_content = f"""
Set oWS = WScript.CreateObject("WScript.Shell")
sLinkFile = "{shortcut_path}"
Set oLink = oWS.CreateShortcut(sLinkFile)
oLink.TargetPath = "{launcher_bat}"
oLink.WorkingDirectory = "{app_dir}"
oLink.Description = "Asta Academie — UNASMOH"
oLink.IconLocation = "{icon_path}"
oLink.Save
"""
    vbs_file = os.path.join(tempfile.gettempdir(), "AstaShortcut.vbs")
    try:
        with open(vbs_file, "w", encoding="utf-8") as f:
            f.write(vbs_content)
        if subprocess.run(f'cscript /nologo "{vbs_file}"', shell=True).returncode == 0:
            print_red("[OK] Raccourci : Bureau\\Asta Academie")
        else:
            print_red("[ATTENTION] Raccourci non cree.")
    except Exception as e:
        print_red(f"[ATTENTION] Raccourci : {e}")
    finally:
        if os.path.exists(vbs_file):
            os.remove(vbs_file)
    print_red("")

    # ── 6. Lancement ───────────────────────────────────────────────────
    print_red("[6/6] Lancement de Asta Academie...")
    print_red("")
    print_red("==============================================================")
    print_red("        INSTALLATION TERMINEE")
    print_red("==============================================================")
    print_red("  Lancer     : LANCER_ASTA_ACADEMIE.bat")
    print_red("  Space AI   : onglet dans l'app (pas de fenetre externe)")
    print_red("  Build exe  : build_asta.bat")
    print_red("==============================================================")

    subprocess.Popen([launcher_bat], cwd=app_dir, shell=True, start_new_session=True)
    sys.exit(0)


if __name__ == '__main__':
    main()
