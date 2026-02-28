"""
投资组合管理API端点
"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel
from datetime import date, datetime
import uuid

from src.database.session import SessionLocal
from src.database.models import UserPortfolio, Stock, User

# 创建路由器
router = APIRouter()

# 数据模型
class PortfolioItemBase(BaseModel):
    stock_id: int
    quantity: int
    avg_cost: float
    current_price: Optional[float] = None
    first_buy_date: Optional[date] = None

class PortfolioItemCreate(PortfolioItemBase):
    pass

class PortfolioItemResponse(PortfolioItemBase):
    id: int
    user_id: uuid.UUID
    market_value: Optional[float] = None
    profit_loss: Optional[float] = None
    profit_loss_percent: Optional[float] = None
    last_update: str
    
    class Config:
        from_attributes = True

class PortfolioItemUpdate(BaseModel):
    quantity: Optional[int] = None
    avg_cost: Optional[float] = None
    current_price: Optional[float] = None

class PortfolioSummary(BaseModel):
    total_value: float
    total_cost: float
    total_profit_loss: float
    total_profit_loss_percent: float
    item_count: int
    last_updated: str

# 依赖注入：数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 获取用户持仓列表
@router.get("/{user_id}/items", response_model=List[PortfolioItemResponse])
async def get_portfolio_items(
    user_id: uuid.UUID,
    db = Depends(get_db)
):
    """获取用户持仓列表"""
    # 验证用户存在
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    portfolio_items = db.query(UserPortfolio).filter(
        UserPortfolio.user_id == user_id
    ).all()
    
    return portfolio_items

# 获取单个持仓项
@router.get("/{user_id}/items/{stock_id}", response_model=PortfolioItemResponse)
async def get_portfolio_item(
    user_id: uuid.UUID,
    stock_id: int,
    db = Depends(get_db)
):
    """获取单个持仓项"""
    # 验证用户存在
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # 验证股票存在
    stock = db.query(Stock).filter(Stock.id == stock_id).first()
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    
    portfolio_item = db.query(UserPortfolio).filter(
        UserPortfolio.user_id == user_id,
        UserPortfolio.stock_id == stock_id
    ).first()
    
    if not portfolio_item:
        raise HTTPException(status_code=404, detail="Portfolio item not found")
    
    return portfolio_item

# 添加持仓
@router.post("/{user_id}/items", response_model=PortfolioItemResponse)
async def add_portfolio_item(
    user_id: uuid.UUID,
    item: PortfolioItemCreate,
    db = Depends(get_db)
):
    """添加持仓项"""
    # 验证用户存在
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # 验证股票存在
    stock = db.query(Stock).filter(Stock.id == item.stock_id).first()
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    
    # 检查是否已存在
    existing = db.query(UserPortfolio).filter(
        UserPortfolio.user_id == user_id,
        UserPortfolio.stock_id == item.stock_id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Portfolio item already exists")
    
    # 创建持仓项
    portfolio_item = UserPortfolio(
        user_id=user_id,
        stock_id=item.stock_id,
        quantity=item.quantity,
        avg_cost=item.avg_cost,
        current_price=item.current_price or 0,
        first_buy_date=item.first_buy_date or date.today()
    )
    
    db.add(portfolio_item)
    db.commit()
    db.refresh(portfolio_item)
    
    return portfolio_item

# 更新持仓
@router.put("/{user_id}/items/{stock_id}", response_model=PortfolioItemResponse)
async def update_portfolio_item(
    user_id: uuid.UUID,
    stock_id: int,
    item_update: PortfolioItemUpdate,
    db = Depends(get_db)
):
    """更新持仓项"""
    # 验证用户存在
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # 验证股票存在
    stock = db.query(Stock).filter(Stock.id == stock_id).first()
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    
    portfolio_item = db.query(UserPortfolio).filter(
        UserPortfolio.user_id == user_id,
        UserPortfolio.stock_id == stock_id
    ).first()
    
    if not portfolio_item:
        raise HTTPException(status_code=404, detail="Portfolio item not found")
    
    # 更新字段
    update_data = item_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(portfolio_item, field, value)
    
    portfolio_item.last_update = datetime.utcnow()
    
    db.commit()
    db.refresh(portfolio_item)
    
    return portfolio_item

# 删除持仓
@router.delete("/{user_id}/items/{stock_id}")
async def delete_portfolio_item(
    user_id: uuid.UUID,
    stock_id: int,
    db = Depends(get_db)
):
    """删除持仓项"""
    # 验证用户存在
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    portfolio_item = db.query(UserPortfolio).filter(
        UserPortfolio.user_id == user_id,
        UserPortfolio.stock_id == stock_id
    ).first()
    
    if not portfolio_item:
        raise HTTPException(status_code=404, detail="Portfolio item not found")
    
    db.delete(portfolio_item)
    db.commit()
    
    return {"message": "Portfolio item deleted successfully"}

# 获取投资组合摘要
@router.get("/{user_id}/summary", response_model=PortfolioSummary)
async def get_portfolio_summary(
    user_id: uuid.UUID,
    db = Depends(get_db)
):
    """获取投资组合摘要"""
    # 验证用户存在
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    portfolio_items = db.query(UserPortfolio).filter(
        UserPortfolio.user_id == user_id
    ).all()
    
    if not portfolio_items:
        return PortfolioSummary(
            total_value=0,
            total_cost=0,
            total_profit_loss=0,
            total_profit_loss_percent=0,
            item_count=0,
            last_updated=datetime.utcnow().isoformat()
        )
    
    total_value = sum(item.market_value or 0 for item in portfolio_items)
    total_cost = sum(item.quantity * item.avg_cost for item in portfolio_items)
    total_profit_loss = sum(item.profit_loss or 0 for item in portfolio_items)
    
    total_profit_loss_percent = 0
    if total_cost > 0:
        total_profit_loss_percent = (total_profit_loss / total_cost) * 100
    
    # 获取最新更新时间
    last_update = max(
        (item.last_update for item in portfolio_items if item.last_update),
        default=datetime.utcnow()
    )
    
    return PortfolioSummary(
        total_value=total_value,
        total_cost=total_cost,
        total_profit_loss=total_profit_loss,
        total_profit_loss_percent=total_profit_loss_percent,
        item_count=len(portfolio_items),
        last_updated=last_update.isoformat()
    )

# 批量更新持仓价格
@router.post("/{user_id}/update-prices")
async def update_portfolio_prices(
    user_id: uuid.UUID,
    price_updates: dict,  # {stock_id: current_price}
    db = Depends(get_db)
):
    """批量更新持仓价格"""
    # 验证用户存在
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    updated_count = 0
    for stock_id_str, current_price in price_updates.items():
        try:
            stock_id = int(stock_id_str)
            current_price_float = float(current_price)
            
            portfolio_item = db.query(UserPortfolio).filter(
                UserPortfolio.user_id == user_id,
                UserPortfolio.stock_id == stock_id
            ).first()
            
            if portfolio_item:
                portfolio_item.current_price = current_price_float
                portfolio_item.last_update = datetime.utcnow()
                updated_count += 1
                
        except (ValueError, TypeError):
            continue
    
    if updated_count > 0:
        db.commit()
    
    return {
        "message": f"Updated prices for {updated_count} portfolio items",
        "updated_count": updated_count
    }

# 获取持仓详情（包含股票信息）
@router.get("/{user_id}/details")
async def get_portfolio_details(
    user_id: uuid.UUID,
    db = Depends(get_db)
):
    """获取持仓详情（包含股票信息）"""
    # 验证用户存在
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # 查询持仓项并连接股票信息
    portfolio_details = db.query(
        UserPortfolio, Stock
    ).join(
        Stock, UserPortfolio.stock_id == Stock.id
    ).filter(
        UserPortfolio.user_id == user_id
    ).all()
    
    result = []
    for portfolio_item, stock in portfolio_details:
        result.append({
            "portfolio_item": {
                "id": portfolio_item.id,
                "quantity": portfolio_item.quantity,
                "avg_cost": portfolio_item.avg_cost,
                "current_price": portfolio_item.current_price,
                "market_value": portfolio_item.market_value,
                "profit_loss": portfolio_item.profit_loss,
                "profit_loss_percent": portfolio_item.profit_loss_percent,
                "first_buy_date": portfolio_item.first_buy_date.isoformat() if portfolio_item.first_buy_date else None,
                "last_update": portfolio_item.last_update.isoformat() if portfolio_item.last_update else None
            },
            "stock": {
                "id": stock.id,
                "symbol": stock.symbol,
                "name": stock.name,
                "market": stock.market,
                "industry": stock.industry,
                "sector": stock.sector
            }
        })
    
    return result

# 清空投资组合
@router.delete("/{user_id}/clear")
async def clear_portfolio(
    user_id: uuid.UUID,
    confirm: bool = Query(False, description="必须设置为true以确认清空"),
    db = Depends(get_db)
):
    """清空投资组合（危险操作）"""
    if not confirm:
        raise HTTPException(
            status_code=400, 
            detail="必须设置confirm=true以确认清空操作"
        )
    
    # 验证用户存在
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # 删除所有持仓项
    deleted_count = db.query(UserPortfolio).filter(
        UserPortfolio.user_id == user_id
    ).delete()
    
    db.commit()
    
    return {
        "message": f"Portfolio cleared successfully",
        "deleted_items": deleted_count
    }