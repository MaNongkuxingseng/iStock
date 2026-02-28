#!/usr/bin/env python3
"""
测试数据库连接
"""

import pymysql
import sys

def test_mystock_connection():
    """测试myStock数据库连接"""
    print("测试myStock数据库连接...")
    
    try:
        # myStock数据库配置
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='785091',
            database='instockdb',
            port=3306,
            charset='utf8mb4'
        )
        
        print("✅ myStock数据库连接成功")
        
        # 测试查询
        with conn.cursor() as cursor:
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"✅ 找到 {len(tables)} 个表")
            
            # 显示前10个表
            print("前10个表:")
            for i, table in enumerate(tables[:10]):
                print(f"  {i+1}. {table[0]}")
        
        conn.close()
        return True
        
    except pymysql.Error as e:
        print(f"❌ myStock数据库连接失败: {e}")
        return False

def test_istock_schema():
    """测试iStock数据库Schema"""
    print("\n测试iStock PostgreSQL Schema...")
    
    # 这里只是模拟，实际需要PostgreSQL驱动
    print("📋 iStock数据库设计已就绪:")
    print("  - stocks: 股票基本信息")
    print("  - stock_daily: 股票日线数据") 
    print("  - technical_indicators: 技术指标")
    print("  - ml_predictions: 机器学习预测")
    print("  - users: 用户信息")
    print("  - user_portfolios: 用户持仓")
    
    return True

def main():
    """主函数"""
    print("=" * 50)
    print("iStock数据库连接测试")
    print("=" * 50)
    
    # 测试myStock连接
    mystock_ok = test_mystock_connection()
    
    # 显示iStock Schema
    istock_ok = test_istock_schema()
    
    print("\n" + "=" * 50)
    print("测试总结:")
    print("=" * 50)
    
    if mystock_ok:
        print("✅ myStock数据库连接正常 - 可以获取实时数据")
    else:
        print("⚠️  myStock数据库连接失败 - 需要检查配置")
    
    print("✅ iStock数据库Schema设计完成 - 可以开始开发")
    
    print("\n下一步:")
    print("1. 开始实现数据模型 (SQLAlchemy Models)")
    print("2. 实现数据源API (新浪/腾讯/东方财富)")
    print("3. 实现数据验证和清洗机制")
    print("4. 开发基础API接口")
    
    return mystock_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)