@echo off
chcp 65001 >nul
echo ========================================
echo iStock 开发环境启动脚本
echo ========================================
echo.

REM 检查Docker是否运行
docker version >nul 2>&1
if errorlevel 1 (
    echo [错误] Docker未运行或未安装
    echo 请启动Docker Desktop并重试
    pause
    exit /b 1
)

echo [信息] 检查Docker Compose配置...
if not exist "docker-compose.yml" (
    echo [错误] docker-compose.yml文件不存在
    pause
    exit /b 1
)

echo [信息] 启动开发环境...
docker-compose up -d

if errorlevel 1 (
    echo [错误] 启动Docker服务失败
    pause
    exit /b 1
)

echo.
echo [成功] 服务已启动！
echo.
echo 访问以下地址：
echo - 后端API: http://localhost:8000
echo - API文档: http://localhost:8000/docs
echo - 前端应用: http://localhost:3000
echo - Flower监控: http://localhost:5555
echo - 数据库: localhost:5432 (用户: mystock_user)
echo - Redis: localhost:6379
echo.
echo 常用命令：
echo - 查看日志: docker-compose logs -f
echo - 停止服务: docker-compose down
echo - 重启服务: docker-compose restart
echo.
echo 按任意键打开API文档...
pause >nul
start http://localhost:8000/docs
exit /b 0