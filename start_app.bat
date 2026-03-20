@echo off
echo.
echo ============================================
echo Starting BumpRadar App...
echo ============================================
echo.

echo Starting Backend Server...
cd backend
start "BumpRadar Backend" cmd /k "python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --timeout-keep-alive 30"

timeout /t 3 /nobreak >nul

echo Starting Frontend Server...
cd ..\frontend
start "BumpRadar Frontend" cmd /k "python simple_server.py"

timeout /t 2 /nobreak >nul

echo.
echo ============================================
echo BumpRadar is now running!
echo ============================================
echo.
echo On your phone, open:
echo    http://192.168.2.10:3000
echo.
echo On this computer:
echo    http://localhost:3000
echo.
echo Make sure your phone is on the same WiFi network!
echo.
echo Close both command windows to stop the servers
echo ============================================
echo.
