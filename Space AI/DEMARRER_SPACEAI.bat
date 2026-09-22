@echo off
TITLE SPACE AI BY SPACE
COLOR 0B
cd /d "%~dp0"
if exist ".\venv\Scripts\python.exe" (
    ".\venv\Scripts\python.exe" "main5.py"
) else (
    python "main5.py"
)
pause
