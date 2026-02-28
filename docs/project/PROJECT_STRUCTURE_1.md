# iStock 项目结构

## 📁 目录结构

```
iStock/
├── 📁 backend/                    # 后端服务
│   ├── 📁 src/                   # 源代码
│   │   ├── 📁 api/              # API路由
│   │   │   ├── 📁 v1/           # API版本1
│   │   │   │   ├── 📁 endpoints/ # 端点定义
│   │   │   │   └── routers.py   # 路由注册
│   │   ├── 📁 core/             # 核心功能
│   │   │   ├── config.py        # 配置管理
│   │   │   ├── security.py      # 安全认证
│   │   │   └── dependencies.py  # 依赖注入
│   │   ├── 📁 database/         # 数据库
│   │   │   ├── models.py        # 数据模型
│   │   │   ├── session.py       # 数据库会话
│   │   │   └── migrations/      # 数据库迁移
│   │   ├── 📁 schemas/          # Pydantic模式
│   │   ├── 📁 services/         # 业务逻辑
│   │   │   ├── stock_service.py # 股票服务
│   │   │   ├── data_service.py  # 数据服务
│   │   │   └── ml_service.py    # 机器学习服务
│   │   ├── 📁 ml/               # 机器学习
│   │   │   ├── 📁 models/       # 模型定义
│   │   │   ├── 📁 training/     # 训练脚本
│   │   │   ├── 📁 prediction/   # 预测服务
│   │   │   └── 📁 features/     # 特征工程
│   │   ├── 📁 tasks/            # 异步任务
│   │   │   ├── celery_app.py    # Celery应用
│   │   │   ├── stock_tasks.py   # 股票任务
│   │   │   └── ml_tasks.py      # 机器学习任务
│   │   ├── 📁 utils/            # 工具函数
│   │   │   ├── data_utils.py    # 数据工具
│   │   │   ├── date_utils.py    # 日期工具
│   │   │   └── logging.py       # 日志配置
│   │   └── main.py              # 应用入口
│   ├── 📁 tests/                # 测试文件
│   │   ├── 📁 unit/             # 单元测试
│   │   ├── 📁 integration/      # 集成测试
│   │   └── 📁 e2e/              # 端到端测试
│   ├── 📁 alembic/              # 数据库迁移
│   │   ├── 📁 versions/         # 迁移版本
│   │   └── env.py               # 迁移环境
│   ├── pyproject.toml           # 项目配置
│   └── requirements.txt         # Python依赖
│
├── 📁 frontend/                  # 前端应用
│   ├── 📁 public/               # 静态资源
│   ├── 📁 src/                  # 源代码
│   │   ├── 📁 components/       # React组件
│   │   ├── 📁 pages/            # 页面组件
│   │   ├── 📁 hooks/            # 自定义Hooks
│   │   ├── 📁 utils/            # 工具函数
│   │   ├── 📁 types/            # TypeScript类型
│   │   ├── 📁 styles/           # 样式文件
│   │   ├── App.tsx              # 主应用组件
│   │   └── main.tsx             # 应用入口
│   ├── package.json             # Node.js依赖
│   ├── tsconfig.json            # TypeScript配置
│   └── vite.config.ts           # Vite配置
│
├── 📁 local/                     # 本地运行模式
│   ├── app.py                   # 本地FastAPI应用
│   ├── config.py                # 本地配置
│   └── start_local.py           # 本地启动脚本
│
├── 📁 docker/                    # Docker配置
│   ├── 📁 postgres/             # PostgreSQL配置
│   │   └── init.sql             # 数据库初始化脚本
│   ├── 📁 nginx/                # Nginx配置
│   │   ├── nginx.conf           # 开发环境配置
│   │   └── nginx.prod.conf      # 生产环境配置
│   ├── 📁 prometheus/           # Prometheus配置
│   │   └── prometheus.yml       # 监控配置
│   └── 📁 grafana/              # Grafana配置
│       ├── 📁 dashboards/       # 仪表板配置
│       └── 📁 datasources/      # 数据源配置
│
├── 📁 scripts/                   # 脚本工具
│   ├── deploy.sh                # 部署脚本
│   ├── seed_data.py             # 数据种子脚本
│   └── backup.sh                # 备份脚本
│
├── 📁 docs/                      # 文档
│   ├── 📁 api/                  # API文档
│   ├── 📁 architecture/         # 架构文档
│   ├── 📁 deployment/           # 部署文档
│   └── 📁 user_guide/           # 用户指南
│
├── 📁 data/                      # 数据存储
│   ├── 📁 models/               # 训练好的模型
│   ├── 📁 cache/                # 缓存数据
│   └── 📁 logs/                 # 日志文件
│
├── 📁 .github/                   # GitHub配置
│   └── 📁 workflows/            # CI/CD工作流
│       └── ci.yml               # 持续集成配置
│
├── .gitignore                   # Git忽略文件
├── .env.example                 # 环境变量示例
├── .pre-commit-config.yaml     # 代码检查配置
├── docker-compose.yml          # 开发环境Docker配置
├── docker-compose.prod.yml     # 生产环境Docker配置
├── Dockerfile.backend          # 后端Dockerfile
├── Dockerfile.frontend         # 前端Dockerfile
├── LICENSE                     # 许可证文件
├── Makefile                    # Make命令
├── pyproject.toml              # Python项目配置
├── README.md                   # 项目说明
├── DEVELOPMENT_PLAN.md         # 开发计划
├── WEEKLY_PLAN.md              # 周计划
├── DATA_ACCURACY_PLAN.md       # 数据准确性计划
└── PROJECT_STRUCTURE.md        # 本项目结构文档
```

## 🔧 技术架构

### 后端架构
```
┌─────────────────────────────────────────────────────────┐
│                    FastAPI 应用层                        │
├─────────────────────────────────────────────────────────┤
│                   业务逻辑层 (Services)                   │
├─────────────────────────────────────────────────────────┤
│                   数据访问层 (Models)                    │
├─────────────────────────────────────────────────────────┤
│                   数据库层 (PostgreSQL)                  │
└─────────────────────────────────────────────────────────┘
```

### 前端架构
```
┌─────────────────────────────────────────────────────────┐
│                   React + TypeScript                     │
├─────────────────────────────────────────────────────────┤
│                  状态管理 (Zustand/Redux)                │
├─────────────────────────────────────────────────────────┤
│                  UI组件库 (Ant Design)                   │
├─────────────────────────────────────────────────────────┤
│                 数据可视化 (ECharts)                     │
└─────────────────────────────────────────────────────────┘
```

### 数据流
```
数据源 → 数据采集 → 数据清洗 → 特征工程 → 模型训练 → 预测 → 可视化
   │         │          │          │          │         │        │
新浪财经   实时API    数据验证    技术指标   机器学习   结果存储   Web界面
腾讯财经   定时任务   异常检测    基本面     深度学习   缓存更新  移动端
东方财富   历史数据   数据修复    市场情绪   集成学习   实时推送  API接口
```

## 🗄️ 数据库设计

### 核心表
1. **stocks** - 股票基本信息
2. **stock_daily** - 股票日线数据
3. **technical_indicators** - 技术指标
4. **ml_predictions** - 机器学习预测
5. **users** - 用户信息
6. **user_portfolios** - 用户持仓

### 数据关系
```
users (1) ── (many) user_portfolios
                │
                └── (1) stocks (1) ── (many) stock_daily
                                        │
                                        └── (1) technical_indicators
                                        │
                                        └── (1) ml_predictions
```

## 🔄 开发工作流

### 代码提交
```bash
# 1. 创建功能分支
git checkout -b feature/your-feature

# 2. 开发代码
# ... 编写代码 ...

# 3. 运行测试和检查
make test
make lint

# 4. 提交代码
git add .
git commit -m "feat: add your feature"

# 5. 推送到远程
git push origin feature/your-feature

# 6. 创建Pull Request
```

### 本地开发
```bash
# 启动开发环境
make dev

# 或使用脚本
./start-dev.bat  # Windows
```

## 📊 监控和运维

### 监控指标
1. **应用性能**：响应时间、错误率、吞吐量
2. **数据质量**：准确性、完整性、时效性
3. **系统资源**：CPU、内存、磁盘、网络
4. **业务指标**：用户活跃、预测准确率、信号质量

### 日志级别
- **DEBUG**: 开发调试信息
- **INFO**: 常规运行信息
- **WARNING**: 警告信息
- **ERROR**: 错误信息
- **CRITICAL**: 严重错误

## 🔒 安全考虑

### 数据安全
1. **加密传输**: HTTPS/TLS
2. **数据加密**: 敏感数据加密存储
3. **访问控制**: 基于角色的权限管理
4. **审计日志**: 操作记录和追踪

### API安全
1. **认证**: JWT Token
2. **授权**: 权限验证
3. **限流**: 请求频率限制
4. **验证**: 输入数据验证

## 🚀 部署策略

### 开发环境
- 本地Docker Compose
- 热重载支持
- 调试工具集成

### 测试环境
- 自动化测试
- 性能测试
- 安全扫描

### 生产环境
- 多容器部署
- 负载均衡
- 监控告警
- 备份恢复

## 📈 扩展性设计

### 水平扩展
- 无状态服务设计
- 数据库读写分离
- 缓存层优化
- 消息队列解耦

### 垂直扩展
- 资源监控和预警
- 自动扩缩容
- 性能优化
- 代码重构

---

**最后更新**: 2026-02-28  
**维护者**: iStock开发团队