@echo off
echo ========================================
echo PostgreSQL 安装状态检查
echo ========================================
echo.

echo [1/4] 检查PostgreSQL服务状态...
sc query postgresql-x64-16 >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ PostgreSQL服务正在运行 (版本16)
    goto :SERVICE_RUNNING
)

sc query postgresql-x64-15 >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ PostgreSQL服务正在运行 (版本15)
    goto :SERVICE_RUNNING
)

sc query postgresql-x64-14 >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ PostgreSQL服务正在运行 (版本14)
    goto :SERVICE_RUNNING
)

sc query postgresql-x64-13 >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ PostgreSQL服务正在运行 (版本13)
    goto :SERVICE_RUNNING
)

echo ❌ PostgreSQL服务未运行
goto :CHECK_INSTALLED

:SERVICE_RUNNING
echo.
echo [2/4] 检查PostgreSQL连接...
psql --version >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=3" %%i in ('psql --version') do set "PG_VERSION=%%i"
    echo ✅ PostgreSQL客户端已安装: 版本 %PG_VERSION%
) else (
    echo ⚠️  PostgreSQL客户端未安装或不在PATH中
)

echo.
echo [3/4] 测试数据库连接...
echo 尝试连接到默认数据库...
psql -h localhost -U postgres -c "SELECT version();" >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ 可以连接到PostgreSQL数据库
    goto :ALL_GOOD
) else (
    echo ❌ 无法连接到PostgreSQL数据库
    echo   可能需要密码或配置问题
)

goto :CHECK_INSTALLED

:CHECK_INSTALLED
echo.
echo [4/4] 检查是否已安装PostgreSQL...
where psql >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ PostgreSQL已安装 (psql命令可用)
    echo   但服务可能未启动
    echo.
    echo 启动PostgreSQL服务命令:
    echo   net start postgresql-x64-16
    echo 或
    echo   net start postgresql-x64-15
    echo 或
    echo   net start postgresql-x64-14
) else (
    echo ❌ PostgreSQL未安装
    echo.
    echo 需要安装PostgreSQL或使用SQLite方案
)

:ALL_GOOD
echo.
echo ========================================
echo 检查完成！
echo ========================================
echo.
echo 下一步:
echo 1. 如果PostgreSQL已运行: 可以继续iStock开发
echo 2. 如果未安装: 运行 install_postgres.bat 或使用SQLite
echo 3. 如果不确定: 联系技术支持
echo.
pause