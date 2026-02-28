@echo off
cd /d "G:\openclaw\workspace\projects\active\myStock\instock\web"
start python app.py --port 9988 --debug
timeout /t 3 /nobreak > nul
netstat -ano | findstr :9988
if errorlevel 1 (
    echo Web service failed to start
) else (
    echo Web service started successfully on port 9988
)