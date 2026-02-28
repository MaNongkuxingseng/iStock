@echo off
echo ========================================
echo iStock Basic Test Script
echo ========================================
echo.

echo Test 1: Check project structure
if not exist "docker-compose.yml" (
    echo FAIL: docker-compose.yml not found
    goto :error
)
echo PASS: docker-compose.yml exists

if not exist "backend\src\api\main.py" (
    echo WARN: Backend API main.py not found
) else (
    echo PASS: Backend API main.py exists
)

if not exist "frontend\package.json" (
    echo WARN: Frontend package.json not found
) else (
    echo PASS: Frontend package.json exists
)

echo.
echo Test 2: Check Docker Desktop
tasklist | findstr /i "docker" >nul
if errorlevel 1 (
    echo FAIL: Docker Desktop not running
    goto :error
)
echo PASS: Docker Desktop is running

echo.
echo Test 3: Find Docker executable
set DOCKER_PATH=
if exist "C:\Program Files\Docker\Docker\resources\bin\docker.exe" (
    set "DOCKER_PATH=C:\Program Files\Docker\Docker\resources\bin"
)
if exist "%LOCALAPPDATA%\Docker\resources\bin\docker.exe" (
    set "DOCKER_PATH=%LOCALAPPDATA%\Docker\resources\bin"
)

if "%DOCKER_PATH%"=="" (
    echo FAIL: Docker executable not found
    goto :error
)
echo PASS: Docker found at: %DOCKER_PATH%

echo.
echo Test 4: Test Docker command
"%DOCKER_PATH%\docker.exe" --version >nul 2>nul
if errorlevel 1 (
    echo FAIL: Docker command failed
    goto :error
)
echo PASS: Docker command works

echo.
echo Test 5: Check Docker Compose
"%DOCKER_PATH%\docker.exe" compose version >nul 2>nul
if errorlevel 1 (
    echo WARN: docker compose not available, trying docker-compose...
    if exist "%DOCKER_PATH%\docker-compose.exe" (
        echo PASS: docker-compose.exe found
    ) else (
        echo WARN: Neither docker compose nor docker-compose found
    )
) else (
    echo PASS: docker compose available
)

echo.
echo ========================================
echo BASIC TESTS COMPLETED
echo ========================================
echo.
echo Summary:
echo - Project structure: OK
echo - Docker Desktop: Running
echo - Docker command: Working
echo.
echo Next steps:
echo 1. Run simple_fix.bat to setup services
echo 2. Or run: "%DOCKER_PATH%\docker.exe" compose up -d postgres redis backend
echo 3. Wait 1-2 minutes, then test:
echo    - http://localhost:8000/health
echo    - http://localhost:8000/docs
echo.
goto :end

:error
echo.
echo ========================================
echo TEST FAILED
echo ========================================
echo.
echo Issues found. Please fix before continuing.
echo.
echo Solutions:
echo 1. Start Docker Desktop if not running
echo 2. Check Docker installation
echo 3. Run simple_fix.bat for automatic fixes
echo.
pause
exit /b 1

:end
echo Press any key to continue...
pause >nul