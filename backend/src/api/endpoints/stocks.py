"""
股票数据API端点
"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import BaseModel
from datetime import date

from src.database.session import SessionLocal
from src.database.models import Stock, StockDaily, TechnicalIndicator

# 创建路由器
router = APIRouter()

# 数据模型
class StockBase(BaseModel):
    symbol: str
    name: str
    market: str
    industry: Optional[str] = None
    sector: Optional[str] = None

class StockCreate(StockBase):
    pass

class StockResponse(StockBase):
    id: int
    created_at: str
    updated_at: str
    
    class Config:
        from_attributes = True

class StockDailyBase(BaseModel):
    date: date
    open: float
    close: float
    high: float
    low: float
    volume: int
    amount: Optional[float] = None
    change: Optional[float] = None
    change_percent: Optional[float] = None

class StockDailyResponse(StockDailyBase):
    id: int
    stock_id: int
    
    class Config:
        from_attributes = True

class TechnicalIndicatorResponse(BaseModel):
    id: int
    stock_daily_id: int
    ma5: Optional[float] = None
    ma10: Optional[float] = None
    ma20: Optional[float] = None
    ma30: Optional[float] = None
    ma60: Optional[float] = None
    macd: Optional[float] = None
    macd_signal: Optional[float] = None
    macd_histogram: Optional[float] = None
    kdj_k: Optional[float] = None
    kdj_d: Optional[float] = None
    kdj_j: Optional[float] = None
    rsi: Optional[float] = None
    boll_upper: Optional[float] = None
    boll_middle: Optional[float] = None
    boll_lower: Optional[float] = None
    
    class Config:
        from_attributes = True

# 依赖注入：数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 股票列表
@router.get("/", response_model=List[StockResponse])
async def list_stocks(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    market: Optional[str] = None,
    db = Depends(get_db)
):
    """获取股票列表"""
    query = db.query(Stock)
    
    if market:
        query = query.filter(Stock.market == market)
    
    stocks = query.offset(skip).limit(limit).all()
    return stocks

# 获取单个股票
@router.get("/{stock_id}", response_model=StockResponse)
async def get_stock(stock_id: int, db = Depends(get_db)):
    """获取单个股票信息"""
    stock = db.query(Stock).filter(Stock.id == stock_id).first()
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    return stock

# 创建股票
@router.post("/", response_model=StockResponse)
async def create_stock(stock: StockCreate, db = Depends(get_db)):
    """创建新股票"""
    # 检查是否已存在
    existing = db.query(Stock).filter(Stock.symbol == stock.symbol).first()
    if existing:
        raise HTTPException(status_code=400, detail="Stock already exists")
    
    db_stock = Stock(**stock.dict())
    db.add(db_stock)
    db.commit()
    db.refresh(db_stock)
    
    return db_stock

# 更新股票
@router.put("/{stock_id}", response_model=StockResponse)
async def update_stock(stock_id: int, stock_update: StockCreate, db = Depends(get_db)):
    """更新股票信息"""
    db_stock = db.query(Stock).filter(Stock.id == stock_id).first()
    if not db_stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    
    # 更新字段
    for field, value in stock_update.dict().items():
        setattr(db_stock, field, value)
    
    db.commit()
    db.refresh(db_stock)
    
    return db_stock

# 删除股票
@router.delete("/{stock_id}")
async def delete_stock(stock_id: int, db = Depends(get_db)):
    """删除股票"""
    db_stock = db.query(Stock).filter(Stock.id == stock_id).first()
    if not db_stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    
    db.delete(db_stock)
    db.commit()
    
    return {"message": "Stock deleted successfully"}

# 获取股票日线数据
@router.get("/{stock_id}/daily", response_model=List[StockDailyResponse])
async def get_stock_daily(
    stock_id: int,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    limit: int = Query(100, ge=1, le=1000),
    db = Depends(get_db)
):
    """获取股票日线数据"""
    # 验证股票存在
    stock = db.query(Stock).filter(Stock.id == stock_id).first()
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    
    query = db.query(StockDaily).filter(StockDaily.stock_id == stock_id)
    
    if start_date:
        query = query.filter(StockDaily.date >= start_date)
    if end_date:
        query = query.filter(StockDaily.date <= end_date)
    
    daily_data = query.order_by(StockDaily.date.desc()).limit(limit).all()
    return daily_data

# 获取技术指标
@router.get("/{stock_id}/indicators", response_model=List[TechnicalIndicatorResponse])
async def get_technical_indicators(
    stock_id: int,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    limit: int = Query(100, ge=1, le=1000),
    db = Depends(get_db)
):
    """获取股票技术指标"""
    # 验证股票存在
    stock = db.query(Stock).filter(Stock.id == stock_id).first()
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    
    # 获取日线数据ID
    daily_query = db.query(StockDaily).filter(StockDaily.stock_id == stock_id)
    
    if start_date:
        daily_query = daily_query.filter(StockDaily.date >= start_date)
    if end_date:
        daily_query = daily_query.filter(StockDaily.date <= end_date)
    
    daily_ids = [d.id for d in daily_query.order_by(StockDaily.date.desc()).limit(limit).all()]
    
    if not daily_ids:
        return []
    
    # 获取技术指标
    indicators = db.query(TechnicalIndicator).filter(
        TechnicalIndicator.stock_daily_id.in_(daily_ids)
    ).all()
    
    return indicators

# 搜索股票
@router.get("/search/{query}")
async def search_stocks(query: str, db = Depends(get_db)):
    """搜索股票"""
    stocks = db.query(Stock).filter(
        (Stock.symbol.contains(query)) | (Stock.name.contains(query))
    ).limit(20).all()
    
    return stocks

# 批量获取股票
@router.post("/batch")
async def get_stocks_batch(symbols: List[str], db = Depends(get_db)):
    """批量获取股票信息"""
    stocks = db.query(Stock).filter(Stock.symbol.in_(symbols)).all()
    
    result = {}
    for stock in stocks:
        result[stock.symbol] = {
            "id": stock.id,
            "name": stock.name,
            "market": stock.market,
            "industry": stock.industry,
            "sector": stock.sector
        }
    
    return result