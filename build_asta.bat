@echo off
chcp 65001 >nul
TITLE Asta Academie - Compilation Globale
COLOR 0C
cd /d "%~dp0"

echo.
echo  ======================================================
echo    ASTA ACADEMIE - Lancement de la Compilation
echo  ======================================================
echo.

set VENV_DIR=.venv
set PYTHON_EXE=%VENV_DIR%\Scripts\python.exe
set PIP_EXE=%VENV_DIR%\Scripts\pip.exe
set PYINSTALLER_EXE=%VENV_DIR%\Scripts\pyinstaller.exe

set FAST_BUILD=0
if "%~1"=="--fast" set FAST_BUILD=1
if "%~1"=="-f" set FAST_BUILD=1
if "%~1"=="fast" set FAST_BUILD=1

if not exist "%PYTHON_EXE%" (
    echo  [!] Environnement virtuel ^(.venv^) introuvable ou incomplet.
    echo  [!] Veuillez d'abord executer "install_asta.bat" ou "reparer_venv.bat".
    echo.
    pause
    exit /b 1
)

echo.
echo  ======================================================
echo    ASTA ACADEMIE - LANCEMENT DE LA COMPILATION ET DU PACKAGE
echo  ======================================================
if "%FAST_BUILD%"=="1" (
    echo    [MODE RAPIDE ACTIVE]
)
echo.

rem 1) Installer les dependances si requirements.txt existe
if "%FAST_BUILD%"=="1" (
    echo  [~] Mode rapide active : saut de l'installation des dependances pip.
) else (
    if exist "requirements.txt" (
        echo  [~] Installation des dependances ^(requirements.txt^)...
        "%PIP_EXE%" install -r requirements.txt
        if %errorlevel% neq 0 (
            echo  [!] Erreur lors de l'installation des dépendances.
            pause
            exit /b %errorlevel%
        )
    )
)

rem 2) Lancer les tests unitaires si pytest est present
if "%FAST_BUILD%"=="1" (
    echo  [~] Mode rapide active : saut des tests unitaires.
) else (
    echo  [~] Verification de la presence de pytest...
    "%PYTHON_EXE%" -m pytest --version >nul 2>&1
    if %errorlevel% EQU 0 (
        echo  [~] Lancement des tests unitaires ^(pytest trouve^)...
        "%PYTHON_EXE%" -m pytest -q
        if %errorlevel% neq 0 (
            echo  [!] Des tests ont echoue.
            set /p CONTINUE_TESTS=Continuer malgre les erreurs ? [O/N]: 
            if /I "%CONTINUE_TESTS%" NEQ "O" (
                echo Annulation.
                exit /b 2
            )
        )
    ) else (
        echo  [~] pytest non trouve. Tests unitaires ignores.
    )
)

rem 3) Pre-build script (build_red.py)
if exist "build_red.py" (
    echo  [~] Execution du script de compilation build_red.py...
    if "%FAST_BUILD%"=="1" (
        "%PYTHON_EXE%" build_red.py --fast
    ) else (
        "%PYTHON_EXE%" build_red.py
    )
    if %errorlevel% neq 0 (
        echo  [!] build_red.py a retourne une erreur.
        pause
        exit /b %errorlevel%
    )
)

rem 4) Packaging via PyInstaller ^(avec spec si present^), uniquement si build_red.py n'existe pas pour eviter une double compilation
if not exist "build_red.py" (
    if exist "%PYINSTALLER_EXE%" (
        echo  [~] PyInstaller detecte dans venv. Utilisation pour la creation de l'executable.
        if exist "AstaAcademie.spec" (
            if "%FAST_BUILD%"=="1" (
                echo  [~] Utilisation du spec AstaAcademie.spec sans --clean
                "%PYINSTALLER_EXE%" --noconfirm AstaAcademie.spec
            ) else (
                echo  [~] Utilisation du spec AstaAcademie.spec
                "%PYINSTALLER_EXE%" --noconfirm --clean AstaAcademie.spec
            )
        ) else (
            if "%FAST_BUILD%"=="1" (
                echo  [~] Aucun spec trouve, creation rapide d'un exe pour main_qt.py sans --clean
                "%PYINSTALLER_EXE%" --noconfirm --onefile main_qt.py
            ) else (
                echo  [~] Aucun spec trouve, creation d'un exe pour main_qt.py
                "%PYINSTALLER_EXE%" --noconfirm --clean --onefile main_qt.py
            )
        )
        if %errorlevel% neq 0 (
            echo  [!] PyInstaller a retourne une erreur.
            pause
            exit /b %errorlevel%
        )
    ) else (
        echo  [!] PyInstaller introuvable dans l'environnement virtuel.
        echo  Vous pouvez l'installer avec: %PIP_EXE% install pyinstaller
        set /p SKIP=Continuer sans PyInstaller ? [O/N]: 
        if /I "%SKIP%" NEQ "O" (
            exit /b 3
        )
    )
)

rem 5) Copier fichiers runtime additionnels vers dist\AstaAcademie ^(si present^)
if exist "dist\AstaAcademie" (
    echo  [~] Copie des éléments additionnels vers dist\AstaAcademie
    xcopy /Y /E "assets" "dist\AstaAcademie\assets" >nul 2>&1
    xcopy /Y /E "ui" "dist\AstaAcademie\ui" >nul 2>&1
    xcopy /Y /E "core" "dist\AstaAcademie\core" >nul 2>&1
    if exist "frontend" xcopy /Y /E "frontend" "dist\AstaAcademie\frontend" >nul 2>&1
    echo  [~] Copie des fichiers de données (db, licence, profile)
    if exist "data" xcopy /Y /E "data" "dist\AstaAcademie\data" >nul 2>&1
)

rem 6) Créer un archive ZIP de la distribution
if exist "dist\AstaAcademie" (
    echo  [~] Creation de l'archive ZIP...
    powershell -Command "if(Test-Path 'dist/AstaAcademie.zip'){Remove-Item 'dist/AstaAcademie.zip'}; Compress-Archive -Path 'dist/AstaAcademie/*' -DestinationPath 'dist/AstaAcademie.zip'"
    if %errorlevel% neq 0 (
        echo  [!] Echec de la creation de l'archive ZIP.
    ) else (
        echo  [OK] Archive dist\AstaAcademie.zip creee.
    )
)

echo.
echo  [OK] Compilation et packaging termines avec succes !
echo.
exit /b 0
