@echo off
cd /d "%~dp0frontend"
npm ci
npm run build
if %errorlevel% neq 0 exit /b %errorlevel%
echo Frontend build OK
