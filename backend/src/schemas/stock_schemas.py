"""
股票数据模式定义
使用Pydantic定义API请求和响应模式
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# 基础模式
class StockBase(BaseModel):
    symbol: str = Field(..., description="股票代码", example="000001")
    name: str = Field(..., description="股票名称", example="平安银行")
    market: Optional[str] = Field(None, description="市场", example="深交所")
    industry: Optional[str] = Field(None, description="行业", example="银行")


# 创建请求
class StockCreate(StockBase):
    full_name: Optional[str] = Field(None, description="公司全称", example="平安银行股份有限公司")
    listing_date: Optional[datetime] = Field(None, description="上市日期")


# 更新请求
class StockUpdate(BaseModel):
    name: Optional[str] = Field(None, description="股票名称")
    market: Optional[str] = Field(None, description="市场")
    industry: Optional[str] = Field(None, description="行业")
    full_name: Optional[str] = Field(None, description="公司全称")
    status: Optional[str] = Field(None, description="状态")


# 响应模式
class StockResponse(StockBase):
    id: int
    status: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class StockDetailResponse(StockResponse):
    full_name: Optional[str]
    listing_date: Optional[datetime]


# 日线数据模式
class StockDailyBase(BaseModel):
    date: datetime = Field(..., description="交易日期")
    open_price: Optional[float] = Field(None, description="开盘价", ge=0)
    close_price: Optional[float] = Field(None, description="收盘价", ge=0)
    high_price: Optional[float] = Field(None, description="最高价", ge=0)
    low_price: Optional[float] = Field(None, description="最低价", ge=0)
    pre_close: Optional[float] = Field(None, description="前收盘价", ge=0)
    volume: Optional[int] = Field(None, description="成交量", ge=0)
    amount: Optional[float] = Field(None, description="成交额", ge=0)
    change: Optional[float] = Field(None, description="涨跌额")
    change_percent: Optional[float] = Field(None, description="涨跌幅(%)")
    turnover_rate: Optional[float] = Field(None, description="换手率(%)", ge=0, le=100)
    amplitude: Optional[float] = Field(None, description="振幅(%)", ge=0)


class StockDailyResponse(StockDailyBase):
    id: int
    stock_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# 技术指标模式
class TechnicalIndicatorBase(BaseModel):
    date: datetime = Field(..., description="日期")
    
    # 移动平均线
    ma5: Optional[float] = Field(None, description="5日均线")
    ma10: Optional[float] = Field(None, description="10日均线")
    ma20: Optional[float] = Field(None, description="20日均线")
    ma30: Optional[float] = Field(None, description="30日均线")
    ma60: Optional[float] = Field(None, description="60日均线")
    
    # MACD指标
    macd: Optional[float] = Field(None, description="MACD值")
    macd_signal: Optional[float] = Field(None, description="MACD信号线")
    macd_histogram: Optional[float] = Field(None, description="MACD柱状图")
    
    # KDJ指标
    k: Optional[float] = Field(None, description="K值", ge=0, le=100)
    d: Optional[float] = Field(None, description="D值", ge=0, le=100)
    j: Optional[float] = Field(None, description="J值")
    
    # RSI指标
    rsi6: Optional[float] = Field(None, description="RSI6", ge=0, le=100)
    rsi12: Optional[float] = Field(None, description="RSI12", ge=0, le=100)
    rsi24: Optional[float] = Field(None, description="RSI24", ge=0, le=100)
    
    # 布林带
    boll_upper: Optional[float] = Field(None, description="布林上轨")
    boll_middle: Optional[float] = Field(None, description="布林中轨")
    boll_lower: Optional[float] = Field(None, description="布林下轨")
    
    # 成交量指标
    volume_ma5: Optional[int] = Field(None, description="5日成交量均线", ge=0)
    volume_ma10: Optional[int] = Field(None, description="10日成交量均线", ge=0)
    
    # 信号标志
    buy_signal: Optional[bool] = Field(False, description="买入信号")
    sell_signal: Optional[bool] = Field(False, description="卖出信号")
    signal_strength: Optional[int] = Field(0, description="信号强度", ge=0, le=5)


class TechnicalIndicatorResponse(TechnicalIndicatorBase):
    id: int
    stock_id: int
    daily_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# 市场概览模式
class MarketOverviewResponse(BaseModel):
    timestamp: datetime
    market_status: str
    statistics: dict
    industry_distribution: List[dict]


# 信号响应模式
class SignalResponse(BaseModel):
    stock: str
    stock_name: str
    period: str
    total_signals: int
    buy_signals: int
    sell_signals: int
    signals: List[dict]


# 批量操作模式
class BatchStockCreate(BaseModel):
    stocks: List[StockCreate]


class BatchStockResponse(BaseModel):
    created: int
    failed: int
    details: List[dict]


# 搜索模式
class StockSearchResponse(BaseModel):
    query: str
    results: List[StockResponse]
    total: int
    page: int
    page_size: int


# 导入导出模式
class StockImportRequest(BaseModel):
    data: List[dict]
    source: str
    overwrite: bool = False


class StockExportRequest(BaseModel):
    symbols: Optional[List[str]] = None
    market: Optional[str] = None
    industry: Optional[str] = None
    format: str = "json"  # json, csv, excel


# 统计分析模式
class StockStatisticsResponse(BaseModel):
    symbol: str
    name: str
    period_start: datetime
    period_end: datetime
    statistics: dict
    indicators: dict


# 价格预测模式
class PricePredictionRequest(BaseModel):
    symbol: str
    days: int = Field(30, ge=1, le=365, description="预测天数")
    model: str = "arima"  # arima, lstm, prophet


class PricePredictionResponse(BaseModel):
    symbol: str
    name: str
    model: str
    predictions: List[dict]
    confidence: float
    metrics: dict