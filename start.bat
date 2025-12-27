@echo off
REM Start script for Projects and Blogs API
REM For Windows

echo ==========================================
echo   Projects and Blogs API - Startup
echo ==========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Error: Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies if requirements.txt exists
if exist "requirements.txt" (
    echo Installing/updating dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Error: Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Check if .env file exists
if not exist ".env" (
    if exist ".env.example" (
        echo Warning: .env file not found. Copying from .env.example...
        copy .env.example .env
        echo Please edit .env file with your configuration before running again.
        pause
        exit /b 1
    ) else (
        echo Warning: No .env file found. Using default settings.
    )
)

echo.
echo ==========================================
echo   Starting API server...
echo ==========================================
echo API will be available at: http://localhost:8000
echo API documentation at: http://localhost:8000/docs
echo Press Ctrl+C to stop the server
echo.

REM Start the server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
