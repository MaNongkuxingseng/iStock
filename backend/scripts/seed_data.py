#!/usr/bin/env python3
"""
数据库种子数据脚本
为iStock项目创建初始测试数据
"""

import os
import sys
from pathlib import Path
from datetime import datetime, date, timedelta
import random

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

def seed_stocks():
    """创建股票数据"""
    print("📈 创建股票数据...")
    
    try:
        from sqlalchemy.orm import Session
        from src.database.session import SessionLocal
        from src.database.models import Stock
        
        db = SessionLocal()
        
        # 热门A股股票
        popular_stocks = [
            # 金融板块
            {"symbol": "000001", "name": "平安银行", "market": "SZ", "industry": "银行", "sector": "金融"},
            {"symbol": "600036", "name": "招商银行", "market": "SH", "industry": "银行", "sector": "金融"},
            {"symbol": "601318", "name": "中国平安", "market": "SH", "industry": "保险", "sector": "金融"},
            
            # 白酒板块
            {"symbol": "600519", "name": "贵州茅台", "market": "SH", "industry": "白酒", "sector": "食品饮料"},
            {"symbol": "000858", "name": "五粮液", "market": "SZ", "industry": "白酒", "sector": "食品饮料"},
            
            # 新能源板块
            {"symbol": "300750", "name": "宁德时代", "market": "SZ", "industry": "新能源", "sector": "电力设备"},
            {"symbol": "002594", "name": "比亚迪", "market": "SZ", "industry": "新能源汽车", "sector": "汽车"},
            
            # 科技板块
            {"symbol": "000063", "name": "中兴通讯", "market": "SZ", "industry": "通信设备", "sector": "信息技术"},
            {"symbol": "002415", "name": "海康威视", "market": "SZ", "industry": "安防设备", "sector": "信息技术"},
            
            # 医药板块
            {"symbol": "600276", "name": "恒瑞医药", "market": "SH", "industry": "医药制造", "sector": "医药生物"},
            {"symbol": "000538", "name": "云南白药", "market": "SZ", "industry": "中药", "sector": "医药生物"},
            
            # 消费板块
            {"symbol": "000333", "name": "美的集团", "market": "SZ", "industry": "家电", "sector": "家用电器"},
            {"symbol": "000651", "name": "格力电器", "market": "SZ", "industry": "家电", "sector": "家用电器"},
        ]
        
        created_count = 0
        for stock_data in popular_stocks:
            # 检查是否已存在
            existing = db.query(Stock).filter_by(symbol=stock_data["symbol"]).first()
            if not existing:
                stock = Stock(**stock_data)
                db.add(stock)
                created_count += 1
        
        db.commit()
        print(f"✅ 创建了 {created_count} 只股票")
        
        # 显示创建的股票
        stocks = db.query(Stock).all()
        print(f"📊 数据库中共有 {len(stocks)} 只股票")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ 创建股票数据失败: {e}")
        return False

