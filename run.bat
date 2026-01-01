@echo off
REM ===================================================
REM  Run AntiGravity - Start all services
REM ===================================================

echo.
echo ========================================
echo   Starting AntiGravity
echo ========================================
echo.

start "AntiGravity Backend" cmd /k "cd backend && venv\Scripts\activate && uvicorn app.main:app --reload --port 8000"

timeout /t 2 > nul

start "AntiGravity Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ========================================
echo   Services Started!
echo ========================================
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo API Docs: http://localhost:8000/docs
echo.
echo Press any key to exit launcher...
pause >nul
