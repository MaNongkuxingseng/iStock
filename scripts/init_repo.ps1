# myStock-AI 项目初始化脚本 (Windows PowerShell版本)
# 用于快速设置开发环境和GitHub仓库

Write-Host "🚀 开始初始化 myStock-AI 项目..." -ForegroundColor Green
Write-Host "=" * 60

# 检查必要工具
Write-Host "🔧 检查必要工具..." -ForegroundColor Yellow

# 检查 Git
try {
    $gitVersion = git --version
    Write-Host "✅ Git 已安装: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ 需要安装 Git" -ForegroundColor Red
    Write-Host "   下载地址: https://git-scm.com/download/win" -ForegroundColor Yellow
}

# 检查 Docker
try {
    $dockerVersion = docker --version
    Write-Host "✅ Docker 已安装: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ 需要安装 Docker Desktop" -ForegroundColor Red
    Write-Host "   下载地址: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
}

# 检查 Docker Compose
try {
    $composeVersion = docker-compose --version
    Write-Host "✅ Docker Compose 已安装: $composeVersion" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Docker Compose 可能需要单独安装" -ForegroundColor Yellow
}

Write-Host "=" * 60

# 创建项目目录结构
Write-Host "📁 创建项目目录结构..." -ForegroundColor Yellow

$directories = @(
    "src\core",
    "src\ml", 
    "src\web",
    "src\utils",
    "data\raw",
    "data\processed",
    "data\models",
    "docs\api",
    "docs\architecture", 
    "docs\deployment",
    "docs\user_guide",
    "tests\unit",
    "tests\integration",
    "tests\e2e",
    "deployment\docker",
    "deployment\nginx",
    "deployment\scripts",
    ".github\workflows",
    "monitoring\prometheus",
    "monitoring\grafana"
)

foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Force -Path $dir | Out-Null
        Write-Host "  创建目录: $dir" -ForegroundColor Gray
    }
}

# 创建基础文件
Write-Host "📄 创建基础配置文件..." -ForegroundColor Yellow

# 创建 .env.example 如果不存在
if (-not (Test-Path ".env.example")) {
    @"
# 数据库配置
DATABASE_URL=postgresql://user:password@localhost:5432/mystock_ai
REDIS_URL=redis://localhost:6379/0

# API 配置
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=true

# 数据源配置
SINA_API_URL=http://hq.sinajs.cn/list=
TENCENT_API_URL=http://qt.gtimg.cn/q=
EASTMONEY_API_URL=http://push2.eastmoney.com/api

# 机器学习配置
ML_MODEL_PATH=./data/models
ML_TRAINING_DATA_PATH=./data/processed

# 前端配置
VITE_API_URL=http://localhost:8000
VITE_APP_TITLE=myStock-AI

# 监控配置
PROMETHEUS_URL=http://localhost:9090
GRAFANA_URL=http://localhost:3001
"@ | Out-File -FilePath ".env.example" -Encoding UTF8
    Write-Host "  创建文件: .env.example" -ForegroundColor Gray
}

# 创建占位文件
Write-Host "📝 创建占位文件..." -ForegroundColor Yellow

$placeholderFiles = @(
    "data\raw\.gitkeep",
    "data\processed\.gitkeep", 
    "data\models\.gitkeep",
    "src\core\__init__.py",
    "src\ml\__init__.py",
    "src\web\__init__.py",
    "src\utils\__init__.py"
)

foreach ($file in $placeholderFiles) {
    if (-not (Test-Path $file)) {
        New-Item -ItemType File -Force -Path $file | Out-Null
        Write-Host "  创建文件: $file" -ForegroundColor Gray
    }
}

# 创建 Docker 基础文件
Write-Host "🐳 创建 Docker 配置文件..." -ForegroundColor Yellow

# 后端 Dockerfile
if (-not (Test-Path "backend\Dockerfile")) {
    @"
FROM python:3.10-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 创建非 root 用户
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# 运行应用
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
"@ | Out-File -FilePath "backend\Dockerfile" -Encoding UTF8
    Write-Host "  创建文件: backend\Dockerfile" -ForegroundColor Gray
}