def seed_stock_daily_data():
    """创建股票日线数据"""
    print("📊 创建股票日线数据...")
    
    try:
        from sqlalchemy.orm import Session
        from src.database.session import SessionLocal
        from src.database.models import Stock, StockDaily
        
        db = SessionLocal()
        
        # 获取所有股票
        stocks = db.query(Stock).all()
        if not stocks:
            print("⚠️  没有股票数据，跳过日线数据创建")
            return True
        
        # 创建最近30天的日线数据
        end_date = date.today()
        start_date = end_date - timedelta(days=30)
        
        created_count = 0
        for stock in stocks:
            current_date = start_date
            base_price = random.uniform(10, 100)  # 随机基础价格
            
            while current_date <= end_date:
                # 跳过周末
                if current_date.weekday() < 5:  # 0-4是周一到周五
                    # 检查是否已存在
                    existing = db.query(StockDaily).filter_by(
                        stock_id=stock.id,
                        date=current_date
                    ).first()
                    
                    if not existing:
                        # 生成随机价格数据
                        open_price = base_price + random.uniform(-2, 2)
                        close_price = open_price + random.uniform(-5, 5)
                        high_price = max(open_price, close_price) + random.uniform(0, 3)
                        low_price = min(open_price, close_price) - random.uniform(0, 3)
                        volume = random.randint(1000000, 10000000)
                        
                        daily_data = StockDaily(
                            stock_id=stock.id,
                            date=current_date,
                            open=open_price,
                            close=close_price,
                            high=high_price,
                            low=low_price,
                            volume=volume,
                            amount=volume * close_price,
                            change=close_price - open_price,
                            change_percent=(close_price - open_price) / open_price * 100 if open_price != 0 else 0
                        )
                        
                        db.add(daily_data)
                        created_count += 1
                
                current_date += timedelta(days=1)
        
        db.commit()
        print(f"✅ 创建了 {created_count} 条日线数据记录")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ 创建日线数据失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def seed_technical_indicators():
    """创建技术指标数据"""
    print("📊 创建技术指标数据...")
    
    try:
        from sqlalchemy.orm import Session
        from src.database.session import SessionLocal
        from src.database.models import StockDaily, TechnicalIndicator
        
        db = SessionLocal()
        
        # 获取最近的日线数据
        recent_daily = db.query(StockDaily).order_by(StockDaily.date.desc()).limit(100).all()
        
        if not recent_daily:
            print("⚠️  没有日线数据，跳过技术指标创建")
            return True
        
        created_count = 0
        for daily in recent_daily:
            # 检查是否已存在
            existing = db.query(TechnicalIndicator).filter_by(
                stock_daily_id=daily.id
            ).first()
            
            if not existing:
                # 生成随机技术指标
                indicator = TechnicalIndicator(
                    stock_daily_id=daily.id,
                    ma5=daily.close + random.uniform(-2, 2),
                    ma10=daily.close + random.uniform(-3, 3),
                    ma20=daily.close + random.uniform(-4, 4),
                    ma30=daily.close + random.uniform(-5, 5),
                    ma60=daily.close + random.uniform(-6, 6),
                    macd=random.uniform(-1, 1),
                    macd_signal=random.uniform(-0.5, 0.5),
                    macd_histogram=random.uniform(-0.3, 0.3),
                    kdj_k=random.uniform(0, 100),
                    kdj_d=random.uniform(0, 100),
                    kdj_j=random.uniform(0, 100),
                    rsi=random.uniform(30, 70),
                    boll_upper=daily.close + random.uniform(2, 5),
                    boll_middle=daily.close,
                    boll_lower=daily.close - random.uniform(2, 5),
                    volume_ma5=random.uniform(0.8, 1.2) * daily.volume,
                    volume_ma10=random.uniform(0.7, 1.3) * daily.volume
                )
                
                db.add(indicator)
                created_count += 1
        
        db.commit()
        print(f"✅ 创建了 {created_count} 条技术指标记录")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ 创建技术指标失败: {e}")
        return False

def seed_users():
    """创建用户数据"""
    print("👤 创建用户数据...")
    
    try:
        from sqlalchemy.orm import Session
        from src.database.session import SessionLocal
        from src.database.models import User
        import uuid
        
        db = SessionLocal()
        
        # 测试用户
        test_users = [
            {
                "username": "investor1",
                "email": "investor1@example.com",
                "hashed_password": "hashed_password_1",
                "full_name": "投资者一号",
                "risk_tolerance": "high",
                "investment_experience": "expert"
            },
            {
                "username": "investor2", 
                "email": "investor2@example.com",
                "hashed_password": "hashed_password_2",
                "full_name": "投资者二号",
                "risk_tolerance": "medium",
                "investment_experience": "intermediate"
            },
            {
                "username": "beginner",
                "email": "beginner@example.com",
                "hashed_password": "hashed_password_3",
                "full_name": "新手投资者",
                "risk_tolerance": "low",
                "investment_experience": "beginner"
            }
        ]
        
        created_count = 0
        for user_data in test_users:
            # 检查是否已存在
            existing = db.query(User).filter_by(username=user_data["username"]).first()
            if not existing:
                user = User(
                    id=uuid.uuid4(),
                    **user_data
                )
                db.add(user)
                created_count += 1
        
        db.commit()
        print(f"✅ 创建了 {created_count} 个用户")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ 创建用户数据失败: {e}")
        return False

