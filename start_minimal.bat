@echo off
echo ========================================
echo iStock Minimal Startup Script
echo ========================================
echo.

echo This script starts iStock with minimal dependencies
echo (No PostgreSQL/Redis required for basic testing)
echo.

echo Step 1: Check Docker
docker --version >nul 2>nul
if errorlevel 1 (
    echo ERROR: Docker command not found
    pause
    exit /b 1
)
echo OK: Docker is available

echo.
echo Step 2: Build backend image
echo Building backend Docker image...
docker build -f Dockerfile.backend -t istock-backend .
if errorlevel 1 (
    echo ERROR: Failed to build backend image
    echo Trying alternative approach...
    goto :start_without_build
)

:start_without_build
echo.
echo Step 3: Start minimal services
echo Starting backend and frontend services...
docker-compose -f docker-compose-minimal.yml up -d
if errorlevel 1 (
    echo ERROR: Failed to start services
    echo Trying to start backend only...
    
    docker run -d --name istock-backend `
      -p 8000:8000 `
      -v "%CD%\backend:/app/backend" `
      -v "%CD%\local:/app/local" `
      -e DATABASE_URL=sqlite:///./istock.db `
      -e DEBUG=true `
      istock-backend `
      sh -c "python -m uvicorn backend.src.api.main:app --host 0.0.0.0 --port 8000 --reload"
    
    if errorlevel 1 (
        echo ERROR: Could not start backend container
        pause
        exit /b 1
    )
    echo OK: Backend container started
)

echo.
echo Step 4: Wait for startup
echo Waiting 30 seconds for services to start...
timeout /t 30 /nobreak >nul

echo.
echo Step 5: Check service status
docker ps --filter "name=istock"
echo.

echo ========================================
echo MINIMAL STARTUP COMPLETE
echo ========================================
echo.
echo Services started:
echo - Backend API: http://localhost:8000
echo - API Docs:    http://localhost:8000/docs
echo - Health Check: http://localhost:8000/health
echo.
echo If backend is not responding:
echo 1. Check Docker Desktop is running
echo 2. Wait 1-2 minutes for full startup
echo 3. View logs: docker logs istock-backend
echo.
echo To stop services:
echo docker stop istock-backend
echo docker rm istock-backend
echo.
pause