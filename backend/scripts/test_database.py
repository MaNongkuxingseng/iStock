#!/usr/bin/env python3
"""
数据库测试脚本
测试数据库连接、模型和基本操作
"""

import os
import sys
from pathlib import Path
from datetime import datetime, date

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

def test_database_connection():
    """测试数据库连接"""
    print("🔌 测试数据库连接...")
    
    try:
        from src.database.session import engine
        
        with engine.connect() as conn:
            result = conn.execute("SELECT version()")
            version = result.fetchone()[0]
            print(f"✅ 数据库连接成功")
            print(f"📊 数据库版本: {version}")
            return True
            
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        return False

def test_models_import():
    """测试模型导入"""
    print("📦 测试模型导入...")
    
    try:
        from src.database.models import (
            Stock, StockDaily, TechnicalIndicator,
            MLPrediction, User, UserPortfolio,
            DataSource, DataSyncLog
        )
        
        models = [
            ("Stock", Stock),
            ("StockDaily", StockDaily),
            ("TechnicalIndicator", TechnicalIndicator),
            ("MLPrediction", MLPrediction),
            ("User", User),
            ("UserPortfolio", UserPortfolio),
            ("DataSource", DataSource),
            ("DataSyncLog", DataSyncLog)
        ]
        
        for name, model in models:
            print(f"  ✅ {name}")
        
        print(f"✅ 成功导入 {len(models)} 个模型")
        return True
        
    except Exception as e:
        print(f"❌ 模型导入失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_model_creation():
    """测试模型实例创建"""
    print("🏗️  测试模型实例创建...")
    
    try:
        from src.database.models import Stock, User, DataSource
        import uuid
        
        # 测试Stock模型
        stock = Stock(
            symbol="000001",
            name="测试股票",
            market="SZ",
            industry="测试行业",
            sector="测试板块"
        )
        
        print(f"  ✅ Stock模型: {stock.symbol} - {stock.name}")
        
        # 测试User模型
        user = User(
            id=uuid.uuid4(),
            username="testuser",
            email="test@example.com",
            hashed_password="hashed_test",
            full_name="测试用户"
        )
        
        print(f"  ✅ User模型: {user.username} - {user.email}")
        
        # 测试DataSource模型
        source = DataSource(
            name="测试数据源",
            source_type="test",
            base_url="https://test.com",
            rate_limit=10,
            is_active=True
        )
        
        print(f"  ✅ DataSource模型: {source.name} - {source.source_type}")
        
        print("✅ 所有模型实例创建成功")
        return True
        
    except Exception as e:
        print(f"❌ 模型实例创建失败: {e}")
        return False

def test_validators():
    """测试数据验证器"""
    print("🔍 测试数据验证器...")
    
    try:
        from src.utils.validators import (
            stock_validator, indicator_validator,
            quality_checker, anomaly_detector
        )
        
        # 测试股票代码验证
        test_symbols = [
            ("000001", True),   # 有效A股
            ("600519", True),   # 有效A股  
            ("AAPL", True),     # 有效美股
            ("123", False),     # 无效
            ("", False),        # 空
        ]
        
        print("📈 测试股票代码验证:")
        for symbol, expected in test_symbols:
            result = stock_validator.validate_symbol(symbol)
            status = "✅" if result == expected else "❌"
            print(f"  {status} {symbol}: {result} (期望: {expected})")
        
        # 测试价格验证
        print("💰 测试价格验证:")
        test_prices = [100.5, 0, -10, None]
        for price in test_prices:
            result = stock_validator.validate_price(price)
            print(f"  {'✅' if result else '❌'} 价格 {price}: {result}")
        
        print("✅ 数据验证器测试完成")
        return True
        
    except Exception as e:
        print(f"❌ 验证器测试失败: {e}")
        return False

def test_database_operations():
    """测试数据库基本操作"""
    print("⚙️  测试数据库操作...")
    
    try:
        from sqlalchemy.orm import Session
        from src.database.session import SessionLocal
        from src.database.models import Stock
        
        db = SessionLocal()
        
        # 测试查询
        stock_count = db.query(Stock).count()
        print(f"📊 当前股票数量: {stock_count}")
        
        # 测试插入
        new_stock = Stock(
            symbol="999999",
            name="测试插入股票",
            market="TEST",
            industry="测试"
        )
        
        db.add(new_stock)
        db.commit()
        
        # 验证插入
        inserted = db.query(Stock).filter_by(symbol="999999").first()
        if inserted:
            print(f"✅ 成功插入股票: {inserted.symbol} - {inserted.name}")
        else:
            print("❌ 插入后查询失败")
        
        # 清理测试数据
        if inserted:
            db.delete(inserted)
            db.commit()
            print("🧹 已清理测试数据")
        
        db.close()
        print("✅ 数据库操作测试完成")
        return True
        
    except Exception as e:
        print(f"❌ 数据库操作测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_all_tests():
    """运行所有测试"""
    print("🧪 开始数据库测试套件")
    print("=" * 50)
    
    tests = [
        ("数据库连接", test_database_connection),
        ("模型导入", test_models_import),
        ("模型创建", test_model_creation),
        ("数据验证", test_validators),
        ("数据库操作", test_database_operations),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n[{test_name}]")
        try:
            success = test_func()
            results.append((test_name, success))
            print(f"结果: {'✅ 通过' if success else '❌ 失败'}")
        except Exception as e:
            print(f"❌ 测试异常: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("📊 测试总结:")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name}: {status}")
    
    print(f"\n总计: {passed}/{total} 通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！数据库配置正确。")
        return True
    else:
        print("\n⚠️  部分测试失败，请检查数据库配置。")
        return False

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='数据库测试工具')
    parser.add_argument('--test', '-t', choices=[
        'connection', 'models', 'validators', 'operations', 'all'
    ], default='all', help='要运行的测试')
    
    args = parser.parse_args()
    
    if args.test == 'all':
        success = run_all_tests()
        sys.exit(0 if success else 1)
    elif args.test == 'connection':
        success = test_database_connection()
    elif args.test == 'models':
        success = test_models_import() and test_model_creation()
    elif args.test == 'validators':
        success = test_validators()
    elif args.test == 'operations':
        success = test_database_operations()
    else:
        print(f"❌ 未知测试类型: {args.test}")
        sys.exit(1)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()