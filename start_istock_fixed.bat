@echo off
REM 设置UTF-8编码
chcp 65001 > nul

echo.
echo ========================================
echo iStock Startup Script - Fixed Version
echo ========================================
echo.

REM 检查是否在正确目录
if not exist "docker-compose.yml" (
    echo ERROR: Please run this script from iStock project root directory
    echo Current directory does not contain docker-compose.yml
    pause
    exit /b 1
)

echo Project Directory: %CD%
echo.

REM 检查Docker
echo Checking Docker...
docker --version >nul 2>nul
if errorlevel 1 (
    echo ERROR: Docker not found or not in PATH
    echo Please install Docker Desktop and ensure it's running
    echo Download: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)
echo OK: Docker installed

REM 检查Docker Compose
echo Checking Docker Compose...
docker-compose --version >nul 2>nul
if errorlevel 1 (
    echo WARNING: docker-compose not found, trying docker compose...
    docker compose version >nul 2>nul
    if errorlevel 1 (
        echo ERROR: Docker Compose not installed
        echo Please install Docker Compose or update Docker Desktop
        pause
        exit /b 1
    )
    echo OK: Docker Compose (plugin) installed
    set DOCKER_COMPOSE_CMD=docker compose
) else (
    echo OK: Docker Compose installed
    set DOCKER_COMPOSE_CMD=docker-compose
)

REM 检查Docker daemon
echo Checking Docker daemon...
docker info >nul 2>nul
if errorlevel 1 (
    echo ERROR: Docker daemon not running
    echo Please start Docker Desktop
    pause
    exit /b 1
)
echo OK: Docker daemon running

REM 创建 .env file if missing
echo.
echo Checking environment configuration...
if not exist ".env" (
    if exist ".env.example" (
        echo Creating .env file from example...
        copy ".env.example" ".env" >nul
        echo OK: .env file created (please modify as needed)
    ) else (
        echo WARNING: .env.example not found
    )
) else (
    echo OK: .env file exists
)

REM 创建必要目录
echo.
echo Creating directory structure...
if not exist "backend\logs" mkdir "backend\logs"
if not exist "frontend\logs" mkdir "frontend\logs"
if not exist "data\postgres" mkdir "data\postgres"
if not exist "data\redis" mkdir "data\redis"
if not exist "data\celery" mkdir "data\celery"
echo OK: Directory structure created

:menu
echo.
echo ========================================
echo MAIN MENU
echo ========================================
echo 1. Start all services (Docker Compose)
echo 2. Build Docker images
echo 3. Initialize database
echo 4. Check project status
echo 5. Stop all services
echo 6. Clean Docker resources
echo 7. Full setup (recommended)
echo 8. Show help
echo 9. Exit
echo ========================================
echo.

set /p choice="Enter option (1-9): "

if "%choice%"=="1" goto start_services
if "%choice%"=="2" goto build_images
if "%choice%"=="3" goto init_database
if "%choice%"=="4" goto check_status
if "%choice%"=="5" goto stop_services
if "%choice%"=="6" goto cleanup
if "%choice%"=="7" goto full_start
if "%choice%"=="8" goto show_help
if "%choice%"=="9" goto exit_script

echo ERROR: Invalid option, please try again
goto menu

:start_services
echo.
echo Starting all services...
%DOCKER_COMPOSE_CMD% up -d
if errorlevel 1 (
    echo ERROR: Failed to start services
    pause
    goto menu
)
echo.
echo OK: Services started successfully
echo Waiting for services to be ready...
timeout /t 10 /nobreak >nul
echo.
echo Service status:
%DOCKER_COMPOSE_CMD% ps
echo.
echo Access URLs:
echo   Backend API: http://localhost:8000
echo   API Docs:    http://localhost:8000/docs
echo   Frontend:    http://localhost:3000
pause
goto menu

:build_images
echo.
echo Building Docker images...
echo Note: This may take several minutes...
echo Building backend image...
%DOCKER_COMPOSE_CMD% build backend
if errorlevel 1 (
    echo ERROR: Failed to build backend image
    pause
    goto menu
)
echo Building frontend image...
%DOCKER_COMPOSE_CMD% build frontend
if errorlevel 1 (
    echo WARNING: Failed to build frontend image
) else (
    echo OK: Frontend image built
)
echo.
echo OK: Image building completed
pause
goto menu

