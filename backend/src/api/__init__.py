"""
iStock API 模块
提供股票分析系统的REST API接口
"""

__version__ = "1.0.0"
__author__ = "iStock Team"

from .main import app
from .endpoints import stocks, users, portfolio, data

__all__ = [
    "app",
    "stocks",
    "users", 
    "portfolio",
    "data"
]