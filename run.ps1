<#
.SYNOPSIS
    HBB Mutation Analyzer PowerShell Launcher
.DESCRIPTION
    Runs the HBB Mutation Analyzer unified launcher script (run.py).
    Starts FastAPI backend and Next.js frontend with live streaming logs.
#>
param(
    [switch]$Stop,
    [switch]$BackendOnly,
    [switch]$FrontendOnly,
    [switch]$Separate,
    [switch]$ReleaseAudit,
    [switch]$Doctor
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

$pythonExe = Join-Path $scriptDir "backend\venv\Scripts\python.exe"
if (-not (Test-Path $pythonExe)) {
    $pythonExe = "python"
}

$pyArgs = @("run.py")
if ($Stop) { $pyArgs += "--stop" }
if ($BackendOnly) { $pyArgs += "--backend-only" }
if ($FrontendOnly) { $pyArgs += "--frontend-only" }
if ($NoBrowser) { $pyArgs += "--no-browser" }
if ($Separate) { $pyArgs += "--separate" }
if ($ReleaseAudit) { $pyArgs += "--release-audit" }
if ($Doctor) { $pyArgs += "--doctor" }

& $pythonExe $pyArgs
