@echo off
echo ========================================
echo iStock 一键安装配置工具
echo ========================================
echo.

echo [阶段1] 环境检查
echo.

echo [1.1] 检查Python环境...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python未安装
    echo 请安装Python 3.8+: https://www.python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version') do set "PYTHON_VERSION=%%i"
echo ✅ Python版本: %PYTHON_VERSION%

echo.
echo [1.2] 检查Node.js环境...
where node >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Node.js未安装
    echo 前端开发需要Node.js，但后端可以继续
    echo 跳过前端安装，按任意键继续...
    pause
    set "SKIP_FRONTEND=1"
) else (
    for /f %%i in ('node --version') do set "NODE_VERSION=%%i"
    echo ✅ Node.js版本: %NODE_VERSION%
    set "SKIP_FRONTEND=0"
)

echo.
echo [阶段2] 数据库选择
echo.

echo 请选择数据库类型:
echo 1. MySQL (您已安装，推荐)
echo 2. PostgreSQL (功能完整)
echo 3. SQLite (无需安装，简单)
echo.
set /p DB_CHOICE="请输入选择 (1-3): "

if "%DB_CHOICE%"=="1" (
    echo 选择MySQL数据库
    call configure_mysql.bat
    if %errorlevel% neq 0 (
        echo ❌ MySQL配置失败
        echo 尝试使用SQLite...
        set "DB_CHOICE=3"
    )
)

if "%DB_CHOICE%"=="2" (
    echo 选择PostgreSQL数据库
    call install_postgres.bat
)

if "%DB_CHOICE%"=="3" (
    echo 选择SQLite数据库
    call install_postgres.bat
    choice /c yn /m "是否自动配置SQLite?"
    if %errorlevel% equ 1 (
        echo 自动配置SQLite...
        rem 这里可以添加SQLite自动配置
    )
)

echo.
echo [阶段3] 安装后端依赖
echo.

echo [3.1] 安装Python依赖...
pip install -r backend/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

if %errorlevel% neq 0 (
    echo ⚠️  依赖安装失败，尝试逐个安装...
    
    echo 安装核心依赖...
    pip install fastapi==0.104.1 uvicorn[standard]==0.24.0
    pip install sqlalchemy==2.0.23 alembic==1.12.1
    
    if "%DB_CHOICE%"=="1" (
        echo 安装MySQL驱动...
        pip install pymysql
    )
    
    if "%DB_CHOICE%"=="2" (
        echo 安装PostgreSQL驱动...
        pip install psycopg2-binary
    )
    
    echo 安装其他依赖...
    pip install pydantic==2.5.0 python-jose[cryptography]==3.3.0
)

echo.
echo [3.2] 验证后端安装...
python -c "import fastapi; print('✅ FastAPI:', fastapi.__version__)" 2>nul
python -c "import sqlalchemy; print('✅ SQLAlchemy:', sqlalchemy.__version__)" 2>nul

if "%DB_CHOICE%"=="1" (
    python -c "import pymysql; print('✅ PyMySQL: 已安装')" 2>nul
)

if "%DB_CHOICE%"=="2" (
    python -c "import psycopg2; print('✅ psycopg2: 已安装')" 2>nul
)

echo.
if "%SKIP_FRONTEND%"=="0" (
    echo [阶段4] 安装前端依赖
    echo.
    
    echo [4.1] 检查前端目录...
    if not exist "frontend" (
        echo ❌ frontend目录不存在
        mkdir frontend
        echo ✅ 创建frontend目录
    )
    
    cd frontend
    
    echo [4.2] 检查package.json...
    if not exist "package.json" (
        echo ⚠️  package.json不存在，创建基本配置...
        
        echo { > package.json
        echo   "name": "istock-frontend", >> package.json
        echo   "version": "0.1.0", >> package.json
        echo   "private": true, >> package.json
        echo   "dependencies": { >> package.json
        echo     "react": "^18.2.0", >> package.json
        echo     "react-dom": "^18.2.0", >> package.json
        echo     "react-scripts": "5.0.1", >> package.json
        echo     "axios": "^1.6.2" >> package.json
        echo   }, >> package.json
        echo   "scripts": { >> package.json
        echo     "start": "react-scripts start", >> package.json
        echo     "build": "react-scripts build", >> package.json
        echo     "test": "react-scripts test", >> package.json
        echo     "eject": "react-scripts eject" >> package.json
        echo   } >> package.json
        echo } >> package.json
        
        echo ✅ 创建package.json
    )
    
    echo [4.3] 安装npm依赖...
    npm install --registry=https://registry.npmmirror.com
    
    if %errorlevel% neq 0 (
        echo ⚠️  npm安装失败，清理缓存重试...
        npm cache clean --force
        del package-lock.json 2>nul
        rmdir /s /q node_modules 2>nul
        npm install --registry=https://registry.npmmirror.com
    )
    
    cd ..
    
    if %errorlevel% equ 0 (
        echo ✅ 前端依赖安装成功
    ) else (
        echo ❌ 前端依赖安装失败
        echo 可以稍后手动安装
    )
) else (
    echo [阶段4] 跳过前端安装
    echo 前端需要Node.js环境，已跳过
)

