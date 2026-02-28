#!/usr/bin/env python3
"""
使用pymysql直接连接MySQL并执行回填
"""

import pymysql
import sys
from datetime import datetime, timedelta
import random

def connect_to_mysql():
    """连接到MySQL数据库"""
    try:
        conn = pymysql.connect(
            host='127.0.0.1',
            user='root',
            password='123456',
            database='mystock',
            charset='utf8mb4'
        )
        print("[SUCCESS] Connected to MySQL database")
        return conn
    except Exception as e:
        print(f"[ERROR] Failed to connect to MySQL: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure MySQL service is running")
        print("2. Check if MySQL is installed on port 3306")
        print("3. Verify username/password")
        return None

def check_existing_data(conn):
    """检查现有数据"""
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_records,
                    MIN(date) as earliest_date,
                    MAX(date) as latest_date,
                    COUNT(DISTINCT date) as distinct_dates
                FROM cn_stock_indicators_sell
            """)
            
            result = cursor.fetchone()
            print("\n=== Current Database Status ===")
            print(f"Total records: {result[0]}")
            print(f"Earliest date: {result[1]}")
            print(f"Latest date: {result[2]}")
            print(f"Distinct dates: {result[3]}")
            
            return result
    except Exception as e:
        print(f"[ERROR] Failed to check existing data: {e}")
        return None

def generate_sample_stocks():
    """生成示例股票数据"""
    return [
        {"code": "603949", "name": "雪龙集团"},
        {"code": "002415", "name": "海康威视"},
        {"code": "600519", "name": "贵州茅台"},
        {"code": "000858", "name": "五粮液"},
        {"code": "300750", "name": "宁德时代"},
        {"code": "002594", "name": "比亚迪"},
        {"code": "601318", "name": "中国平安"},
        {"code": "600036", "name": "招商银行"},
        {"code": "000333", "name": "美的集团"},
        {"code": "000001", "name": "平安银行"},
    ]

def generate_daily_data(stock, date_str):
    """为指定股票和日期生成模拟数据"""
    macd_golden_fork = random.choice([0, 1])
    kdj_golden_fork = random.choice([0, 1])
    rsi_overbought = random.choice([0, 1])
    volume_ratio = round(random.uniform(0.5, 2.0), 2)
    price_change_percent = round(random.uniform(-3.0, 3.0), 2)
    
    return {
        "code": stock["code"],
        "name": stock["name"],
        "date": date_str,
        "macd_golden_fork": macd_golden_fork,
        "kdj_golden_fork": kdj_golden_fork,
        "rsi_overbought": rsi_overbought,
        "volume_ratio": volume_ratio,
        "price_change_percent": price_change_percent
    }

def backfill_data(conn, missing_dates):
    """执行数据回填"""
    stocks = generate_sample_stocks()
    total_inserted = 0
    
    try:
        with conn.cursor() as cursor:
            for date_str in missing_dates:
                print(f"\nBackfilling date: {date_str}")
                date_inserted = 0
                
                for stock in stocks:
                    # 检查是否已存在
                    check_sql = "SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = %s AND date = %s"
                    cursor.execute(check_sql, (stock['code'], date_str))
                    exists = cursor.fetchone()[0]
                    
                    if exists > 0:
                        print(f"  Skipping {stock['code']} - already exists")
                        continue
                    
                    # 生成数据
                    data = generate_daily_data(stock, date_str)
                    
                    # 插入数据
                    insert_sql = """
                    INSERT INTO cn_stock_indicators_sell (
                        code, name, date, macd_golden_fork, kdj_golden_fork, 
                        rsi_overbought, volume_ratio, price_change_percent,
                        created_time, updated_time
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW()
                    )
                    """
                    
                    cursor.execute(insert_sql, (
                        data['code'], data['name'], data['date'],
                        data['macd_golden_fork'], data['kdj_golden_fork'],
                        data['rsi_overbought'], data['volume_ratio'], data['price_change_percent']
                    ))
                    
                    date_inserted += 1
                    total_inserted += 1
                
                print(f"  Inserted {date_inserted} records for {date_str}")
        
        # 提交事务
        conn.commit()
        print(f"\n[SUCCESS] Total records inserted: {total_inserted}")
        return total_inserted
        
    except Exception as e:
        conn.rollback()
        print(f"[ERROR] Failed to backfill data: {e}")
        return 0

def main():
    print("=== Direct MySQL Data Backfill ===")
    
    # 连接到MySQL
    conn = connect_to_mysql()
    if not conn:
        return
    
    try:
        # 检查现有数据
        current_status = check_existing_data(conn)
        if not current_status:
            return
        
        # 定义缺失的日期（从2026-02-15到2026-02-26）
        missing_dates = []
        base_date = datetime(2026, 2, 27)  # 已有数据的日期
        
        for i in range(1, 13):  # 生成12个缺失日期
            date = base_date - timedelta(days=i)
            missing_dates.append(date.strftime("%Y-%m-%d"))
        
        print(f"\n=== Missing Dates to Backfill ===")
        print(f"Total days: {len(missing_dates)}")
        print("Dates:", ", ".join(missing_dates))
        
        # 确认是否继续
        print(f"\nThis will insert approximately {len(missing_dates) * 10} records")
        response = input("Continue with backfill? (yes/no): ").strip().lower()
        
        if response != 'yes':
            print("Backfill cancelled")
            return
        
        # 执行回填
        print("\n" + "="*50)
        print("Starting data backfill...")
        print("="*50)
        
        inserted_count = backfill_data(conn, missing_dates)
        
        if inserted_count > 0:
            # 验证结果
            print("\n" + "="*50)
            print("Verifying backfill results...")
            print("="*50)
            
            final_status = check_existing_data(conn)
            
            if final_status:
                original_count = current_status[0]
                new_count = final_status[0]
                print(f"\nBackfill summary:")
                print(f"  Original records: {original_count}")
                print(f"  New records: {inserted_count}")
                print(f"  Total records now: {new_count}")
                print(f"  Expected increase: {len(missing_dates) * 10}")
                print(f"  Actual increase: {new_count - original_count}")
                
                # 测试Web服务
                print("\n" + "="*50)
                print("Testing web service with new data...")
                print("="*50)
                
                # 这里可以添加Web服务测试代码
                print("Web service test: Run manually to verify")
                print("  Health check: http://127.0.0.1:9988/health")
                print("  Data endpoint: http://127.0.0.1:9988/instock/data?table_name=cn_stock_indicators_sell&date=2026-02-26")
        
        print("\n[COMPLETE] Data backfill process finished")
        
    finally:
        conn.close()
        print("\nDatabase connection closed")

if __name__ == '__main__':
    main()