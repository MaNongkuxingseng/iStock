"""
iStock数据库模型定义
使用SQLAlchemy ORM定义数据表结构
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .session_mysql import Base


class Stock(Base):
    """股票基本信息表"""
    __tablename__ = "stocks"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(10), unique=True, index=True, nullable=False, comment="股票代码")
    name = Column(String(100), nullable=False, comment="股票名称")
    market = Column(String(20), comment="市场(沪/深/创业板等)")
    industry = Column(String(50), comment="行业")
    full_name = Column(String(200), comment="公司全称")
    listing_date = Column(DateTime, comment="上市日期")
    status = Column(String(20), default="active", comment="状态(active/suspended/delisted)")
    
    # 审计字段
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")
    
    # 关系
    daily_data = relationship("StockDaily", back_populates="stock", cascade="all, delete-orphan")
    indicators = relationship("TechnicalIndicator", back_populates="stock", cascade="all, delete-orphan")


class StockDaily(Base):
    """股票日线数据表"""
    __tablename__ = "stock_daily"
    
    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey("stocks.id"), index=True, nullable=False)
    date = Column(DateTime, index=True, nullable=False, comment="交易日期")
    
    # 价格数据
    open_price = Column(Float, comment="开盘价")
    close_price = Column(Float, comment="收盘价")
    high_price = Column(Float, comment="最高价")
    low_price = Column(Float, comment="最低价")
    pre_close = Column(Float, comment="前收盘价")
    
    # 成交量数据
    volume = Column(Integer, comment="成交量(股)")
    amount = Column(Float, comment="成交额(元)")
    
    # 涨跌幅
    change = Column(Float, comment="涨跌额")
    change_percent = Column(Float, comment="涨跌幅(%)")
    
    # 其他指标
    turnover_rate = Column(Float, comment="换手率(%)")
    amplitude = Column(Float, comment="振幅(%)")
    
    # 审计字段
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    stock = relationship("Stock", back_populates="daily_data")
    indicators = relationship("TechnicalIndicator", back_populates="daily_data", cascade="all, delete-orphan")


class TechnicalIndicator(Base):
    """技术指标表"""
    __tablename__ = "technical_indicators"
    
    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey("stocks.id"), index=True, nullable=False)
    daily_id = Column(Integer, ForeignKey("stock_daily.id"), index=True, nullable=False)
    date = Column(DateTime, index=True, nullable=False)
    
    # 移动平均线
    ma5 = Column(Float, comment="5日均线")
    ma10 = Column(Float, comment="10日均线")
    ma20 = Column(Float, comment="20日均线")
    ma30 = Column(Float, comment="30日均线")
    ma60 = Column(Float, comment="60日均线")
    
    # MACD指标
    macd = Column(Float, comment="MACD值")
    macd_signal = Column(Float, comment="MACD信号线")
    macd_histogram = Column(Float, comment="MACD柱状图")
    
    # KDJ指标
    k = Column(Float, comment="K值")
    d = Column(Float, comment="D值")
    j = Column(Float, comment="J值")
    
    # RSI指标
    rsi6 = Column(Float, comment="RSI6")
    rsi12 = Column(Float, comment="RSI12")
    rsi24 = Column(Float, comment="RSI24")
    
    # 布林带
    boll_upper = Column(Float, comment="布林上轨")
    boll_middle = Column(Float, comment="布林中轨")
    boll_lower = Column(Float, comment="布林下轨")
    
    # 成交量指标
    volume_ma5 = Column(Integer, comment="5日成交量均线")
    volume_ma10 = Column(Integer, comment="10日成交量均线")
    
    # 信号标志
    buy_signal = Column(Boolean, default=False, comment="买入信号")
    sell_signal = Column(Boolean, default=False, comment="卖出信号")
    signal_strength = Column(Integer, default=0, comment="信号强度(1-5)")
    
    # 审计字段
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    stock = relationship("Stock", back_populates="indicators")
    daily_data = relationship("StockDaily", back_populates="indicators")


class User(Base):
    """用户表"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False, comment="用户名")
    email = Column(String(100), unique=True, index=True, nullable=False, comment="邮箱")
    hashed_password = Column(String(255), nullable=False, comment="加密密码")
    full_name = Column(String(100), comment="姓名")
    
    # 用户状态
    is_active = Column(Boolean, default=True, comment="是否激活")
    is_superuser = Column(Boolean, default=False, comment="是否超级用户")
    
    # 偏好设置
    notification_enabled = Column(Boolean, default=True, comment="是否启用通知")
    risk_level = Column(String(20), default="medium", comment="风险等级(low/medium/high)")
    
    # 审计字段
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, comment="最后登录时间")
    
    # 关系
    portfolios = relationship("UserPortfolio", back_populates="user", cascade="all, delete-orphan")


