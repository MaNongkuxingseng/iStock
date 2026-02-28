"""
数据验证规则
"""

import re
from datetime import datetime, date
from typing import Optional, Any, Dict, List
from decimal import Decimal


class StockValidator:
    """股票数据验证器"""
    
    @staticmethod
    def validate_symbol(symbol: str) -> bool:
        """
        验证股票代码格式
        
        Args:
            symbol: 股票代码
            
        Returns:
            bool: 是否有效
        """
        if not symbol or not isinstance(symbol, str):
            return False
        
        # 中国A股: 6位数字
        if re.match(r'^(00|30|60|68|83|87)\d{4}$', symbol):
            return True
        
        # 港股: 4-5位数字
        if re.match(r'^\d{4,5}$', symbol):
            return True
        
        # 美股: 1-5位字母
        if re.match(r'^[A-Z]{1,5}$', symbol):
            return True
        
        return False
    
    @staticmethod
    def validate_market(market: str) -> bool:
        """
        验证市场代码
        
        Args:
            market: 市场代码
            
        Returns:
            bool: 是否有效
        """
        valid_markets = {'SH', 'SZ', 'BJ', 'HK', 'US', 'SS', 'SZSE'}
        return market in valid_markets
    
    @staticmethod
    def validate_price(price: Any) -> bool:
        """
        验证价格
        
        Args:
            price: 价格值
            
        Returns:
            bool: 是否有效
        """
        try:
            if price is None:
                return True  # 允许为空
            
            price_val = Decimal(str(price))
            return price_val >= 0
        except:
            return False
    
    @staticmethod
    def validate_volume(volume: Any) -> bool:
        """
        验证成交量
        
        Args:
            volume: 成交量
            
        Returns:
            bool: 是否有效
        """
        try:
            if volume is None:
                return True  # 允许为空
            
            volume_val = int(volume)
            return volume_val >= 0
        except:
            return False
    
    @staticmethod
    def validate_date_range(start_date: date, end_date: date) -> bool:
        """
        验证日期范围
        
        Args:
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            bool: 是否有效
        """
        return start_date <= end_date


class TechnicalIndicatorValidator:
    """技术指标验证器"""
    
    @staticmethod
    def validate_ma_value(value: Any) -> bool:
        """
        验证移动平均线值
        
        Args:
            value: MA值
            
        Returns:
            bool: 是否有效
        """
        try:
            if value is None:
                return True  # 允许为空
            
            val = Decimal(str(value))
            return val >= 0
        except:
            return False
    
    @staticmethod
    def validate_rsi_value(value: Any) -> bool:
        """
        验证RSI值
        
        Args:
            value: RSI值
            
        Returns:
            bool: 是否有效
        """
        try:
            if value is None:
                return True  # 允许为空
            
            val = Decimal(str(value))
            return 0 <= val <= 100
        except:
            return False
    
    @staticmethod
    def validate_macd_value(value: Any) -> bool:
        """
        验证MACD值
        
        Args:
            value: MACD值
            
        Returns:
            bool: 是否有效
        """
        try:
            if value is None:
                return True  # 允许为空
            
            val = Decimal(str(value))
            return True  # MACD可以为负
        except:
            return False


