@echo off
TITLE Asta Academie — Launcher Complet
COLOR 0A
cd /d "%~dp0"

echo.
echo  ==============================================
echo    ASTA ACADEMIE v2.0 — Lancement Complet
echo  ==============================================
echo.

:: ══════════════════════════════════════════════
:: 1. Démarrer le backend Python (api_bridge.py)
::    dans un terminal séparé minimisé
:: ══════════════════════════════════════════════
echo  [1/2] Démarrage backend Python (Space AI + Oracle + Quiz)...

set PYTHON_OK=0

if exist ".venv\Scripts\pythonw.exe" (
    start "AstaBridge" /min ".venv\Scripts\python.exe" "api_bridge.py"
    set PYTHON_OK=1
) else if exist ".venv\Scripts\python.exe" (
    start "AstaBridge" /min ".venv\Scripts\python.exe" "api_bridge.py"
    set PYTHON_OK=1
) else (
    where python >nul 2>&1
    if %errorlevel%==0 (
        start "AstaBridge" /min python "api_bridge.py"
        set PYTHON_OK=1
    )
)

if %PYTHON_OK%==1 (
    echo  [✓] Backend Python démarré ^(port 5005^)
) else (
    echo  [!] Python non trouvé — onglets Oracle/Quiz/Notes en mode hors-ligne
)

:: Attendre que le serveur soit prêt
timeout /t 2 /nobreak >nul

:: ══════════════════════════════════════════════
:: 2. Lancer l'application C# WPF
:: ══════════════════════════════════════════════
echo  [2/2] Lancement de l'application C# WPF...

if exist "dist\AstaWPF\AstaAcademieApp.exe" (
    start "" "dist\AstaWPF\AstaAcademieApp.exe"
    echo  [✓] Application lancée !
    exit /b 0
)

if exist "csharp\AstaAcademieApp\bin\Debug\net9.0-windows\AstaAcademieApp.exe" (
    start "" "csharp\AstaAcademieApp\bin\Debug\net9.0-windows\AstaAcademieApp.exe"
    echo  [✓] Application lancée depuis Debug build.
    exit /b 0
)

echo  [!] App C# non trouvée. Lance build_csharp.bat d'abord.
pause
exit /b 1
