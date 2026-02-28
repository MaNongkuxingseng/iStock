"""
股票数据API
提供股票基本信息、行情数据、技术指标等接口
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from ..database.session_mysql import get_db
from ..database.models import Stock, StockDaily, TechnicalIndicator
from ..schemas.stock_schemas import (
    StockResponse, StockDetailResponse, 
    StockDailyResponse, TechnicalIndicatorResponse,
    StockCreate, StockUpdate
)

router = APIRouter(prefix="/stocks", tags=["stocks"])


@router.get("/", response_model=List[StockResponse])
async def get_stocks(
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(100, ge=1, le=1000, description="返回记录数"),
    symbol: Optional[str] = Query(None, description="股票代码筛选"),
    market: Optional[str] = Query(None, description="市场筛选"),
    industry: Optional[str] = Query(None, description="行业筛选"),
    db: Session = Depends(get_db)
):
    """
    获取股票列表
    - **skip**: 跳过记录数（分页）
    - **limit**: 返回记录数（分页）
    - **symbol**: 按股票代码筛选
    - **market**: 按市场筛选
    - **industry**: 按行业筛选
    """
    query = db.query(Stock)
    
    # 应用筛选条件
    if symbol:
        query = query.filter(Stock.symbol.like(f"%{symbol}%"))
    if market:
        query = query.filter(Stock.market == market)
    if industry:
        query = query.filter(Stock.industry.like(f"%{industry}%"))
    
    # 分页查询
    stocks = query.offset(skip).limit(limit).all()
    return stocks


@router.get("/{symbol}", response_model=StockDetailResponse)
async def get_stock_by_symbol(
    symbol: str,
    db: Session = Depends(get_db)
):
    """
    根据股票代码获取股票详细信息
    - **symbol**: 股票代码（如：000001）
    """
    stock = db.query(Stock).filter(Stock.symbol == symbol).first()
    if not stock:
        raise HTTPException(status_code=404, detail=f"股票 {symbol} 不存在")
    return stock


@router.get("/{symbol}/daily", response_model=List[StockDailyResponse])
async def get_stock_daily_data(
    symbol: str,
    start_date: Optional[str] = Query(None, description="开始日期(YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="结束日期(YYYY-MM-DD)"),
    limit: int = Query(100, ge=1, le=1000, description="返回记录数"),
    db: Session = Depends(get_db)
):
    """
    获取股票日线数据
    - **symbol**: 股票代码
    - **start_date**: 开始日期
    - **end_date**: 结束日期
    - **limit**: 返回记录数
    """
    # 获取股票
    stock = db.query(Stock).filter(Stock.symbol == symbol).first()
    if not stock:
        raise HTTPException(status_code=404, detail=f"股票 {symbol} 不存在")
    
    # 构建查询
    query = db.query(StockDaily).filter(StockDaily.stock_id == stock.id)
    
    # 应用日期筛选
    if start_date:
        try:
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
            query = query.filter(StockDaily.date >= start_dt)
        except ValueError:
            raise HTTPException(status_code=400, detail="开始日期格式错误，请使用YYYY-MM-DD格式")
    
    if end_date:
        try:
            end_dt = datetime.strptime(end_date, "%Y-%m-%d")
            query = query.filter(StockDaily.date <= end_dt)
        except ValueError:
            raise HTTPException(status_code=400, detail="结束日期格式错误，请使用YYYY-MM-DD格式")
    
    # 按日期降序排序并限制数量
    daily_data = query.order_by(StockDaily.date.desc()).limit(limit).all()
    return daily_data


@router.get("/{symbol}/latest", response_model=StockDailyResponse)
async def get_latest_stock_data(
    symbol: str,
    db: Session = Depends(get_db)
):
    """
    获取股票最新行情数据
    - **symbol**: 股票代码
    """
    stock = db.query(Stock).filter(Stock.symbol == symbol).first()
    if not stock:
        raise HTTPException(status_code=404, detail=f"股票 {symbol} 不存在")
    
    latest_data = db.query(StockDaily)\
        .filter(StockDaily.stock_id == stock.id)\
        .order_by(StockDaily.date.desc())\
        .first()
    
    if not latest_data:
        raise HTTPException(status_code=404, detail=f"股票 {symbol} 没有行情数据")
    
    return latest_data


@router.get("/{symbol}/indicators", response_model=List[TechnicalIndicatorResponse])
async def get_stock_indicators(
    symbol: str,
    start_date: Optional[str] = Query(None, description="开始日期(YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="结束日期(YYYY-MM-DD)"),
    limit: int = Query(100, ge=1, le=1000, description="返回记录数"),
    db: Session = Depends(get_db)
):
    """
    获取股票技术指标
    - **symbol**: 股票代码
    - **start_date**: 开始日期
    - **end_date**: 结束日期
    - **limit**: 返回记录数
    """
    stock = db.query(Stock).filter(Stock.symbol == symbol).first()
    if not stock:
        raise HTTPException(status_code=404, detail=f"股票 {symbol} 不存在")
    
    # 构建查询
    query = db.query(TechnicalIndicator).filter(TechnicalIndicator.stock_id == stock.id)
    
    # 应用日期筛选
    if start_date:
        try:
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
            query = query.filter(TechnicalIndicator.date >= start_dt)
        except ValueError:
            raise HTTPException(status_code=400, detail="开始日期格式错误，请使用YYYY-MM-DD格式")
    
    if end_date:
        try:
            end_dt = datetime.strptime(end_date, "%Y-%m-%d")
            query = query.filter(TechnicalIndicator.date <= end_dt)
        except ValueError:
            raise HTTPException(status_code=400, detail="结束日期格式错误，请使用YYYY-MM-DD格式")
    
    # 按日期降序排序并限制数量
    indicators = query.order_by(TechnicalIndicator.date.desc()).limit(limit).all()
    return indicators


@router.get("/{symbol}/signals")
async def get_stock_signals(
    symbol: str,
    signal_type: Optional[str] = Query(None, description="信号类型(buy/sell)"),
    days: int = Query(30, ge=1, le=365, description="查询天数"),
    db: Session = Depends(get_db)
):
    """
    获取股票买卖信号
    - **symbol**: 股票代码
    - **signal_type**: 信号类型(buy/sell)
    - **days**: 查询天数
    """
    stock = db.query(Stock).filter(Stock.symbol == symbol).first()
    if not stock:
        raise HTTPException(status_code=404, detail=f"股票 {symbol} 不存在")
    
    # 计算开始日期
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    # 构建查询
    query = db.query(TechnicalIndicator)\
        .filter(
            TechnicalIndicator.stock_id == stock.id,
            TechnicalIndicator.date >= start_date,
            TechnicalIndicator.date <= end_date
        )
    
    # 应用信号类型筛选
    if signal_type == "buy":
        query = query.filter(TechnicalIndicator.buy_signal == True)
    elif signal_type == "sell":
        query = query.filter(TechnicalIndicator.sell_signal == True)
    
    # 获取信号数据
    signals = query.order_by(TechnicalIndicator.date.desc()).all()
    
    # 统计信息
    buy_signals = [s for s in signals if s.buy_signal]
    sell_signals = [s for s in signals if s.sell_signal]
    
    return {
        "stock": stock.symbol,
        "stock_name": stock.name,
        "period": f"{start_date.date()} 至 {end_date.date()}",
        "total_signals": len(signals),
        "buy_signals": len(buy_signals),
        "sell_signals": len(sell_signals),
        "signals": [
            {
                "date": signal.date,
                "type": "buy" if signal.buy_signal else "sell",
                "strength": signal.signal_strength,
                "indicators": {
                    "macd": signal.macd,
                    "kdj_k": signal.k,
                    "kdj_d": signal.d,
                    "rsi": signal.rsi6
                }
            }
            for signal in signals
        ]
    }


@router.get("/market/overview")
async def get_market_overview(db: Session = Depends(get_db)):
    """
    获取市场概览
    """
    # 获取股票总数
    total_stocks = db.query(Stock).count()
    
    # 获取有最新数据的股票数
    latest_date = db.query(StockDaily.date)\
        .order_by(StockDaily.date.desc())\
        .first()
    
    if latest_date:
        stocks_with_data = db.query(StockDaily.stock_id)\
            .filter(StockDaily.date == latest_date[0])\
            .distinct()\
            .count()
    else:
        stocks_with_data = 0
    
    # 获取买卖信号统计
    buy_signals = db.query(TechnicalIndicator)\
        .filter(
            TechnicalIndicator.buy_signal == True,
            TechnicalIndicator.date >= datetime.now() - timedelta(days=1)
        )\
        .count()
    
    sell_signals = db.query(TechnicalIndicator)\
        .filter(
            TechnicalIndicator.sell_signal == True,
            TechnicalIndicator.date >= datetime.now() - timedelta(days=1)
        )\
        .count()
    
    # 获取行业分布
    industry_dist = db.query(Stock.industry, db.func.count(Stock.id).label("count"))\
        .filter(Stock.industry.isnot(None))\
        .group_by(Stock.industry)\
        .order_by(db.func.count(Stock.id).desc())\
        .limit(10)\
        .all()
    
    return {
        "timestamp": datetime.now(),
        "market_status": "open" if 9 <= datetime.now().hour < 15 else "closed",
        "statistics": {
            "total_stocks": total_stocks,
            "stocks_with_data": stocks_with_data,
            "data_coverage": f"{(stocks_with_data/total_stocks*100):.1f}%" if total_stocks > 0 else "0%",
            "buy_signals_today": buy_signals,
            "sell_signals_today": sell_signals,
            "signal_ratio": f"{buy_signals}:{sell_signals}"
        },
        "industry_distribution": [
            {"industry": industry, "count": count}
            for industry, count in industry_dist
        ]
    }


# 管理接口（需要权限）
@router.post("/", response_model=StockResponse)
async def create_stock(
    stock_data: StockCreate,
    db: Session = Depends(get_db)
):
    """
    创建新股票记录（管理接口）
    """
    # 检查股票是否已存在
    existing_stock = db.query(Stock).filter(Stock.symbol == stock_data.symbol).first()
    if existing_stock:
        raise HTTPException(status_code=400, detail=f"股票 {stock_data.symbol} 已存在")
    
    # 创建新股票
    db_stock = Stock(**stock_data.dict())
    db.add(db_stock)
    db.commit()
    db.refresh(db_stock)
    
    return db_stock


@router.put("/{symbol}", response_model=StockResponse)
async def update_stock(
    symbol: str,
    stock_data: StockUpdate,
    db: Session = Depends(get_db)
):
    """
    更新股票信息（管理接口）
    """
    stock = db.query(Stock).filter(Stock.symbol == symbol).first()
    if not stock:
        raise HTTPException(status_code=404, detail=f"股票 {symbol} 不存在")
    
    # 更新字段
    update_data = stock_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(stock, field, value)
    
    stock.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(stock)
    
    return stock


@router.delete("/{symbol}")
async def delete_stock(
    symbol: str,
    db: Session = Depends(get_db)
):
    """
    删除股票记录（管理接口）
    """
    stock = db.query(Stock).filter(Stock.symbol == symbol).first()
    if not stock:
        raise HTTPException(status_code=404, detail=f"股票 {symbol} 不存在")
    
    db.delete(stock)
    db.commit()
    
    return {"message": f"股票 {symbol} 已删除"}