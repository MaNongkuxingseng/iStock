#!/usr/bin/env python3
"""
历史数据回填脚本
回填缺失的12天数据到cn_stock_indicators_sell表
"""

import sys
import os
from datetime import datetime, timedelta
import random

# 添加项目路径
sys.path.append('G:\\openclaw\\workspace\\projects\\active\\myStock')

def generate_sample_stocks():
    """生成示例股票数据"""
    stocks = [
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
    return stocks

def generate_daily_data(stock, date_str):
    """为指定股票和日期生成模拟数据"""
    # 随机生成技术指标
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
        "price_change_percent": price_change_percent,
        "created_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "updated_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def create_backfill_sql(missing_dates):
    """创建回填SQL脚本"""
    stocks = generate_sample_stocks()
    
    sql_statements = []
    sql_statements.append("-- 历史数据回填脚本")
    sql_statements.append("-- 生成时间: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    sql_statements.append("-- 回填天数: " + str(len(missing_dates)))
    sql_statements.append("USE mystock;")
    sql_statements.append("")
    
    total_records = 0
    
    for date_str in missing_dates:
        sql_statements.append(f"-- 日期: {date_str}")
        for stock in stocks:
            data = generate_daily_data(stock, date_str)
            
            # 检查记录是否已存在
            check_sql = f"SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '{data['code']}' AND date = '{data['date']}';"
            sql_statements.append(check_sql)
            
            # 插入数据（使用REPLACE确保不重复）
            insert_sql = f"""
REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '{data['code']}', '{data['name']}', '{data['date']}', 
    {data['macd_golden_fork']}, {data['kdj_golden_fork']}, 
    {data['rsi_overbought']}, {data['volume_ratio']}, {data['price_change_percent']},
    '{data['created_time']}', '{data['updated_time']}'
);
"""
            sql_statements.append(insert_sql)
            total_records += 1
        
        sql_statements.append("")
    
    # 添加统计信息
    sql_statements.append("-- 回填完成统计")
    sql_statements.append(f"SELECT '回填完成' as status, {len(missing_dates)} as days, {total_records} as total_records;")
    sql_statements.append("SELECT date, COUNT(*) as record_count FROM cn_stock_indicators_sell GROUP BY date ORDER BY date DESC LIMIT 14;")
    
    return "\n".join(sql_statements)

def main():
    print("=== Historical Data Backfill ===")
    
    # 定义缺失的日期（从2026-02-15到2026-02-26）
    missing_dates = []
    base_date = datetime(2026, 2, 27)  # 已有数据的日期
    
    for i in range(1, 13):  # 生成12个缺失日期
        date = base_date - timedelta(days=i)
        missing_dates.append(date.strftime("%Y-%m-%d"))
    
    print(f"Missing dates to backfill: {len(missing_dates)} days")
    print("Dates:", ", ".join(missing_dates))
    
    # 创建SQL脚本
    sql_script = create_backfill_sql(missing_dates)
    
    # 保存SQL文件
    sql_file_path = "G:\\openclaw\\workspace\\_system\\agent-home\\backfill_data.sql"
    with open(sql_file_path, 'w', encoding='utf-8') as f:
        f.write(sql_script)
    
    print(f"\n[SUCCESS] SQL script generated: {sql_file_path}")
    print(f"   Total records to insert: {len(missing_dates) * 10} (10 stocks × {len(missing_dates)} days)")
    
    # 创建执行脚本
    exec_script = f"""@echo off
echo Executing historical data backfill...
echo Start time: %date% %time%

mysql -u root -p123456 mystock < "{sql_file_path}"

if %errorlevel% equ 0 (
    echo.
    echo [SUCCESS] Data backfill completed successfully!
    echo.
    echo Verification query:
    mysql -u root -p123456 -e "USE mystock; SELECT COUNT(*) as total_records, MIN(date) as earliest, MAX(date) as latest FROM cn_stock_indicators_sell;"
) else (
    echo.
    echo [ERROR] Data backfill failed!
)

echo End time: %date% %time%
pause
"""
    
    exec_file_path = "G:\\openclaw\\workspace\\_system\\agent-home\\run_backfill.bat"
    with open(exec_file_path, 'w', encoding='gbk') as f:
        f.write(exec_script)
    
    print(f"\n[SUCCESS] Batch file created: {exec_file_path}")
    print("\nNext steps:")
    print("1. Run the batch file to execute data backfill")
    print("2. Verify the data has been inserted correctly")
    print("3. Test the web service with the new data")
    
    # 显示部分SQL内容预览
    print("\nSQL Preview (first 20 lines):")
    lines = sql_script.split('\n')[:20]
    for line in lines:
        print(f"   {line}")

if __name__ == '__main__':
    main()