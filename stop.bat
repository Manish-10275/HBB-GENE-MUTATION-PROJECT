@echo off
setlocal enabledelayedexpansion
title Stop HBB Mutation Analyzer Services
cd /d "%~dp0"

echo ========================================================
echo       Stopping HBB Mutation Analyzer Services
echo ========================================================
echo.

:: Detect Python executable (prefer backend virtual environment)
if exist "backend\venv\Scripts\python.exe" (
    set "PYTHON_CMD=backend\venv\Scripts\python.exe"
) else (
    where python >nul 2>nul
    if %ERRORLEVEL% equ 0 (
        set "PYTHON_CMD=python"
    ) else (
        echo [ERROR] Python was not found!
        pause
        exit /b 1
    )
)

"%PYTHON_CMD%" run.py --stop

ping 127.0.0.1 -n 3 >nul
