# iStock项目设置验证脚本
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "iStock项目设置验证" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# 1. 检查基本文件
Write-Host "1. 检查基本文件..." -ForegroundColor Yellow
$requiredFiles = @(
    "README.md",
    "docker-compose.yml",
    "Dockerfile.backend",
    "Dockerfile.frontend",
    "requirements.txt",
    "pyproject.toml",
    ".gitignore",
    "LICENSE"
)

$allFilesExist = $true
foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "   ✅ $file" -ForegroundColor Green
    } else {
        Write-Host "   ❌ $file (缺失)" -ForegroundColor Red
        $allFilesExist = $false
    }
}

# 2. 检查目录结构
Write-Host "`n2. 检查目录结构..." -ForegroundColor Yellow
$requiredDirs = @(
    "backend",
    "frontend", 
    "local",
    "docker",
    ".github/workflows",
    "scripts"
)

foreach ($dir in $requiredDirs) {
    if (Test-Path $dir) {
        Write-Host "   ✅ $dir/" -ForegroundColor Green
    } else {
        Write-Host "   ❌ $dir/ (缺失)" -ForegroundColor Red
        $allFilesExist = $false
    }
}

# 3. 检查docker-compose配置
Write-Host "`n3. 检查Docker配置..." -ForegroundColor Yellow
if (Test-Path "docker-compose.yml") {
    $content = Get-Content "docker-compose.yml" -Raw
    $services = @("postgres", "redis", "backend", "frontend")
    $missingServices = @()
    
    foreach ($service in $services) {
        if ($content -match $service) {
            Write-Host "   ✅ $service 服务" -ForegroundColor Green
        } else {
            Write-Host "   ⚠️  $service 服务 (未找到)" -ForegroundColor Yellow
            $missingServices += $service
        }
    }
    
    if ($missingServices.Count -eq 0) {
        Write-Host "   ✅ Docker Compose配置完整" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  缺少服务: $($missingServices -join ', ')" -ForegroundColor Yellow
    }
} else {
    Write-Host "   ❌ docker-compose.yml 不存在" -ForegroundColor Red
    $allFilesExist = $false
}

# 4. 检查Git状态
Write-Host "`n4. 检查Git状态..." -ForegroundColor Yellow
try {
    $gitBranch = git rev-parse --abbrev-ref HEAD 2>$null
    $gitRemote = git remote get-url origin 2>$null
    
    if ($gitBranch) {
        Write-Host "   ✅ 当前分支: $gitBranch" -ForegroundColor Green
    }
    
    if ($gitRemote) {
        Write-Host "   ✅ 远程仓库: $gitRemote" -ForegroundColor Green
    }
} catch {
    Write-Host "   ⚠️  Git信息获取失败" -ForegroundColor Yellow
}

# 5. 总结
Write-Host "`n==========================================" -ForegroundColor Cyan
Write-Host "验证总结" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

if ($allFilesExist) {
    Write-Host "✅ 项目结构完整！" -ForegroundColor Green
    Write-Host ""
    Write-Host "下一步操作：" -ForegroundColor Yellow
    Write-Host "1. 安装Docker Desktop" -ForegroundColor White
    Write-Host "2. 运行: docker-compose up -d" -ForegroundColor White
    Write-Host "3. 访问以下地址：" -ForegroundColor White
    Write-Host "   - API文档: http://localhost:8000/docs" -ForegroundColor White
    Write-Host "   - 前端应用: http://localhost:3000" -ForegroundColor White
    Write-Host "   - 数据库: localhost:5432" -ForegroundColor White
    Write-Host "   - Redis: localhost:6379" -ForegroundColor White
    Write-Host ""
    Write-Host "或者使用本地模式：" -ForegroundColor Yellow
    Write-Host "1. 安装Python依赖: pip install -r requirements.txt" -ForegroundColor White
    Write-Host "2. 运行: python local/app.py" -ForegroundColor White
} else {
    Write-Host "⚠️  项目结构不完整，请检查缺失的文件" -ForegroundColor Red
}

Write-Host "`nGitHub仓库：" -ForegroundColor Yellow
Write-Host "https://github.com/MaNongkuxingseng/iStock" -ForegroundColor White
Write-Host "分支: develop, feature/week1-initialization" -ForegroundColor White