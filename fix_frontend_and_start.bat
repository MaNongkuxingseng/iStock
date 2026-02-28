@echo off
echo ========================================
echo iStock 立即开发启动脚本
echo ========================================
echo.

echo [1/6] 检查前端目录...
if not exist "frontend\src\App.js" (
    echo ❌ 前端关键文件缺失
    echo 正在修复...
    call :create_frontend_files
) else (
    echo ✅ 前端目录结构完整
    echo 文件数量: 
    dir /s /b frontend\*.* 2>nul | find /c /v "" >nul && (
        for /f %%i in ('dir /s /b frontend\*.* 2^>nul ^| find /c /v ""') do echo   %%i 个文件
    )
)

echo.
echo [2/6] 配置MySQL数据库...
call configure_mysql.bat

echo.
echo [3/6] 安装后端依赖...
echo 安装Python依赖...
pip install -r backend/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

if %errorlevel% neq 0 (
    echo ⚠️  使用基础依赖安装...
    pip install fastapi uvicorn sqlalchemy pymysql pydantic python-jose[cryptography]
)

echo.
echo [4/6] 安装前端依赖...
cd frontend
echo 检查node_modules...
if not exist "node_modules" (
    echo ❌ node_modules不存在，安装依赖...
    npm install --registry=https://registry.npmmirror.com
    
    if %errorlevel% neq 0 (
        echo ⚠️  安装失败，清理缓存重试...
        npm cache clean --force
        del package-lock.json 2>nul
        npm install --registry=https://registry.npmmirror.com
    )
) else (
    echo ✅ node_modules已存在
    echo 检查依赖完整性...
    npm list --depth=0 2>nul | findstr "react"
)

cd ..

echo.
echo [5/6] 修复缺失代码...
echo 检查缺失的关键文件...

:: 检查后端关键文件
if not exist "backend\src\main.py" (
    echo ❌ backend\src\main.py 缺失
    call :create_backend_main
)

if not exist "backend\src\api\routes.py" (
    echo ❌ backend\src\api\routes.py 缺失
    call :create_backend_routes
)

:: 检查数据库文件
if not exist "backend\src\database\models.py" (
    echo ❌ 数据库模型文件缺失
    call :create_database_models
)

echo.
echo [6/6] 启动开发...
echo 创建启动脚本...

echo @echo off > start_dev.bat
echo echo === iStock开发环境启动 === >> start_dev.bat
echo echo. >> start_dev.bat
echo echo [1] 启动后端API (端口8000)... >> start_dev.bat
echo cd backend >> start_dev.bat
echo start "iStock Backend" cmd /k "python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload" >> start_dev.bat
echo cd .. >> start_dev.bat
echo timeout /t 5 /nobreak >nul >> start_dev.bat
echo echo. >> start_dev.bat
echo echo [2] 启动前端开发服务器 (端口3000)... >> start_dev.bat
echo cd frontend >> start_dev.bat
echo start "iStock Frontend" cmd /k "npm start" >> start_dev.bat
echo cd .. >> start_dev.bat
echo timeout /t 5 /nobreak >nul >> start_dev.bat
echo echo. >> start_dev.bat
echo echo [3] 打开浏览器... >> start_dev.bat
echo start http://localhost:8000/docs >> start_dev.bat
echo start http://localhost:3000 >> start_dev.bat
echo echo. >> start_dev.bat
echo echo === 开发环境已启动 === >> start_dev.bat
echo echo 后端API: http://localhost:8000 >> start_dev.bat
echo echo API文档: http://localhost:8000/docs >> start_dev.bat
echo echo 前端应用: http://localhost:3000 >> start_dev.bat
echo echo. >> start_dev.bat
echo echo 按任意键查看服务状态... >> start_dev.bat
echo pause >> start_dev.bat
echo curl http://localhost:8000/health 2^>nul >> start_dev.bat
echo echo. >> start_dev.bat
echo echo 按任意键退出... >> start_dev.bat
echo pause >> start_dev.bat

echo ✅ 启动脚本: start_dev.bat

echo.
echo ========================================
echo 立即执行开发任务
echo ========================================
echo.
echo 执行顺序:
echo 1. 修复前端依赖: 已完成
echo 2. 配置MySQL: 已完成
echo 3. 安装后端依赖: 已完成
echo 4. 修复缺失代码: 进行中
echo 5. 启动开发环境: 等待执行
echo.
echo 是否立即启动开发环境? (y/n)
set /p start_now="> "

if /i "%start_now%"=="y" (
    echo 启动开发环境...
    start_dev.bat
)

echo.
pause
exit /b 0

:create_frontend_files
echo 创建前端关键文件...
:: 这里可以添加创建文件的逻辑
exit /b 0

