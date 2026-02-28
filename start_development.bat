@echo off
echo ========================================
echo iStock 开发环境启动脚本
echo ========================================
echo.

echo [1] 安装Python依赖...
pip install fastapi uvicorn sqlalchemy pymysql python-jose[cryptography] passlib[bcrypt]

echo.
echo [2] 初始化MySQL数据库...
cd backend
python scripts/init_database.py
cd ..

echo.
echo [3] 启动后端API服务...
cd backend
start "iStock Backend" cmd /k "python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload"
cd ..

echo 等待后端启动...
timeout /t 5 /nobreak >nul

echo.
echo [4] 启动前端开发服务器...
cd frontend
start "iStock Frontend" cmd /k "npm start"
cd ..

echo 等待前端启动...
timeout /t 5 /nobreak >nul

echo.
echo [5] 打开开发工具...
start http://localhost:8000/docs
start http://localhost:3000

echo.
echo ========================================
echo 开发环境已启动！
echo ========================================
echo.
echo 服务地址:
echo - 后端API: http://localhost:8000
echo - API文档: http://localhost:8000/docs
echo - 前端应用: http://localhost:3000
echo.
echo API端点示例:
echo - 股票列表: http://localhost:8000/api/stocks
echo - 市场概览: http://localhost:8000/api/stocks/market/overview
echo - 健康检查: http://localhost:8000/health
echo.
echo 按任意键查看服务状态...
pause >nul

echo.
echo 测试后端服务...
curl http://localhost:8000/health 2>nul
echo.
echo 测试股票API...
curl http://localhost:8000/api/stocks 2>nul
echo.

echo 按任意键退出...
pause >nul