:init_database
echo.
echo Initializing database...
echo Running database migrations...
%DOCKER_COMPOSE_CMD% exec backend alembic upgrade head
if errorlevel 1 (
    echo ERROR: Database migration failed
    pause
    goto menu
)
echo OK: Database migrations completed
echo.
echo Seeding initial data...
%DOCKER_COMPOSE_CMD% exec backend python backend/scripts/seed_data.py
if errorlevel 1 (
    echo WARNING: Data seeding failed
) else (
    echo OK: Initial data seeded
)
pause
goto menu

:check_status
echo.
echo Checking project status...
python scripts/check_status.py
if errorlevel 1 (
    echo WARNING: Status check found issues
)
pause
goto menu

:stop_services
echo.
echo Stopping all services...
%DOCKER_COMPOSE_CMD% down
if errorlevel 1 (
    echo WARNING: Error stopping services
) else (
    echo OK: Services stopped
)
pause
goto menu

:cleanup
echo.
echo Cleaning Docker resources...
echo This will remove unused images, containers and volumes
set /p confirm="Confirm cleanup? (y/N): "
if /i not "%confirm%"=="y" (
    echo Cleanup cancelled
    goto menu
)
echo Cleaning unused Docker resources...
docker system prune -a -f
echo OK: Cleanup completed
pause
goto menu

:full_start
echo.
echo Starting full setup process...
echo ========================================

echo 1. Building Docker images...
%DOCKER_COMPOSE_CMD% build backend
if errorlevel 1 (
    echo ERROR: Build failed
    pause
    goto menu
)

echo 2. Starting all services...
%DOCKER_COMPOSE_CMD% up -d
if errorlevel 1 (
    echo ERROR: Start failed
    pause
    goto menu
)

echo 3. Waiting for services to be ready...
timeout /t 15 /nobreak >nul

echo 4. Initializing database...
%DOCKER_COMPOSE_CMD% exec backend alembic upgrade head
if errorlevel 1 (
    echo ERROR: Database initialization failed
    pause
    goto menu
)

echo 5. Seeding initial data...
%DOCKER_COMPOSE_CMD% exec backend python backend/scripts/seed_data.py
if errorlevel 1 (
    echo WARNING: Data seeding failed
)

echo.
echo ========================================
echo iStock Project Setup Complete!
echo ========================================
echo.
echo Service status:
%DOCKER_COMPOSE_CMD% ps
echo.
echo Access URLs:
echo   Backend API:      http://localhost:8000
echo   API Docs:         http://localhost:8000/docs
echo   Frontend App:     http://localhost:3000
echo   Database:         localhost:5432
echo   Redis:            localhost:6379
echo   Celery Monitor:   http://localhost:5555
echo.
echo Management commands:
echo   Check status:     %DOCKER_COMPOSE_CMD% ps
echo   View logs:        %DOCKER_COMPOSE_CMD% logs -f
echo   Stop services:    %DOCKER_COMPOSE_CMD% down
echo.
pause
goto menu

:show_help
echo.
echo iStock Project Help
echo ========================================
echo.
echo Project: Intelligent Stock Analysis System
echo Features:
echo   • Real-time stock data monitoring
echo   • Technical indicator analysis
echo   • Machine learning predictions
echo   • Investment portfolio management
echo.
echo Tech Stack:
echo   • Backend: FastAPI + PostgreSQL + Redis
echo   • Frontend: React + TypeScript
echo   • Task Queue: Celery + Flower
echo   • Container: Docker + Docker Compose
echo.
echo Quick Start:
echo   1. Ensure Docker Desktop is installed
echo   2. Run this script (start_istock_fixed.bat)
echo   3. Select option 7 for full setup
echo   4. Visit http://localhost:3000
echo.
echo Support:
echo   • GitHub: https://github.com/MaNongkuxingseng/iStock
echo   • Issues: Create GitHub Issue
echo.
pause
goto menu

:exit_script
echo.
echo Thank you for using iStock project!
echo.
pause
exit /b 0