import subprocess
import sys
import re
import os
from pathlib import Path

# Expression régulière pour supprimer les codes d'échappement ANSI existants
ANSI_ESCAPE = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

def print_red(text):
    """Affiche le texte spécifié en rouge vif dans la console."""
    # \033[91m = Rouge vif, \033[0m = Réinitialiser
    sys.stdout.write(f"\033[91m{text}\033[0m\n")
    sys.stdout.flush()

def run_command_red(cmd_args, cwd=None):
    """Exécute une commande et force toute sa sortie à s'afficher en rouge."""
    # Si c'est une liste d'arguments, on la convertit en chaîne pour shell=True ou on la garde selon le besoin
    process = subprocess.Popen(
        cmd_args,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding='utf-8',
        errors='replace',
        cwd=cwd
    )
    
    # Lire la sortie ligne par ligne en temps réel
    while True:
        line = process.stdout.readline()
        if not line and process.poll() is not None:
            break
        if line:
            clean_line = ANSI_ESCAPE.sub('', line).rstrip('\r\n')
            print_red(clean_line)
            
    return process.returncode

def main():
    # Éviter les plantages d'encodage Unicode sur les terminaux Windows (CP1252)
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(errors='replace')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(errors='replace')

    # Activer le support des codes ANSI sur Windows via ctypes si nécessaire
    if os.name == 'nt':
        import ctypes
        kernel32 = ctypes.windll.kernel32
        # Enable VT100 emulation
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-12), 7)

    fast_mode = "--fast" in sys.argv or "-f" in sys.argv or "fast" in sys.argv

    print_red("==============================================================")
    print_red("       COMPILATION D'ASTA ACADEMIE VERS .EXE (PySide6)")
    if fast_mode:
        print_red("                      [MODE RAPIDE ACTIVE]")
    print_red("==============================================================")
    print_red("==============================================================")
    print_red("")

    print_red("[0/4] Fermeture des instances en cours (Prevention WinError 5)...")
    run_command_red("taskkill /F /IM AstaAcademie.exe >nul 2>&1")
    run_command_red("taskkill /F /IM AstaAdmin.exe >nul 2>&1")
    print_red("")

    print_red("[1/5] Verification des dependances (PyInstaller, PySide6, Space AI)...")
    root = Path(__file__).resolve().parent
    os.chdir(root)  # Force le dossier courant pour éviter les erreurs "chemin introuvable"
    sys.path.insert(0, str(root))

    if fast_mode:
        print_red("[MODE RAPIDE] Saut de la verification/installation des dependances pip.")
    else:
        from utils.deps_install import install_build_deps
        if not install_build_deps(print_red):
            print_red("[ERREUR] Impossible d'installer PyInstaller ou les dependances.")
            print_red("Astuce : reparer_venv.bat puis build_asta.bat (Internet requis pour PyPI).")
            if hasattr(sys.stdin, 'isatty') and sys.stdin.isatty():
                input("\nAppuyez sur une touche pour continuer...")
            sys.exit(1)
    print_red("")

    print_red("[2/5] Configuration des DLL PySide6...")
    print_red("PyInstaller gere les DLL Qt nativement. Exclusion des modules lourds inutiles (WebEngine, 3D)...")
    print_red("")

    print_red("[2.5/5] Compilation des modules natifs (C++ / C#)...")
    import shutil
    
    if shutil.which("cmake") and shutil.which("cl"):
        if fast_mode and os.path.exists("core/core_speed.pyd"):
            print_red("---> Compilation du module C++ ignoree (deja existant en mode --fast)")
        else:
            print_red("---> Compilation du module C++ (core_speed.pyd)")
            run_command_red('cd cpp && mkdir build 2>nul & cd build && cmake .. -A x64 -DCMAKE_BUILD_TYPE=Release && cmake --build . --config Release')
            if os.path.exists("cpp/build/Release/core_speed.pyd"):
                os.makedirs("core", exist_ok=True)
                shutil.copy2("cpp/build/Release/core_speed.pyd", "core/")
                print_red("     [OK] core_speed.pyd copie dans core/")
            else:
                print_red("     [AVERTISSEMENT] Echec de la compilation C++ (core_speed.pyd introuvable).")
                
            if os.path.exists("cpp/build/Release/native_security.dll"):
                os.makedirs("dist", exist_ok=True)
                shutil.copy2("cpp/build/Release/native_security.dll", "csharp/AstaLauncher/")
                shutil.copy2("cpp/build/Release/native_security.dll", "dist/")
                print_red("     [OK] native_security.dll compile avec succes !")
    else:
        print_red("---> Outils C++ (cmake/cl) non trouves. Ignore.")

    if shutil.which("dotnet"):
        # AstaLauncher
        if fast_mode and os.path.exists("dist/AstaLauncher.exe"):
            print_red("---> Compilation de AstaLauncher.exe ignoree (deja existant en mode --fast)")
        else:
            print_red("---> Compilation de l'interface WPF (AstaLauncher.exe)")
            run_command_red('cd csharp\\AstaLauncher && dotnet publish -c Release -r win-x64 --self-contained true -p:PublishSingleFile=true -p:PublishReadyToRun=true -p:IncludeNativeLibrariesForSelfExtract=true')
            exe_launcher = "csharp/AstaLauncher/bin/Release/net8.0-windows/win-x64/publish/AstaLauncher.exe"
            if not os.path.exists(exe_launcher):
                exe_launcher = "csharp/AstaLauncher/bin/Release/net8.0/win-x64/publish/AstaLauncher.exe"
            if os.path.exists(exe_launcher):
                os.makedirs("dist", exist_ok=True)
                shutil.copy2(exe_launcher, "dist/")
                print_red("     [OK] AstaLauncher.exe copie dans dist/")

        # AstaAcademieLauncher
        if fast_mode and os.path.exists("dist/AstaAcademieLauncher.exe"):
            print_red("---> Compilation de AstaAcademieLauncher.exe ignoree (deja existant en mode --fast)")
        else:
            print_red("---> Compilation de l'interface WPF Etudiante (AstaAcademieLauncher.exe)")
            run_command_red('cd csharp\\AstaAcademieLauncher && dotnet publish -c Release -r win-x64 --self-contained true -p:PublishSingleFile=true -p:PublishReadyToRun=true -p:IncludeNativeLibrariesForSelfExtract=true')
            exe_student_launcher = "csharp/AstaAcademieLauncher/bin/Release/net8.0-windows/win-x64/publish/AstaAcademieLauncher.exe"
            if not os.path.exists(exe_student_launcher):
                exe_student_launcher = "csharp/AstaAcademieLauncher/bin/Release/net8.0/win-x64/publish/AstaAcademieLauncher.exe"
            if os.path.exists(exe_student_launcher):
                shutil.copy2(exe_student_launcher, "dist/")
                print_red("     [OK] AstaAcademieLauncher.exe copie dans dist/")

        # AstaAcademieApp
        if fast_mode and os.path.exists("dist/AstaWPF/AstaAcademieApp.exe"):
            print_red("---> Compilation de AstaAcademieApp.exe ignoree (deja existant en mode --fast)")
            # Copy assets (cours/ and data/) just in case they were updated
            if os.path.exists("cours"):
                shutil.copytree("cours", "dist/AstaWPF/cours", dirs_exist_ok=True)
                print_red("     [OK] cours/ copie dans dist/AstaWPF/cours/")
            if os.path.exists("data"):
                shutil.copytree("data", "dist/AstaWPF/data", dirs_exist_ok=True)
                print_red("     [OK] data/ copie dans dist/AstaWPF/data/")
        else:
            print_red("---> Compilation de l'interface WPF Principale (AstaAcademieApp.exe)")
            run_command_red('cd csharp\\AstaAcademieApp && dotnet publish -c Release -r win-x64 --self-contained true -p:PublishSingleFile=true -p:PublishReadyToRun=true -p:IncludeNativeLibrariesForSelfExtract=true')
            exe_app = "csharp/AstaAcademieApp/bin/Release/net9.0-windows/win-x64/publish/AstaAcademieApp.exe"
            if not os.path.exists(exe_app):
                exe_app = "csharp/AstaAcademieApp/bin/Release/net9.0/win-x64/publish/AstaAcademieApp.exe"
            if os.path.exists(exe_app):
                os.makedirs("dist/AstaWPF", exist_ok=True)
                shutil.copy2(exe_app, "dist/AstaWPF/")
                print_red("     [OK] AstaAcademieApp.exe copie dans dist/AstaWPF/")
                
                # Copy native_security.dll to dist/AstaWPF if available
                if os.path.exists("cpp/build/Release/native_security.dll"):
                    shutil.copy2("cpp/build/Release/native_security.dll", "dist/AstaWPF/")
                    print_red("     [OK] native_security.dll copie dans dist/AstaWPF/")
                elif os.path.exists("dist/native_security.dll"):
                    shutil.copy2("dist/native_security.dll", "dist/AstaWPF/")
                    print_red("     [OK] native_security.dll copie depuis dist/ vers dist/AstaWPF/")
                    
                # Copy assets (cours/ and data/)
                if os.path.exists("cours"):
                    shutil.copytree("cours", "dist/AstaWPF/cours", dirs_exist_ok=True)
                    print_red("     [OK] cours/ copie dans dist/AstaWPF/cours/")
                if os.path.exists("data"):
                    shutil.copytree("data", "dist/AstaWPF/data", dirs_exist_ok=True)
                    print_red("     [OK] data/ copie dans dist/AstaWPF/data/")
    else:
        print_red("---> .NET SDK (dotnet) non trouve. Ignore.")
    print_red("")

    print_red("[3/5] Compression des modules Premium (Hacking)...")
    run_command_red(".venv\\Scripts\\python.exe utils\\compress_hacking.py")
    print_red("")

    print_red("[4/5] Lancement de PyInstaller...")
    print_red("---> Compilation de l'application principale (AstaAcademie.exe)")
    
    cmd_academie = (
        ".venv\\Scripts\\python.exe -m PyInstaller --clean --noconfirm --onefile --windowed --name \"AstaAcademie\" "
        "--icon \"assets\\Space_logo.ico\" "
        "--exclude-module \"PySide6.QtWebEngine\" "
        "--exclude-module \"PySide6.QtWebEngineCore\" "
        "--exclude-module \"PySide6.QtWebEngineWidgets\" "
        "--exclude-module \"PySide6.QtNetwork\" "
        "--exclude-module \"PySide6.QtQml\" "
        "--exclude-module \"PySide6.QtQuick\" "
        "--exclude-module \"PySide6.Qt3D\" "
        "--exclude-module \"PySide6.QtMultimedia\" "
        "--exclude-module \"tkinter\" "
        "--add-data \"security\\security_auth.py;security\" "
        "--add-data \"security\\crypto_manager.py;security\" "
        "--add-data \"database\\db_manager.py;database\" "
        "--add-data \"core\\config.py;core\" "
        "--add-data \"core\\logic_tools.py;core\" "
        "--add-data \"ui\\themes\\theme_manager.py;ui/themes\" "
        "--add-data \"ui\\components\\widgets.py;ui/components\" "
        "--hidden-import \"views.dashboard_view\" "
        "--hidden-import \"views.courses_view\" "
        "--hidden-import \"views.notes_view\" "
        "--hidden-import \"views.quiz_view\" "
        "--hidden-import \"views.profile_view\" "
        "--hidden-import \"views.settings_view\" "
        "--hidden-import \"views.tools_view\" "
        "--hidden-import \"views.grades_view\" "
        "--hidden-import \"views.shortcuts_view\" "
        "--hidden-import \"views.about_view\" "
        "--hidden-import \"views.space_ai_view\" "
        "--hidden-import \"views.oracle_view\" "
        "--hidden-import \"views.guide_view\" "
        "--hidden-import \"views.hacking_view\" "
        "--hidden-import \"views.career_view\" "
        "--hidden-import \"views.legal_view\" "
        "--hidden-import \"views.auth_view\" "
        "--hidden-import \"core.config\" "
        "--hidden-import \"core.space_ai_bridge\" "
        "--hidden-import \"core.local_llm\" "
        "--hidden-import \"google.genai\" "
        "--hidden-import \"google.genai.types\" "
        "--hidden-import \"PySide6.QtSvg\" "
        "--hidden-import \"speech_recognition\" "
        "--hidden-import \"pyttsx3\" "
        "--hidden-import \"core.voice_assistant\" "
        "--hidden-import \"bcrypt\" "
        "--add-data \"core\\voice_assistant.py;core\" "
        "--add-data \"core\\local_llm.py;core\" "
        "--add-data \"utils\\shortcuts_data.py;utils\" "
        "--add-data \"utils\\oracle_hub.py;utils\" "
        "--add-data \"core\\space_code.py;core\" "
        "--add-data \"lessons\\cours_data.py;lessons\" "
        "--add-data \"utils\\updates_asta.py;utils\" "
        "--add-data \"assets\\offline_docs\\legal.md;assets/offline_docs\" "
        "--add-data \"assets\\offline_docs\\faq.md;assets/offline_docs\" "
        "--add-data \"assets\\hacking_payloads.zip;assets\" "
        "--add-data \"assets\\Space_logo.ico;assets\" "
        "--add-data \"assets\\Space_logo_256.png;assets\" "
        "--add-data \"assets\\space_ai_logo.svg;assets\" "
        "--add-data \"assets\\asta_academie_mark.svg;assets\" "
        "--add-data \"core\\space_ai_bridge.py;core\" "
        "--add-data \"hacking;hacking\" "
        "--add-data \"cours;cours\" "
        "--add-data \"core\\health_manager.py;core\" "
        "--add-data \"core\\auth_manager.py;core\" "
        "--add-data \"core\\memory.py;core\" "
        "--add-data \"core\\synonym_map.py;core\" "
        "--add-data \"core\\intent_parser.py;core\" "
        "--add-data \"core\\math_solver.py;core\" "
        "--add-data \"core\\knowledge_base.py;core\" "
        "--add-data \"core\\ai_engine.py;core\" "
        "--add-data \"core\\chatbot_patterns.py;core\" "
        "--add-data \"views\\auth_view.py;views\" "
        "--add-data \"utils\\cache_manager.py;utils\" "
        "--add-data \"utils\\status_manager.py;utils\" "
        "--add-data \"utils\\event_bus.py;utils\" "
    )
    
    if os.path.exists("core/core_speed.pyd"):
        cmd_academie += " --add-binary \"core\\core_speed.pyd;core\" "
    if os.path.exists("core/AstaAdminTool.exe"):
        cmd_academie += " --add-binary \"core\\AstaAdminTool.exe;core\" "
        
    cmd_academie += " \"main_qt.py\""
    
    if fast_mode:
        cmd_academie = cmd_academie.replace(" --clean ", " ")

    code_acad = run_command_red(cmd_academie)
    if code_acad != 0:
        print_red("[ERREUR] La compilation d'AstaAcademie a echoue.")
        if hasattr(sys.stdin, 'isatty') and sys.stdin.isatty():
            input("\nAppuyez sur une touche pour continuer...")
        sys.exit(1)

    print_red("")
    print_red("[5/5] Packaging du dossier Space AI (JARVIS) dans dist/...")
    code_bundle = run_command_red(".venv\\Scripts\\python.exe packaging\\bundle_space_ai.py")
    if code_bundle != 0:
        print_red("[AVERTISSEMENT] Bundle Space AI non copie — verifiez le dossier 'Space AI'.")

    try:
        import shutil
        launcher = Path("LANCER_ASTA_ACADEMIE.bat")
        if launcher.is_file():
            shutil.copy2(launcher, Path("dist") / launcher.name)
            print_red("[OK] LANCER_ASTA_ACADEMIE.bat copie dans dist/")
        readme = Path("dist") / "LISEZMOI_DISTRIBUTION.txt"
        readme.write_text(
            "ASTA ACADEMIE\n"
            "=============\n\n"
            "Lancez : LANCER_ASTA_ACADEMIE.bat  (ou AstaAcademie.exe)\n\n"
            "Space AI est DANS l'application (onglet Space AI).\n"
            "Cle Gemini : %APPDATA%\\AstaAcademie\\space_ai.env\n"
            "  GEMINI_API_KEY=votre_cle\n\n"
            "Le dossier Space AI\\ est optionnel (ancien JARVIS externe).\n",
            encoding="utf-8",
        )
        print_red(f"[OK] Guide : {readme}")
    except Exception as exc:
        print_red(f"[INFO] Fichiers dist : {exc}")

    print_red("")
    print_red("==============================================================")
    print_red("       COMPILATION TERMINEE AVEC SUCCES !")
    print_red("==============================================================")
    print_red("Distribution : copiez TOUT le dossier \"dist\" (AstaAcademie.exe + Space AI/).")
    print_red("Space AI : ajoutez GEMINI_API_KEY dans dist\\Space AI\\.env")
    print_red("JARVIS complet : lancez dist\\Space AI\\install.bat une fois, puis DEMARRER_SPACEAI.bat")
    if hasattr(sys.stdin, 'isatty') and sys.stdin.isatty():
        input("\nAppuyez sur une touche pour continuer...")

if __name__ == '__main__':
    main()
