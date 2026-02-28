"""
数据服务
提供数据采集、处理和同步的业务逻辑
"""

from typing import Optional, Dict, Any, List, Tuple
from datetime import datetime, date, timedelta
import asyncio
import aiohttp
import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
import json

from src.database.models import Stock, StockDaily, DataSource, DataSyncLog
from src.database.session import SessionLocal


class DataService:
    """数据服务类"""
    
    def __init__(self, db: Session = None):
        """初始化服务"""
        self.db = db or SessionLocal()
    
    # ==================== 数据源管理 ====================
    
    def get_data_source(self, source_id: int) -> Optional[DataSource]:
        """获取数据源"""
        return self.db.query(DataSource).filter(DataSource.id == source_id).first()
    
    def list_data_sources(self, active_only: bool = True) -> List[DataSource]:
        """获取数据源列表"""
        query = self.db.query(DataSource)
        
        if active_only:
            query = query.filter(DataSource.is_active == True)
        
        return query.order_by(DataSource.name).all()
    
    def create_data_source(self, source_data: Dict[str, Any]) -> DataSource:
        """创建数据源"""
        # 检查是否已存在
        existing = self.db.query(DataSource).filter(
            DataSource.name == source_data.get("name", "")
        ).first()
        
        if existing:
            raise ValueError(f"Data source with name {source_data['name']} already exists")
        
        source = DataSource(**source_data)
        self.db.add(source)
        self.db.commit()
        self.db.refresh(source)
        
        return source
    
    def update_data_source(self, source_id: int, update_data: Dict[str, Any]) -> Optional[DataSource]:
        """更新数据源"""
        source = self.get_data_source(source_id)
        if not source:
            return None
        
        for key, value in update_data.items():
            if hasattr(source, key):
                setattr(source, key, value)
        
        self.db.commit()
        self.db.refresh(source)
        
        return source
    
    # ==================== 股票数据采集 ====================
    
    async def fetch_stock_data(
        self, 
        symbol: str, 
        source_type: str = "sina",
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> Optional[pd.DataFrame]:
        """获取股票数据（模拟）"""
        # 在实际实现中，这里应该调用实际的API
        # 这里返回模拟数据
        
        if start_date is None:
            start_date = date.today() - timedelta(days=30)
        if end_date is None:
            end_date = date.today()
        
        # 生成模拟数据
        dates = pd.date_range(start=start_date, end=end_date, freq='B')
        n_days = len(dates)
        
        # 模拟价格数据
        np.random.seed(hash(symbol) % 10000)
        base_price = 100 + (hash(symbol) % 100)
        returns = np.random.randn(n_days) * 0.02
        
        prices = base_price * (1 + returns).cumprod()
        
        # 创建DataFrame
        df = pd.DataFrame({
            'date': dates,
            'open': prices * (1 + np.random.randn(n_days) * 0.01),
            'high': prices * (1 + np.abs(np.random.randn(n_days)) * 0.015),
            'low': prices * (1 - np.abs(np.random.randn(n_days)) * 0.015),
            'close': prices,
            'volume': np.random.randint(1000000, 10000000, n_days),
            'symbol': symbol
        })
        
        # 计算涨跌幅
        df['change'] = df['close'].diff()
        df['change_percent'] = (df['change'] / df['close'].shift(1)) * 100
        
        return df
    
    async def fetch_realtime_quote(self, symbol: str, source_type: str = "sina") -> Optional[Dict[str, Any]]:
        """获取实时行情（模拟）"""
        # 模拟实时数据
        base_price = 100 + (hash(symbol) % 100)
        change = np.random.randn() * base_price * 0.02
        
        return {
            'symbol': symbol,
            'name': f"股票{symbol}",
            'price': base_price + change,
            'change': change,
            'change_percent': (change / base_price) * 100,
            'open': base_price * (1 + np.random.randn() * 0.01),
            'high': base_price * (1 + np.abs(np.random.randn()) * 0.015),
            'low': base_price * (1 - np.abs(np.random.randn()) * 0.015),
            'volume': np.random.randint(1000000, 10000000),
            'amount': np.random.randint(50000000, 500000000),
            'timestamp': datetime.utcnow().isoformat(),
            'source': source_type
        }
    
    # ==================== 数据存储 ====================
    
    def save_stock_daily_data(self, stock_id: int, daily_data: pd.DataFrame) -> int:
        """保存股票日线数据"""
        saved_count = 0
        
        for _, row in daily_data.iterrows():
            # 检查是否已存在该日期的数据
            existing = self.db.query(StockDaily).filter(
                StockDaily.stock_id == stock_id,
                StockDaily.date == row['date'].date()
            ).first()
            
            if existing:
                # 更新现有数据
                existing.open = float(row['open'])
                existing.high = float(row['high'])
                existing.low = float(row['low'])
                existing.close = float(row['close'])
                existing.volume = int(row['volume'])
                existing.amount = float(row.get('amount', 0))
                existing.change = float(row.get('change', 0))
                existing.change_percent = float(row.get('change_percent', 0))
            else:
                # 创建新数据
                stock_daily = StockDaily(
                    stock_id=stock_id,
                    date=row['date'].date(),
                    open=float(row['open']),
                    high=float(row['high']),
                    low=float(row['low']),
                    close=float(row['close']),
                    volume=int(row['volume']),
                    amount=float(row.get('amount', 0)),
                    change=float(row.get('change', 0)),
                    change_percent=float(row.get('change_percent', 0))
                )
                self.db.add(stock_daily)
            
            saved_count += 1
        
        self.db.commit()
        return saved_count
    
    # ==================== 数据同步 ====================
    
    async def sync_stock_data(
        self, 
        stock_symbol: str,
        source_id: Optional[int] = None,
        sync_type: str = "historical",
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> Dict[str, Any]:
        """同步股票数据"""
        # 创建同步日志
        sync_log = DataSyncLog(
            data_source_id=source_id,
            sync_type=sync_type,
            start_time=datetime.utcnow(),
            status="started",
            records_fetched=0,
            records_processed=0
        )
        
        self.db.add(sync_log)
        self.db.commit()
        self.db.refresh(sync_log)
        
        try:
            # 获取或创建股票记录
            stock = self.db.query(Stock).filter(Stock.symbol == stock_symbol).first()
            if not stock:
                # 创建新的股票记录
                stock = Stock(
                    symbol=stock_symbol,
                    name=f"股票{stock_symbol}",
                    market="SZ" if stock_symbol.startswith("0") else "SH",
                    industry="科技",
                    sector="信息技术"
                )
                self.db.add(stock)
                self.db.commit()
                self.db.refresh(stock)
            
            # 获取数据
            if sync_type == "realtime":
                # 获取实时数据
                quote = await self.fetch_realtime_quote(stock_symbol)
                records_fetched = 1 if quote else 0
                
                # 保存实时数据（在实际实现中可能需要不同的表）
                # 这里暂时只更新日志
                
            else:
                # 获取历史数据
                df = await self.fetch_stock_data(
                    stock_symbol, 
                    start_date=start_date,
                    end_date=end_date
                )
                
                records_fetched = len(df) if df is not None else 0
                
                if df is not None and not df.empty:
                    # 保存数据
                    records_processed = self.save_stock_daily_data(stock.id, df)
                else:
                    records_processed = 0
            
            # 更新同步日志
            sync_log.end_time = datetime.utcnow()
            sync_log.status = "success" if records_fetched > 0 else "partial"
            sync_log.records_fetched = records_fetched
            sync_log.records_processed = records_processed
            
            # 更新数据源的最后同步时间
            if source_id:
                source = self.get_data_source(source_id)
                if source:
                    source.last_sync = datetime.utcnow()
            
            self.db.commit()
            
            return {
                "success": True,
                "sync_log_id": sync_log.id,
                "stock_id": stock.id,
                "records_fetched": records_fetched,
                "records_processed": records_processed,
                "duration_seconds": (sync_log.end_time - sync_log.start_time).total_seconds()
            }
            
        except Exception as e:
            # 更新同步日志为失败
            sync_log.end_time = datetime.utcnow()
            sync_log.status = "failed"
            sync_log.error_message = str(e)
            self.db.commit()
            
            return {
                "success": False,
                "sync_log_id": sync_log.id,
                "error": str(e)
            }
    
    # ==================== 数据统计 ====================
    
    def get_data_statistics(self) -> Dict[str, Any]:
        """获取数据统计信息"""
        # 股票统计
        total_stocks = self.db.query(Stock).count()
        
        # 日线数据统计
        total_daily_records = self.db.query(StockDaily).count()
        
        if total_daily_records > 0:
            latest_record = self.db.query(StockDaily).order_by(
                StockDaily.date.desc()
            ).first()
            latest_date = latest_record.date if latest_record else None
        else:
            latest_date = None
        
        # 数据源统计
        total_sources = self.db.query(DataSource).count()
        active_sources = self.db.query(DataSource).filter(DataSource.is_active == True).count()
        
        # 同步日志统计
        total_syncs = self.db.query(DataSyncLog).count()
        successful_syncs = self.db.query(DataSyncLog).filter(
            DataSyncLog.status == "success"
        ).count()
        
        # 总记录数
        total_fetched = self.db.query(
            self.db.func.sum(DataSyncLog.records_fetched)
        ).scalar() or 0
        
        total_processed = self.db.query(
            self.db.func.sum(DataSyncLog.records_processed)
        ).scalar() or 0
        
        return {
            "stocks": {
                "total": total_stocks,
                "by_market": self._get_stocks_by_market()
            },
            "daily_data": {
                "total_records": total_daily_records,
                "latest_date": latest_date.isoformat() if latest_date else None,
                "records_per_stock": total_daily_records / total_stocks if total_stocks > 0 else 0
            },
            "data_sources": {
                "total": total_sources,
                "active": active_sources
            },
            "sync_operations": {
                "total": total_syncs,
                "successful": successful_syncs,
                "success_rate": (successful_syncs / total_syncs * 100) if total_syncs > 0 else 0
            },
            "records": {
                "total_fetched": total_fetched,
                "total_processed": total_processed,
                "processing_rate": (total_processed / total_fetched * 100) if total_fetched > 0 else 0
            },
            "calculated_at": datetime.utcnow().isoformat()
        }
    
    def _get_stocks_by_market(self) -> Dict[str, int]:
        """按市场统计股票数量"""
        result = self.db.query(
            Stock.market,
            self.db.func.count(Stock.id).label('count')
        ).group_by(Stock.market).all()
        
        return {market: count for market, count in result}
    
    # ==================== 技术指标计算 ====================
    
    def calculate_technical_indicators(self, stock_id: int, days: int = 100) -> pd.DataFrame:
        """计算技术指标"""
        # 获取股票日线数据
        daily_data = self.db.query(StockDaily).filter(
            StockDaily.stock_id == stock_id
        ).order_by(StockDaily.date.desc()).limit(days).all()
        
        if not daily_data:
            return pd.DataFrame()
        
        # 转换为DataFrame
        df = pd.DataFrame([{
            'date': d.date,
            'open': d.open,
            'high': d.high,
            'low': d.low,
            'close': d.close,
            'volume': d.volume
        } for d in daily_data])
        
        df = df.sort_values('date').reset_index(drop=True)
        
        # 计算移动平均线
        df['ma5'] = df['close'].rolling(window=5).mean()
        df['ma10'] = df['close'].rolling(window=10).mean()
        df['ma20'] = df['close'].rolling(window=20).mean()
        df['ma30'] = df['close'].rolling(window=30).mean()
        df['ma60'] = df['close'].rolling(window=60).mean()
        
        # 计算MACD
        exp1 = df['close'].ewm(span=12, adjust=False).mean()
        exp2 = df['close'].ewm(span=26, adjust=False).mean()
        df['macd'] = exp1 - exp2
        df['macd_signal'] = df['macd'].ewm(span=9, adjust=False).mean()
        df['macd_histogram'] = df['macd'] - df['macd_signal']
        
        # 计算RSI
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['rsi'] = 100 - (100 / (1 + rs))
        
        return df
    
    # ==================== 数据清理 ====================
    
    def cleanup_old_data(self, older_than_days: int = 365) -> Dict[str, int]:
        """清理旧数据"""
        cutoff_date = date.today() - timedelta(days=older_than_days)
        
        # 删除旧的日线数据
        deleted_daily = self.db.query(StockDaily).filter(
            StockDaily.date < cutoff_date
        ).delete()
        
        # 删除旧的同步日志
        cutoff_datetime = datetime.utcnow() - timedelta(days=older_than_days * 2)
        deleted_sync_logs = self.db.query(DataSyncLog).filter(
            DataSyncLog.start_time < cutoff_datetime
        ).delete()
        
        self.db.commit()
        
        return {
            "deleted_daily_records": deleted_daily,
            "deleted_sync_logs": deleted_sync_logs,
            "cutoff_date": cutoff_date.isoformat()
        }
    
    def close(self):
        """关闭数据库会话"""
        if self.db:
            self.db.close()