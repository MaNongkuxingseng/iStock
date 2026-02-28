@echo off
echo Starting iStock...
echo.

REM Check if in correct directory
if not exist "docker-compose.yml" (
    echo Error: Run this from iStock project directory
    pause
    exit /b 1
)

REM Find Docker
set DOCKER_PATH=C:\Program Files\Docker\Docker\resources\bin
if not exist "%DOCKER_PATH%\docker.exe" (
    set DOCKER_PATH=%LOCALAPPDATA%\Docker\resources\bin
)

if not exist "%DOCKER_PATH%\docker.exe" (
    echo Error: Docker not found
    pause
    exit /b 1
)

echo Using Docker from: %DOCKER_PATH%
echo.

REM Use fixed compose file if exists
if exist "docker-compose-fixed.yml" (
    copy docker-compose-fixed.yml docker-compose.yml >nul
    echo Using Chinese mirror version
)

REM Stop existing services
echo Stopping old services...
"%DOCKER_PATH%\docker.exe" compose down 2>nul

REM Start services
echo Starting services...
echo This may take a few minutes...
echo.

"%DOCKER_PATH%\docker.exe" compose up -d postgres redis backend

if errorlevel 1 (
    echo.
    echo Failed to start with Docker Compose
    echo Trying minimal version...
    echo.
    
    REM Build and run minimal version
    "%DOCKER_PATH%\docker.exe" build -f Dockerfile.backend -t istock-backend .
    
    "%DOCKER_PATH%\docker.exe" run -d --name istock-backend ^
      -p 8000:8000 ^
      -v "%CD%\backend:/app/backend" ^
      -v "%CD%\local:/app/local" ^
      -e DATABASE_URL=sqlite:///./istock.db ^
      istock-backend ^
      sh -c "python -m uvicorn backend.src.api.main:app --host 0.0.0.0 --port 8000 --reload"
    
    echo Minimal backend started
) else (
    echo Services started successfully
)

echo.
echo Waiting 30 seconds for startup...
timeout /t 30 /nobreak >nul

echo.
echo ========================================
echo iStock should now be running
echo ========================================
echo.
echo Test these URLs:
echo 1. http://localhost:8000/health
echo 2. http://localhost:8000/docs
echo 3. http://localhost:3000
echo.
echo If not working:
echo 1. Check Docker Desktop is running
echo 2. Wait 2-3 minutes
echo 3. Run: docker-compose logs
echo.
pause