class DataQualityChecker:
    """数据质量检查器"""
    
    @staticmethod
    def check_stock_data_completeness(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        检查股票数据完整性
        
        Args:
            data: 股票数据
            
        Returns:
            Dict: 检查结果
        """
        required_fields = ['symbol', 'name', 'market']
        missing_fields = []
        
        for field in required_fields:
            if field not in data or not data[field]:
                missing_fields.append(field)
        
        completeness_score = 1.0 - (len(missing_fields) / len(required_fields))
        
        return {
            'is_complete': len(missing_fields) == 0,
            'missing_fields': missing_fields,
            'completeness_score': completeness_score,
            'total_fields': len(required_fields),
            'present_fields': len(required_fields) - len(missing_fields)
        }
    
    @staticmethod
    def check_daily_data_consistency(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        检查日线数据一致性
        
        Args:
            data: 日线数据
            
        Returns:
            Dict: 检查结果
        """
        issues = []
        
        # 检查价格关系
        if all(key in data for key in ['open', 'high', 'low', 'close']):
            try:
                open_price = Decimal(str(data['open']))
                high_price = Decimal(str(data['high']))
                low_price = Decimal(str(data['low']))
                close_price = Decimal(str(data['close']))
                
                if high_price < low_price:
                    issues.append('high_price < low_price')
                if high_price < open_price:
                    issues.append('high_price < open_price')
                if high_price < close_price:
                    issues.append('high_price < close_price')
                if low_price > open_price:
                    issues.append('low_price > open_price')
                if low_price > close_price:
                    issues.append('low_price > close_price')
                    
            except:
                issues.append('price_conversion_error')
        
        # 检查成交量
        if 'volume' in data and data['volume']:
            try:
                volume = int(data['volume'])
                if volume < 0:
                    issues.append('negative_volume')
            except:
                issues.append('volume_conversion_error')
        
        consistency_score = 1.0 - (len(issues) / 10)  # 假设最多10个问题
        
        return {
            'is_consistent': len(issues) == 0,
            'issues': issues,
            'consistency_score': consistency_score,
            'total_checks': 10,
            'passed_checks': 10 - len(issues)
        }
    
    @staticmethod
    def check_data_freshness(last_update: datetime, threshold_hours: int = 24) -> Dict[str, Any]:
        """
        检查数据新鲜度
        
        Args:
            last_update: 最后更新时间
            threshold_hours: 阈值小时数
            
        Returns:
            Dict: 检查结果
        """
        now = datetime.now()
        hours_since_update = (now - last_update).total_seconds() / 3600
        
        is_fresh = hours_since_update <= threshold_hours
        freshness_score = max(0, 1.0 - (hours_since_update / (threshold_hours * 2)))
        
        return {
            'is_fresh': is_fresh,
            'hours_since_update': hours_since_update,
            'freshness_score': freshness_score,
            'threshold_hours': threshold_hours
        }


class DataAnomalyDetector:
    """数据异常检测器"""
    
    @staticmethod
    def detect_price_anomalies(prices: List[Decimal], threshold: float = 0.1) -> List[Dict[str, Any]]:
        """
        检测价格异常
        
        Args:
            prices: 价格序列
            threshold: 异常阈值（百分比）
            
        Returns:
            List: 异常点列表
        """
        anomalies = []
        
        if len(prices) < 2:
            return anomalies
        
        for i in range(1, len(prices)):
            prev_price = prices[i-1]
            curr_price = prices[i]
            
            if prev_price == 0:
                continue
                
            change_percent = abs((curr_price - prev_price) / prev_price)
            
            if change_percent > threshold:
                anomalies.append({
                    'index': i,
                    'price': curr_price,
                    'prev_price': prev_price,
                    'change_percent': change_percent,
                    'threshold': threshold,
                    'type': 'price_spike'
                })
        
        return anomalies
    
    @staticmethod
    def detect_volume_anomalies(volumes: List[int], threshold: float = 3.0) -> List[Dict[str, Any]]:
        """
        检测成交量异常
        
        Args:
            volumes: 成交量序列
            threshold: 异常阈值（倍数）
            
        Returns:
            List: 异常点列表
        """
        anomalies = []
        
        if len(volumes) < 10:
            return anomalies
        
        # 计算移动平均
        ma_volume = sum(volumes[-10:]) / 10
        
        for i, volume in enumerate(volumes[-5:]):  # 检查最近5天
            if ma_volume > 0 and volume > ma_volume * threshold:
                anomalies.append({
                    'index': len(volumes) - 5 + i,
                    'volume': volume,
                    'ma_volume': ma_volume,
                    'ratio': volume / ma_volume,
                    'threshold': threshold,
                    'type': 'volume_spike'
                })
        
        return anomalies
    
    @staticmethod
    def detect_missing_data_dates(expected_dates: List[date], actual_dates: List[date]) -> List[date]:
        """
        检测缺失数据日期
        
        Args:
            expected_dates: 预期日期列表
            actual_dates: 实际日期列表
            
        Returns:
            List: 缺失日期列表
        """
        actual_set = set(actual_dates)
        missing_dates = [d for d in expected_dates if d not in actual_set]
        return missing_dates


# 验证器实例
stock_validator = StockValidator()
indicator_validator = TechnicalIndicatorValidator()
quality_checker = DataQualityChecker()
anomaly_detector = DataAnomalyDetector()