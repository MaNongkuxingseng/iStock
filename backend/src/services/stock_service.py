"""
股票服务
提供股票数据相关的业务逻辑
"""

from typing import List, Optional, Dict, Any
from datetime import date, datetime
from sqlalchemy.orm import Session

from src.database.models import Stock, StockDaily, TechnicalIndicator
from src.database.session import SessionLocal


class StockService:
    """股票服务类"""
    
    def __init__(self, db: Session = None):
        """初始化服务"""
        self.db = db or SessionLocal()
    
    def get_stock_by_id(self, stock_id: int) -> Optional[Stock]:
        """根据ID获取股票"""
        return self.db.query(Stock).filter(Stock.id == stock_id).first()
    
    def get_stock_by_symbol(self, symbol: str) -> Optional[Stock]:
        """根据股票代码获取股票"""
        return self.db.query(Stock).filter(Stock.symbol == symbol).first()
    
    def list_stocks(
        self, 
        skip: int = 0, 
        limit: int = 100,
        market: Optional[str] = None,
        industry: Optional[str] = None
    ) -> List[Stock]:
        """获取股票列表"""
        query = self.db.query(Stock)
        
        if market:
            query = query.filter(Stock.market == market)
        
        if industry:
            query = query.filter(Stock.industry == industry)
        
        return query.offset(skip).limit(limit).all()
    
    def create_stock(self, stock_data: Dict[str, Any]) -> Stock:
        """创建新股票"""
        # 检查是否已存在
        existing = self.get_stock_by_symbol(stock_data.get("symbol", ""))
        if existing:
            raise ValueError(f"Stock with symbol {stock_data['symbol']} already exists")
        
        stock = Stock(**stock_data)
        self.db.add(stock)
        self.db.commit()
        self.db.refresh(stock)
        
        return stock
    
    def update_stock(self, stock_id: int, update_data: Dict[str, Any]) -> Optional[Stock]:
        """更新股票信息"""
        stock = self.get_stock_by_id(stock_id)
        if not stock:
            return None
        
        for key, value in update_data.items():
            if hasattr(stock, key):
                setattr(stock, key, value)
        
        self.db.commit()
        self.db.refresh(stock)
        
        return stock
    
    def delete_stock(self, stock_id: int) -> bool:
        """删除股票"""
        stock = self.get_stock_by_id(stock_id)
        if not stock:
            return False
        
        self.db.delete(stock)
        self.db.commit()
        
        return True
    
    def search_stocks(self, query: str, limit: int = 20) -> List[Stock]:
        """搜索股票"""
        return self.db.query(Stock).filter(
            (Stock.symbol.contains(query)) | (Stock.name.contains(query))
        ).limit(limit).all()
    
    def get_stock_daily_data(
        self, 
        stock_id: int,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        limit: int = 100
    ) -> List[StockDaily]:
        """获取股票日线数据"""
        query = self.db.query(StockDaily).filter(StockDaily.stock_id == stock_id)
        
        if start_date:
            query = query.filter(StockDaily.date >= start_date)
        
        if end_date:
            query = query.filter(StockDaily.date <= end_date)
        
        return query.order_by(StockDaily.date.desc()).limit(limit).all()
    
    def add_daily_data(self, stock_id: int, daily_data: Dict[str, Any]) -> StockDaily:
        """添加日线数据"""
        # 检查是否已存在该日期的数据
        existing = self.db.query(StockDaily).filter(
            StockDaily.stock_id == stock_id,
            StockDaily.date == daily_data.get("date")
        ).first()
        
        if existing:
            # 更新现有数据
            for key, value in daily_data.items():
                if hasattr(existing, key):
                    setattr(existing, key, value)
            
            self.db.commit()
            self.db.refresh(existing)
            return existing
        
        # 创建新数据
        daily_data["stock_id"] = stock_id
        stock_daily = StockDaily(**daily_data)
        
        self.db.add(stock_daily)
        self.db.commit()
        self.db.refresh(stock_daily)
        
        return stock_daily
    
    def get_technical_indicators(
        self,
        stock_daily_id: int
    ) -> Optional[TechnicalIndicator]:
        """获取技术指标"""
        return self.db.query(TechnicalIndicator).filter(
            TechnicalIndicator.stock_daily_id == stock_daily_id
        ).first()
    
    def add_technical_indicator(
        self, 
        stock_daily_id: int, 
        indicator_data: Dict[str, Any]
    ) -> TechnicalIndicator:
        """添加技术指标"""
        # 检查是否已存在
        existing = self.get_technical_indicators(stock_daily_id)
        
        if existing:
            # 更新现有指标
            for key, value in indicator_data.items():
                if hasattr(existing, key):
                    setattr(existing, key, value)
            
            self.db.commit()
            self.db.refresh(existing)
            return existing
        
        # 创建新指标
        indicator_data["stock_daily_id"] = stock_daily_id
        indicator = TechnicalIndicator(**indicator_data)
        
        self.db.add(indicator)
        self.db.commit()
        self.db.refresh(indicator)
        
        return indicator
    
    def calculate_stock_statistics(self, stock_id: int) -> Dict[str, Any]:
        """计算股票统计信息"""
        # 获取最近100天的数据
        daily_data = self.get_stock_daily_data(stock_id, limit=100)
        
        if not daily_data:
            return {
                "stock_id": stock_id,
                "data_points": 0,
                "message": "No daily data available"
            }
        
        # 计算基本统计
        closes = [d.close for d in daily_data]
        volumes = [d.volume for d in daily_data]
        
        avg_close = sum(closes) / len(closes)
        avg_volume = sum(volumes) / len(volumes)
        
        # 计算价格变化
        price_changes = []
        for i in range(1, len(daily_data)):
            change = daily_data[i].close - daily_data[i-1].close
            change_percent = (change / daily_data[i-1].close) * 100
            price_changes.append({
                "date": daily_data[i].date,
                "change": change,
                "change_percent": change_percent
            })
        
        # 最新数据
        latest = daily_data[0]
        
        return {
            "stock_id": stock_id,
            "data_points": len(daily_data),
            "latest_data": {
                "date": latest.date.isoformat() if latest.date else None,
                "close": latest.close,
                "volume": latest.volume,
                "change": latest.change,
                "change_percent": latest.change_percent
            },
            "statistics": {
                "average_close": avg_close,
                "average_volume": avg_volume,
                "max_close": max(closes),
                "min_close": min(closes),
                "max_volume": max(volumes),
                "min_volume": min(volumes)
            },
            "price_changes": price_changes[:10],  # 最近10次变化
            "calculated_at": datetime.utcnow().isoformat()
        }
    
    def batch_create_stocks(self, stocks_data: List[Dict[str, Any]]) -> List[Stock]:
        """批量创建股票"""
        created_stocks = []
        
        for stock_data in stocks_data:
            try:
                # 检查是否已存在
                existing = self.get_stock_by_symbol(stock_data.get("symbol", ""))
                if existing:
                    continue
                
                stock = Stock(**stock_data)
                self.db.add(stock)
                created_stocks.append(stock)
                
            except Exception as e:
                print(f"Error creating stock {stock_data.get('symbol')}: {e}")
                continue
        
        if created_stocks:
            self.db.commit()
            for stock in created_stocks:
                self.db.refresh(stock)
        
        return created_stocks
    
    def get_stock_count_by_market(self) -> Dict[str, int]:
        """按市场统计股票数量"""
        result = self.db.query(
            Stock.market,
            self.db.func.count(Stock.id).label('count')
        ).group_by(Stock.market).all()
        
        return {market: count for market, count in result}
    
    def get_stock_count_by_industry(self) -> Dict[str, int]:
        """按行业统计股票数量"""
        result = self.db.query(
            Stock.industry,
            self.db.func.count(Stock.id).label('count')
        ).filter(Stock.industry.isnot(None)).group_by(Stock.industry).all()
        
        return {industry: count for industry, count in result if industry}
    
    def close(self):
        """关闭数据库会话"""
        if self.db:
            self.db.close()