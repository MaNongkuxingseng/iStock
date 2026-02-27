# myStock-AI Backend

后端服务基于 FastAPI + PostgreSQL + Redis 构建，提供完整的股票数据分析、机器学习预测和API服务。

## 功能特性

- 🚀 基于 FastAPI 的高性能 API
- 🗄️ PostgreSQL 数据库存储
- 🔄 Redis 缓存和消息队列
- 🤖 机器学习模型集成
- 📊 实时数据处理
- 🔐 JWT 认证和授权
- 📈 技术指标计算
- 🧪 完整的测试覆盖
- 📝 自动 API 文档生成

## 技术栈

### 核心框架
- **FastAPI**: 现代、快速的 Web 框架
- **SQLAlchemy**: Python SQL 工具包和 ORM
- **Alembic**: 数据库迁移工具
- **Pydantic**: 数据验证和设置管理

### 数据存储
- **PostgreSQL**: 关系型数据库
- **Redis**: 缓存和消息代理
- **Asyncpg**: 异步 PostgreSQL 驱动

### 机器学习
- **PyTorch**: 深度学习框架
- **Scikit-learn**: 机器学习库
- **TA-Lib**: 技术指标计算
- **Pandas/Numpy**: 数据处理

### 任务队列
- **Celery**: 分布式任务队列
- **Flower**: Celery 监控工具

### 工具和工具
- **Loguru**: 日志记录
- **Python-dotenv**: 环境变量管理
- **HTTPX**: 异步 HTTP 客户端

## 开发环境

### 环境要求
- Python 3.10+
- PostgreSQL 14+
- Redis 7+
- Docker & Docker Compose（推荐）

### 安装依赖
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 环境变量配置
```bash
cp .env.example .env
# 编辑 .env 文件配置你的设置
```

### 数据库设置
```bash
# 使用 Docker（推荐）
docker-compose up -d postgres redis

# 或手动安装
# 1. 安装 PostgreSQL 和 Redis
# 2. 创建数据库: mystock_ai
# 3. 运行迁移: alembic upgrade head
```

### 启动开发服务器
```bash
# 开发模式（热重载）
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# 或使用脚本
python src/main.py
```

### 访问 API 文档
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 项目结构

```
backend/
├── src/
│   ├── main.py              # 应用入口
│   ├── config/              # 配置管理
│   ├── database/            # 数据库配置
│   ├── models/              # 数据模型
│   ├── schemas/             # Pydantic 模式
│   ├── api/                 # API 路由
│   │   ├── v1/              # API 版本 1
│   │   │   ├── endpoints/   # 端点定义
│   │   │   └── routers.py   # 路由注册
│   ├── core/                # 核心功能
│   │   ├── security.py      # 安全认证
│   │   ├── dependencies.py  # 依赖注入
│   │   └── exceptions.py    # 异常处理
│   ├── services/            # 业务逻辑
│   │   ├── stock_service.py # 股票服务
│   │   ├── ml_service.py    # 机器学习服务
│   │   └── data_service.py  # 数据服务
│   ├── ml/                  # 机器学习
│   │   ├── models/          # 模型定义
│   │   ├── training/        # 训练脚本
│   │   ├── prediction/      # 预测服务
│   │   └── features/        # 特征工程
│   ├── tasks/               # 异步任务
│   │   ├── celery_app.py    # Celery 应用
│   │   ├── stock_tasks.py   # 股票相关任务
│   │   └── ml_tasks.py      # ML 相关任务
│   ├── utils/               # 工具函数
│   │   ├── data_utils.py    # 数据工具
│   │   ├── date_utils.py    # 日期工具
│   │   └── logging.py       # 日志配置
│   └── tests/               # 测试文件
├── alembic/                 # 数据库迁移
│   ├── versions/            # 迁移版本
│   └── env.py               # 迁移环境
├── data/                    # 数据文件
│   ├── models/              # 训练好的模型
│   └── cache/               # 缓存数据
├── logs/                    # 日志文件
├── .env.example             # 环境变量示例
├── requirements.txt         # Python 依赖
├── pyproject.toml           # 项目配置
└── Dockerfile              # Docker 配置
```

## API 设计

### RESTful API 规范
- 使用 HTTP 方法：GET, POST, PUT, DELETE, PATCH
- 资源使用复数名词：`/api/v1/stocks`
- 版本控制：`/api/v1/`
- 状态码遵循 REST 规范

### 认证和授权
- JWT Token 认证
- 基于角色的访问控制（RBAC）
- API Key 用于第三方集成

### 响应格式
```json
{
  "success": true,
  "data": {...},
  "message": "操作成功",
  "timestamp": "2026-02-27T13:45:00Z"
}
```

### 错误处理
```json
{
  "success": false,
  "error": {
    "code": "STOCK_NOT_FOUND",
    "message": "股票不存在",
    "details": {...}
  },
  "timestamp": "2026-02-27T13:45:00Z"
}
```

## 数据库设计

