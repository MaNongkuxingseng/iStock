@echo off
cd /d "G:\openclaw\workspace\projects\active\myStock\instock\web"
python web_service.py
timeout /t 5 /nobreak > nul
netstat -ano | findstr :9988
if errorlevel 1 (
    echo Web service failed to start
    exit /b 1
) else (
    echo Web service started successfully on port 9988
    echo Testing connection...
    curl -s http://127.0.0.1:9988/health
)