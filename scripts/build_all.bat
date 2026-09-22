@echo off
setlocal enabledelayedexpansion

echo Building frontend...
cd /d "%~dp0frontend"
npm ci || exit /b 1
npm run build || exit /b 1

echo Building native C++...
cd /d "%~dp0native"
if exist build rmdir /s /q build
mkdir build
cd build
cmake .. || exit /b 1
cmake --build . --config Release || exit /b 1

echo Building .NET solution...
cd /d "%~dp0"
msbuild /m /p:Configuration=Release || exit /b 1

echo Build complete.
endlocal
