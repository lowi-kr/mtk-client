@echo off
title MTK Client — Setup & Launch
color 0A

echo.
echo  ███╗   ███╗████████╗██╗  ██╗     ██████╗██╗     ██╗███████╗███╗   ██╗████████╗
echo  ████╗ ████║╚══██╔══╝██║ ██╔╝    ██╔════╝██║     ██║██╔════╝████╗  ██║╚══██╔══╝
echo  ██╔████╔██║   ██║   █████╔╝     ██║     ██║     ██║█████╗  ██╔██╗ ██║   ██║
echo  ██║╚██╔╝██║   ██║   ██╔═██╗     ██║     ██║     ██║██╔══╝  ██║╚██╗██║   ██║
echo  ██║ ╚═╝ ██║   ██║   ██║  ██╗    ╚██████╗███████╗██║███████╗██║ ╚████║   ██║
echo  ╚═╝     ╚═╝   ╚═╝   ╚═╝  ╚═╝     ╚═════╝╚══════╝╚═╝╚══════╝╚═╝  ╚═══╝   ╚═╝
echo.
echo  MediaTek Flash Tool — Windows Launcher
echo  ─────────────────────────────────────────────────────────────────
echo.

:: Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo  [ERROR] Python not found. Install Python 3.10+ from https://python.org
    pause
    exit /b 1
)

for /f "tokens=2 delims= " %%v in ('python --version') do set PYVER=%%v
echo  [OK] Python %PYVER% found.

:: Install deps
echo  [..] Installing / verifying dependencies...
pip install PyQt6 pyserial --quiet --disable-pip-version-check
if %errorlevel% neq 0 (
    echo  [ERROR] Failed to install dependencies.
    pause
    exit /b 1
)
echo  [OK] PyQt6 + pyserial ready.

echo.
echo  [>>] Launching MTK Client...
echo.

python mtk_client.py

if %errorlevel% neq 0 (
    echo.
    echo  [ERROR] MTK Client crashed. Check error above.
    pause
)