def seed_user_portfolios():
    """创建用户持仓数据"""
    print("💼 创建用户持仓数据...")
    
    try:
        from sqlalchemy.orm import Session
        from src.database.session import SessionLocal
        from src.database.models import User, Stock, UserPortfolio
        
        db = SessionLocal()
        
        # 获取用户和股票
        users = db.query(User).all()
        stocks = db.query(Stock).limit(5).all()  # 取前5只股票
        
        if not users or not stocks:
            print("⚠️  没有用户或股票数据，跳过持仓创建")
            return True
        
        created_count = 0
        for user in users:
            for stock in stocks[:2]:  # 每个用户持有2只股票
                # 检查是否已存在
                existing = db.query(UserPortfolio).filter_by(
                    user_id=user.id,
                    stock_id=stock.id
                ).first()
                
                if not existing:
                    portfolio = UserPortfolio(
                        user_id=user.id,
                        stock_id=stock.id,
                        quantity=random.randint(100, 1000),
                        avg_cost=random.uniform(10, 50),
                        current_price=random.uniform(15, 60),
                        first_buy_date=date.today() - timedelta(days=random.randint(30, 365))
                    )
                    
                    db.add(portfolio)
                    created_count += 1
        
        db.commit()
        print(f"✅ 创建了 {created_count} 条持仓记录")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ 创建用户持仓失败: {e}")
        return False

def seed_ml_predictions():
    """创建机器学习预测数据"""
    print("🤖 创建机器学习预测数据...")
    
    try:
        from sqlalchemy.orm import Session
        from src.database.session import SessionLocal
        from src.database.models import Stock, MLPrediction
        
        db = SessionLocal()
        
        # 获取股票
        stocks = db.query(Stock).limit(3).all()  # 取前3只股票
        
        if not stocks:
            print("⚠️  没有股票数据，跳过预测数据创建")
            return True
        
        created_count = 0
        for stock in stocks:
            # 创建未来5天的预测
            for days_ahead in range(1, 6):
                prediction_date = date.today() + timedelta(days=days_ahead)
                
                # 检查是否已存在
                existing = db.query(MLPrediction).filter_by(
                    stock_id=stock.id,
                    prediction_date=prediction_date
                ).first()
                
                if not existing:
                    prediction = MLPrediction(
                        stock_id=stock.id,
                        prediction_date=prediction_date,
                        predicted_price=random.uniform(50, 150),
                        confidence=random.uniform(0.6, 0.95),
                        model_name="lstm_predictor",
                        model_version="1.0.0",
                        features_used=["price", "volume", "technical_indicators"],
                        prediction_type="price_forecast"
                    )
                    
                    db.add(prediction)
                    created_count += 1
        
        db.commit()
        print(f"✅ 创建了 {created_count} 条预测记录")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ 创建预测数据失败: {e}")
        return False

def seed_all_data():
    """播种所有数据"""
    print("🚀 开始播种所有初始数据")
    print("=" * 50)
    
    seed_functions = [
        ("股票数据", seed_stocks),
        ("股票日线数据", seed_stock_daily_data),
        ("技术指标数据", seed_technical_indicators),
        ("用户数据", seed_users),
        ("用户持仓数据", seed_user_portfolios),
        ("机器学习预测数据", seed_ml_predictions),
    ]
    
    results = []
    for name, func in seed_functions:
        print(f"\n[{name}]")
        try:
            success = func()
            results.append((name, success))
            print(f"结果: {'✅ 成功' if success else '❌ 失败'}")
        except Exception as e:
            print(f"❌ 播种异常: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 50)
    print("📊 播种总结:")
    print("=" * 50)
    
    successful = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ 成功" if result else "❌ 失败"
        print(f"{name}: {status}")
    
    print(f"\n总计: {successful}/{total} 成功")
    
    if successful == total:
        print("\n🎉 所有数据播种完成！")
        return True
    else:
        print("\n⚠️  部分数据播种失败，但系统仍可运行。")
        return False

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='数据库种子数据工具')
    parser.add_argument('--data', '-d', choices=[
        'stocks', 'daily', 'indicators', 'users', 
        'portfolios', 'predictions', 'all'
    ], default='all', help='要播种的数据类型')
    
    args = parser.parse_args()
    
    if args.data == 'all':
        success = seed_all_data()
    elif args.data == 'stocks':
        success = seed_stocks()
    elif args.data == 'daily':
        success = seed_stock_daily_data()
    elif args.data == 'indicators':
        success = seed_technical_indicators()
    elif args.data == 'users':
        success = seed_users()
    elif args.data == 'portfolios':
        success = seed_user_portfolios()
    elif args.data == 'predictions':
        success = seed_ml_predictions()
    else:
        print(f"❌ 未知数据类型: {args.data}")
        sys.exit(1)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()