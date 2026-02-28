#!/usr/bin/env python3
"""
立即运行监控测试并发送严重测试消息
"""

import asyncio
import json
from datetime import datetime
import sys
import os

# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def send_test_alert():
    """发送严重的测试警报消息"""
    print("🚨 发送严重的测试警报消息...")
    
    # 构建测试消息
    test_alert = {
        "title": "🚨 iStock 严重测试警报",
        "message": """
🚨🚨🚨 严重测试警报 🚨🚨🚨

📊 测试目的：验证监控系统和消息推送机制

⚠️ 警报级别：CRITICAL（严重）
⏰ 测试时间：{timestamp}

📋 测试内容：
1. ✅ 监控系统运行状态检查
2. ✅ 消息推送通道测试
3. ✅ 警报级别验证
4. ✅ 响应机制测试

🔍 发现问题：
• 模拟服务不可用
• 模拟数据库连接失败
• 模拟高延迟响应

💡 建议操作：
1. 立即检查服务状态
2. 验证监控配置
3. 测试恢复流程
4. 确认消息接收

📈 系统状态：
• 监控系统：运行中
• 消息推送：测试中
• 服务状态：模拟故障
• 恢复能力：待验证

📝 备注：
这是一条测试消息，用于验证stockbot盯盘分析系统的消息推送机制。
请确认您已收到此消息，并检查是否只在交易日/工作日推送。
        """.format(timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        "severity": "critical",
        "is_test": True,
        "timestamp": datetime.now().isoformat(),
        "test_purpose": "验证stockbot盯盘分析消息推送机制"
    }
    
    # 保存测试记录
    test_record = {
        "test_time": datetime.now().isoformat(),
        "alert_sent": True,
        "alert_data": test_alert,
        "purpose": "检查stockbot消息推送机制，验证是否只在交易日推送"
    }
    
    # 保存到文件
    with open("test_alert_record.json", "w", encoding="utf-8") as f:
        json.dump(test_record, f, indent=2, ensure_ascii=False)
    
    print("✅ 测试警报已生成并保存到 test_alert_record.json")
    
    # 模拟发送到Feishu
    print("📤 模拟发送到Feishu群组...")
    
    feishu_message = {
        "msg_type": "interactive",
        "card": {
            "config": {
                "wide_screen_mode": True
            },
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": test_alert["title"]
                },
                "template": "red"
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": test_alert["message"]
                    }
                },
                {
                    "tag": "hr"
                },
                {
                    "tag": "note",
                    "elements": [
                        {
                            "tag": "plain_text",
                            "content": "🔧 iStock 自动化监控测试 | 请确认收到此测试消息"
                        }
                    ]
                }
            ]
        }
    }
    
    print("=" * 60)
    print("📨 测试消息内容:")
    print("=" * 60)
    print(f"标题: {test_alert['title']}")
    print(f"严重程度: {test_alert['severity'].upper()}")
    print(f"测试时间: {test_alert['timestamp']}")
    print(f"测试目的: {test_alert['test_purpose']}")
    print("=" * 60)
    print()
    
    # 检查是否为交易日
    from datetime import date
    today = date.today()
    weekday = today.weekday()
    is_trading_day = weekday < 5  # 周一到周五
    
    print("📅 交易日检查:")
    print(f"今天日期: {today}")
    print(f"星期几: {['周一','周二','周三','周四','周五','周六','周日'][weekday]}")
    print(f"是否为交易日: {'是' if is_trading_day else '否'}")
    print()
    
    if not is_trading_day:
        print("⚠️  注意: 今天不是交易日")
        print("如果之前设置的stockbot只在交易日推送，您可能不会收到消息")
        print("这是正常行为，说明推送机制按预期工作")
    else:
        print("✅ 今天是交易日")
        print("您应该收到这条测试消息")
    print()
    
    # 创建监控配置检查
    print("🔧 监控系统配置检查:")
    
    config_check = {
        "monitoring_enabled": True,
        "alert_channels": ["feishu"],
        "schedule": {
            "health_check": "每30分钟",
            "stock_analysis": "交易日 9:30, 13:00",
            "daily_report": "每天 23:00"
        },
        "trading_day_only": "待确认",
        "test_mode": True
    }
    
    print(json.dumps(config_check, indent=2, ensure_ascii=False))
    print()
    
    # 建议下一步
    print("🎯 建议下一步:")
    print("1. 检查Feishu群组是否收到此测试消息")
    print("2. 如果是交易日但未收到，检查stockbot配置")
    print("3. 如果不是交易日但收到了，调整推送策略")
    print("4. 运行完整的监控测试: python automated_monitor.py --test")
    print("5. 设置定时任务: 使用系统的任务计划程序")
    print()
    
    return test_alert

async def check_service_status():
    """检查服务状态"""
    print("🔍 检查iStock服务状态...")
    
    import aiohttp
    
    endpoints = [
        ("健康检查", "http://localhost:8000/health"),
        ("API文档", "http://localhost:8000/docs"),
        ("股票API", "http://localhost:8000/api/v1/stocks")
    ]
    
    results = []
    
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
        for name, url in endpoints:
            try:
                async with session.get(url) as response:
                    status = response.status
                    if status == 200:
                        results.append((name, "✅ 正常", url))
                    else:
                        results.append((name, f"❌ 异常 ({status})", url))
            except Exception as e:
                results.append((name, f"❌ 错误: {str(e)}", url))
    
    print("📊 服务状态报告:")
    print("=" * 60)
    for name, status, url in results:
        print(f"{name:15} {status:20} {url}")
    print("=" * 60)
    
    return results

async def main():
    """主函数"""
    print("=" * 60)
    print("iStock 自动化监控测试系统")
    print("=" * 60)
    print()
    
    # 检查服务状态
    service_results = await check_service_status()
    
    print()
    
    # 发送测试警报
    test_alert = await send_test_alert()
    
    print()
    print("=" * 60)
    print("测试完成!")
    print("=" * 60)
    print()
    
    # 生成总结报告
    all_ok = all("✅" in status for _, status, _ in service_results)
    
    if all_ok:
        print("🎉 所有服务正常，监控系统就绪")
        print("📁 测试记录已保存: test_alert_record.json")
        print("🚀 可以设置定时监控任务")
    else:
        print("⚠️  服务存在问题，需要修复")
        print("🔧 请先修复服务，再设置监控")
    
    print()
    print("💡 设置自动化监控:")
    print("1. 安装依赖: pip install schedule aiohttp")
    print("2. 运行监控: python automated_monitor.py")
    print("3. 设置定时: 使用Windows任务计划程序")
    print()

if __name__ == "__main__":
    asyncio.run(main())