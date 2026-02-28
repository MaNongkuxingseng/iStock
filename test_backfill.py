#!/usr/bin/env python3
"""
测试数据回填功能
"""

import sys
import os

# 添加项目路径
project_path = r"G:\openclaw\workspace\projects\active\myStock"
sys.path.append(project_path)

try:
    # 导入相关模块
    import instock.job.strategy_data_daily_job as strategy_job
    import instock.core.tablestructure as tbs
    
    print("Modules imported successfully")
    print(f"Available strategies: {tbs.TABLE_CN_STOCK_STRATEGIES}")
    
    # 测试prepare函数
    test_date = "2026-02-14"
    test_strategy = "cn_stock_indicators_sell"
    
    print(f"\nTesting prepare function for date: {test_date}, strategy: {test_strategy}")
    
    # 尝试调用prepare函数
    result = strategy_job.prepare(test_date, test_strategy)
    print(f"Prepare result: {result}")
    
    # 尝试运行main函数
    print("\nTesting main function...")
    strategy_job.main()
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()