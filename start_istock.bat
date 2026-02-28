@echo off
chcp 65001 > nul
echo.
echo ========================================
echo 🚀 iStock 智能股票分析系统 - 启动脚本
echo ========================================
echo.

REM 检查是否以管理员身份运行
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ⚠️  建议以管理员身份运行此脚本
    echo 右键点击 -> "以管理员身份运行"
    echo.
    pause
)

REM 设置项目目录
set PROJECT_DIR=%~dp0
echo 📁 项目目录: %PROJECT_DIR%

REM 检查Docker
echo.
echo 🔍 检查Docker...
docker --version >nul 2>&1
if %errorLevel% neq 0 (
    echo ❌ Docker未安装或未在PATH中
    echo 请先安装Docker Desktop并确保已启动
    echo 下载地址: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)
echo ✅ Docker已安装

REM 检查Docker Compose
echo.
echo 🔍 检查Docker Compose...
docker-compose --version >nul 2>&1
if %errorLevel% neq 0 (
    echo ⚠️  Docker Compose未安装，尝试使用docker compose...
    docker compose version >nul 2>&1
    if %errorLevel% neq 0 (
        echo ❌ Docker Compose未安装
        echo 请安装Docker Compose或更新Docker Desktop
        pause
        exit /b 1
    )
    echo ✅ Docker Compose (插件版) 已安装
) else (
    echo ✅ Docker Compose已安装
)

REM 检查Docker守护进程
echo.
echo 🔍 检查Docker守护进程...
docker info >nul 2>&1
if %errorLevel% neq 0 (
    echo ❌ Docker守护进程未运行
    echo 请启动Docker Desktop
    pause
    exit /b 1
)
echo ✅ Docker守护进程运行正常

REM 创建.env文件（如果不存在）
echo.
echo ⚙️  检查环境配置...
if not exist "%PROJECT_DIR%.env" (
    if exist "%PROJECT_DIR%.env.example" (
        echo 📄 创建.env配置文件...
        copy "%PROJECT_DIR%.env.example" "%PROJECT_DIR%.env" >nul
        echo ✅ .env文件已创建（请根据需要修改配置）
    ) else (
        echo ⚠️  未找到.env.example文件
    )
) else (
    echo ✅ .env文件已存在
)

REM 创建必要目录
echo.
echo 📁 创建目录结构...
mkdir "%PROJECT_DIR%backend\logs" 2>nul
mkdir "%PROJECT_DIR%frontend\logs" 2>nul
mkdir "%PROJECT_DIR%data\postgres" 2>nul
mkdir "%PROJECT_DIR%data\redis" 2>nul
mkdir "%PROJECT_DIR%data\celery" 2>nul
echo ✅ 目录结构已创建

REM 显示菜单
:menu
echo.
echo ========================================
echo 📋 请选择操作:
echo ========================================
echo 1. 🐳 启动所有服务 (Docker Compose)
echo 2. 🔨 构建Docker镜像
echo 3. 🗄️  初始化数据库
echo 4. 📊 检查项目状态
echo 5. 🛑 停止所有服务
echo 6. 🧹 清理Docker资源
echo 7. 🚀 完整启动 (推荐)
echo 8. 📖 显示帮助信息
echo 9. ❌ 退出
echo ========================================
echo.

set /p choice="请输入选项 (1-9): "

if "%choice%"=="1" goto start_services
if "%choice%"=="2" goto build_images
if "%choice%"=="3" goto init_database
if "%choice%"=="4" goto check_status
if "%choice%"=="5" goto stop_services
if "%choice%"=="6" goto cleanup
if "%choice%"=="7" goto full_start
if "%choice%"=="8" goto show_help
if "%choice%"=="9" goto exit_script

echo ❌ 无效选项，请重新输入
goto menu

:start_services
echo.
echo 🚀 启动所有服务...
cd /d "%PROJECT_DIR%"
docker-compose up -d
if %errorLevel% neq 0 (
    echo ❌ 启动服务失败
    pause
    goto menu
)
echo.
echo ✅ 服务启动成功
echo ⏳ 等待服务就绪...
timeout /t 10 /nobreak >nul
echo.
echo 📊 服务状态:
docker-compose ps
echo.
echo 🌐 访问地址:
echo   后端API: http://localhost:8000
echo   API文档: http://localhost:8000/docs
echo   前端应用: http://localhost:3000
pause
goto menu

:build_images
echo.
echo 🔨 构建Docker镜像...
echo 注意: 构建可能需要几分钟时间...
cd /d "%PROJECT_DIR%"
echo 构建后端镜像...
docker-compose build backend
if %errorLevel% neq 0 (
    echo ❌ 构建后端镜像失败
    pause
    goto menu
)
echo 构建前端镜像...
docker-compose build frontend
if %errorLevel% neq 0 (
    echo ⚠️  构建前端镜像失败
) else (
    echo ✅ 前端镜像构建完成
)
echo.
echo ✅ 镜像构建完成
pause
goto menu

