@echo off
TITLE Asta Academie — Launcher
COLOR 0A
cd /d "%~dp0"

echo.
echo  ==============================================
echo    ASTA ACADEMIE v2.0
echo  ==============================================
echo.

:: ══════════════════════════════════════════════
:: Backend Python (optionnel, améliore les onglets)
:: ══════════════════════════════════════════════
if exist ".venv\Scripts\python.exe" (
    start "AstaBridge" /min ".venv\Scripts\python.exe" "api_bridge.py"
    echo  [+] Backend Python démarré ^(Space AI / Oracle / Quiz^)
    timeout /t 2 /nobreak >nul
)

:: ══════════════════════════════════════════════
:: PRIORITE 1 : C# WPF — dossier dist\AstaWPF\
:: ══════════════════════════════════════════════
if exist "dist\AstaWPF\AstaAcademieApp.exe" (
    echo  [C#] Lancement Asta Academie WPF...
    start "" "dist\AstaWPF\AstaAcademieApp.exe"
    exit /b 0
)

:: ══════════════════════════════════════════════
:: PRIORITE 2 : Debug build (dev)
:: ══════════════════════════════════════════════
set CSHARP_EXE=csharp\AstaAcademieApp\bin\Debug\net9.0-windows\AstaAcademieApp.exe
if exist "%CSHARP_EXE%" (
    echo  [C#] Lancement depuis Debug build...
    start "" "%CSHARP_EXE%"
    exit /b 0
)

:: ══════════════════════════════════════════════
:: PRIORITE 3 : Build auto
:: ══════════════════════════════════════════════
where dotnet >nul 2>&1
if %errorlevel%==0 (
    echo  [C#] Build en cours...
    dotnet build "csharp\AstaAcademieApp\AstaAcademieApp.csproj" -c Debug --nologo -v quiet
    if exist "%CSHARP_EXE%" (
        start "" "%CSHARP_EXE%"
        exit /b 0
    )
)

:: ══════════════════════════════════════════════
:: FALLBACK : Legacy Python
:: ══════════════════════════════════════════════
if exist "dist\AstaAcademieLauncher.exe" (
    echo  [PY] Fallback Python...
    start "" "dist\AstaAcademieLauncher.exe"
    exit /b 0
)

if exist "dist\AstaAcademie.exe" (
    start "" "dist\AstaAcademie.exe"
    exit /b 0
)

if exist ".venv\Scripts\pythonw.exe" (
    start "" ".venv\Scripts\pythonw.exe" "main_qt.py"
    exit /b 0
)

echo.
echo  [!] Aucune application trouvee.
echo  Lancez build_csharp.bat pour compiler l'app.
echo.
pause
exit /b 1
