@echo off
echo ============================================
echo   Crop Disease Knowledge Assistant
echo   Starting Frontend Server...
echo ============================================
echo.

cd /d "%~dp0frontend"

if not exist "node_modules" (
    echo [INFO] Installing Node dependencies...
    npm install --legacy-peer-deps
)

echo [INFO] Starting React dev server on http://localhost:5173
echo [INFO] Press Ctrl+C to stop.
echo.

npm run dev
pause