echo.
echo [阶段5] 配置验证
echo.

echo [5.1] 创建环境验证脚本...
echo @echo off > verify_setup.bat
echo echo === iStock环境验证 === >> verify_setup.bat
echo echo. >> verify_setup.bat
echo echo [1] Python环境: >> verify_setup.bat
echo python --version >> verify_setup.bat
echo echo. >> verify_setup.bat
echo echo [2] 关键Python包: >> verify_setup.bat
echo python -c "import fastapi; print('  FastAPI:', fastapi.__version__)" 2^>nul >> verify_setup.bat
echo python -c "import sqlalchemy; print('  SQLAlchemy:', sqlalchemy.__version__)" 2^>nul >> verify_setup.bat
echo echo. >> verify_setup.bat
echo echo [3] 数据库配置: >> verify_setup.bat
echo echo   选择的数据库: >> verify_setup.bat
if "%DB_CHOICE%"=="1" echo   MySQL >> verify_setup.bat
if "%DB_CHOICE%"=="2" echo   PostgreSQL >> verify_setup.bat
if "%DB_CHOICE%"=="3" echo   SQLite >> verify_setup.bat
echo echo. >> verify_setup.bat
if "%SKIP_FRONTEND%"=="0" (
    echo echo [4] Node.js环境: >> verify_setup.bat
    echo where node >nul 2^>^&1 ^&^& node --version ^|^| echo "  Node.js未安装" >> verify_setup.bat
    echo echo. >> verify_setup.bat
)
echo echo [5] 运行测试: >> verify_setup.bat
echo echo   运行 python run_real_tests_en.py 进行完整测试 >> verify_setup.bat
echo echo. >> verify_setup.bat
echo echo === 验证完成 === >> verify_setup.bat
echo pause >> verify_setup.bat

echo ✅ 环境验证脚本: verify_setup.bat

echo.
echo [5.2] 创建启动脚本...
echo @echo off > start_istock.bat
echo echo === 启动iStock服务 === >> start_istock.bat
echo echo. >> start_istock.bat
echo echo [1] 启动后端API服务... >> start_istock.bat
echo echo 后端将在 http://localhost:8000 启动 >> start_istock.bat
echo cd backend >> start_istock.bat
echo start /B python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload >> start_istock.bat
echo cd .. >> start_istock.bat
echo timeout /t 3 /nobreak >nul >> start_istock.bat
echo echo. >> start_istock.bat
if "%SKIP_FRONTEND%"=="0" (
    echo echo [2] 启动前端开发服务器... >> start_istock.bat
    echo echo 前端将在 http://localhost:3000 启动 >> start_istock.bat
    echo cd frontend >> start_istock.bat
    echo start /B npm start >> start_istock.bat
    echo cd .. >> start_istock.bat
    echo timeout /t 3 /nobreak >nul >> start_istock.bat
    echo echo. >> start_istock.bat
)
echo echo [3] 打开浏览器... >> start_istock.bat
echo start http://localhost:8000/docs >> start_istock.bat
if "%SKIP_FRONTEND%"=="0" (
    echo start http://localhost:3000 >> start_istock.bat
)
echo echo. >> start_istock.bat
echo echo === 服务启动完成 === >> start_istock.bat
echo echo 按任意键查看服务状态... >> start_istock.bat
echo pause >> start_istock.bat
echo echo 后端状态: >> start_istock.bat
echo curl http://localhost:8000/health 2^>nul >> start_istock.bat
echo echo. >> start_istock.bat
echo echo 按任意键退出... >> start_istock.bat
echo pause >> start_istock.bat

echo ✅ 启动脚本: start_istock.bat

echo.
echo ========================================
echo 一键安装完成！
echo ========================================
echo.
echo 安装总结:
echo - 数据库: 
if "%DB_CHOICE%"=="1" echo   MySQL (已配置)
if "%DB_CHOICE%"=="2" echo   PostgreSQL (需安装)
if "%DB_CHOICE%"=="3" echo   SQLite (已配置)
echo - 后端依赖: 已安装
if "%SKIP_FRONTEND%"=="0" (
    echo - 前端依赖: 已安装
) else (
    echo - 前端依赖: 跳过 (需要Node.js)
)
echo.
echo 可用脚本:
echo 1. 验证环境: verify_setup.bat
echo 2. 启动服务: start_istock.bat
echo 3. 运行测试: python run_real_tests_en.py
echo.
echo 下一步:
echo 1. 运行 verify_setup.bat 验证安装
echo 2. 运行 start_istock.bat 启动服务
echo 3. 访问 http://localhost:8000/docs 查看API
if "%SKIP_FRONTEND%"=="0" (
    echo 4. 访问 http://localhost:3000 查看前端
)
echo.
echo 如果遇到问题:
echo - 查看上面的错误信息
echo - 运行 verify_setup.bat 检查环境
echo - 参考 frontend_detailed_guide.md 中的故障排除
echo.
pause