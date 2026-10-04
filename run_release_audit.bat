@echo off
setlocal
cd /d "%~dp0"
echo ======================================================================
echo    HBB MUTATION ANALYZER - AUTOMATED RELEASE READINESS AUDIT
echo ======================================================================
if exist backend\venv\Scripts\python.exe (
    backend\venv\Scripts\python.exe tools\release_audit.py %*
) else (
    python tools\release_audit.py %*
)
exit /b %ERRORLEVEL%
