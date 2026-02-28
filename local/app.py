from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
import uvicorn
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)  

# 创建FastAPI应用
app = FastAPI(
    title="iStock Local Mode",
    description="iStock本地化运行模式 - 快速验证版本",
    version="1.0.0",
    debug=True
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 健康检查端点
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "mode": "local",
        "timestamp": datetime.now().isoformat()
    }

# 股票数据端点（本地化）
@app.get("/api/v1/stocks/{code}")
async def get_stock_data(code: str):
    """
    获取股票数据（本地化模式）
    """
    try:
        # 使用本地SQLite数据库或模拟数据
        stock_data = {
            "code": code,
            "name": f"股票{code}",
            "price": 100.0,
            "change": 2.5,
            "volume": 1000000,
            "pe_ratio": 25.5,
            "industry": "科技"
        }
        return stock_data
    except Exception as e:
        logger.error(f"获取股票数据失败: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(
        "local.app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )