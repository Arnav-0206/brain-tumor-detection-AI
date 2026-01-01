@echo off
REM ===================================================
REM  AntiGravity - Quick Setup Script for Windows
REM ===================================================

echo.
echo ========================================
echo   AntiGravity Setup Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.11+ from https://python.org
    pause
    exit /b 1
)

echo [1/5] Setting up backend...
cd backend

REM Create virtual environment
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
) else (
    echo Virtual environment already exists
)

REM Activate venv and install dependencies
echo Installing Python dependencies...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Copy .env.example to .env if not exists
if not exist .env (
    echo Creating .env file...
    copy .env.example .env
) else (
    echo .env file already exists
)

cd ..

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo WARNING: Node.js is not installed
    echo Please install Node.js from https://nodejs.org
    echo Skipping frontend setup...
    goto :skip_frontend
)

echo.
echo [2/5] Setting up frontend...
cd frontend

REM Install npm dependencies
echo Installing Node.js dependencies...
call npm install

cd ..

:skip_frontend

echo.
echo [3/5] Creating data directories...
if not exist data\raw mkdir data\raw
if not exist data\processed mkdir data\processed

echo.
echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo Next steps:
echo   1. Download dataset (see data\README.md)
echo   2. Start backend: cd backend ^&^& venv\Scripts\activate ^&^& uvicorn app.main:app --reload
echo   3. Start frontend: cd frontend ^&^& npm run dev
echo.
echo For more information, see README.md
echo.
pause
