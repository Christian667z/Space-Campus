@echo off
TITLE Asta Academie — Lanceur Rust Desktop
COLOR 0B
cd /d "%~dp0"

echo.
echo  ==============================================================
echo    ASTA ACADEMIE v2.0 (Architecture Rust .rs & Tauri Natif)
echo    UNASMOH - Promo 2024-2028 - Christian Alvaro
echo  ==============================================================
echo.

:: ══════════════════════════════════════════════════════════════════
:: PRIORITÉ 1 : Exécutable Rust / Tauri natif compilé (.rs)
:: ══════════════════════════════════════════════════════════════════
set RUST_RELEASE_EXE=src-tauri\target\release\asta-campus-desktop.exe
if exist "%RUST_RELEASE_EXE%" (
    echo  [+] Lancement d'Asta Academie (Binaire Rust Release)...
    start "" "%RUST_RELEASE_EXE%"
    exit /b 0
)

set RUST_DEBUG_EXE=src-tauri\target\debug\asta-campus-desktop.exe
if exist "%RUST_DEBUG_EXE%" (
    echo  [+] Lancement d'Asta Academie (Binaire Rust Debug)...
    start "" "%RUST_DEBUG_EXE%"
    exit /b 0
)

:: ══════════════════════════════════════════════════════════════════
:: PRIORITÉ 2 : Environnement de développement Cargo / Tauri
:: ══════════════════════════════════════════════════════════════════
where cargo >nul 2>&1
if %errorlevel%==0 (
    echo  [+] Cargo Rust detecte.
    echo  [1] Lancer Tauri Desktop (Rust + UI Moderne)
    echo  [2] Lancer Serveur Rust REST (asta-server)
    echo  [3] Lancer CLI Rust Administration (asta-cli)
    echo.
    set /p choix="Votre choix [1-3] (Defaut: 1): "
    if "%choix%"=="2" (
        cargo run --bin asta-server
        exit /b 0
    )
    if "%choix%"=="3" (
        cargo run --bin asta-cli -- --help
        pause
        exit /b 0
    )
    
    echo  [+] Demarrage du moteur Tauri v2 Rust...
    where npx >nul 2>&1
    if %errorlevel%==0 (
        call npx tauri dev
        exit /b 0
    ) else (
        cargo run --manifest-path src-tauri\Cargo.toml
        exit /b 0
    )
)

:: ══════════════════════════════════════════════════════════════════
:: PRIORITÉ 3 : Interface C# WPF (Secours)
:: ══════════════════════════════════════════════════════════════════
if exist "dist\AstaWPF\AstaAcademieApp.exe" (
    echo  [C#] Lancement de secours Asta WPF...
    start "" "dist\AstaWPF\AstaAcademieApp.exe"
    exit /b 0
)

echo.
echo  [!] Pour compiler et lancer l'application en Rust :
echo      1. Installez Rust : https://rustup.rs
echo      2. Executez : cargo run --bin asta-server
echo      3. Ou : npx tauri dev
echo.
pause
exit /b 1
