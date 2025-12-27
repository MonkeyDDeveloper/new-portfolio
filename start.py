#!/usr/bin/env python3
"""
Cross-platform startup script for Projects and Blogs API
Works on Windows, Linux, and macOS
"""

import os
import sys
import subprocess
import platform
from pathlib import Path


def print_header():
    """Print startup header"""
    print("=" * 50)
    print("  Projects and Blogs API - Startup")
    print("=" * 50)
    print()


def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        sys.exit(1)


def get_pip_executable(venv_path):
    """Get the path to pip executable in virtual environment"""
    system = platform.system()
    if system == "Windows":
        return venv_path / "Scripts" / "pip.exe"
    else:
        return venv_path / "bin" / "pip"


def check_env_file():
    """Check if .env file exists"""
    env_file = Path(".env")
    env_example = Path(".env.example")

    if not env_file.exists():
        if env_example.exists():
            print("Warning: .env file not found. Copying from .env.example...")
            import shutil
            shutil.copy(env_example, env_file)
            print("Please edit .env file with your configuration before running again.")
            sys.exit(1)
        else:
            print("Warning: No .env file found. Using default settings.")


def kill_port(port=8000):
    """Kill process using the specified port"""
    import signal

    if platform.system() == "Windows":
        subprocess.run(f"for /f \"tokens=5\" %a in ('netstat -ano ^| findstr :{port}') do taskkill /PID %a /F",
                       shell=True, capture_output=True)
    else:
        result = subprocess.run(f"lsof -ti:{port}", shell=True, capture_output=True, text=True)
        if result.stdout.strip():
            pids = result.stdout.strip().split('\n')
            for pid in pids:
                os.kill(int(pid), signal.SIGKILL)
            print(f"Killed existing process on port {port}")

def start_server():
    """Start the FastAPI server"""

    kill_port(port=8000)

    print()
    print("=" * 50)
    print("  Starting API server...")
    print("=" * 50)
    print("API will be available at: http://localhost:8000")
    print("API documentation at: http://localhost:8000/docs")
    print("Press Ctrl+C to stop the server")
    print()

    try:
        subprocess.run([
            "python", "-m", "uvicorn",
            "main:app",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload"
        ], check=True)
    except subprocess.CalledProcessError:
        print("Error: Failed to start server")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nServer stopped by entities")
        sys.exit(0)

def main():
    """Main function"""
    print_header()
    check_python_version()
    check_env_file()
    start_server()


if __name__ == "__main__":
    main()
