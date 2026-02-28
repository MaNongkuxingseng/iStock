# iStock开发启动脚本 - 修复版

Write-Host "=== iStock开发立即开始 ===" -ForegroundColor Green
Write-Host ""

# 1. 安装缺失的依赖
Write-Host "[1/4] 安装缺失依赖..." -ForegroundColor Yellow

# 安装uvicorn
Write-Host "安装uvicorn..." -ForegroundColor Cyan
python -m pip install uvicorn[standard] fastapi

# 安装其他依赖
if (Test-Path "backend/requirements.txt") {
    Write-Host "安装requirements.txt中的依赖..." -ForegroundColor Cyan
    python -m pip install -r backend/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
}

# 2. 启动后端服务
Write-Host ""
Write-Host "[2/4] 启动后端API服务..." -ForegroundColor Yellow

# 检查后端主文件
if (-not (Test-Path "backend/src/main.py")) {
    Write-Host "创建后端主文件..." -ForegroundColor Cyan
    
    if (-not (Test-Path "backend/src")) {
        New-Item -ItemType Directory -Path "backend/src" -Force
    }
    
    @"
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="iStock API", version="1.0.0")

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "iStock API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "iStock API"}

@app.get("/api/stocks")
async def get_stocks():
    return [
        {"symbol": "000001", "name": "平安银行", "price": 15.42, "change": 0.32},
        {"symbol": "000002", "name": "万科A", "price": 12.85, "change": -0.15},
        {"symbol": "000858", "name": "五粮液", "price": 168.50, "change": 2.30}
    ]
"@ | Out-File -FilePath "backend/src/main.py" -Encoding UTF8
    
    Write-Host "✅ 创建 backend/src/main.py" -ForegroundColor Green
}

# 启动后端
Write-Host "启动后端服务 (端口8000)..." -ForegroundColor Cyan
$backendJob = Start-Job -ScriptBlock {
    Set-Location "G:\openclaw\workspace\_system\agent-home\myStock-AI\backend"
    python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
}

Start-Sleep -Seconds 3

# 3. 启动前端服务
Write-Host ""
Write-Host "[3/4] 启动前端开发服务器..." -ForegroundColor Yellow

# 检查前端依赖
if (Test-Path "frontend") {
    Set-Location "frontend"
    
    # 检查node_modules
    if (-not (Test-Path "node_modules")) {
        Write-Host "安装前端依赖..." -ForegroundColor Cyan
        
        # 使用npm.cmd而不是npm
        & npm.cmd install --registry=https://registry.npmmirror.com
        
        if ($LASTEXITCODE -ne 0) {
            Write-Host "清理缓存重试..." -ForegroundColor Yellow
            & npm.cmd cache clean --force
            Remove-Item "package-lock.json" -ErrorAction SilentlyContinue
            Remove-Item "node_modules" -Recurse -Force -ErrorAction SilentlyContinue
            & npm.cmd install --registry=https://registry.npmmirror.com
        }
    }
    
    # 启动前端
    Write-Host "启动前端服务 (端口3000)..." -ForegroundColor Cyan
    $frontendJob = Start-Job -ScriptBlock {
        Set-Location "G:\openclaw\workspace\_system\agent-home\myStock-AI\frontend"
        & npm.cmd start
    }
    
    Set-Location ".."
} else {
    Write-Host "❌ frontend目录不存在" -ForegroundColor Red
}

Start-Sleep -Seconds 3

# 4. 打开浏览器
Write-Host ""
Write-Host "[4/4] 打开开发工具..." -ForegroundColor Yellow

Write-Host "打开浏览器..." -ForegroundColor Cyan
Start-Process "http://localhost:8000/docs"
Start-Process "http://localhost:3000"

Write-Host ""
Write-Host "=" * 70 -ForegroundColor Green
Write-Host "开发环境已启动！" -ForegroundColor Green
Write-Host "=" * 70 -ForegroundColor Green
Write-Host ""
Write-Host "服务地址:" -ForegroundColor Yellow
Write-Host "• 后端API: http://localhost:8000" -ForegroundColor Cyan
Write-Host "• API文档: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "• 前端应用: http://localhost:3000" -ForegroundColor Cyan
Write-Host "• 股票API: http://localhost:8000/api/stocks" -ForegroundColor Cyan
Write-Host ""
Write-Host "立即开始开发任务:" -ForegroundColor Yellow
Write-Host "1. 验证服务运行" -ForegroundColor White
Write-Host "2. 实现数据库连接" -ForegroundColor White
Write-Host "3. 开发股票数据功能" -ForegroundColor White
Write-Host "4. 完善前端界面" -ForegroundColor White
Write-Host ""
Write-Host "按任意键继续开发..." -ForegroundColor Green
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")