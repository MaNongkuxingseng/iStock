@echo off
chcp 65001 >nul
echo.
echo ========================================
echo 🚀 iStock 智能股票分析系统 - 一键启动
echo ========================================
echo.

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python未安装或不在PATH中
    echo 请先安装Python 3.8+
    pause
    exit /b 1
)

REM 检查Docker
docker --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Docker未安装或不在PATH中
    echo 将使用本地模式启动...
    set USE_DOCKER=0
) else (
    echo ✅ Docker已安装
    set USE_DOCKER=1
)

echo.
echo 📊 检查项目状态...
python scripts/check_project.py --check all

echo.
echo 🔧 启动iStock项目...

if "%USE_DOCKER%"=="1" (
    echo 🐳 使用Docker模式启动...
    python scripts/start_project.py --mode docker
) else (
    echo 💻 使用本地模式启动...
    python scripts/start_project.py --mode local
)

if errorlevel 1 (
    echo.
    echo ❌ 启动失败
    echo.
    echo 🔧 故障排除:
    echo   1. 检查Docker Desktop是否运行
    echo   2. 检查端口是否被占用
    echo   3. 查看详细日志: docker-compose logs
    echo   4. 手动启动: docker-compose up
    pause
    exit /b 1
)

echo.
echo ========================================
echo 🎉 iStock项目启动成功！
echo ========================================
echo.
echo 🔗 访问地址:
echo   🌐 后端API:      http://localhost:8000
echo   📖 API文档:      http://localhost:8000/docs
echo   🎨 前端应用:     http://localhost:3000
echo   📊 Celery监控:   http://localhost:5555
echo.
echo ⚙️  常用命令:
echo   📊 查看状态:     docker-compose ps
echo   📝 查看日志:     docker-compose logs -f
echo   ⏸️  停止服务:     docker-compose down
echo   🔄 重启服务:     docker-compose restart
echo.
echo 💡 提示: 服务可能需要几分钟完全启动
echo       请耐心等待并刷新浏览器
echo.
pause