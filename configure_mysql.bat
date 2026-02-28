@echo off
echo ========================================
echo MySQL 数据库配置工具
echo ========================================
echo.

echo [1/6] 检查MySQL安装状态...
where mysql >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ MySQL客户端未安装或不在PATH中
    echo 请确保MySQL已安装并添加到PATH
    goto :CHECK_SERVICE
)

for /f "tokens=3" %%i in ('mysql --version') do set "MYSQL_VERSION=%%i"
echo ✅ MySQL客户端版本: %MYSQL_VERSION%

:CHECK_SERVICE
echo.
echo [2/6] 检查MySQL服务状态...
sc query MySQL80 >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ MySQL服务正在运行 (MySQL80)
    set "MYSQL_SERVICE=MySQL80"
    goto :TEST_CONNECTION
)

sc query MySQL57 >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ MySQL服务正在运行 (MySQL57)
    set "MYSQL_SERVICE=MySQL57"
    goto :TEST_CONNECTION
)

sc query MySQL >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ MySQL服务正在运行 (MySQL)
    set "MYSQL_SERVICE=MySQL"
    goto :TEST_CONNECTION
)

echo ❌ MySQL服务未运行
echo 启动MySQL服务命令:
echo   net start MySQL80
echo 或
echo   net start MySQL57
echo 或
echo   net start MySQL
echo.
set /p start_service="是否启动MySQL服务? (y/n): "
if /i "%start_service%"=="y" (
    net start MySQL80 2>nul || net start MySQL57 2>nul || net start MySQL 2>nul
    timeout /t 5 /nobreak >nul
)

:TEST_CONNECTION
echo.
echo [3/6] 测试MySQL连接...
echo 尝试连接到MySQL...
mysql -u root -p -e "SELECT VERSION();" 2>nul
if %errorlevel% equ 0 (
    echo ✅ MySQL连接成功
    goto :CONFIGURE_DATABASE
)

echo ⚠️  需要MySQL密码
set /p mysql_password="请输入MySQL root密码: "
mysql -u root -p%mysql_password% -e "SELECT VERSION();" 2>nul
if %errorlevel% equ 0 (
    echo ✅ MySQL连接成功
    set "MYSQL_PASSWORD=%mysql_password%"
    goto :CONFIGURE_DATABASE
)

echo ❌ MySQL连接失败
echo 可能的原因:
echo 1. 密码错误
echo 2. MySQL服务未运行
echo 3. 用户权限问题
echo.
echo 跳过数据库配置，使用默认设置
goto :CREATE_CONFIG

:CONFIGURE_DATABASE
echo.
echo [4/6] 创建iStock数据库...
mysql -u root -p%MYSQL_PASSWORD% -e "CREATE DATABASE IF NOT EXISTS istock CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;" 2>nul
if %errorlevel% equ 0 (
    echo ✅ 创建数据库: istock
) else (
    echo ⚠️  创建数据库失败，尝试无密码连接
    mysql -u root -e "CREATE DATABASE IF NOT EXISTS istock CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;" 2>nul
    if %errorlevel% equ 0 (
        echo ✅ 创建数据库: istock (无密码)
    ) else (
        echo ❌ 无法创建数据库
    )
)

:CREATE_CONFIG
echo.
echo [5/6] 创建MySQL配置文件...
echo # MySQL数据库配置 > mysql_config.py
echo DATABASE_URL = "mysql+pymysql://root:%MYSQL_PASSWORD%@localhost:3306/istock?charset=utf8mb4" >> mysql_config.py
echo.

echo [6/6] 更新iStock配置...
if exist "backend\src\database\session.py" (
    echo 备份原配置...
    copy "backend\src\database\session.py" "backend\src\database\session.py.backup"
    
    echo 创建MySQL会话配置...
    echo from sqlalchemy import create_engine > backend\src\database\session_mysql.py
    echo from sqlalchemy.orm import sessionmaker >> backend\src\database\session_mysql.py
    echo. >> backend\src\database\session_mysql.py
    echo # MySQL数据库连接 >> backend\src\database\session_mysql.py
    echo SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:%MYSQL_PASSWORD%@localhost:3306/istock?charset=utf8mb4" >> backend\src\database\session_mysql.py
    echo. >> backend\src\database\session_mysql.py
    echo engine = create_engine( >> backend\src\database\session_mysql.py
    echo     SQLALCHEMY_DATABASE_URL, >> backend\src\database\session_mysql.py
    echo     pool_pre_ping=True, >> backend\src\database\session_mysql.py
    echo     pool_recycle=3600 >> backend\src\database\session_mysql.py
    echo ) >> backend\src\database\session_mysql.py
    echo SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) >> backend\src\database\session_mysql.py
    
    echo ✅ MySQL配置已创建
    echo 文件: backend\src\database\session_mysql.py
)

echo.
echo ========================================
echo MySQL配置完成！
echo ========================================
echo.
echo 还需要:
echo 1. 安装MySQL驱动: pip install pymysql
echo 2. 修改main.py使用MySQL配置
echo 3. 运行数据库迁移
echo.
echo 自动安装MySQL驱动? (y/n)
set /p install_driver="> "
if /i "%install_driver%"=="y" (
    echo 安装pymysql...
    pip install pymysql
    echo ✅ MySQL驱动安装完成
)

echo.
echo 配置总结:
echo - 数据库: MySQL
echo - 主机: localhost:3306
echo - 数据库名: istock
echo - 用户: root
echo - 配置文件: mysql_config.py
echo - 会话配置: backend\src\database\session_mysql.py
echo.
pause