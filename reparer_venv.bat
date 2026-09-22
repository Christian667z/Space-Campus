@echo off
TITLE Reparation Asta Academie
COLOR 0C
cd /d "%~dp0"
echo.
echo  Suppression du dossier .venv corrompu...
if exist ".venv" (
    rmdir /s /q ".venv"
    echo  [OK] .venv supprime.
) else (
    echo  [INFO] Pas de .venv existant.
)
echo.
echo  Relance de l'installateur complet...
call install_asta.bat
