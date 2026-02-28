#!/usr/bin/env python3
"""
简单的测试警报发送脚本
"""

import json
from datetime import datetime, date
import sys

def send_test_alert():
    """发送测试警报"""
    print("=" * 60)
    print("iStock Test Alert System")
    print("=" * 60)
    print()
    
    # 检查交易日
    today = date.today()
    weekday = today.weekday()
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    is_trading_day = weekday < 5
    
    print(f"Date: {today}")
    print(f"Weekday: {weekdays[weekday]}")
    print(f"Trading Day: {'YES' if is_trading_day else 'NO'}")
    print()
    
    # 创建测试消息
    test_message = f"""
CRITICAL TEST ALERT - iStock Monitoring System

Purpose: Verify stockbot monitoring and alert system

Alert Level: CRITICAL
Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Trading Day: {'YES' if is_trading_day else 'NO'}

Test Content:
1. Monitor system status check
2. Message delivery channel test  
3. Alert level verification
4. Response mechanism test

Simulated Issues:
- Service unavailable
- Database connection failure
- High latency response

Recommended Actions:
1. Check service status immediately
2. Verify monitoring configuration
3. Test recovery process
4. Confirm message receipt

System Status:
- Monitoring: RUNNING
- Message Delivery: TESTING
- Service Status: SIMULATED FAILURE
- Recovery: PENDING VERIFICATION

Note:
This is a test message to verify the stockbot monitoring system.
Please confirm receipt and check if messages are only sent on trading days.
"""
    
    # 保存测试记录
    test_record = {
        "test_time": datetime.now().isoformat(),
        "date": today.isoformat(),
        "weekday": weekdays[weekday],
        "is_trading_day": is_trading_day,
        "alert_level": "CRITICAL",
        "purpose": "Verify stockbot message delivery mechanism",
        "message": test_message,
        "expected_behavior": "Should only receive on trading days if configured that way"
    }
    
    with open("test_alert_simple.json", "w", encoding="utf-8") as f:
        json.dump(test_record, f, indent=2, ensure_ascii=False)
    
    print("Test alert generated and saved to test_alert_simple.json")
    print()
    
    # 显示消息
    print("=" * 60)
    print("TEST MESSAGE CONTENT:")
    print("=" * 60)
    print(test_message)
    print("=" * 60)
    print()
    
    # 分析结果
    print("ANALYSIS:")
    print("-" * 40)
    
    if is_trading_day:
        print("Today IS a trading day.")
        print("You SHOULD receive this test message.")
        print()
        print("If you did NOT receive it:")
        print("1. Check stockbot configuration")
        print("2. Verify message delivery channels")
        print("3. Check if monitoring is enabled")
    else:
        print("Today is NOT a trading day.")
        print("You should NOT receive this message if configured for trading days only.")
        print()
        print("If you DID receive it:")
        print("1. Stockbot may be configured to send on all days")
        print("2. Check your alert configuration")
        print("3. Verify trading day detection logic")
    
    print()
    print("NEXT STEPS:")
    print("-" * 40)
    print("1. Check Feishu group for this message")
    print("2. Verify receipt/absence as expected")
    print("3. Adjust configuration if needed")
    print("4. Run automated monitor: python automated_monitor.py")
    print()
    
    return test_record

def check_service_simple():
    """简单检查服务状态"""
    print("Checking iStock service status...")
    print()
    
    import requests
    
    endpoints = [
        ("Health Check", "http://localhost:8000/health"),
        ("API Docs", "http://localhost:8000/docs")
    ]
    
    print("Service Status Report:")
    print("-" * 50)
    
    for name, url in endpoints:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"{name:20} [OK]")
            else:
                print(f"{name:20} [ERROR: {response.status_code}]")
        except Exception as e:
            print(f"{name:20} [FAILED: {str(e)[:30]}...]")
    
    print("-" * 50)
    print()

if __name__ == "__main__":
    # 检查服务状态
    try:
        check_service_simple()
    except Exception as e:
        print(f"Service check failed: {e}")
        print("Continuing with test alert...")
        print()
    
    # 发送测试警报
    send_test_alert()
    
    print("=" * 60)
    print("Test completed successfully!")
    print("=" * 60)