@echo off
echo ========================================
echo iStock 立即启动脚本
echo ========================================
echo.

echo 步骤1: 使用修复版docker-compose文件
copy docker-compose-fixed.yml docker-compose.yml
echo.

echo 步骤2: 使用完整路径启动Docker
set DOCKER_PATH=C:\Program Files\Docker\Docker\resources\bin
if exist "%DOCKER_PATH%\docker.exe" (
    echo 找到Docker在: %DOCKER_PATH%
) else (
    set DOCKER_PATH=%LOCALAPPDATA%\Docker\resources\bin
    if exist "%DOCKER_PATH%\docker.exe" (
        echo 找到Docker在: %DOCKER_PATH%
    ) else (
        echo 错误: 找不到Docker可执行文件
        pause
        exit /b 1
    )
)

echo.
echo 步骤3: 启动核心服务
echo 使用国内镜像源，避免网络问题...
"%DOCKER_PATH%\docker.exe" compose up -d postgres redis backend
if errorlevel 1 (
    echo.
    echo 启动失败，尝试最小化版本...
    echo.
    start_minimal.bat
) else (
    echo.
    echo ========================================
    echo 服务启动成功！
    echo ========================================
    echo.
    echo 请等待1-2分钟让服务完全启动
    echo.
    echo 测试链接:
    echo 1. 健康检查: http://localhost:8000/health
    echo 2. API文档: http://localhost:8000/docs
    echo 3. 前端页面: http://localhost:3000
    echo.
    echo 查看服务状态:
    "%DOCKER_PATH%\docker.exe" compose ps
    echo.
    pause
)