@echo off
echo === 开始综合修复 ===

echo 1. 刷新DNS缓存...
ipconfig /flushdns

echo 2. 安装Web服务依赖...
pip install tornado --target="D:\Program Files\Python\Lib\site-packages"
pip install pymysql --target="D:\Program Files\Python\Lib\site-packages"
pip install sqlalchemy --target="D:\Program Files\Python\Lib\site-packages"

echo 3. 启动Web服务...
cd /d "G:\openclaw\workspace\projects\active\myStock\instock\web"
start /B python web_service.py
timeout /t 5 /nobreak > nul

echo 4. 检查端口...
netstat -ano | findstr :9988 > nul
if errorlevel 1 (
    echo   Web服务启动失败
) else (
    echo   Web服务已在端口9988运行
)

echo 5. 验证数据库...
"C:\Program Files\MySQL\MySQL Server 9.4\bin\mysql.exe" -uroot -p785091 instockdb -e "SELECT COUNT(*) as record_count FROM cn_stock_indicators_sell" 2>nul
if errorlevel 1 (
    echo   数据库连接失败
) else (
    echo   数据库连接正常
)

echo.
echo === 修复完成 ===
echo 请验证：
echo 1. 访问 http://127.0.0.1:9988/health
echo 2. 检查Feishu消息
echo 3. 运行: SELECT COUNT(*) FROM cn_stock_indicators_sell;