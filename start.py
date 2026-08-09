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

    # Check if running in production (via environment variable)
    environment = os.getenv("ENVIRONMENT", "development")

    if not env_file.exists():
        if environment == "production":
            print("Running in production mode - using system environment variables")
            return

        if env_example.exists():
            print("Warning: .env file not found. Copying from .env.example...")
            import shutil
            shutil.copy(env_example, env_file)
            print("Please edit .env file with your configuration before running again.")
            sys.exit(1)
        else:
            print("Warning: No .env file found. Using environment variables.")


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

def init_db():
    """Initialize database schema if tables don't exist"""
    import pymysql
    from decouple import config
    import os

    current_dir = os.path.dirname(os.path.abspath(__file__))
    schema_file = os.path.join(current_dir, "database", "schema.sql")

    if not os.path.exists(schema_file):
        print("Warning: schema.sql not found, skipping DB initialization")
        return

    print("Checking database schema...")

    conn = pymysql.connect(
        host=config("HOST"),
        port=int(config("DB_PORT")),
        user=config("USERNAME"),
        password=config("PASSWORD"),
        database=config("DATABASE"),
    )

    try:
        with conn.cursor() as cursor:
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            if tables:
                print(f"Database already has {len(tables)} tables, skipping initialization")
                return

        with open(schema_file, "r", encoding="utf-8") as f:
            sql_content = f.read()

        statements = [stmt.strip() for stmt in sql_content.split(";") if stmt.strip()]

        with conn.cursor() as cursor:
            for stmt in statements:
                if stmt.startswith("--"):
                    continue
                cursor.execute(stmt)
        conn.commit()
        print(f"Database initialized with {len(statements)} SQL statements")
    except Exception as e:
        conn.rollback()
        print(f"Warning: DB initialization failed: {e}")
    finally:
        conn.close()


def start_server():
    """Start the FastAPI server"""

    # Get port from environment variable or use default
    port = int(os.getenv("PORT", "8000"))
    environment = os.getenv("ENVIRONMENT", "development")

    kill_port(port=port)

    print()
    print("=" * 50)
    print("  Starting API server...")
    print("=" * 50)
    print(f"API will be available at: http://localhost:{port}")
    print(f"API documentation at: http://localhost:{port}/docs")
    print("Press Ctrl+C to stop the server")
    print()

    try:
        # In production, disable reload for better performance
        reload_enabled = environment != "production"

        cmd = [
            "python", "-m", "uvicorn",
            "main:app",
            "--host", "0.0.0.0",
            "--port", str(port)
        ]

        # Only add --reload flag in development
        if reload_enabled:
            cmd.append("--reload")

        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError:
        print("Error: Failed to start server")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nServer stopped by user")
        sys.exit(0)

def main():
    """Main function"""
    print_header()
    check_python_version()
    check_env_file()
    init_db()
    start_server()


if __name__ == "__main__":
    main()