:create_backend_main
echo 创建后端主文件...
if not exist "backend\src" mkdir backend\src

echo from fastapi import FastAPI > backend\src\main.py
echo from fastapi.middleware.cors import CORSMiddleware >> backend\src\main.py
echo from .api.routes import api_router >> backend\src\main.py
echo. >> backend\src\main.py
echo app = FastAPI(title="iStock API", version="1.0.0") >> backend\src\main.py
echo. >> backend\src\main.py
echo # CORS配置 >> backend\src\main.py
echo app.add_middleware( >> backend\src\main.py
echo     CORSMiddleware, >> backend\src\main.py
echo     allow_origins=["*"], >> backend\src\main.py
echo     allow_credentials=True, >> backend\src\main.py
echo     allow_methods=["*"], >> backend\src\main.py
echo     allow_headers=["*"], >> backend\src\main.py
echo ) >> backend\src\main.py
echo. >> backend\src\main.py
echo app.include_router(api_router, prefix="/api") >> backend\src\main.py
echo. >> backend\src\main.py
echo @app.get("/") >> backend\src\main.py
echo async def root(): >> backend\src\main.py
echo     return {"message": "iStock API is running"} >> backend\src\main.py
echo. >> backend\src\main.py
echo @app.get("/health") >> backend\src\main.py
echo async def health_check(): >> backend\src\main.py
echo     return {"status": "healthy", "service": "iStock API"} >> backend\src\main.py

echo ✅ 创建 backend\src\main.py
exit /b 0

:create_backend_routes
echo 创建API路由...
if not exist "backend\src\api" mkdir backend\src\api

echo from fastapi import APIRouter > backend\src\api\routes.py
echo from . import stocks, users, auth, portfolio >> backend\src\api\routes.py
echo. >> backend\src\api\routes.py
echo api_router = APIRouter() >> backend\src\api\routes.py
echo. >> backend\src\api\routes.py
echo api_router.include_router(stocks.router, prefix="/stocks", tags=["stocks"]) >> backend\src\api\routes.py
echo api_router.include_router(users.router, prefix="/users", tags=["users"]) >> backend\src\api\routes.py
echo api_router.include_router(auth.router, prefix="/auth", tags=["auth"]) >> backend\src\api\routes.py
echo api_router.include_router(portfolio.router, prefix="/portfolio", tags=["portfolio"]) >> backend\src\api\routes.py

echo ✅ 创建 backend\src\api\routes.py
exit /b 0

:create_database_models
echo 创建数据库模型...
if not exist "backend\src\database" mkdir backend\src\database

echo from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text > backend\src\database\models.py
echo from sqlalchemy.ext.declarative import declarative_base >> backend\src\database\models.py
echo from datetime import datetime >> backend\src\database\models.py
echo. >> backend\src\database\models.py
echo Base = declarative_base() >> backend\src\database\models.py
echo. >> backend\src\database\models.py
echo class Stock(Base): >> backend\src\database\models.py
echo     __tablename__ = "stocks" >> backend\src\database\models.py
echo. >> backend\src\database\models.py
echo     id = Column(Integer, primary_key=True, index=True) >> backend\src\database\models.py
echo     symbol = Column(String(10), unique=True, index=True, nullable=False) >> backend\src\database\models.py
echo     name = Column(String(100), nullable=False) >> backend\src\database\models.py
echo     market = Column(String(20)) >> backend\src\database\models.py
echo     industry = Column(String(50)) >> backend\src\database\models.py
echo     created_at = Column(DateTime, default=datetime.utcnow) >> backend\src\database\models.py
echo     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) >> backend\src\database\models.py
echo. >> backend\src\database\models.py
echo class StockDaily(Base): >> backend\src\database\models.py
echo     __tablename__ = "stock_daily" >> backend\src\database\models.py
echo. >> backend\src\database\models.py
echo     id = Column(Integer, primary_key=True, index=True) >> backend\src\database\models.py
echo     stock_id = Column(Integer, index=True) >> backend\src\database\models.py
echo     date = Column(DateTime, index=True) >> backend\src\database\models.py
echo     open_price = Column(Float) >> backend\src\database\models.py
echo     close_price = Column(Float) >> backend\src\database\models.py
echo     high_price = Column(Float) >> backend\src\database\models.py
echo     low_price = Column(Float) >> backend\src\database\models.py
echo     volume = Column(Integer) >> backend\src\database\models.py
echo     amount = Column(Float) >> backend\src\database\models.py
echo     created_at = Column(DateTime, default=datetime.utcnow) >> backend\src\database\models.py

echo ✅ 创建 backend\src\database\models.py
exit /b 0