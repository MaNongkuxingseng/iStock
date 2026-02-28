@echo off
echo ========================================
echo iStock 服务测试启动脚本
echo ========================================
echo.

echo [1/4] 检查Python环境...
python --version
if errorlevel 1 (
    echo ❌ Python未安装或不在PATH中
    pause
    exit /b 1
)

echo.
echo [2/4] 检查后端依赖...
cd backend
pip install -r requirements.txt > nul 2>&1
if errorlevel 1 (
    echo ⚠️ 依赖安装失败，尝试继续...
)

echo.
echo [3/4] 启动后端API服务...
echo 启动后端服务在端口 8000...
start /B python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
timeout /t 3 /nobreak > nul

echo.
echo [4/4] 启动前端开发服务器...
cd ..\frontend
echo 启动前端服务在端口 3000...
echo 注意：需要先安装Node.js和npm
echo 如果未安装，请手动运行：npm install && npm start

echo.
echo ========================================
echo 服务启动完成！
echo ========================================
echo.
echo 访问地址：
echo 后端API: http://localhost:8000
echo API文档: http://localhost:8000/docs
echo 健康检查: http://localhost:8000/health
echo.
echo 前端应用: http://localhost:3000 (需要手动启动)
echo.
echo 按任意键退出...
pause > nul