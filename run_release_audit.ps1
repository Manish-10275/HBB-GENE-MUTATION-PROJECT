# HBB Mutation Analyzer - Automated Release Readiness Audit PowerShell Launcher
$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "   HBB MUTATION ANALYZER - AUTOMATED RELEASE READINESS AUDIT" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan

$PythonExe = "$ScriptDir\backend\venv\Scripts\python.exe"
if (-not (Test-Path $PythonExe)) {
    $PythonExe = "python"
}

& $PythonExe "$ScriptDir\tools\release_audit.py" $args
exit $LASTEXITCODE
