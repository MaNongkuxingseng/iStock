#!/usr/bin/env python3
"""
数据库初始化脚本
创建数据库表结构和初始数据
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from src.database.session import engine, Base, init_database
from src.database.models import (
    Stock, StockDaily, TechnicalIndicator, 
    MLPrediction, User, UserPortfolio,
    DataSource, DataSyncLog
)

def create_tables():
    """创建所有数据库表"""
    print("🔧 创建数据库表...")
    
    try:
        # 导入所有模型以确保它们被注册
        from src.database import models
        
        # 创建所有表
        Base.metadata.create_all(bind=engine)
        print("✅ 数据库表创建完成")
        
        # 显示创建的表
        tables = Base.metadata.tables.keys()
        print(f"📊 创建了 {len(tables)} 个表:")
        for i, table_name in enumerate(sorted(tables), 1):
            print(f"  {i}. {table_name}")
        
        return True
        
    except Exception as e:
        print(f"❌ 创建表失败: {e}")
        return False

def seed_initial_data():
    """播种初始数据"""
    print("🌱 播种初始数据...")
    
    try:
        from sqlalchemy.orm import Session
        from src.database.session import SessionLocal
        
        db = SessionLocal()
        
        # 1. 创建数据源
        print("📡 创建数据源...")
        data_sources = [
            DataSource(
                name="新浪财经",
                source_type="sina",
                base_url="https://hq.sinajs.cn",
                rate_limit=10,
                is_active=True
            ),
            DataSource(
                name="腾讯财经", 
                source_type="tencent",
                base_url="https://qt.gtimg.cn",
                rate_limit=10,
                is_active=True
            ),
            DataSource(
                name="东方财富",
                source_type="eastmoney",
                base_url="https://push2.eastmoney.com",
                rate_limit=5,
                is_active=True
            )
        ]
        
        for source in data_sources:
            db.add(source)
        
        db.commit()
        print(f"✅ 创建了 {len(data_sources)} 个数据源")
        
        # 2. 创建示例股票
        print("📈 创建示例股票...")
        sample_stocks = [
            Stock(
                symbol="000001",
                name="平安银行",
                market="SZ",
                industry="银行",
                sector="金融"
            ),
            Stock(
                symbol="600519",
                name="贵州茅台", 
                market="SH",
                industry="白酒",
                sector="食品饮料"
            ),
            Stock(
                symbol="300750",
                name="宁德时代",
                market="SZ",
                industry="新能源",
                sector="电力设备"
            )
        ]
        
        for stock in sample_stocks:
            db.add(stock)
        
        db.commit()
        print(f"✅ 创建了 {len(sample_stocks)} 只示例股票")
        
        # 3. 创建测试用户
        print("👤 创建测试用户...")
        import uuid
        from datetime import datetime
        
        test_user = User(
            id=uuid.uuid4(),
            username="test_user",
            email="test@istock.com",
            hashed_password="hashed_password_placeholder",  # 实际使用中需要加密
            full_name="测试用户",
            is_active=True,
            risk_tolerance="medium"
        )
        
        db.add(test_user)
        db.commit()
        print("✅ 创建了测试用户")
        
        # 4. 创建用户持仓示例
        print("💼 创建用户持仓...")
        if sample_stocks and test_user:
            portfolio = UserPortfolio(
                user_id=test_user.id,
                stock_id=sample_stocks[0].id,
                quantity=100,
                avg_cost=15.50,
                current_price=16.20,
                first_buy_date=datetime.now().date()
            )
            
            db.add(portfolio)
            db.commit()
            print("✅ 创建了用户持仓示例")
        
        db.close()
        print("🎉 初始数据播种完成")
        return True
        
    except Exception as e:
        print(f"❌ 播种数据失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def verify_database():
    """验证数据库结构"""
    print("🔍 验证数据库结构...")
    
    try:
        from sqlalchemy import inspect
        
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        expected_tables = [
            'stocks', 'stock_daily', 'technical_indicators',
            'ml_predictions', 'users', 'user_portfolios',
            'data_sources', 'data_sync_logs'
        ]
        
        print(f"📊 数据库中有 {len(tables)} 个表")
        
        missing_tables = []
        for expected in expected_tables:
            if expected in tables:
                print(f"  ✅ {expected}")
            else:
                print(f"  ❌ {expected} (缺失)")
                missing_tables.append(expected)
        
        if missing_tables:
            print(f"⚠️  缺失 {len(missing_tables)} 个表")
            return False
        else:
            print("✅ 所有表都存在")
            return True
            
    except Exception as e:
        print(f"❌ 验证数据库失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 iStock数据库初始化")
    print("=" * 50)
    
    # 创建表
    if not create_tables():
        print("❌ 数据库表创建失败")
        return
    
    # 验证表结构
    if not verify_database():
        print("❌ 数据库验证失败")
        return
    
    # 播种初始数据
    seed_option = input("是否播种初始数据? (y/N): ").strip().lower()
    if seed_option in ['y', 'yes']:
        if not seed_initial_data():
            print("⚠️  初始数据播种失败，但表结构已创建")
    
    print("=" * 50)
    print("🎉 数据库初始化完成")
    print("\n下一步:")
    print("1. 运行测试: python -m pytest backend/tests/")
    print("2. 启动服务: docker-compose up -d")
    print("3. 访问API: http://localhost:8000/docs")

if __name__ == "__main__":
    main()