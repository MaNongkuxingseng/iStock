@echo off
echo ========================================
echo iStock 依赖安装脚本
echo ========================================
echo.

echo [1/8] 检查Python环境...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python未安装或不在PATH中
    echo 请安装Python 3.8+: https://www.python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version') do set "PYTHON_VERSION=%%i"
echo ✅ Python版本: %PYTHON_VERSION%

echo.
echo [2/8] 检查pip...
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  pip未安装，正在安装...
    python -m ensurepip --upgrade
)

echo.
echo [3/8] 安装后端依赖...
echo 安装 requirements.txt 中的依赖...
pip install -r backend/requirements.txt

if %errorlevel% neq 0 (
    echo ⚠️  使用国内镜像重试...
    pip install -r backend/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
)

if %errorlevel% neq 0 (
    echo ❌ 后端依赖安装失败
    echo 尝试逐个安装主要依赖...
    
    echo 安装FastAPI...
    pip install fastapi==0.104.1 uvicorn[standard]==0.24.0
    
    echo 安装数据库驱动...
    pip install sqlalchemy==2.0.23 alembic==1.12.1
    
    echo 安装其他依赖...
    pip install pydantic==2.5.0 python-jose[cryptography]==3.3.0 passlib[bcrypt]==1.7.4
)

echo.
echo [4/8] 检查Node.js环境...
where node >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js未安装或不在PATH中
    echo 请安装Node.js 14+: https://nodejs.org/
    echo 或跳过前端安装 (按任意键继续)
    pause
    goto :SKIP_FRONTEND
)

for /f %%i in ('node --version') do set "NODE_VERSION=%%i"
echo ✅ Node.js版本: %NODE_VERSION%

where npm >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ npm未安装
    goto :SKIP_FRONTEND
)

for /f %%i in ('npm --version') do set "NPM_VERSION=%%i"
echo ✅ npm版本: %NPM_VERSION%

echo.
echo [5/8] 安装前端依赖...
if not exist "frontend\package.json" (
    echo ❌ frontend\package.json 不存在
    echo 正在创建基本的package.json...
    
    echo { > frontend\package.json
    echo   "name": "istock-frontend", >> frontend\package.json
    echo   "version": "0.1.0", >> frontend\package.json
    echo   "private": true, >> frontend\package.json
    echo   "dependencies": { >> frontend\package.json
    echo     "react": "^18.2.0", >> frontend\package.json
    echo     "react-dom": "^18.2.0", >> frontend\package.json
    echo     "react-scripts": "5.0.1" >> frontend\package.json
    echo   }, >> frontend\package.json
    echo   "scripts": { >> frontend\package.json
    echo     "start": "react-scripts start", >> frontend\package.json
    echo     "build": "react-scripts build", >> frontend\package.json
    echo     "test": "react-scripts test", >> frontend\package.json
    echo     "eject": "react-scripts eject" >> frontend\package.json
    echo   } >> frontend\package.json
    echo } >> frontend\package.json
    
    echo ✅ 创建了基本的package.json
)

cd frontend
echo 安装npm依赖...
npm install

if %errorlevel% neq 0 (
    echo ⚠️  使用淘宝镜像重试...
    npm install --registry=https://registry.npmmirror.com
)

if %errorlevel% neq 0 (
    echo ❌ npm安装失败，清理缓存重试...
    npm cache clean --force
    del package-lock.json 2>nul
    rmdir /s /q node_modules 2>nul
    npm install --registry=https://registry.npmmirror.com
)

cd ..
:SKIP_FRONTEND

echo.
echo [6/8] 检查数据库配置...
call check_postgres.bat

echo.
echo [7/8] 验证安装...
echo 验证Python包...
python -c "import fastapi; print('✅ FastAPI:', fastapi.__version__)" 2>nul
python -c "import sqlalchemy; print('✅ SQLAlchemy:', sqlalchemy.__version__)" 2>nul

echo 验证Node.js包...
if exist "frontend\node_modules" (
    cd frontend
    npm list --depth=0 2>nul | findstr "react"
    cd ..
)

echo.
echo [8/8] 创建环境验证脚本...
echo @echo off > verify_environment.bat
echo echo 验证iStock环境... >> verify_environment.bat
echo echo. >> verify_environment.bat
echo echo [1] Python环境: >> verify_environment.bat
echo python --version >> verify_environment.bat
echo echo. >> verify_environment.bat
echo echo [2] 关键Python包: >> verify_environment.bat
echo python -c "import fastapi; print('  FastAPI:', fastapi.__version__)" 2^>nul >> verify_environment.bat
echo python -c "import sqlalchemy; print('  SQLAlchemy:', sqlalchemy.__version__)" 2^>nul >> verify_environment.bat
echo echo. >> verify_environment.bat
echo echo [3] Node.js环境: >> verify_environment.bat
echo where node >nul 2^>^&1 ^&^& node --version ^|^| echo "  Node.js未安装" >> verify_environment.bat
echo echo. >> verify_environment.bat
echo echo [4] 数据库状态: >> verify_environment.bat
echo call check_postgres.bat >> verify_environment.bat
echo echo. >> verify_environment.bat
echo echo [5] 运行测试: >> verify_environment.bat
echo echo 运行 python run_real_tests_en.py 进行完整测试 >> verify_environment.bat
echo pause >> verify_environment.bat

echo ✅ 环境验证脚本: verify_environment.bat

echo.
echo ========================================
echo 依赖安装完成！
echo ========================================
echo.
echo 下一步:
echo 1. 运行环境验证: verify_environment.bat
echo 2. 运行真实测试: python run_real_tests_en.py
echo 3. 启动服务测试
echo.
echo 如果遇到问题:
echo - 查看上面的错误信息
echo - 运行 verify_environment.bat 检查环境
echo - 参考 CLEAR_INSTRUCTIONS.md 中的故障排除
echo.
pause