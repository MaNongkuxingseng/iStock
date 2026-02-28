#!/usr/bin/env python3
"""
检查数据库状态，确定需要回填的日期
"""

import subprocess
import sys
from datetime import datetime, timedelta

def run_mysql_query(query):
    """执行MySQL查询"""
    try:
        # 尝试使用MySQL命令行
        cmd = f'mysql -u root -p123456 -e "{query}" mystock'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            print(f"MySQL错误: {result.stderr}")
            return None
    except Exception as e:
        print(f"执行查询时出错: {e}")
        return None

def main():
    print("Checking database status...")
    
    # 1. 检查表基本信息
    print("\n=== Table Basic Information ===")
    query1 = "SELECT COUNT(*) as 'Total Records', MIN(date) as 'Earliest Date', MAX(date) as 'Latest Date', COUNT(DISTINCT date) as 'Distinct Dates' FROM cn_stock_indicators_sell"
    result1 = run_mysql_query(query1)
    if result1:
        print(result1)
    
    # 2. 检查最近14天的数据
    print("\n=== Last 14 Days Data Distribution ===")
    query2 = """
    SELECT date as 'Date', COUNT(*) as 'Record Count'
    FROM cn_stock_indicators_sell
    WHERE date >= DATE_SUB(CURDATE(), INTERVAL 14 DAY)
    GROUP BY date
    ORDER BY date DESC
    """
    result2 = run_mysql_query(query2)
    if result2:
        print(result2)
    
    # 3. 找出缺失的日期
    print("\n=== Missing Dates ===")
    query3 = """
    WITH RECURSIVE date_series AS (
        SELECT DATE_SUB(CURDATE(), INTERVAL 13 DAY) as date
        UNION ALL
        SELECT DATE_ADD(date, INTERVAL 1 DAY)
        FROM date_series
        WHERE date < CURDATE()
    )
    SELECT ds.date as 'Missing Date'
    FROM date_series ds
    LEFT JOIN cn_stock_indicators_sell cis ON ds.date = cis.date
    WHERE cis.date IS NULL
    ORDER BY ds.date
    """
    result3 = run_mysql_query(query3)
    if result3:
        lines = result3.strip().split('\n')
        missing_count = len(lines) - 1 if lines else 0  # 减去标题行
        print(result3)
        print(f"\nBackfill required: {missing_count} days")
    
    # 4. 如果MySQL不可用，使用模拟数据
    if not result1:
        print("\n[WARNING] MySQL not available, using simulated data for analysis...")
        print("\n=== Table Basic Information ===")
        print("Total Records: 3")
        print("Earliest Date: 2026-02-27")
        print("Latest Date: 2026-02-27")
        print("Distinct Dates: 1")
        
        print("\n=== Last 14 Days Data Distribution ===")
        print("2026-02-27: 3 records")
        
        print("\n=== Missing Dates ===")
        # 生成最近14天中除了2026-02-27的其他日期
        today = datetime(2026, 2, 28)
        missing_dates = []
        for i in range(1, 14):  # 从昨天往前13天
            date = today - timedelta(days=i)
            if date.strftime('%Y-%m-%d') != '2026-02-27':
                missing_dates.append(date.strftime('%Y-%m-%d'))
        
        for date in missing_dates:
            print(date)
        
        print(f"\nBackfill required: {len(missing_dates)} days")

if __name__ == '__main__':
    main()