:init_database
echo.
echo 🗄️  初始化数据库...
cd /d "%PROJECT_DIR%"
echo 运行数据库迁移...
docker-compose exec backend alembic upgrade head
if %errorLevel% neq 0 (
    echo ❌ 数据库迁移失败
    pause
    goto menu
)
echo ✅ 数据库迁移完成
echo.
echo 🌱 播种初始数据...
docker-compose exec backend python backend/scripts/seed_data.py
if %errorLevel% neq 0 (
    echo ⚠️  播种数据失败
) else (
    echo ✅ 初始数据播种完成
)
pause
goto menu

:check_status
echo.
echo 📊 检查项目状态...
cd /d "%PROJECT_DIR%"
python scripts/check_status.py
if %errorLevel% neq 0 (
    echo ⚠️  状态检查发现问题
)
pause
goto menu

:stop_services
echo.
echo 🛑 停止所有服务...
cd /d "%PROJECT_DIR%"
docker-compose down
if %errorLevel% neq 0 (
    echo ⚠️  停止服务时出错
) else (
    echo ✅ 服务已停止
)
pause
goto menu

:cleanup
echo.
echo 🧹 清理Docker资源...
echo 这将删除未使用的镜像、容器和卷
set /p confirm="确认清理? (y/N): "
if /i "%confirm%" neq "y" (
    echo 取消清理
    goto menu
)
echo 清理未使用的Docker资源...
docker system prune -a -f
echo ✅ 清理完成
pause
goto menu

:full_start
echo.
echo 🚀 执行完整启动流程...
echo ========================================
cd /d "%PROJECT_DIR%"

echo 1. 构建Docker镜像...
docker-compose build backend
if %errorLevel% neq 0 (
    echo ❌ 构建失败
    pause
    goto menu
)

echo 2. 启动所有服务...
docker-compose up -d
if %errorLevel% neq 0 (
    echo ❌ 启动失败
    pause
    goto menu
)

echo 3. 等待服务就绪...
timeout /t 15 /nobreak >nul

echo 4. 初始化数据库...
docker-compose exec backend alembic upgrade head
if %errorLevel% neq 0 (
    echo ❌ 数据库初始化失败
    pause
    goto menu
)

echo 5. 播种初始数据...
docker-compose exec backend python backend/scripts/seed_data.py
if %errorLevel% neq 0 (
    echo ⚠️  播种数据失败
)

echo.
echo ========================================
echo 🎉 iStock项目启动完成！
echo ========================================
echo.
echo 📊 服务状态:
docker-compose ps
echo.
echo 🌐 访问地址:
echo   后端API:      http://localhost:8000
echo   API文档:      http://localhost:8000/docs
echo   前端应用:      http://localhost:3000
echo   数据库管理:    localhost:5432
echo   Redis管理:     localhost:6379
echo   Celery监控:   http://localhost:5555
echo.
echo 🔧 管理命令:
echo   查看服务状态:  docker-compose ps
echo   查看服务日志:  docker-compose logs -f
echo   停止服务:      docker-compose down
echo.
pause
goto menu

:show_help
echo.
echo 📖 iStock项目帮助信息
echo ========================================
echo.
echo 🎯 项目简介:
echo   iStock是一个智能股票分析系统，提供:
echo   • 实时股票数据监控
echo   • 技术指标分析
echo   • 机器学习预测
echo   • 投资组合管理
echo.
echo 🛠️  技术栈:
echo   • 后端: FastAPI + PostgreSQL + Redis
echo   • 前端: React + TypeScript
echo   • 任务队列: Celery + Flower
echo   • 容器化: Docker + Docker Compose
echo.
echo 📁 项目结构:
echo   backend/     - 后端代码
echo   frontend/    - 前端代码
echo   docker/      - Docker配置
echo   scripts/     - 管理脚本
echo   local/       - 本地开发配置
echo.
echo 🚀 快速开始:
echo   1. 确保已安装Docker Desktop
echo   2. 双击此脚本 (start_istock.bat)
echo   3. 选择选项7进行完整启动
echo   4. 访问 http://localhost:3000
echo.
echo 📞 支持:
echo   • GitHub: https://github.com/MaNongkuxingseng/iStock
echo   • 问题反馈: 创建GitHub Issue
echo.
pause
goto menu

:exit_script
echo.
echo 👋 感谢使用iStock项目！
echo.
pause
exit /b 0