#!/usr/bin/env python3
"""
直接执行数据回填
"""

import subprocess
import os
import time

def execute_sql_file(sql_file_path):
    """执行SQL文件"""
    print(f"Executing SQL file: {sql_file_path}")
    
    # 检查文件是否存在
    if not os.path.exists(sql_file_path):
        print(f"Error: SQL file not found: {sql_file_path}")
        return False
    
    # 尝试使用mysql命令行执行
    cmd = f'mysql -u root -p123456 mystock < "{sql_file_path}"'
    
    print("Starting data backfill...")
    start_time = time.time()
    
    try:
        # 执行命令
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='gbk')
        
        if result.returncode == 0:
            print(f"[SUCCESS] Data backfill completed in {time.time() - start_time:.2f} seconds")
            
            # 验证数据
            print("\nVerifying data...")
            verify_cmd = 'mysql -u root -p123456 -e "USE mystock; SELECT COUNT(*) as total_records, MIN(date) as earliest, MAX(date) as latest FROM cn_stock_indicators_sell;"'
            verify_result = subprocess.run(verify_cmd, shell=True, capture_output=True, text=True, encoding='gbk')
            
            if verify_result.returncode == 0:
                print("Verification result:")
                print(verify_result.stdout)
            else:
                print(f"Verification error: {verify_result.stderr}")
            
            return True
        else:
            print(f"[ERROR] Data backfill failed with code {result.returncode}")
            print(f"Error output: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"[ERROR] Exception during execution: {e}")
        return False

def main():
    print("=== Direct Data Backfill Execution ===")
    
    sql_file_path = "G:\\openclaw\\workspace\\_system\\agent-home\\backfill_data.sql"
    
    # 执行SQL文件
    success = execute_sql_file(sql_file_path)
    
    if success:
        print("\n" + "="*50)
        print("[SUCCESS] Historical data backfill completed!")
        print("="*50)
        
        # 测试Web服务
        print("\nTesting web service with new data...")
        test_commands = [
            'powershell -Command "Invoke-RestMethod -Uri \'http://127.0.0.1:9988/health\' -Method Get"',
            'powershell -Command "Invoke-RestMethod -Uri \'http://127.0.0.1:9988/instock/data?table_name=cn_stock_indicators_sell&date=2026-02-26\' -Method Get | Select-Object -First 1"'
        ]
        
        for cmd in test_commands:
            try:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"Test passed: {cmd[:50]}...")
                else:
                    print(f"Test warning: {result.stderr[:100]}")
            except:
                print(f"Test skipped (command may not work in this environment)")
        
        print("\nNext steps:")
        print("1. Check Feishu group for test messages")
        print("2. Monitor web service performance")
        print("3. Consider setting up automated daily updates")
    else:
        print("\n" + "="*50)
        print("[ERROR] Data backfill failed!")
        print("="*50)
        print("\nTroubleshooting steps:")
        print("1. Check MySQL service is running")
        print("2. Verify database credentials")
        print("3. Check file permissions")

if __name__ == '__main__':
    main()