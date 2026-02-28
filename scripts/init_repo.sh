#!/bin/bash

# myStock-AI 项目初始化脚本
# 用于快速设置开发环境和GitHub仓库

set -e  # 遇到错误时退出

echo "🚀 开始初始化 myStock-AI 项目..."

# 检查必要工具
echo "🔧 检查必要工具..."
command -v git >/dev/null 2>&1 || { echo "❌ 需要安装 git"; exit 1; }
command -v docker >/dev/null 2>&1 || { echo "❌ 需要安装 docker"; exit 1; }
command -v docker-compose >/dev/null 2>&1 || { echo "❌ 需要安装 docker-compose"; exit 1; }

# 创建项目目录结构
echo "📁 创建项目目录结构..."
mkdir -p src/{core,ml,web,utils}
mkdir -p data/{raw,processed,models}
mkdir -p docs/{api,architecture,deployment,user_guide}
mkdir -p tests/{unit,integration,e2e}
mkdir -p deployment/{docker,nginx,scripts}
mkdir -p .github/workflows
mkdir -p monitoring/{prometheus,grafana}

# 创建基础文件
echo "📄 创建基础配置文件..."

# Python 环境配置
cat > .python-version << 'EOF'
3.10
EOF

cat > .env.example << 'EOF'
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
EOF

# Git 配置
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual Environments
venv/
env/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Database
*.db
*.sqlite3

# Data
data/raw/
data/processed/
data/models/
!data/raw/.gitkeep
!data/processed/.gitkeep
!data/models/.gitkeep

# Logs
logs/
*.log

# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# Frontend
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
dist/
build/
.coverage
.nyc_output

# Coverage
.coverage
.coverage.*
.coverage*
htmlcov/

# Jupyter Notebook
.ipynb_checkpoints

# PyCharm
.idea/

# VS Code
.vscode/

# Docker
docker-compose.override.yml
EOF

# 创建占位文件
echo "📝 创建占位文件..."
touch data/raw/.gitkeep
touch data/processed/.gitkeep
touch data/models/.gitkeep
touch src/core/__init__.py
touch src/ml/__init__.py
touch src/web/__init__.py
touch src/utils/__init__.py

# 创建基础 README
echo "📖 创建基础文档..."
cat > docs/quickstart.md << 'EOF'
# 快速开始指南

## 环境要求

### 系统要求
- Python 3.10+
- Node.js 18+
- Docker 20.10+
- Docker Compose 2.0+

### 开发工具
- Git
- VS Code 或 PyCharm
- PostgreSQL 14+ (可选，Docker中包含)
- Redis 7+ (可选，Docker中包含)

## 本地开发设置

### 1. 克隆仓库
```bash
git clone https://github.com/yourname/myStock-AI.git
cd myStock-AI
```

### 2. 设置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件，配置你的设置
```

### 3. 启动开发环境
```bash
# 使用 Docker Compose
docker-compose up -d

# 或手动启动各个服务
# 启动数据库
docker-compose up -d postgres redis

# 启动后端
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python src/main.py

# 启动前端
cd frontend
npm install
npm run dev
```

### 4. 访问应用
- 前端: http://localhost:3000
- 后端API: http://localhost:8000
- API文档: http://localhost:8000/docs
- 监控面板: http://localhost:3001 (用户名: admin, 密码: admin)

## 开发工作流

### 代码规范
```bash
# 代码格式化
black src/
isort src/

# 代码检查
flake8 src/
mypy src/

# 运行测试
pytest tests/
```

### Git 工作流
1. 创建功能分支: `git checkout -b feature/your-feature`
2. 开发并提交: `git add . && git commit -m "feat: add your feature"`
3. 推送到远程: `git push origin feature/your-feature`
4. 创建 Pull Request

## 常见问题

### 数据库连接问题
```bash
# 检查数据库状态
docker-compose ps

# 查看数据库日志
docker-compose logs postgres

# 重置数据库
docker-compose down -v
docker-compose up -d
```

### 前端构建问题
```bash
# 清理缓存
rm -rf node_modules
npm cache clean --force
npm install
```

### 后端依赖问题
```bash
# 重新创建虚拟环境
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 获取帮助

- 查看详细文档: `docs/` 目录
- 报告问题: GitHub Issues
- 讨论功能: GitHub Discussions
EOF

# 创建 Docker 基础文件
echo "🐳 创建 Docker 配置文件..."

