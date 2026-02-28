@echo off
echo ========================================
echo iStock Simple Fix Script
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

echo Step 2: Check if Docker Desktop is running
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
set DOCKER_FOUND=0

if exist "C:\Program Files\Docker\Docker\resources\bin\docker.exe" (
    echo Found Docker at: C:\Program Files\Docker\Docker\resources\bin
    set "DOCKER_PATH=C:\Program Files\Docker\Docker\resources\bin"
    set DOCKER_FOUND=1
)

if exist "%LOCALAPPDATA%\Docker\resources\bin\docker.exe" (
    echo Found Docker at: %LOCALAPPDATA%\Docker\resources\bin
    set "DOCKER_PATH=%LOCALAPPDATA%\Docker\resources\bin"
    set DOCKER_FOUND=1
)

if %DOCKER_FOUND% equ 0 (
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

echo Step 5: Create project directories
if not exist "backend\logs" mkdir "backend\logs"
if not exist "frontend\logs" mkdir "frontend\logs"
if not exist "data\postgres" mkdir "data\postgres"
if not exist "data\redis" mkdir "data\redis"
if not exist "data\celery" mkdir "data\celery"
echo OK: Directories created
echo.

echo Step 6: Create .env file if missing
if not exist ".env" (
    if exist ".env.example" (
        echo Creating .env from example...
        copy ".env.example" ".env" >nul
        echo OK: .env created
    ) else (
        echo Creating basic .env file...
        echo # iStock Environment Variables > .env
        echo DATABASE_URL=postgresql://mystock_user:mystock_password@postgres:5432/mystock_ai >> .env
        echo REDIS_URL=redis://redis:6379/0 >> .env
        echo DEBUG=true >> .env
        echo OK: Basic .env created
    )
) else (
    echo OK: .env file exists
)
echo.

echo Step 7: Create minimal frontend if missing
if not exist "frontend\package.json" (
    echo Creating minimal frontend structure...
    
    if not exist "frontend" mkdir frontend
    
    echo Creating package.json...
    echo { > frontend\package.json
    echo   "name": "istock-frontend", >> frontend\package.json
    echo   "version": "1.0.0", >> frontend\package.json
    echo   "private": true, >> frontend\package.json
    echo   "dependencies": { >> frontend\package.json
    echo     "react": "^18.2.0", >> frontend\package.json
    echo     "react-dom": "^18.2.0" >> frontend\package.json
    echo   }, >> frontend\package.json
    echo   "scripts": { >> frontend\package.json
    echo     "start": "echo 'Frontend would start here'", >> frontend\package.json
    echo     "build": "echo 'Frontend would build here'" >> frontend\package.json
    echo   } >> frontend\package.json
    echo } >> frontend\package.json
    
    if not exist "frontend\public" mkdir frontend\public
    echo Creating index.html...
    echo ^<!DOCTYPE html^> > frontend\public\index.html
    echo ^<html^> >> frontend\public\index.html
    echo ^<head^> >> frontend\public\index.html
    echo   ^<title^>iStock - Coming Soon^</title^> >> frontend\public\index.html
    echo ^</head^> >> frontend\public\index.html
    echo ^<body^> >> frontend\public\index.html
    echo   ^<h1^>iStock Frontend^</h1^> >> frontend\public\index.html
    echo   ^<p^>Frontend is being set up. Backend services should be available.^</p^> >> frontend\public\index.html
    echo ^</body^> >> frontend\public\index.html
    echo ^</html^> >> frontend\public\index.html
    
    echo OK: Minimal frontend created
) else (
    echo OK: Frontend package.json exists
)
echo.

echo Step 8: Stop existing services
echo Stopping Docker Compose services...
"%DOCKER_PATH%\docker.exe" compose down 2>nul
echo OK: Services stopped (if any were running)
echo.

echo Step 9: Start core services
echo Starting PostgreSQL, Redis, and Backend...
echo This may take several minutes...
echo.

"%DOCKER_PATH%\docker.exe" compose up -d postgres redis backend
if errorlevel 1 (
    echo ERROR: Failed to start services
    echo Trying alternative: start database only...
    
    "%DOCKER_PATH%\docker.exe" compose up -d postgres redis
    if errorlevel 1 (
        echo ERROR: Failed to start database services
        pause
        exit /b 1
    )
    echo OK: Database services started
) else (
    echo OK: Core services started
)
echo.

echo Step 10: Wait for startup
echo Waiting 30 seconds for services to start...
timeout /t 30 /nobreak >nul
echo.

echo Step 11: Check service status
echo Docker Compose service status:
"%DOCKER_PATH%\docker.exe" compose ps
echo.

echo ========================================
echo FIX SCRIPT COMPLETED
echo ========================================
echo.
echo What to do next:
echo.
echo 1. Wait 1-2 minutes for full startup
echo 2. Open browser and test:
echo    - Backend API: http://localhost:8000/health
echo    - API Docs:    http://localhost:8000/docs
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