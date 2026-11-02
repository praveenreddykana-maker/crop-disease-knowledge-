@echo off
echo ============================================
echo   Crop Disease Knowledge Assistant
echo   Starting Backend Server...
echo ============================================
echo.

cd /d "%~dp0backend"

if not exist "venv\Scripts\uvicorn.exe" (
    echo [ERROR] venv not found. Please run setup first:
    echo   python -m venv venv
    echo   venv\Scripts\pip install -r requirements.txt
    pause
    exit /b 1
)

if not exist ".env" (
    echo [WARNING] .env not found. Copying from .env.example...
    copy .env.example .env
    echo Please edit backend\.env and set your GEMINI_API_KEY, then re-run.
    pause
    exit /b 1
)

echo [INFO] Starting FastAPI on http://localhost:8000
echo [INFO] API Docs: http://localhost:8000/docs
echo [INFO] Press Ctrl+C to stop.
echo.

rem Run uvicorn directly from venv (no activation needed, avoids PowerShell policy errors)
.\venv\Scripts\uvicorn.exe main:app --host 0.0.0.0 --port 8000 --reload
pause
