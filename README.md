# iStock 🚀

智能股票分析与预测系统 - 基于机器学习的专业投资助手

## 📊 项目概述

iStock是一个集成了实时行情监控、技术指标分析、机器学习预测和Web可视化界面的智能股票分析系统。系统旨在为投资者提供专业的数据分析和决策支持。

## 🎯 核心功能

### ✅ 已实现功能
- 实时股票价格监控（新浪财经API）
- 专业级技术指标分析（10+个指标）
- 智能警报系统（三级警报机制）
- 投资组合风险评估
- Feishu消息自动推送

### 🚧 开发中功能
- 机器学习价格预测模型
- Web可视化管理界面
- 多数据源验证系统
- 历史回测分析

### 📅 规划功能
- AI智能推荐系统
- 自动化交易接口
- 多用户SaaS平台
- 移动端应用

## 🏗️ 系统架构

```
iStock/
├── 📁 data/                    # 数据存储
├── 📁 src/                    # 源代码
│   ├── core/                  # 核心逻辑
│   ├── ml/                    # 机器学习
│   ├── web/                   # Web界面
│   └── utils/                 # 工具函数
├── 📁 docs/                   # 文档
├── 📁 tests/                  # 测试
├── 📁 deployment/             # 部署配置
└── 📁 scripts/                # 脚本工具
```

## 🔧 技术栈

### 后端技术
- **Python 3.10+**: 主要开发语言
- **FastAPI**: Web API框架
- **SQLAlchemy**: ORM数据库操作
- **Celery**: 异步任务队列
- **Redis**: 缓存和消息队列

### 机器学习
- **PyTorch**: 深度学习框架
- **Scikit-learn**: 传统机器学习
- **TA-Lib**: 技术指标计算
- **Pandas/Numpy**: 数据处理

### 前端技术
- **React 18**: 前端框架
- **TypeScript**: 类型安全
- **Ant Design**: UI组件库
- **ECharts**: 数据可视化
- **Vite**: 构建工具

### 数据存储
- **PostgreSQL**: 主数据库
- **Redis**: 缓存数据库
- **MinIO**: 对象存储（可选）

### 部署运维
- **Docker**: 容器化
- **Docker Compose**: 服务编排
- **Nginx**: Web服务器
- **GitHub Actions**: CI/CD

## 🚀 快速开始

### 环境要求
- Python 3.10+
- Node.js 18+
- Docker & Docker Compose
- PostgreSQL 14+
- Redis 7+

### 本地开发
```bash
# 克隆仓库
git clone https://github.com/yourname/iStock.git
cd iStock

# 后端环境
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 前端环境
cd frontend
npm install
npm run dev

# 启动服务
docker-compose up -d
```

### 生产部署
```bash
# 使用Docker部署
docker-compose -f docker-compose.prod.yml up -d

# 或使用部署脚本
./scripts/deploy.sh
```

## 📊 数据源

### 主要数据源
1. **新浪财经API**: 实时行情数据
2. **腾讯财经API**: 备用数据源
3. **东方财富API**: 基本面数据
4. **聚宽数据**: 历史数据（付费）

### 数据准确性保障
- 多数据源交叉验证
- 实时数据质量监控
- 异常数据自动过滤
- 历史数据回补机制

## 🤖 机器学习模型

### 预测模型
1. **价格预测**: LSTM/GRU时间序列模型
2. **趋势分类**: XGBoost/Random Forest
3. **异常检测**: 孤立森林/AutoEncoder
4. **推荐系统**: 协同过滤/深度学习

### 模型训练流程
```
数据收集 → 特征工程 → 模型训练 → 验证评估 → 部署上线
```

## 📈 系统特性

### 实时性
- 秒级数据更新
- 实时计算技术指标
- 即时警报推送
- 动态图表更新

### 准确性
- 多数据源验证
- 机器学习模型优化
- 历史回测验证
- 实时监控调整

### 可扩展性
- 模块化架构设计
- 插件式功能扩展
- 分布式部署支持
- 多租户架构

### 安全性
- 数据加密传输
- 用户权限控制
- 操作日志审计
- 系统备份恢复

## 📱 用户界面

### 主要页面
1. **仪表板**: 实时概览和关键指标
2. **持仓分析**: 详细持仓和技术分析
3. **股票推荐**: 系统推荐和买入建议
4. **预测分析**: 机器学习预测结果
5. **系统管理**: 配置和监控

### 交互特性
- 响应式设计（支持移动端）
- 实时数据推送（WebSocket）
- 交互式图表（缩放、拖拽）
- 个性化设置（主题、布局）

## 🔄 开发流程

### 代码规范
- **Git提交**: Conventional Commits
- **代码风格**: Black + isort + flake8
- **类型检查**: mypy (Python) + TypeScript
- **测试覆盖**: pytest + Jest

### CI/CD流程
```yaml
# GitHub Actions工作流
1. 代码提交 → 2. 自动化测试 → 3. 代码检查
4. 构建镜像 → 5. 安全扫描 → 6. 部署上线
```

### 版本管理
- **主分支**: main (生产环境)
- **开发分支**: develop (集成测试)
- **功能分支**: feature/* (新功能开发)
- **发布分支**: release/* (版本发布)

## 📚 文档

### 用户文档
- [快速开始指南](docs/user_guide/quickstart.md)
- [功能使用说明](docs/user_guide/features.md)
- [常见问题解答](docs/user_guide/faq.md)

### 开发文档
- [API接口文档](docs/api/)
- [架构设计文档](docs/architecture/)
- [部署指南](docs/deployment/)

### 运维文档
- [监控告警配置](docs/ops/monitoring.md)
- [故障排除指南](docs/ops/troubleshooting.md)
- [备份恢复方案](docs/ops/backup.md)

## 🤝 贡献指南

### 开发流程
1. Fork本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启Pull Request

### 代码要求
- 添加适当的测试用例
- 更新相关文档
- 确保代码通过所有检查
- 遵循项目代码规范

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 支持与联系

### 问题反馈
- GitHub Issues: [问题报告](https://github.com/yourname/iStock/issues)
- 邮件支持: support@istock.com

### 社区交流
- Discord: [加入讨论](https://discord.gg/istock)
- 微信群: 扫码加入（待创建）

## 🙏 致谢

感谢所有为项目做出贡献的开发者！

---

**iStock - 让投资更智能，让决策更科学** 🚀