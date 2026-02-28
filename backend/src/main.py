"""
iStock后端主应用
FastAPI应用入口点
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import uvicorn

from .api import stocks, users, auth, portfolio
from .database.session_mysql import test_connection, create_tables

# 创建FastAPI应用
app = FastAPI(
    title="iStock API",
    version="1.0.0",
    description="智能股票分析系统API",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# 配置CORS（跨域资源共享）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应限制为特定域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 添加可信主机中间件
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  # 生产环境应限制为特定域名
)

# 注册路由
app.include_router(stocks.router, prefix="/api/stocks", tags=["stocks"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(portfolio.router, prefix="/api/portfolio", tags=["portfolio"])


@app.on_event("startup")
async def startup_event():
    """应用启动时执行"""
    print("🚀 iStock API 正在启动...")
    
    # 测试数据库连接
    if test_connection():
        print("✅ 数据库连接成功")
        
        # 创建数据库表（如果不存在）
        if create_tables():
            print("✅ 数据库表创建/验证完成")
        else:
            print("⚠️  数据库表创建失败，请检查数据库权限")
    else:
        print("❌ 数据库连接失败，请检查MySQL配置")
    
    print("✅ iStock API 启动完成")


@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时执行"""
    print("🛑 iStock API 正在关闭...")


@app.get("/")
async def root():
    """根路径，返回API基本信息"""
    return {
        "message": "欢迎使用 iStock API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
        "endpoints": {
            "stocks": "/api/stocks",
            "users": "/api/users",
            "auth": "/api/auth",
            "portfolio": "/api/portfolio"
        }
    }


@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {
        "status": "healthy",
        "service": "iStock API",
        "timestamp": "2026-03-01T02:15:00Z",
        "version": "1.0.0",
        "database": "connected" if test_connection() else "disconnected"
    }


@app.get("/info")
async def api_info():
    """API信息端点"""
    return {
        "name": "iStock API",
        "description": "智能股票分析系统",
        "version": "1.0.0",
        "author": "iStock Team",
        "contact": {
            "email": "support@istock.com",
            "website": "https://istock.com"
        },
        "license": {
            "name": "MIT",
            "url": "https://opensource.org/licenses/MIT"
        },
        "repository": {
            "type": "git",
            "url": "https://github.com/MaNongkuxingseng/iStock"
        },
        "features": [
            "股票数据管理",
            "技术指标分析",
            "用户投资组合",
            "实时市场监控",
            "买卖信号推送"
        ]
    }


@app.get("/status")
async def system_status():
    """系统状态端点"""
    from datetime import datetime
    import psutil
    import os
    
    # 获取系统信息
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    # 获取进程信息
    process = psutil.Process(os.getpid())
    
    return {
        "timestamp": datetime.now().isoformat(),
        "system": {
            "cpu_usage": f"{cpu_percent}%",
            "memory_usage": f"{memory.percent}%",
            "memory_available": f"{memory.available / 1024 / 1024:.1f} MB",
            "disk_usage": f"{disk.percent}%",
            "disk_free": f"{disk.free / 1024 / 1024 / 1024:.1f} GB"
        },
        "process": {
            "pid": process.pid,
            "name": process.name(),
            "memory": f"{process.memory_info().rss / 1024 / 1024:.1f} MB",
            "cpu": f"{process.cpu_percent()}%",
            "threads": process.num_threads(),
            "status": process.status()
        },
        "database": {
            "connected": test_connection(),
            "tables": ["stocks", "stock_daily", "technical_indicators", "users", "user_portfolios"]
        },
        "api": {
            "endpoints": len(app.routes),
            "uptime": "0 minutes",  # 实际应用中应该计算运行时间
            "requests": 0  # 实际应用中应该统计请求数
        }
    }


# 错误处理
@app.exception_handler(404)
async def not_found_handler(request, exc):
    """404错误处理"""
    return {
        "error": "Not Found",
        "message": f"请求的资源 {request.url.path} 不存在",
        "status_code": 404
    }


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """500错误处理"""
    return {
        "error": "Internal Server Error",
        "message": "服务器内部错误，请稍后重试",
        "status_code": 500
    }


# 开发模式运行
if __name__ == "__main__":
    print("🚀 启动 iStock 开发服务器...")
    print("📊 API文档: http://localhost:8000/docs")
    print("🔧 健康检查: http://localhost:8000/health")
    print("💡 按 Ctrl+C 停止服务器")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )