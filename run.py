#!/usr/bin/env python3
"""
HBB Mutation Analyzer - Unified Project Launcher
=================================================
Starts both the FastAPI Backend and Next.js Frontend with a single command.
- Automatically validates virtual environment and dependencies.
- Automatically creates .env from .env.example if missing.
- Cleans up any stale processes on ports 8000 and 3000.
- Live color-coded log streaming in a single unified terminal.
- Automatically opens http://localhost:3000 in your browser when ready.
- Graceful shutdown of both servers on Ctrl+C.
"""

import argparse
import os
import platform
import shutil
import signal
import socket
import subprocess
import sys
import threading
import time
import urllib.request
import webbrowser
from pathlib import Path

# Paths
ROOT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = ROOT_DIR / "backend"
FRONTEND_DIR = ROOT_DIR / "frontend"
ENV_FILE = ROOT_DIR / ".env"
ENV_EXAMPLE = ROOT_DIR / ".env.example"

# ANSI Colors
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
MAGENTA = "\033[95m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"

# Ensure UTF-8 output on Windows consoles
try:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# Enable ANSI colors on Windows if possible
if platform.system() == "Windows":
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        # ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    except Exception:
        pass


def log(prefix: str, msg: str, color: str = RESET) -> None:
    timestamp = time.strftime("%H:%M:%S")
    print(f"{DIM}[{timestamp}]{RESET} {color}{BOLD}[{prefix}]{RESET} {msg}", flush=True)


def is_port_in_use(port: int, host: str = "127.0.0.1") -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex((host, port)) == 0


def free_port(port: int) -> None:
    """Terminates processes listening on the given port (Windows / Unix)."""
    if not is_port_in_use(port):
        return

    log("Launcher", f"Port {port} is in use. Cleaning up stale process...", YELLOW)
    try:
        if platform.system() == "Windows":
            out = subprocess.check_output(f"netstat -ano | findstr :{port}", shell=True, text=True, stderr=subprocess.DEVNULL)
            pids = set()
            for line in out.strip().splitlines():
                parts = line.split()
                if len(parts) >= 5 and f":{port}" in parts[1] and parts[3] == "LISTENING":
                    pid = parts[4]
                    if pid != "0" and pid != str(os.getpid()):
                        pids.add(pid)
            for pid in pids:
                subprocess.run(f"taskkill /F /PID {pid}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            subprocess.run(f"fuser -k {port}/tcp", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(1)
    except Exception:
        pass


def ensure_env_file() -> None:
    if not ENV_FILE.exists() and ENV_EXAMPLE.exists():
        log("Launcher", "Copying .env.example -> .env ...", CYAN)
        shutil.copy(ENV_EXAMPLE, ENV_FILE)
        log("Launcher", "Created .env configuration file.", GREEN)


def get_backend_python() -> str:
    """Finds the Python executable inside backend/venv or fallback."""
    if platform.system() == "Windows":
        venv_py = BACKEND_DIR / "venv" / "Scripts" / "python.exe"
    else:
        venv_py = BACKEND_DIR / "venv" / "bin" / "python"

    if venv_py.exists():
        return str(venv_py)

    log("Launcher", f"Virtual environment not found at {venv_py}. Using current python: {sys.executable}", YELLOW)
    return sys.executable


def get_npm_cmd() -> str:
    """Finds npm command executable."""
    if platform.system() == "Windows":
        npm_cmd = shutil.which("npm.cmd") or shutil.which("npm") or "npm.cmd"
    else:
        npm_cmd = shutil.which("npm") or "npm"
    return npm_cmd


def stream_output(process: subprocess.Popen, prefix: str, color: str) -> None:
    """Streams stdout and stderr from a subprocess line-by-line."""
    if process.stdout is None:
        return
    for line in iter(process.stdout.readline, ""):
        line = line.rstrip("\r\n")
        if line:
            print(f"{color}{BOLD}[{prefix}]{RESET} {line}", flush=True)


def wait_for_backend(url: str = "http://127.0.0.1:8000/health", timeout: float = 20.0) -> bool:
    """Polls backend health check until it responds or times out."""
    start = time.time()
    while time.time() - start < timeout:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "HBB-Launcher"})
            with urllib.request.urlopen(req, timeout=1.0) as resp:
                if resp.status == 200:
                    return True
        except Exception:
            time.sleep(0.5)
    return False


def main() -> None:
    parser = argparse.ArgumentParser(description="HBB Mutation Analyzer Project Launcher")
    parser.add_argument("--stop", action="store_true", help="Stop any running backend and frontend services (frees ports 8000 & 3000)")
    parser.add_argument("--release-audit", action="store_true", help="Execute the complete automated release readiness audit pipeline")
    parser.add_argument("--backend-only", action="store_true", help="Launch only the backend server")
    parser.add_argument("--frontend-only", action="store_true", help="Launch only the frontend server")
    parser.add_argument("--no-browser", action="store_true", help="Do not automatically open the browser")
    parser.add_argument("--separate", action="store_true", help="Launch backend and frontend in separate command windows (Windows only)")
    args = parser.parse_args()

    if args.release_audit:
        audit_tool = ROOT_DIR / "tools" / "release_audit.py"
        py_exe = get_backend_python()
        ret = subprocess.run([py_exe, str(audit_tool)], cwd=str(ROOT_DIR))
        sys.exit(ret.returncode)

    if args.stop:
        print(f"\n{BOLD}{YELLOW}Stopping any running HBB Mutation Analyzer processes...{RESET}")
        free_port(8000)
        free_port(3000)
        print(f"{GREEN}{BOLD}[+] Ports 8000 and 3000 have been freed successfully.{RESET}\n")
        return

    print(f"\n{BOLD}{CYAN}======================================================{RESET}")
    print(f"{BOLD}{CYAN}        HBB Mutation Analyzer - Project Launcher      {RESET}")
    print(f"{BOLD}{CYAN}======================================================{RESET}\n")

    # 1. Validate environment
    ensure_env_file()

    python_exe = get_backend_python()
    npm_exe = get_npm_cmd()

    # Check node_modules
    if not (FRONTEND_DIR / "node_modules").exists() and not args.backend_only:
        log("Launcher", "frontend/node_modules not found. Installing dependencies...", YELLOW)
        subprocess.run([npm_exe, "install"], cwd=str(FRONTEND_DIR), check=True)

    # 2. Cleanup stale ports
    if not args.frontend_only:
        free_port(8000)
    if not args.backend_only:
        free_port(3000)

    # Windows Separate Windows Mode
    if args.separate and platform.system() == "Windows":
        log("Launcher", "Launching services in separate windows...", CYAN)
        if not args.frontend_only:
            backend_cmd = f'title HBB Backend (8000) && cd /d "{ROOT_DIR}" && set PYTHONPATH=backend && "{python_exe}" -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload'
            subprocess.Popen(f'start "HBB Backend (Port 8000)" cmd /k "{backend_cmd}"', shell=True)
            log("Launcher", "Backend window opened.", GREEN)

        if not args.backend_only:
            frontend_cmd = f'title HBB Frontend (3000) && cd /d "{FRONTEND_DIR}" && "{npm_exe}" run dev'
            subprocess.Popen(f'start "HBB Frontend (Port 3000)" cmd /k "{frontend_cmd}"', shell=True)
            log("Launcher", "Frontend window opened.", GREEN)

        if not args.no_browser and not args.backend_only:
            time.sleep(3)
            log("Launcher", "Opening browser at http://localhost:3000 ...", CYAN)
            webbrowser.open("http://localhost:3000")

        print(f"\n{GREEN}{BOLD}[+] Both services are running in their respective windows!{RESET}")
        print(f"{DIM}You can close this launcher window now, or use stop.bat to stop the services.{RESET}\n")
        return

    # Unified Mode (Subprocesses managed directly)
    processes = []

    # Environment for backend
    backend_env = os.environ.copy()
    backend_env["PYTHONPATH"] = str(BACKEND_DIR)

    try:
        # Start Backend
        if not args.frontend_only:
            log("Launcher", f"Starting Backend (FastAPI) on {BOLD}http://127.0.0.1:8000{RESET} ...", GREEN)
            backend_proc = subprocess.Popen(
                [python_exe, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000", "--reload"],
                cwd=str(ROOT_DIR),
                env=backend_env,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
            )
            processes.append(("Backend", backend_proc))
            threading.Thread(target=stream_output, args=(backend_proc, "Backend", GREEN), daemon=True).start()

        # Start Frontend
        if not args.backend_only:
            log("Launcher", f"Starting Frontend (Next.js) on {BOLD}http://localhost:3000{RESET} ...", CYAN)
            frontend_proc = subprocess.Popen(
                [npm_exe, "run", "dev"],
                cwd=str(FRONTEND_DIR),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
            )
            processes.append(("Frontend", frontend_proc))
            threading.Thread(target=stream_output, args=(frontend_proc, "Frontend", CYAN), daemon=True).start()

        # Wait for Backend & Open Browser
        def open_browser_when_ready():
            if not args.backend_only:
                if not args.frontend_only:
                    ready = wait_for_backend()
                    if ready:
                        log("Launcher", "Backend is healthy! API Swagger docs at http://127.0.0.1:8000/docs", GREEN)
                else:
                    time.sleep(2)

                if not args.no_browser:
                    time.sleep(1.5)
                    log("Launcher", f"Opening browser at {BOLD}http://localhost:3000{RESET} ...", MAGENTA)
                    webbrowser.open("http://localhost:3000")

        threading.Thread(target=open_browser_when_ready, daemon=True).start()

        print(f"\n{BOLD}{GREEN}[+] Services started successfully!{RESET}")
        print(f"  * Frontend:  {BOLD}http://localhost:3000{RESET}")
        print(f"  * Backend:   {BOLD}http://127.0.0.1:8000{RESET}")
        print(f"  * API Docs:  {BOLD}http://127.0.0.1:8000/docs{RESET}")
        print(f"\n{YELLOW}Press Ctrl+C at any time to shut down all services.{RESET}\n")

        # Keep parent alive while child processes run
        while all(p.poll() is None for _, p in processes):
            time.sleep(0.5)

    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}{BOLD}Shutting down HBB Mutation Analyzer services...{RESET}")
    finally:
        for name, proc in processes:
            if proc.poll() is None:
                log("Launcher", f"Stopping {name} (PID {proc.pid})...", YELLOW)
                try:
                    if platform.system() == "Windows":
                        subprocess.run(f"taskkill /F /T /PID {proc.pid}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    else:
                        proc.terminate()
                except Exception:
                    pass
        time.sleep(0.5)
        print(f"{GREEN}{BOLD}[+] All services stopped cleanly. Goodbye!{RESET}\n")


if __name__ == "__main__":
    main()
