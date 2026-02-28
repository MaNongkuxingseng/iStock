#!/usr/bin/env python3
"""
批量数据回填脚本
回填2026-02-14至2026-02-26的数据
"""

import subprocess
import sys
import os
import time
from datetime import datetime, timedelta

def run_backfill(date):
    """运行单日数据回填"""
    print(f"回填数据: {date}")
    
    # 切换到工作目录
    job_dir = r"G:\openclaw\workspace\projects\active\myStock\instock\job"
    os.chdir(job_dir)
    
    # 执行回填命令
    cmd = [sys.executable, "strategy_data_daily_job.py", "--date", date]
    
    try:
        start_time = time.time()
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300  # 5分钟超时
        )
        elapsed = time.time() - start_time
        
        if result.returncode == 0:
            print(f"  ✓ 成功 ({elapsed:.1f}秒)")
            if result.stdout:
                print(f"    输出: {result.stdout[:100]}...")
            return True
        else:
            print(f"  ✗ 失败 ({elapsed:.1f}秒)")
            if result.stderr:
                print(f"    错误: {result.stderr[:200]}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"  ⚠ 超时 (300秒)")
        return False
    except Exception as e:
        print(f"  ✗ 异常: {e}")
        return False

def check_database_records():
    """检查数据库记录"""
    print("\n检查数据库记录...")
    
    try:
        # 使用MySQL命令行检查
        mysql_cmd = [
            r"C:\Program Files\MySQL\MySQL Server 9.4\bin\mysql.exe",
            "-uroot", "-p785091", "instockdb",
            "-e", "SELECT date, COUNT(*) as records FROM cn_stock_indicators_sell GROUP BY date ORDER BY date DESC;"
        ]
        
        result = subprocess.run(
            mysql_cmd,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("当前数据表记录:")
            print(result.stdout)
        else:
            print("数据库查询失败")
            
    except Exception as e:
        print(f"数据库检查异常: {e}")

def main():
    """主函数"""
    print("=" * 60)
    print("批量数据回填 - 2026-02-14 至 2026-02-26")
    print("=" * 60)
    
    # 生成日期列表
    start_date = datetime(2026, 2, 14)
    end_date = datetime(2026, 2, 26)
    
    dates = []
    current_date = start_date
    while current_date <= end_date:
        dates.append(current_date.strftime("%Y-%m-%d"))
        current_date += timedelta(days=1)
    
    print(f"需要回填 {len(dates)} 天数据")
    print(f"日期范围: {dates[0]} 至 {dates[-1]}")
    print()
    
    # 检查当前数据
    check_database_records()
    
    print("\n开始批量回填...")
    print("-" * 40)
    
    success_count = 0
    fail_count = 0
    
    # 逐日回填
    for date in dates:
        if run_backfill(date):
            success_count += 1
        else:
            fail_count += 1
        
        # 每完成一天，等待一下
        time.sleep(2)
    
    print("\n" + "=" * 60)
    print("批量回填完成统计:")
    print(f"  成功: {success_count} 天")
    print(f"  失败: {fail_count} 天")
    print(f"  总计: {len(dates)} 天")
    print("=" * 60)
    
    # 最终检查
    print("\n最终数据检查:")
    check_database_records()
    
    print("\n批量回填完成!")

if __name__ == "__main__":
    main()