# 后端 Dockerfile
cat > backend/Dockerfile << 'EOF'
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
EOF

# 前端 Dockerfile
cat > frontend/Dockerfile << 'EOF'
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
EOF

# 创建 requirements.txt
cat > backend/requirements.txt << 'EOF'
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
EOF

# 创建 package.json
cat > frontend/package.json << 'EOF'
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
EOF

# 创建数据库初始化脚本
cat > scripts/init-db.sql << 'EOF'
-- 创建扩展
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 创建股票基本信息表
CREATE TABLE stocks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    code VARCHAR(10) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    market VARCHAR(10),
    industry VARCHAR(100),
    listing_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建股票日线数据表
CREATE TABLE stock_daily (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    stock_id UUID REFERENCES stocks(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    open DECIMAL(10, 3),
    high DECIMAL(10, 3),
    low DECIMAL(10, 3),
    close DECIMAL(10, 3),
    volume BIGINT,
    amount DECIMAL(20, 3),
    change DECIMAL(10, 3),
    change_percent DECIMAL(10, 3),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(stock_id, date)
);

-- 创建技术指标表
CREATE TABLE technical_indicators (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    stock_id UUID REFERENCES stocks(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    ma5 DECIMAL(10, 3),
    ma10 DECIMAL(10, 3),
    ma20 DECIMAL(10, 3),
    ma60 DECIMAL(10, 3),
    rsi DECIMAL(10, 3),
    macd DECIMAL(10, 3),
    macd_signal DECIMAL(10, 3),
    macd_hist DECIMAL(10, 3),
    kdj_k DECIMAL(10, 3),
    kdj_d DECIMAL(10, 3),
    kdj_j DECIMAL(10, 3),
    boll_upper DECIMAL(10, 3),
    boll_middle DECIMAL(10, 3),
    boll_lower DECIMAL(10, 3),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(stock_id, date)
);

-- 创建机器学习预测表
CREATE TABLE ml_predictions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    stock_id UUID REFERENCES stocks(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    model_name VARCHAR(100),
    prediction_type VARCHAR(50),
    predicted_value DECIMAL(10, 3),
    confidence DECIMAL(5, 3),
    features JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(stock_id, date, model_name, prediction_type)
);

-- 创建用户持仓表
CREATE TABLE user_positions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    stock_id UUID REFERENCES stocks(id) ON DELETE CASCADE,
    shares INTEGER NOT NULL,
    cost_price DECIMAL(10, 3) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, stock_id)
);

-- 创建数据质量监控表
CREATE TABLE data_quality (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    data_source VARCHAR(50),
    data_type VARCHAR(50),
    check_time TIMESTAMP NOT NULL,
    completeness_score DECIMAL(5, 3),
    accuracy_score DECIMAL(5, 3),
    timeliness_score DECIMAL(5, 3),
    issues JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引
CREATE INDEX idx_stock_daily_stock_id ON stock_daily(stock_id);
CREATE INDEX idx_stock_daily_date ON stock_daily(date);
CREATE INDEX idx_technical_indicators_stock_id ON technical_indicators(stock_id);
CREATE INDEX idx_technical_indicators_date ON technical_indicators(date);
CREATE INDEX idx_ml_predictions_stock_id ON ml_predictions(stock_id);
CREATE INDEX idx_ml_predictions_date ON ml_predictions(date);
CREATE INDEX idx_user_positions_user_id ON user_positions(user_id);
CREATE INDEX idx_data_quality_check_time ON data_quality(check_time);

-- 创建更新时间的触发器函数
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- 为需要更新时间的表添加触发器
CREATE TRIGGER update_stocks_updated_at BEFORE UPDATE ON stocks
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_positions_updated_at BEFORE UPDATE ON user_positions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
EOF

echo "✅ 项目结构创建完成！"
echo ""
echo "📋 下一步操作："
echo "1. 初始化 Git 仓库:"
echo "   git init"
echo "   git add ."
echo "   git commit -m 'feat: initial project structure'"
echo ""
echo "2. 连接到 GitHub:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/myStock-AI.git"
echo "   git push -u origin main"
echo ""
echo "3. 设置开发环境:"
echo "   cp .env.example .env"
echo "   # 编辑 .env 文件配置你的设置"
echo ""
echo "4. 启动开发环境:"
echo "   docker-compose up -d"
echo ""
echo "🎉 项目初始化完成！开始开发吧！"