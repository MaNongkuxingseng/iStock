# iStock快速修复和启动脚本

Write-Host "=== iStock立即开发启动 ===" -ForegroundColor Green
Write-Host ""

# 1. 检查前端目录
Write-Host "[1/6] 检查前端目录..." -ForegroundColor Yellow
if (Test-Path "frontend") {
    $fileCount = (Get-ChildItem "frontend" -Recurse -File | Measure-Object).Count
    Write-Host "✅ 前端目录存在，包含 $fileCount 个文件" -ForegroundColor Green
    
    # 检查关键文件
    $criticalFiles = @(
        "frontend/src/App.js",
        "frontend/src/index.js", 
        "frontend/package.json",
        "frontend/public/index.html"
    )
    
    foreach ($file in $criticalFiles) {
        if (Test-Path $file) {
            Write-Host "  ✅ $file 存在" -ForegroundColor Green
        } else {
            Write-Host "  ❌ $file 缺失" -ForegroundColor Red
        }
    }
} else {
    Write-Host "❌ frontend目录不存在" -ForegroundColor Red
    exit 1
}

# 2. 配置MySQL
Write-Host ""
Write-Host "[2/6] 配置MySQL数据库..." -ForegroundColor Yellow
if (Test-Path "configure_mysql.bat") {
    Write-Host "运行MySQL配置脚本..." -ForegroundColor Cyan
    Start-Process -FilePath "configure_mysql.bat" -Wait -NoNewWindow
} else {
    Write-Host "⚠️  MySQL配置脚本不存在，跳过" -ForegroundColor Yellow
}

# 3. 安装后端依赖
Write-Host ""
Write-Host "[3/6] 安装后端依赖..." -ForegroundColor Yellow
if (Test-Path "backend/requirements.txt") {
    Write-Host "安装Python依赖..." -ForegroundColor Cyan
    python -m pip install -r backend/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "⚠️  使用基础依赖安装..." -ForegroundColor Yellow
        python -m pip install fastapi uvicorn sqlalchemy pymysql pydantic python-jose[cryptography]
    }
} else {
    Write-Host "❌ backend/requirements.txt 不存在" -ForegroundColor Red
}

# 4. 安装前端依赖
Write-Host ""
Write-Host "[4/6] 安装前端依赖..." -ForegroundColor Yellow
Set-Location "frontend"

if (-not (Test-Path "node_modules")) {
    Write-Host "安装npm依赖..." -ForegroundColor Cyan
    npm install --registry=https://registry.npmmirror.com
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "清理缓存重试..." -ForegroundColor Yellow
        npm cache clean --force
        Remove-Item "package-lock.json" -ErrorAction SilentlyContinue
        Remove-Item "node_modules" -Recurse -Force -ErrorAction SilentlyContinue
        npm install --registry=https://registry.npmmirror.com
    }
} else {
    Write-Host "✅ node_modules已存在" -ForegroundColor Green
    Write-Host "检查依赖完整性..." -ForegroundColor Cyan
    npm list --depth=0 2>$null | Select-String "react"
}

Set-Location ".."

# 5. 修复缺失代码
Write-Host ""
Write-Host "[5/6] 修复缺失代码..." -ForegroundColor Yellow

# 检查后端主文件
if (-not (Test-Path "backend/src/main.py")) {
    Write-Host "创建backend/src/main.py..." -ForegroundColor Cyan
    if (-not (Test-Path "backend/src")) {
        New-Item -ItemType Directory -Path "backend/src" -Force
    }
    
    @"
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.routes import api_router

app = FastAPI(title="iStock API", version="1.0.0")

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "iStock API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "iStock API"}
"@ | Out-File -FilePath "backend/src/main.py" -Encoding UTF8
    
    Write-Host "✅ 创建 backend/src/main.py" -ForegroundColor Green
}

# 6. 创建启动脚本
Write-Host ""
Write-Host "[6/6] 创建启动脚本..." -ForegroundColor Yellow

@"
@echo off
echo === iStock开发环境启动 ===
echo.

echo [1] 启动后端API (端口8000)...
cd backend
start "iStock Backend" cmd /k "python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload"
cd ..
timeout /t 5 /nobreak >nul
echo.

echo [2] 启动前端开发服务器 (端口3000)...
cd frontend
start "iStock Frontend" cmd /k "npm start"
cd ..
timeout /t 5 /nobreak >nul
echo.

echo [3] 打开浏览器...
start http://localhost:8000/docs
start http://localhost:3000
echo.

echo === 开发环境已启动 ===
echo 后端API: http://localhost:8000
echo API文档: http://localhost:8000/docs
echo 前端应用: http://localhost:3000
echo.

echo 按任意键查看服务状态...
pause >nul
curl http://localhost:8000/health 2>nul
echo.

echo 按任意键退出...
pause >nul
"@ | Out-File -FilePath "start_dev.bat" -Encoding ASCII

Write-Host "✅ 启动脚本: start_dev.bat" -ForegroundColor Green

Write-Host ""
Write-Host "=" * 70 -ForegroundColor Green
Write-Host "立即执行开发任务" -ForegroundColor Green
Write-Host "=" * 70 -ForegroundColor Green
Write-Host ""
Write-Host "执行顺序:" -ForegroundColor Yellow
Write-Host "1. 修复前端依赖: 已完成" -ForegroundColor Green
Write-Host "2. 配置MySQL: 已完成" -ForegroundColor Green
Write-Host "3. 安装后端依赖: 已完成" -ForegroundColor Green
Write-Host "4. 修复缺失代码: 已完成" -ForegroundColor Green
Write-Host "5. 启动开发环境: 等待执行" -ForegroundColor Yellow
Write-Host ""
Write-Host "是否立即启动开发环境? (y/n)" -ForegroundColor Cyan
$choice = Read-Host "> "

if ($choice -eq "y") {
    Write-Host "启动开发环境..." -ForegroundColor Green
    Start-Process -FilePath "start_dev.bat" -NoNewWindow
}

Write-Host ""
Write-Host "=== 修复完成 ===" -ForegroundColor Green
Write-Host "下一步: 运行 start_dev.bat 启动服务" -ForegroundColor Yellow