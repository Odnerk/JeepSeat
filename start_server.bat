@echo off
title JeepSeat Server - http://127.0.0.1:8000
cd /d "%~dp0"
echo ==============================================
echo   Starting JeepSeat Development Server
echo   Open in browser: http://127.0.0.1:8000/
echo ==============================================
py manage.py runserver 127.0.0.1:8000
if %errorlevel% neq 0 (
    echo.
    echo Trying direct python executable...
    "C:\Users\krist\AppData\Local\Python\pythoncore-3.14-64\python.exe" manage.py runserver 127.0.0.1:8000
)
pause
