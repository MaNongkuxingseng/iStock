"""
投资组合服务
提供投资组合管理和分析的业务逻辑
"""

from typing import Optional, Dict, Any, List, Tuple
from datetime import datetime, date
import uuid
from sqlalchemy.orm import Session
import pandas as pd
import numpy as np

from src.database.models import UserPortfolio, Stock, StockDaily, User
from src.database.session import SessionLocal


class PortfolioService:
    """投资组合服务类"""
    
    def __init__(self, db: Session = None):
        """初始化服务"""
        self.db = db or SessionLocal()
    
    # ==================== 投资组合项管理 ====================
    
    def get_portfolio_item(self, user_id: uuid.UUID, stock_id: int) -> Optional[UserPortfolio]:
        """获取投资组合项"""
        return self.db.query(UserPortfolio).filter(
            UserPortfolio.user_id == user_id,
            UserPortfolio.stock_id == stock_id
        ).first()
    
    def get_portfolio_item_by_id(self, item_id: int) -> Optional[UserPortfolio]:
        """根据ID获取投资组合项"""
        return self.db.query(UserPortfolio).filter(UserPortfolio.id == item_id).first()
    
    def list_portfolio_items(self, user_id: uuid.UUID) -> List[UserPortfolio]:
        """获取用户的所有投资组合项"""
        return self.db.query(UserPortfolio).filter(
            UserPortfolio.user_id == user_id
        ).all()
    
    def add_portfolio_item(self, user_id: uuid.UUID, item_data: Dict[str, Any]) -> UserPortfolio:
        """添加投资组合项"""
        # 检查是否已存在
        existing = self.get_portfolio_item(user_id, item_data.get("stock_id"))
        if existing:
            raise ValueError(f"Portfolio item for stock {item_data['stock_id']} already exists")
        
        # 验证股票存在
        stock = self.db.query(Stock).filter(Stock.id == item_data.get("stock_id")).first()
        if not stock:
            raise ValueError(f"Stock {item_data['stock_id']} not found")
        
        # 设置默认值
        item_data.setdefault("user_id", user_id)
        item_data.setdefault("first_buy_date", date.today())
        item_data.setdefault("current_price", 0)
        
        portfolio_item = UserPortfolio(**item_data)
        self.db.add(portfolio_item)
        self.db.commit()
        self.db.refresh(portfolio_item)
        
        # 更新计算字段
        self._update_portfolio_item_calculations(portfolio_item)
        
        return portfolio_item
    
    def update_portfolio_item(
        self, 
        user_id: uuid.UUID, 
        stock_id: int, 
        update_data: Dict[str, Any]
    ) -> Optional[UserPortfolio]:
        """更新投资组合项"""
        portfolio_item = self.get_portfolio_item(user_id, stock_id)
        if not portfolio_item:
            return None
        
        # 不允许更新某些字段
        restricted_fields = ["id", "user_id", "stock_id", "first_buy_date"]
        for field in restricted_fields:
            update_data.pop(field, None)
        
        # 更新字段
        for key, value in update_data.items():
            if hasattr(portfolio_item, key):
                setattr(portfolio_item, key, value)
        
        portfolio_item.last_update = datetime.utcnow()
        self.db.commit()
        
        # 更新计算字段
        self._update_portfolio_item_calculations(portfolio_item)
        
        return portfolio_item
    
    def delete_portfolio_item(self, user_id: uuid.UUID, stock_id: int) -> bool:
        """删除投资组合项"""
        portfolio_item = self.get_portfolio_item(user_id, stock_id)
        if not portfolio_item:
            return False
        
        self.db.delete(portfolio_item)
        self.db.commit()
        
        return True
    
    def _update_portfolio_item_calculations(self, portfolio_item: UserPortfolio) -> None:
        """更新投资组合项的计算字段"""
        if portfolio_item.current_price > 0 and portfolio_item.quantity > 0:
            # 计算市值
            portfolio_item.market_value = portfolio_item.current_price * portfolio_item.quantity
            
            # 计算成本
            total_cost = portfolio_item.avg_cost * portfolio_item.quantity
            
            # 计算盈亏
            portfolio_item.profit_loss = portfolio_item.market_value - total_cost
            
            # 计算盈亏百分比
            if total_cost > 0:
                portfolio_item.profit_loss_percent = (portfolio_item.profit_loss / total_cost) * 100
            else:
                portfolio_item.profit_loss_percent = 0
        
        self.db.commit()
    
    # ==================== 投资组合分析 ====================
    
    def get_portfolio_summary(self, user_id: uuid.UUID) -> Dict[str, Any]:
        """获取投资组合摘要"""
        portfolio_items = self.list_portfolio_items(user_id)
        
        if not portfolio_items:
            return self._get_empty_portfolio_summary()
        
        # 计算汇总统计
        total_value = 0
        total_cost = 0
        total_profit_loss = 0
        item_count = len(portfolio_items)
        
        for item in portfolio_items:
            if item.market_value:
                total_value += item.market_value
            
            item_cost = item.avg_cost * item.quantity
            total_cost += item_cost
            
            if item.profit_loss:
                total_profit_loss += item.profit_loss
        
        # 计算总盈亏百分比
        total_profit_loss_percent = 0
        if total_cost > 0:
            total_profit_loss_percent = (total_profit_loss / total_cost) * 100
        
        # 获取最新更新时间
        last_update = max(
            (item.last_update for item in portfolio_items if item.last_update),
            default=datetime.utcnow()
        )
        
        # 按行业分布
        industry_distribution = self._get_industry_distribution(portfolio_items)
        
        # 按市场分布
        market_distribution = self._get_market_distribution(portfolio_items)
        
        # 表现最好的和最差的股票
        best_performers = self._get_best_performers(portfolio_items, limit=3)
        worst_performers = self._get_worst_performers(portfolio_items, limit=3)
        
        return {
            "user_id": str(user_id),
            "summary": {
                "total_value": total_value,
                "total_cost": total_cost,
                "total_profit_loss": total_profit_loss,
                "total_profit_loss_percent": total_profit_loss_percent,
                "item_count": item_count,
                "last_updated": last_update.isoformat()
            },
            "distribution": {
                "by_industry": industry_distribution,
                "by_market": market_distribution
            },
            "performance": {
                "best_performers": best_performers,
                "worst_performers": worst_performers
            },
            "calculated_at": datetime.utcnow().isoformat()
        }
    
    def _get_empty_portfolio_summary(self) -> Dict[str, Any]:
        """获取空投资组合的摘要"""
        return {
            "summary": {
                "total_value": 0,
                "total_cost": 0,
                "total_profit_loss": 0,
                "total_profit_loss_percent": 0,
                "item_count": 0,
                "last_updated": datetime.utcnow().isoformat()
            },
            "distribution": {
                "by_industry": {},
                "by_market": {}
            },
            "performance": {
                "best_performers": [],
                "worst_performers": []
            },
            "calculated_at": datetime.utcnow().isoformat()
        }
    
    def _get_industry_distribution(self, portfolio_items: List[UserPortfolio]) -> Dict[str, float]:
        """获取行业分布"""
        industry_values = {}
        
        for item in portfolio_items:
            if item.market_value:
                # 获取股票信息
                stock = self.db.query(Stock).filter(Stock.id == item.stock_id).first()
                if stock and stock.industry:
                    industry = stock.industry
                    industry_values[industry] = industry_values.get(industry, 0) + item.market_value
        
        # 计算百分比
        total_value = sum(industry_values.values())
        if total_value > 0:
            return {industry: (value / total_value * 100) for industry, value in industry_values.items()}
        
        return {}
    
    def _get_market_distribution(self, portfolio_items: List[UserPortfolio]) -> Dict[str, float]:
        """获取市场分布"""
        market_values = {}
        
        for item in portfolio_items:
            if item.market_value:
                # 获取股票信息
                stock = self.db.query(Stock).filter(Stock.id == item.stock_id).first()
                if stock and stock.market:
                    market = stock.market
                    market_values[market] = market_values.get(market, 0) + item.market_value
        
        # 计算百分比
        total_value = sum(market_values.values())
        if total_value > 0:
            return {market: (value / total_value * 100) for market, value in market_values.items()}
        
        return {}
    
    def _get_best_performers(self, portfolio_items: List[UserPortfolio], limit: int = 3) -> List[Dict[str, Any]]:
        """获取表现最好的股票"""
        performers = []
        
        for item in portfolio_items:
            if item.profit_loss_percent is not None:
                # 获取股票信息
                stock = self.db.query(Stock).filter(Stock.id == item.stock_id).first()
                if stock:
                    performers.append({
                        "stock_id": item.stock_id,
                        "symbol": stock.symbol,
                        "name": stock.name,
                        "profit_loss_percent": item.profit_loss_percent,
                        "profit_loss": item.profit_loss,
                        "market_value": item.market_value
                    })
        
        # 按盈亏百分比排序（降序）
        performers.sort(key=lambda x: x["profit_loss_percent"], reverse=True)
        
        return performers[:limit]
    
    def _get_worst_performers(self, portfolio_items: List[UserPortfolio], limit: int = 3) -> List[Dict[str, Any]]:
        """获取表现最差的股票"""
        performers = []
        
        for item in portfolio_items:
            if item.profit_loss_percent is not None:
                # 获取股票信息
                stock = self.db.query(Stock).filter(Stock.id == item.stock_id).first()
                if stock:
                    performers.append({
                        "stock_id": item.stock_id,
                        "symbol": stock.symbol,
                        "name": stock.name,
                        "profit_loss_percent": item.profit_loss_percent,
                        "profit_loss": item.profit_loss,
                        "market_value": item.market_value
                    })
        
        # 按盈亏百分比排序（升序）
        performers.sort(key=lambda x: x["profit_loss_percent"])
        
        return performers[:limit]
    
    # ==================== 投资组合详情 ====================
    
    def get_portfolio_details(self, user_id: uuid.UUID) -> List[Dict[str, Any]]:
        """获取投资组合详情（包含股票信息）"""
        portfolio_items = self.list_portfolio_items(user_id)
        
        details = []
        for item in portfolio_items:
            # 获取股票信息
            stock = self.db.query(Stock).filter(Stock.id == item.stock_id).first()
            if stock:
                details.append({
                    "portfolio_item": {
                        "id": item.id,
                        "quantity": item.quantity,
                        "avg_cost": item.avg_cost,
                        "current_price": item.current_price,
                        "market_value": item.market_value,
                        "profit_loss": item.profit_loss,
                        "profit_loss_percent": item.profit_loss_percent,
                        "first_buy_date": item.first_buy_date.isoformat() if item.first_buy_date else None,
                        "last_update": item.last_update.isoformat() if item.last_update else None
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
        
        return details
    
    # ==================== 价格更新 ====================
    
    def update_portfolio_prices(
        self, 
        user_id: uuid.UUID, 
        price_updates: Dict[int, float]
    ) -> Dict[str, Any]:
        """批量更新投资组合价格"""
        updated_count = 0
        
        for stock_id, current_price in price_updates.items():
            portfolio_item = self.get_portfolio_item(user_id, stock_id)
            
            if portfolio_item:
                portfolio_item.current_price = current_price
                portfolio_item.last_update = datetime.utcnow()
                
                # 更新计算字段
                self._update_portfolio_item_calculations(portfolio_item)
                
                updated_count += 1
        
        if updated_count > 0:
            self.db.commit()
        
        return {
            "user_id": str(user_id),
            "updated_items": updated_count,
            "total_items": len(price_updates),
            "updated_at": datetime.utcnow().isoformat()
        }
    
    async def update_all_portfolio_prices(self, user_id: uuid.UUID) -> Dict[str, Any]:
        """更新所有投资组合项的价格"""
        portfolio_items = self.list_portfolio_items(user_id)
        
        if not portfolio_items:
            return {
                "user_id": str(user_id),
                "updated_items": 0,
                "total_items": 0,
                "message": "No portfolio items found"
            }
        
        # 在实际实现中，这里应该调用实时行情API
        # 这里使用模拟价格更新
        
        price_updates = {}
        for item in portfolio_items:
            # 获取股票信息
            stock = self.db.query(Stock).filter(Stock.id == item.stock_id).first()
            if stock:
                # 模拟价格变化（±5%）
                current_price = item.current_price or item.avg_cost
                change_percent = (np.random.rand() - 0.5) * 0.1  # ±5%
                new_price = current_price * (1 + change_percent)
                
                price_updates[item.stock_id] = round(new_price, 2)
        
        # 批量更新价格
        result = self.update_portfolio_prices(user_id, price_updates)
        
        return result
    
    # ==================== 投资组合分析报告 ====================
    
    def generate_portfolio_report(self, user_id: uuid.UUID) -> Dict[str, Any]:
        """生成投资组合分析报告"""
        portfolio_summary = self.get_portfolio_summary(user_id)
        portfolio_details = self.get_portfolio_details(user_id)
        
        # 风险分析
        risk_analysis = self._analyze_portfolio_risk(portfolio_details)
        
        # 多样化分析
        diversification_analysis = self._analyze_diversification(portfolio_details)
        
        # 表现分析
        performance_analysis = self._analyze_performance(portfolio_details)
        
        return {
            "report_id": str(uuid.uuid4()),
            "user_id": str(user_id),
            "generated_at": datetime.utcnow().isoformat(),
            "summary": portfolio_summary["summary"],
            "risk_analysis": risk_analysis,
            "diversification_analysis": diversification_analysis,
            "performance_analysis": performance_analysis,
            "recommendations": self._generate_recommendations(
                portfolio_summary, 
                risk_analysis, 
                diversification_analysis
            )
        }
    
    def _analyze_portfolio_risk(self, portfolio_details: List[Dict[str, Any]]) -> Dict[str, Any]:
        """分析投资组合风险"""
        if not portfolio_details:
            return {"message": "No portfolio items to analyze"}
        
        # 计算波动率（模拟）
        total_volatility = 0
        high_risk_items = []
        
        for detail in portfolio_details:
            item = detail["portfolio_item"]
            stock = detail["stock"]
            
            # 模拟波动率计算
            volatility = np.random.rand() * 0.3  # 0-30% 波动率
            total_volatility += volatility * (item["market_value"] or 0)
            
            if volatility > 0.2:  # 高波动率
                high_risk_items.append({
                    "symbol": stock["symbol"],
                    "name": stock["name"],
                    "volatility": round(volatility * 100, 2),
                    "market_value": item["market_value"]
                })
        
        # 计算平均波动率
        total_value = sum(d["portfolio_item"]["market_value"] or 0 for d in portfolio_details)
        avg_volatility = (total_volatility / total_value * 100) if total_value > 0 else 0
        
        # 风险评估
        risk_level = "低"
        if avg_volatility > 20:
            risk_level = "高"
        elif avg_volatility > 10:
            risk_level = "中"
        
        return {
            "average_volatility": round(avg_volatility, 2),
            "risk_level": risk_level,
            "high_risk_items": high_risk_items[:5],  # 最多显示5个高风险项
            "analysis_date": datetime.utcnow().isoformat()
        }
    
    def _analyze_diversification(self, portfolio_details: List[Dict[str, Any]]) -> Dict[str, Any]:
        """分析投资组合多样化"""
        if not portfolio_details:
            return {"message": "No portfolio items to analyze"}
        
        # 行业分布
        industry_dist = {}
        market_dist = {}
        
        for detail in portfolio_details:
            item = detail["portfolio_item"]
            stock = detail["stock"]
            
            industry = stock["industry"] or "未知"
            market = stock["market"] or "未知"
            
            industry_dist[industry] = industry_dist.get(industry, 0) + (item["market_value"] or 0)
            market_dist[market] = market_dist.get(market, 0) + (item["market_value"] or 0)
        
