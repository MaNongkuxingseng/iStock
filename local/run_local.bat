@echo off
echo 🚀 启动iStock本地化运行模式...
echo ================================

:: 检查Python
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python未安装，请先安装Python 3.10+
    pause
    exit /b 1
)

:: 创建虚拟环境
echo 🔧 创建虚拟环境...
python -m venv venv_local
call venv_local\Scripts\activate.bat

:: 安装依赖
echo 📦 安装依赖...
pip install --upgrade pip
pip install -r local/requirements.txt

:: 启动应用
echo 🌐 启动iStock服务...
start "" http://localhost:8000/docs
python local/app.py

pause