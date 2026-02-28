@echo off
chcp 65001 >nul
echo ========================================
echo iStock Clean Startup Script
echo ========================================
echo.

echo Step 1: Check current directory
if not exist "docker-compose.yml" (
    echo ERROR: Not in iStock project directory!
    echo Current directory: %CD%
    echo Please navigate to the iStock project folder.
    pause
    exit /b 1
)
echo OK: In iStock project directory
echo.

echo Step 2: Check Docker Desktop
echo Checking Docker processes...
tasklist | findstr /i "docker" >nul
if errorlevel 1 (
    echo WARNING: Docker Desktop may not be running
    echo Please start Docker Desktop first
    echo.
    echo You can:
    echo 1. Search for "Docker Desktop" in Start Menu
    echo 2. Look for Docker whale icon in system tray
    echo 3. Wait 1-2 minutes after starting
    echo.
    set /p continue="Continue anyway? (y/N): "
    if /i not "%continue%"=="y" (
        echo Exiting...
        pause
        exit /b 1
    )
) else (
    echo OK: Docker Desktop processes detected
)
echo.

echo Step 3: Find Docker executable
set DOCKER_PATH=

if exist "C:\Program Files\Docker\Docker\resources\bin\docker.exe" (
    set "DOCKER_PATH=C:\Program Files\Docker\Docker\resources\bin"
    echo Found Docker at: %DOCKER_PATH%
)

if exist "%LOCALAPPDATA%\Docker\resources\bin\docker.exe" (
    set "DOCKER_PATH=%LOCALAPPDATA%\Docker\resources\bin"
    echo Found Docker at: %DOCKER_PATH%
)

if "%DOCKER_PATH%"=="" (
    echo ERROR: Could not find Docker executable
    echo Please ensure Docker Desktop is properly installed.
    echo.
    echo Common installation paths:
    echo   C:\Program Files\Docker\Docker\resources\bin
    echo   %LOCALAPPDATA%\Docker\resources\bin
    pause
    exit /b 1
)

echo.
echo Step 4: Test Docker command
"%DOCKER_PATH%\docker.exe" --version
if errorlevel 1 (
    echo ERROR: Docker command failed
    echo Docker Desktop may not be fully started
    pause
    exit /b 1
)
echo OK: Docker command works
echo.

echo Step 5: Use fixed docker-compose file
if exist "docker-compose-fixed.yml" (
    copy docker-compose-fixed.yml docker-compose.yml >nul
    echo Using fixed docker-compose with Chinese mirrors
) else (
    echo Using original docker-compose.yml
)
echo.

echo Step 6: Stop existing services
echo Stopping Docker Compose services...
"%DOCKER_PATH%\docker.exe" compose down 2>nul
echo OK: Services stopped (if any were running)
echo.

echo Step 7: Start core services
echo Starting PostgreSQL, Redis, and Backend...
echo This may take several minutes...
echo.

"%DOCKER_PATH%\docker.exe" compose up -d postgres redis backend
if errorlevel 1 (
    echo ERROR: Failed to start services
    echo.
    echo Trying alternative: start minimal version...
    echo.
    call :start_minimal
    goto :show_results
)

:show_results
echo.
echo Step 8: Wait for startup
echo Waiting 30 seconds for services to start...
timeout /t 30 /nobreak >nul
echo.

echo Step 9: Check service status
echo Docker Compose service status:
"%DOCKER_PATH%\docker.exe" compose ps
echo.

echo ========================================
echo STARTUP COMPLETED
echo ========================================
echo.
echo What to do next:
echo.
echo 1. Wait 1-2 minutes for full startup
echo 2. Open browser and test:
echo    - Backend API: http://localhost:8000/health
echo    - API Docs:    http://localhost:8000/docs
echo    - Frontend:    http://localhost:3000
echo.
echo 3. If services aren't running:
echo    - Check Docker Desktop is fully started
echo    - Wait 2-3 minutes
echo    - Run: "%DOCKER_PATH%\docker.exe" compose logs
echo.
echo 4. For detailed troubleshooting:
echo    - Read MANUAL_TEST_GUIDE.md
echo    - Read FIX_DOCKER_PATH.md
echo.
pause
exit /b 0

:start_minimal
echo Starting minimal version (backend only)...
echo Building backend image...
"%DOCKER_PATH%\docker.exe" build -f Dockerfile.backend -t istock-backend .
if errorlevel 1 (
    echo ERROR: Failed to build backend image
    echo Trying to run existing image...
)

echo Starting backend container...
"%DOCKER_PATH%\docker.exe" run -d --name istock-backend ^
  -p 8000:8000 ^
  -v "%CD%\backend:/app/backend" ^
  -v "%CD%\local:/app/local" ^
  -e DATABASE_URL=sqlite:///./istock.db ^
  -e DEBUG=true ^
  istock-backend ^
  sh -c "python -m uvicorn backend.src.api.main:app --host 0.0.0.0 --port 8000 --reload"

if errorlevel 1 (
    echo ERROR: Could not start backend container
    echo.
    echo Alternative: Run local Python development
    echo cd backend
    echo python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
) else (
    echo OK: Backend container started
)
exit /b 0