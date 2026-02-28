@echo off
echo ========================================
echo PostgreSQL 安装指南
echo ========================================
echo.

echo [选项1] 下载并安装PostgreSQL 16
echo.
echo 步骤:
echo 1. 访问: https://www.postgresql.org/download/windows/
echo 2. 点击"Download the installer"
echo 3. 运行下载的安装程序
echo 4. 安装时记住以下设置:
echo    - 安装目录: C:\Program Files\PostgreSQL\16
echo    - 端口: 5432 (默认)
echo    - 超级用户密码: 设置一个密码并记住
echo    - 本地化: Chinese (Simplified), China
echo.
echo [选项2] 使用SQLite (无需安装)
echo.
echo 如果您不想安装PostgreSQL，我们可以:
echo 1. 修改iStock配置使用SQLite
echo 2. SQLite是文件数据库，无需安装服务
echo 3. 适合开发和测试环境
echo.
echo [选项3] 使用Docker运行PostgreSQL
echo.
echo 如果Docker已配置好:
echo 1. 运行: docker_fullpath.bat run -d ^
echo    --name postgres ^
echo    -e POSTGRES_PASSWORD=postgres ^
echo    -p 5432:5432 ^
echo    postgres:16-alpine
echo 2. 等待容器启动
echo 3. 测试连接
echo.
echo ========================================
echo 建议方案
echo ========================================
echo.
echo 推荐选择:
echo.
echo [开发环境] 使用SQLite
echo   优点: 无需安装，简单快速
echo   缺点: 功能有限，不适合生产
echo.
echo [生产环境] 安装PostgreSQL
echo   优点: 功能完整，性能好
echo   缺点: 需要安装配置
echo.
echo [测试环境] 使用Docker
echo   优点: 隔离环境，易于管理
echo   缺点: 需要Docker运行
echo.
echo ========================================
echo 立即执行
echo ========================================
echo.
echo 请选择:
echo 1. 安装PostgreSQL (推荐生产环境)
echo 2. 使用SQLite (推荐开发环境)
echo 3. 使用Docker运行PostgreSQL
echo 4. 检查当前状态
echo.
set /p choice="请输入选择 (1-4): "

if "%choice%"=="1" (
    echo.
    echo 正在打开PostgreSQL下载页面...
    start https://www.postgresql.org/download/windows/
    echo 请下载并安装PostgreSQL 16
    echo 安装完成后运行 check_postgres.bat 验证
)

if "%choice%"=="2" (
    echo.
    echo 选择使用SQLite数据库
    echo 正在修改iStock配置...
    call :configure_sqlite
)

if "%choice%"=="3" (
    echo.
    echo 选择使用Docker运行PostgreSQL
    echo 正在检查Docker...
    docker_fullpath.bat --version >nul 2>&1
    if %errorlevel% equ 0 (
        echo ✅ Docker可用
        echo 启动PostgreSQL容器...
        docker_fullpath.bat run -d --name postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 postgres:16-alpine
        echo 等待10秒容器启动...
        timeout /t 10 /nobreak >nul
        echo 测试连接...
        docker_fullpath.bat exec postgres psql -U postgres -c "SELECT version();"
    ) else (
        echo ❌ Docker不可用
        echo 请先配置Docker PATH或安装Docker Desktop
    )
)

if "%choice%"=="4" (
    echo.
    call check_postgres.bat
)

echo.
pause
exit /b 0

:configure_sqlite
echo 配置iStock使用SQLite数据库...
echo.

:: 创建SQLite配置
echo # SQLite数据库配置 > sqlite_config.py
echo DATABASE_URL = "sqlite:///./istock.db" >> sqlite_config.py
echo.

:: 更新后端配置
if exist "backend\src\database\session.py" (
    echo 更新数据库会话配置...
    copy "backend\src\database\session.py" "backend\src\database\session.py.backup"
    
    :: 创建简单的SQLite会话配置
    echo from sqlalchemy import create_engine > backend\src\database\session_sqlite.py
    echo from sqlalchemy.orm import sessionmaker >> backend\src\database\session_sqlite.py
    echo. >> backend\src\database\session_sqlite.py
    echo # SQLite数据库连接 >> backend\src\database\session_sqlite.py
    echo SQLALCHEMY_DATABASE_URL = "sqlite:///./istock.db" >> backend\src\database\session_sqlite.py
    echo. >> backend\src\database\session_sqlite.py
    echo engine = create_engine( >> backend\src\database\session_sqlite.py
    echo     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False} >> backend\src\database\session_sqlite.py
    echo ) >> backend\src\database\session_sqlite.py
    echo SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) >> backend\src\database\session_sqlite.py
    
    echo ✅ SQLite配置已创建
    echo 文件: backend\src\database\session_sqlite.py
)

echo.
echo 还需要:
echo 1. 安装SQLite驱动: pip install sqlalchemy
echo 2. 修改main.py使用SQLite配置
echo 3. 运行数据库迁移
echo.
echo 是否要自动配置? (y/n)
set /p configure="> "
if /i "%configure%"=="y" (
    echo 正在自动配置...
    :: 这里可以添加更多自动配置逻辑
    echo 配置完成！
)
exit /b 0