@echo off
TITLE Asta Academie — Build C#
COLOR 0B
cd /d "%~dp0"

echo.
echo  ==============================================
echo    ASTA ACADEMIE — Build + Deploy
echo  ==============================================
echo.

set PROJECT=csharp\AstaAcademieApp\AstaAcademieApp.csproj
set BUILD_OUT=csharp\AstaAcademieApp\bin\Debug\net9.0-windows
set DEPLOY_DIR=dist\AstaWPF

:: ── Vérifier dotnet ──────────────────────────────────────────────────────────
where dotnet >nul 2>&1
if %errorlevel% neq 0 (
    echo  [!] dotnet non trouve. Installez .NET 9 SDK.
    pause
    exit /b 1
)

:: ── Fermer l'app si elle tourne ──────────────────────────────────────────────
tasklist /FI "IMAGENAME eq AstaAcademieApp.exe" 2>nul | find /I "AstaAcademieApp" >nul
if %errorlevel%==0 (
    echo  [~] Fermeture de AstaAcademieApp...
    taskkill /F /IM AstaAcademieApp.exe >nul 2>&1
    timeout /t 2 /nobreak >nul
)

:: ── Compilation ──────────────────────────────────────────────────────────────
echo  [1/3] Compilation du projet C#...
dotnet build "%PROJECT%" -c Debug --nologo -v quiet
if %errorlevel% neq 0 (
    echo.
    echo  [!] ECHEC de la compilation. Verifie les erreurs ci-dessus.
    pause
    exit /b 1
)
echo  [OK] Build reussie.

:: ── Déploiement vers dist\AstaWPF\ ──────────────────────────────────────────
echo  [2/3] Déploiement vers %DEPLOY_DIR%\...
if not exist "%DEPLOY_DIR%" mkdir "%DEPLOY_DIR%"
xcopy /E /Y /Q "%BUILD_OUT%\*" "%DEPLOY_DIR%\" >nul
echo  [OK] Binaires copiés.

:: ── Copie du contenu (cours/, data/) ─────────────────────────────────────────
echo  [3/3] Copie des ressources...

if exist "cours" (
    if exist "%DEPLOY_DIR%\cours" rd /S /Q "%DEPLOY_DIR%\cours"
    xcopy /E /Y /Q "cours\*" "%DEPLOY_DIR%\cours\" >nul
    echo  [OK] cours/ synchronise.
)

if exist "data" (
    if exist "%DEPLOY_DIR%\data" rd /S /Q "%DEPLOY_DIR%\data"
    xcopy /E /Y /Q "data\*" "%DEPLOY_DIR%\data\" >nul
    echo  [OK] data/ synchronise.
)

:: ── Résumé ───────────────────────────────────────────────────────────────────
echo.
echo  ==============================================
echo    BUILD COMPLETE
echo  ==============================================
for %%A in ("%DEPLOY_DIR%\AstaAcademieApp.exe") do (
    echo    Exe  : %%~zA bytes
)
echo    Dir  : %DEPLOY_DIR%\
echo.
echo  Pour lancer : double-cliquer LANCER_ASTA_ACADEMIE.bat
echo.

:: ── Lancer automatiquement ───────────────────────────────────────────────────
set /p LAUNCH="  Lancer l'application maintenant ? (O/N) : "
if /i "%LAUNCH%"=="O" (
    start "" "%DEPLOY_DIR%\AstaAcademieApp.exe"
)

exit /b 0
