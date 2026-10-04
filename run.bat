@echo off
setlocal enabledelayedexpansion
title HBB Mutation Analyzer Launcher
cd /d "%~dp0"

echo ========================================================
echo       HBB Mutation Analyzer - Starting Services
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
        echo Please ensure Python or backend\venv is set up.
        pause
        exit /b 1
    )
)

:: Run the unified launcher script
"%PYTHON_CMD%" run.py %*

if %ERRORLEVEL% neq 0 (
    echo.
    echo [Launcher stopped with exit code %ERRORLEVEL%]
    pause
)
