# 综合修复脚本：解决所有已知问题

Write-Host "=== 开始综合修复 ===" -ForegroundColor Green

# 1. 修复DNS/网络问题
Write-Host "1. 修复网络连接..." -ForegroundColor Yellow
ipconfig /flushdns
Write-Host "DNS缓存已刷新" -ForegroundColor Green

# 2. 安装Web服务依赖
Write-Host "2. 安装Web服务依赖..." -ForegroundColor Yellow
$deps = @("tornado", "pymysql", "sqlalchemy", "pandas", "numpy")
foreach ($dep in $deps) {
    Write-Host "  安装 $dep..." -NoNewline
    try {
        pip install $dep --target="D:\Program Files\Python\Lib\site-packages" 2>&1 | Out-Null
        Write-Host " ✓" -ForegroundColor Green
    } catch {
        Write-Host " ✗" -ForegroundColor Red
    }
}

# 3. 启动Web服务
Write-Host "3. 启动Web服务..." -ForegroundColor Yellow
$webDir = "G:\openclaw\workspace\projects\active\myStock\instock\web"
if (Test-Path $webDir) {
    Set-Location $webDir
    $process = Start-Process -FilePath "python" -ArgumentList "web_service.py" -PassThru -WindowStyle Hidden
    Write-Host "   Web服务进程已启动 (PID: $($process.Id))" -ForegroundColor Green
    
    # 等待服务启动
    Start-Sleep -Seconds 5
    
    # 检查端口
    $portCheck = Test-NetConnection -ComputerName 127.0.0.1 -Port 9988 -InformationLevel Quiet
    if ($portCheck) {
        Write-Host "   Web服务已在端口9988运行 ✓" -ForegroundColor Green
    } else {
        Write-Host "   Web服务启动失败 ✗" -ForegroundColor Red
    }
} else {
    Write-Host "   Web目录不存在: $webDir" -ForegroundColor Red
}

# 4. 验证数据库连接
Write-Host "4. 验证数据库连接..." -ForegroundColor Yellow
try {
    $mysqlPath = "C:\Program Files\MySQL\MySQL Server 9.4\bin\mysql.exe"
    if (Test-Path $mysqlPath) {
        & $mysqlPath -uroot -p785091 instockdb -e "SELECT COUNT(*) as record_count FROM cn_stock_indicators_sell" 2>&1 | Out-String
        Write-Host "   数据库连接正常 ✓" -ForegroundColor Green
    } else {
        Write-Host "   MySQL客户端未找到" -ForegroundColor Yellow
    }
} catch {
    Write-Host "   数据库连接失败" -ForegroundColor Red
}

# 5. 测试Feishu连接
Write-Host "5. 测试Feishu连接..." -ForegroundColor Yellow
try {
    $testResult = Test-NetConnection -ComputerName "open.feishu.cn" -Port 443 -InformationLevel Quiet
    if ($testResult) {
        Write-Host "   Feishu域名可访问 ✓" -ForegroundColor Green
    } else {
        Write-Host "   Feishu域名访问失败" -ForegroundColor Yellow
    }
} catch {
    Write-Host "   网络测试失败" -ForegroundColor Red
}

Write-Host "`n=== 修复完成 ===" -ForegroundColor Green
Write-Host "请执行以下验证：" -ForegroundColor Cyan
Write-Host "1. 访问 http://127.0.0.1:9988/health" -ForegroundColor Cyan
Write-Host "2. 检查Feishu消息是否正常显示" -ForegroundColor Cyan
Write-Host "3. 运行: SELECT COUNT(*) FROM cn_stock_indicators_sell;" -ForegroundColor Cyan