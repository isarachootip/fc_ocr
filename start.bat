@echo off
chcp 65001 > nul
echo ===================================================
echo   Starting Vendor Master Registration & OCR System
echo ===================================================
echo.

cd /d "%~dp0backend"
echo [1/2] Starting Backend & Frontend Web Application on http://localhost:8000 ...
start "Vendor API & Web App" python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

echo [2/2] Opening application in your default browser...
timeout /t 3 /nobreak > nul
start http://localhost:8000

echo.
echo System is running at http://localhost:8000
echo Press any key in the backend window to close.
pause
