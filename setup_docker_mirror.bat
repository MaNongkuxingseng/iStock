@echo off
echo ========================================
echo Docker Mirror Setup Script
echo ========================================
echo.

echo This script will help setup Docker mirror for China
echo.

echo Step 1: Check current Docker configuration
docker info | findstr "Registry Mirrors"
if errorlevel 1 (
    echo No registry mirrors configured
) else (
    echo Registry mirrors already configured
)

echo.
echo Step 2: Setup Docker Desktop mirror (Windows)
echo Please follow these steps manually:
echo.
echo 1. Right-click Docker Desktop icon in system tray
echo 2. Select "Settings"
echo 3. Go to "Docker Engine" tab
echo 4. Add the following to the configuration:
echo.
echo   "registry-mirrors": [
echo     "https://docker.mirrors.ustc.edu.cn",
echo     "https://hub-mirror.c.163.com",
echo     "https://mirror.baidubce.com"
echo   ]
echo.
echo 5. Click "Apply & Restart"
echo.
echo Step 3: Alternative - Use fixed docker-compose file
echo Copy docker-compose-fixed.yml to docker-compose.yml:
copy docker-compose-fixed.yml docker-compose.yml
echo.
echo Step 4: Try pulling images again
echo Trying to pull PostgreSQL image...
docker pull registry.cn-hangzhou.aliyuncs.com/google_containers/postgres:15-alpine

echo.
echo Trying to pull Redis image...
docker pull registry.cn-hangzhou.aliyuncs.com/google_containers/redis:7-alpine

echo.
echo ========================================
echo SETUP COMPLETED
echo ========================================
echo.
echo Next steps:
echo 1. If mirror setup successful, run: docker-compose up -d
echo 2. Or use the fixed version: docker-compose -f docker-compose-fixed.yml up -d
echo 3. Wait 2-3 minutes for services to start
echo 4. Test: http://localhost:8000/health
echo.
pause