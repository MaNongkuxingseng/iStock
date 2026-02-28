"""
iStock本地化运行配置
"""
import os
from pathlib import Path

# 基础配置
DEBUG = True
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# 数据库配置
DATABASE_URL = "sqlite:///./local/istock.db"

# API配置
API_VERSION = "v1"
API_PREFIX = f"/api/{API_VERSION}"

# 股票数据源配置
DATA_SOURCES = {
    'primary': 'sina',  # 新浪财经
    'backup': ['tencent', 'eastmoney'],
    'fallback': 'manual'  # 手动输入
}

# 缓存配置
CACHE_TYPE = 'simple'
CACHE_DEFAULT_TIMEOUT = 300

# 日志配置
LOG_LEVEL = 'INFO'
LOG_FILE = './local/istock.log'

# 本地化运行特性
LOCAL_MODE = True
FAST_STARTUP = True
MINIMAL_DEPS = True