### 核心表结构
```sql
-- 股票基本信息
CREATE TABLE stocks (
    id UUID PRIMARY KEY,
    code VARCHAR(10) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    market VARCHAR(10),
    industry VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 股票日线数据
CREATE TABLE stock_daily (
    id UUID PRIMARY KEY,
    stock_id UUID REFERENCES stocks(id),
    date DATE NOT NULL,
    open DECIMAL(10,3),
    high DECIMAL(10,3),
    low DECIMAL(10,3),
    close DECIMAL(10,3),
    volume BIGINT,
    UNIQUE(stock_id, date)
);

-- 技术指标
CREATE TABLE technical_indicators (
    id UUID PRIMARY KEY,
    stock_id UUID REFERENCES stocks(id),
    date DATE NOT NULL,
    ma5 DECIMAL(10,3),
    ma10 DECIMAL(10,3),
    rsi DECIMAL(10,3),
    macd DECIMAL(10,3),
    UNIQUE(stock_id, date)
);
```

### 数据关系
```
stocks (1) ── (many) stock_daily
stocks (1) ── (many) technical_indicators
stocks (1) ── (many) ml_predictions
```

## 机器学习集成

### 模型类型
1. **价格预测模型** (LSTM/GRU)
   - 输入：历史价格序列
   - 输出：未来价格预测
   - 用途：短期交易信号

2. **趋势分类模型** (XGBoost/Random Forest)
   - 输入：技术指标特征
   - 输出：上涨/下跌/震荡
   - 用途：趋势判断

3. **异常检测模型** (Isolation Forest/AutoEncoder)
   - 输入：多维特征
   - 输出：异常分数
   - 用途：风险预警

### 训练流程
```python
# 1. 数据准备
data = prepare_training_data(stock_code, start_date, end_date)

# 2. 特征工程
features = extract_features(data)

# 3. 模型训练
model = train_model(features, labels)

# 4. 模型评估
metrics = evaluate_model(model, test_data)

# 5. 模型部署
deploy_model(model, version='1.0.0')
```

### 预测服务
```python
@app.post("/api/v1/predict")
async def predict_price(
    stock_code: str,
    model_version: str = "latest"
):
    # 获取实时数据
    data = await get_stock_data(stock_code)
    
    # 特征提取
    features = extract_features(data)
    
    # 模型预测
    prediction = ml_service.predict(features, model_version)
    
    # 返回结果
    return {
        "stock_code": stock_code,
        "prediction": prediction,
        "confidence": prediction.confidence,
        "timestamp": datetime.now()
    }
```

## 任务队列

### Celery 配置
```python
# tasks/celery_app.py
from celery import Celery

celery_app = Celery(
    "mystock_ai",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
    include=["tasks.stock_tasks", "tasks.ml_tasks"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Shanghai",
    enable_utc=True,
)
```

### 定时任务
```python
# 每天收盘后更新数据
@celery_app.task
def update_daily_data():
    stocks = get_all_stocks()
    for stock in stocks:
        update_stock_data.delay(stock.code)

# 每小时计算技术指标
@celery_app.task
def calculate_technical_indicators():
    stocks = get_active_stocks()
    for stock in stocks:
        calculate_indicators.delay(stock.code)
```

## 测试

### 测试结构
```bash
tests/
├── unit/           # 单元测试
├── integration/    # 集成测试
├── e2e/           # 端到端测试
└── fixtures/      # 测试数据
```

### 运行测试
```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/unit/test_stock_service.py

# 带覆盖率报告
pytest --cov=src --cov-report=html

# 运行集成测试
pytest tests/integration/ -v
```

### 测试示例
```python
# tests/unit/test_stock_service.py
import pytest
from src.services.stock_service import StockService

@pytest.mark.asyncio
async def test_get_stock_data():
    service = StockService()
    data = await service.get_stock_data("603949")
    
    assert data is not None
    assert "code" in data
    assert data["code"] == "603949"
    assert "price" in data
    assert data["price"] > 0
```

## 部署

### Docker 部署
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 生产环境配置
```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  backend:
    build: .
    environment:
      DATABASE_URL: postgresql://user:password@postgres:5432/mystock_ai
      REDIS_URL: redis://redis:6379/0
      DEBUG: "false"
    ports:
      - "8000:8000"
    depends_on:
      - postgres
      - redis
```

### 监控和日志
- **应用日志**: Loguru 结构化日志
- **性能监控**: Prometheus + Grafana
- **错误追踪**: Sentry
- **健康检查**: `/health` 端点

## 性能优化

### 数据库优化
- 使用连接池
- 添加适当索引
- 查询优化
- 读写分离

### 缓存策略
- Redis 缓存热点数据
- 内存缓存频繁访问数据
- CDN 缓存静态资源

### 异步处理
- 使用异步数据库驱动
- Celery 处理耗时任务
- 消息队列解耦服务

## 安全考虑

### 数据安全
- 数据库连接加密
- 敏感数据加密存储
- 定期数据备份
- 访问日志审计

### API 安全
- JWT Token 认证
- 请求频率限制
- SQL 注入防护
- XSS 和 CSRF 防护

### 系统安全
- 定期安全更新
- 漏洞扫描
- 访问控制
- 安全监控

## 贡献指南

1. Fork 仓库
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

MIT License