class UserPortfolio(Base):
    """用户投资组合表"""
    __tablename__ = "user_portfolios"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    stock_id = Column(Integer, ForeignKey("stocks.id"), index=True, nullable=False)
    
    # 持仓信息
    quantity = Column(Integer, default=0, comment="持仓数量")
    avg_cost = Column(Float, comment="平均成本")
    current_value = Column(Float, comment="当前市值")
    profit_loss = Column(Float, comment="盈亏金额")
    profit_loss_percent = Column(Float, comment="盈亏百分比")
    
    # 交易信息
    first_buy_date = Column(DateTime, comment="首次买入日期")
    last_buy_date = Column(DateTime, comment="最后买入日期")
    last_sell_date = Column(DateTime, comment="最后卖出日期")
    
    # 状态
    is_watching = Column(Boolean, default=True, comment="是否关注")
    target_price = Column(Float, comment="目标价")
    stop_loss_price = Column(Float, comment="止损价")
    
    # 审计字段
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    user = relationship("User", back_populates="portfolios")
    stock = relationship("Stock")


class DataSource(Base):
    """数据源配置表"""
    __tablename__ = "data_sources"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False, comment="数据源名称")
    source_type = Column(String(20), nullable=False, comment="类型(api/file/database)")
    endpoint = Column(String(255), comment="API端点或文件路径")
    api_key = Column(String(255), comment="API密钥")
    
    # 配置
    is_active = Column(Boolean, default=True, comment="是否激活")
    priority = Column(Integer, default=1, comment="优先级(1-10)")
    update_frequency = Column(String(20), default="daily", comment="更新频率")
    
    # 状态
    last_success_time = Column(DateTime, comment="最后成功时间")
    last_error_time = Column(DateTime, comment="最后错误时间")
    error_count = Column(Integer, default=0, comment="错误计数")
    
    # 审计字段
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class DataSyncLog(Base):
    """数据同步日志表"""
    __tablename__ = "data_sync_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer, ForeignKey("data_sources.id"), index=True, nullable=False)
    
    # 同步信息
    sync_type = Column(String(20), nullable=False, comment="同步类型(full/incremental)")
    start_time = Column(DateTime, nullable=False, comment="开始时间")
    end_time = Column(DateTime, comment="结束时间")
    
    # 结果
    status = Column(String(20), nullable=False, comment="状态(success/failed/running)")
    records_fetched = Column(Integer, default=0, comment="获取记录数")
    records_processed = Column(Integer, default=0, comment="处理记录数")
    records_inserted = Column(Integer, default=0, comment="插入记录数")
    records_updated = Column(Integer, default=0, comment="更新记录数")
    
    # 错误信息
    error_message = Column(Text, comment="错误信息")
    stack_trace = Column(Text, comment="堆栈跟踪")
    
    # 审计字段
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    source = relationship("DataSource")


# 创建所有表的函数
def create_all_tables():
    """创建所有数据库表"""
    Base.metadata.create_all(bind=Base.metadata.bind)


if __name__ == "__main__":
    # 测试模型定义
    print("✅ 数据库模型定义完成")
    print(f"表数量: {len(Base.metadata.tables)}")
    for table_name in Base.metadata.tables.keys():
        print(f"  - {table_name}")