# 前端 Dockerfile
if (-not (Test-Path "frontend\Dockerfile")) {
    @"
FROM node:18-alpine as builder

WORKDIR /app

# 复制依赖文件
COPY package*.json ./

# 安装依赖
RUN npm ci --only=production

# 复制源代码
COPY . .

# 构建应用
RUN npm run build

# 生产环境
FROM nginx:alpine

# 复制构建文件
COPY --from=builder /app/dist /usr/share/nginx/html

# 复制 nginx 配置
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
"@ | Out-File -FilePath "frontend\Dockerfile" -Encoding UTF8
    Write-Host "  创建文件: frontend\Dockerfile" -ForegroundColor Gray
}

# 创建 requirements.txt
if (-not (Test-Path "backend\requirements.txt")) {
    @"
# 基础依赖
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-multipart==0.0.6

# 数据库
sqlalchemy==2.0.23
alembic==1.12.1
psycopg2-binary==2.9.9
asyncpg==0.29.0

# 缓存和消息队列
redis==5.0.1
celery==5.3.4

# 数据处理
pandas==2.1.4
numpy==1.26.2
scipy==1.11.4

# 机器学习
scikit-learn==1.3.2
torch==2.1.1
torchvision==0.16.1
xgboost==2.0.2

# 技术指标
TA-Lib==0.4.28

# HTTP 客户端
httpx==0.25.1
aiohttp==3.9.1
requests==2.31.0

# 工具库
python-dotenv==1.0.0
pydantic==2.5.0
pydantic-settings==2.1.0
loguru==0.7.2

# 测试
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0

# 开发工具
black==23.11.0
isort==5.12.0
flake8==6.1.0
mypy==1.7.0
pre-commit==3.5.0
"@ | Out-File -FilePath "backend\requirements.txt" -Encoding UTF8
    Write-Host "  创建文件: backend\requirements.txt" -ForegroundColor Gray
}

# 创建 package.json
if (-not (Test-Path "frontend\package.json")) {
    @"
{
  "name": "mystock-ai-frontend",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
    "format": "prettier --write .",
    "test": "jest"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0",
    "antd": "^5.12.2",
    "@ant-design/icons": "^5.2.6",
    "@ant-design/charts": "^2.0.2",
    "axios": "^1.6.2",
    "zustand": "^4.4.7",
    "dayjs": "^1.11.10",
    "lodash": "^4.17.21"
  },
  "devDependencies": {
    "@types/react": "^18.2.37",
    "@types/react-dom": "^18.2.15",
    "@typescript-eslint/eslint-plugin": "^6.13.2",
    "@typescript-eslint/parser": "^6.13.2",
    "@vitejs/plugin-react": "^4.2.0",
    "eslint": "^8.55.0",
    "eslint-plugin-react-hooks": "^4.6.0",
    "eslint-plugin-react-refresh": "^0.4.5",
    "jest": "^29.7.0",
    "prettier": "^3.1.0",
    "typescript": "^5.2.2",
    "vite": "^5.0.0"
  }
}
"@ | Out-File -FilePath "frontend\package.json" -Encoding UTF8
    Write-Host "  创建文件: frontend\package.json" -ForegroundColor Gray
}

Write-Host "=" * 60
Write-Host "✅ 项目结构创建完成！" -ForegroundColor Green
Write-Host ""

Write-Host "📋 下一步操作：" -ForegroundColor Cyan
Write-Host "1. 代码已推送到 GitHub: https://github.com/MaNongkuxingseng/iStock" -ForegroundColor White
Write-Host ""
Write-Host "2. 设置开发环境：" -ForegroundColor Cyan
Write-Host "   复制 .env.example 为 .env" -ForegroundColor White
Write-Host "   编辑 .env 文件配置你的设置" -ForegroundColor White
Write-Host ""
Write-Host "3. 启动开发环境：" -ForegroundColor Cyan
Write-Host "   docker-compose up -d" -ForegroundColor White
Write-Host ""
Write-Host "4. 验证服务运行：" -ForegroundColor Cyan
Write-Host "   docker-compose ps" -ForegroundColor White
Write-Host "   前端: http://localhost:3000" -ForegroundColor White  
Write-Host "   后端API: http://localhost:8000" -ForegroundColor White
Write-Host "   API文档: http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "🎉 项目初始化完成！开始开发吧！" -ForegroundColor Green