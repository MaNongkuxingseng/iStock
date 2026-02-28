# 📁 iStock 项目结构

## 🏗️ 项目架构

```
iStock/
├── 📁 backend/                    # 后端服务
│   ├── 📁 src/                   # 源代码
│   │   ├── 📁 api/              # API接口
│   │   ├── 📁 database/         # 数据库相关
│   │   ├── 📁 models/           # 数据模型
│   │   ├── 📁 services/         # 业务服务
│   │   └── 📁 utils/            # 工具函数
│   ├── 📁 scripts/              # 管理脚本
│   └── requirements.txt         # Python依赖
│
├── 📁 frontend/                  # 前端应用
│   ├── 📁 public/               # 静态资源
│   ├── 📁 src/                  # 源代码
│   │   ├── 📁 components/       # 组件
│   │   ├── 📁 pages/            # 页面
│   │   ├── 📁 services/         # API服务
│   │   └── 📁 contexts/         # 上下文
│   └── package.json             # Node.js依赖
│
├── 📁 docker/                    # Docker配置
│   ├── 📁 nginx/                # Nginx配置
│   ├── 📁 postgres/             # PostgreSQL初始化
│   └── nginx.conf               # Nginx主配置
│
├── 📁 scripts/                   # 项目脚本
│   ├── git_commit_notify.py     # Git提交通知
│   └── project_management.py    # 项目管理
│
├── 📁 docs/                      # 项目文档
│   ├── 📁 project/              # 项目文档
│   ├── 📁 guides/               # 使用指南
│   ├── 📁 reports/              # 分析报告
│   ├── 📁 api/                  # API文档
│   └── 📁 development/          # 开发文档
│
├── 📁 knowledge/                 # 知识库
│   ├── project_overview.md      # 项目概述
│   ├── development_workflow.md  # 开发工作流
│   ├── api_documentation.md     # API文档
│   └── deployment_guide.md      # 部署指南
│
├── 📁 data/                      # 数据文件
│   ├── 📁 raw/                  # 原始数据
│   ├── 📁 processed/            # 处理后的数据
│   └── 📁 models/               # 机器学习模型
│
├── 📁 local/                     # 本地开发环境
│   ├── app.py                   # 本地应用
│   └── start_local.py           # 本地启动脚本
│
├── 📁 .github/                   # GitHub配置
│   └── 📁 workflows/            # CI/CD工作流
│
├── docker-compose.yml           # Docker开发环境
├── docker-compose.prod.yml      # Docker生产环境
├── requirements.txt             # Python主依赖
├── requirements-dev.txt         # Python开发依赖
├── pyproject.toml               # 项目配置
├── Makefile                     # 构建命令
├── .env.example                 # 环境变量示例
├── .gitignore                   # Git忽略文件
├── LICENSE                      # 许可证
└── README.md                    # 项目说明
```

## 🔧 核心文件说明

### 后端服务 (`backend/`)
- `src/api/` - FastAPI路由和端点
- `src/database/` - 数据库连接和会话管理
- `src/models/` - SQLAlchemy数据模型
- `src/services/` - 业务逻辑服务层
- `src/utils/` - 工具函数和辅助类

### 前端应用 (`frontend/`)
- `src/components/` - React组件
- `src/pages/` - 页面组件
- `src/services/` - API调用服务
- `src/contexts/` - React上下文

### Docker配置 (`docker/`)
- `nginx/` - Web服务器配置
- `postgres/` - 数据库初始化脚本
- 多环境Docker Compose配置

### 文档 (`docs/`)
- `project/` - 项目规划和设计文档
- `guides/` - 用户指南和操作手册
- `reports/` - 分析报告和审计文档
- `api/` - API接口文档
- `development/` - 开发文档和规范

### 知识库 (`knowledge/`)
- 项目概述和核心概念
- 开发工作流和最佳实践
- API参考和部署指南
- 故障排除和维护

## 🚀 开发工作流

### 1. 环境设置
```bash
# 复制环境变量
cp .env.example .env

# 安装依赖
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 启动开发环境
docker-compose up -d
```

### 2. 代码开发
```bash
# 后端开发
cd backend
python -m uvicorn src.main:app --reload

# 前端开发
cd frontend
npm start
```

### 3. 测试验证
```bash
# 运行测试
pytest

# 代码检查
black .
flake8 .
mypy .
```

### 4. 提交代码
```bash
# 使用中文提交消息
git commit -m "feat: 添加新功能"

# 推送到远程
git push origin develop
```

## 📊 项目状态

### 当前版本: v0.1.0
### 完成度: ~85%
### 最后更新: 2026-02-28

## 🔗 相关链接

- [GitHub仓库](https://github.com/MaNongkuxingseng/iStock)
- [开发计划](docs/project/DEVELOPMENT_PLAN.md)
- [API文档](docs/api/API_DOCUMENTATION.md)
- [部署指南](docs/guides/DEPLOYMENT_GUIDE.md)