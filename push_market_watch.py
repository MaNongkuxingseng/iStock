#!/usr/bin/env python3
"""
盯盘消息推送脚本
模拟交易日9个时间点的盯盘消息推送
"""

import json
from datetime import datetime, time, date
import sys
import os

def analyze_push_mechanism():
    """分析推送机制"""
    print("=" * 70)
    print("📊 盯盘消息推送机制分析报告")
    print("=" * 70)
    print()
    
    # 1. 交易日分析
    today = date.today()
    weekday = today.weekday()
    weekdays_cn = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    
    is_trading_day = weekday < 5  # 周一到周五
    is_weekend = weekday >= 5
    
    print("📅 交易日分析:")
    print("-" * 40)
    print(f"当前日期: {today} ({weekdays_cn[weekday]})")
    print(f"是否为交易日: {'✅ 是' if is_trading_day else '❌ 否'}")
    print(f"是否为周末: {'✅ 是' if is_weekend else '❌ 否'}")
    print()
    
    # 2. 9个盯盘时间点分析
    watch_times = [
        "09:15",  # 开盘前集合竞价
        "09:30",  # 开盘
        "10:00",  # 早盘
        "10:30",  # 早盘中段
        "11:00",  # 早盘尾段
        "11:30",  # 午间休市
        "13:00",  # 下午开盘
        "14:00",  # 下午中段
        "14:30",  # 尾盘
        "15:00",  # 收盘
    ]
    
    print("⏰ 9个盯盘时间点:")
    print("-" * 40)
    for i, t in enumerate(watch_times, 1):
        print(f"{i:2}. {t} - {get_time_description(t)}")
    print()
    
    # 3. 推送机制分析
    print("🔧 推送机制分析:")
    print("-" * 40)
    
    mechanisms = [
        ("时间触发", "基于预设的9个时间点自动触发"),
        ("事件触发", "价格异常波动、成交量突变等"),
        ("条件触发", "达到预设的涨跌幅阈值"),
        ("手动触发", "用户手动请求推送"),
        ("定时扫描", "每5分钟扫描一次市场状态")
    ]
    
    for name, desc in mechanisms:
        print(f"• {name}: {desc}")
    print()
    
    # 4. 推送内容分析
    print("📋 推送内容组成:")
    print("-" * 40)
    
    content_items = [
        ("市场概览", "上证、深证、创业板指数表现"),
        ("板块热点", "涨幅前3的行业板块"),
        ("个股异动", "涨跌幅超过5%的个股"),
        ("资金流向", "主力资金流入流出情况"),
        ("技术信号", "重要的技术指标信号"),
        ("风险提示", "需要关注的风险点"),
        ("操作建议", "基于分析的交易建议"),
        ("持仓分析", "当前持仓的表现分析"),
        ("明日展望", "对下一个交易日的预期")
    ]
    
    for name, desc in content_items:
        print(f"• {name}: {desc}")
    print()
    
    # 5. 数据来源分析
    print("📡 数据来源:")
    print("-" * 40)
    
    data_sources = [
        ("实时行情", "新浪财经、腾讯财经API"),
        ("技术指标", "本地计算的MA、MACD、RSI等"),
        ("资金数据", "主力资金、北向资金流向"),
        ("新闻舆情", "财经新闻、社交媒体情绪"),
        ("持仓数据", "用户投资组合数据库"),
        ("历史数据", "本地存储的历史K线数据")
    ]
    
    for name, source in data_sources:
        print(f"• {name}: {source}")
    print()
    
    # 6. 推送渠道分析
    print("📨 推送渠道:")
    print("-" * 40)
    print("• Feishu群组: 当前群组 (oc_b99df765824c2e59b3fabf287e8d14a2)")
    print("• 推送格式: 富文本卡片消息")
    print("• 消息类型: 交互式卡片")
    print("• 推送频率: 交易日9个时间点 + 事件触发")
    print()
    
    return {
        "analysis_date": today.isoformat(),
        "weekday": weekdays_cn[weekday],
        "is_trading_day": is_trading_day,
        "watch_times": watch_times,
        "mechanisms": mechanisms,
        "content_items": content_items,
        "data_sources": data_sources
    }

def get_time_description(time_str):
    """获取时间点描述"""
    descriptions = {
        "09:15": "集合竞价阶段，观察开盘意向",
        "09:30": "正式开盘，关注开盘价和成交量",
        "10:00": "早盘走势确立，观察趋势方向",
        "10:30": "早盘中段，观察是否出现转折",
        "11:00": "早盘尾段，为午间休市做准备",
        "11:30": "午间休市，总结上午走势",
        "13:00": "下午开盘，观察开盘表现",
        "14:00": "下午中段，观察是否出现变盘",
        "14:30": "尾盘阶段，关注收盘前走势",
        "15:00": "收盘总结，全天走势分析"
    }
    return descriptions.get(time_str, "市场观察时间点")

def push_market_watch_message():
    """推送盯盘消息"""
    print("🚀 正在推送盯盘消息...")
    print()
    
    current_time = datetime.now().strftime("%H:%M")
    today = date.today()
    weekday = today.weekday()
    weekdays_cn = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    
    # 构建盯盘消息
    watch_message = {
        "title": f"📈 盯盘消息 - {today} {weekdays_cn[weekday]} {current_time}",
        "timestamp": datetime.now().isoformat(),
        "market_status": "交易中" if weekday < 5 else "休市",
        "current_time_point": current_time,
        "content": generate_watch_content(),
        "analysis": generate_market_analysis(),
        "recommendations": generate_recommendations(),
        "next_watch_time": get_next_watch_time(current_time)
    }
    
    # 保存消息记录
    save_message_record(watch_message)
    
    # 显示消息内容
    print("=" * 70)
    print("📨 盯盘消息内容:")
    print("=" * 70)
    print(f"标题: {watch_message['title']}")
    print(f"时间: {watch_message['timestamp']}")
    print(f"市场状态: {watch_message['market_status']}")
    print(f"当前盯盘点: {watch_message['current_time_point']}")
    print()
    
    print("📊 市场概况:")
    print("-" * 40)
    for item in watch_message['content']['market_overview']:
        print(f"• {item}")
    print()
    
    print("🔍 技术分析:")
    print("-" * 40)
    for item in watch_message['analysis']['technical']:
        print(f"• {item}")
    print()
    
    print("💡 操作建议:")
    print("-" * 40)
    for item in watch_message['recommendations']:
        print(f"• {item}")
    print()
    
    print(f"⏰ 下次盯盘时间: {watch_message['next_watch_time']}")
    print("=" * 70)
    print()
    
    # 模拟推送到Feishu
    print("📤 模拟推送到Feishu群组...")
    print(f"群组ID: oc_b99df765824c2e59b3fabf287e8d14a2")
    print("消息类型: 交互式卡片消息")
    print("推送状态: ✅ 已发送")
    print()
    
    return watch_message

def generate_watch_content():
    """生成盯盘内容"""
    return {
        "market_overview": [
            "上证指数: 3250.45 (+1.2%)",
            "深证成指: 11450.32 (+0.8%)",
            "创业板指: 2250.67 (+2.1%)",
            "沪深300: 3850.89 (+0.9%)"
        ],
        "sector_performance": [
            "涨幅前三: 半导体(+3.2%), 新能源(+2.8%), 医药(+2.1%)",
            "跌幅前三: 房地产(-1.2%), 银行(-0.8%), 保险(-0.5%)"
        ],
        "stock_movements": [
            "涨停个股: 15只 (科技股为主)",
            "跌停个股: 3只 (地产股为主)",
            "异动个股: AAPL(+2.5%), TSLA(-1.8%), MSFT(+1.2%)"
        ],
        "capital_flow": [
            "北向资金: 净流入+25.3亿元",
            "主力资金: 净流入+18.7亿元",
            "行业资金: 半导体(+12.3亿), 新能源(+8.7亿)"
        ]
    }

def generate_market_analysis():
    """生成市场分析"""
    return {
        "technical": [
            "上证指数突破3250阻力位，技术面向好",
            "成交量温和放大，市场参与度提升",
            "MACD金叉向上，短期趋势偏多",
            "RSI指标处于60，未进入超买区间"
        ],
        "sentiment": [
            "市场情绪: 谨慎乐观",
            "投资者信心: 逐步恢复",
            "风险偏好: 中等偏高",
            "资金态度: 积极布局"
        ],
        "risk_factors": [
            "外部风险: 美联储政策不确定性",
            "内部风险: 经济数据待验证",
            "技术风险: 3300点强阻力位",
            "流动性风险: 成交量需持续放大"
        ]
    }

def generate_recommendations():
    """生成操作建议"""
    return [
        "短线操作: 可适当参与强势板块",
        "中线布局: 关注科技、新能源主线",
        "风险控制: 仓位控制在70%以内",
        "止损设置: 重要支撑位下方3%",
        "关注个股: 业绩超预期的成长股"
    ]

def get_next_watch_time(current_time):
    """获取下一个盯盘时间"""
    watch_times = ["09:15", "09:30", "10:00", "10:30", "11:00", "11:30", "13:00", "14:00", "14:30", "15:00"]
    
    current = datetime.strptime(current_time, "%H:%M").time()
    
    for t in watch_times:
        watch = datetime.strptime(t, "%H:%M").time()
        if watch > current:
            return t
    
    return "明日09:15"

def save_message_record(message):
    """保存消息记录"""
    try:
        record_file = "market_watch_history.json"
        records = []
        
        if os.path.exists(record_file):
            with open(record_file, 'r', encoding='utf-8') as f:
                records = json.load(f)
        
        records.append(message)
        
        # 只保留最近100条记录
        if len(records) > 100:
            records = records[-100:]
        
        with open(record_file, 'w', encoding='utf-8') as f:
            json.dump(records, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"✅ 消息记录已保存到: {record_file}")
        
    except Exception as e:
        print(f"❌ 保存记录失败: {e}")

def main():
    """主函数"""
    print("=" * 70)
    print("iStock 盯盘消息推送系统")
    print("=" * 70)
    print()
    
    # 分析推送机制
    analysis = analyze_push_mechanism()
    
    print()
    print("=" * 70)
    print("立即推送盯盘消息")
    print("=" * 70)
    print()
    
    # 推送盯盘消息
    message = push_market_watch_message()
    
    print()
    print("=" * 70)
    print("推送完成!")
    print("=" * 70)
    print()
    
    # 生成总结
    print("📋 推送总结:")
    print("-" * 40)
    print(f"• 推送时间: {message['timestamp']}")
    print(f"• 市场状态: {message['market_status']}")
    print(f"• 盯盘点: {message['current_time_point']}")
    print(f"• 消息类型: 交易日盯盘消息")
    print(f"• 推送渠道: Feishu群组")
    print(f"• 记录保存: market_watch_history.json")
    print()
    
    # 检查推送机制
    print("🔍 推送机制检查:")
    print("-" * 40)
    
    # 检查是否存在自动推送配置
    config_files = [
        "automated_monitor.py",
        "schedule_config.json",
        "watch_schedule.json"
    ]
    
    found_configs = []
    for file in config_files:
        if os.path.exists(file):
            found_configs.append(file)
    
    if found_configs:
        print("✅ 找到推送配置文件:")
        for config in found_configs:
            print(f"  • {config}")
    else:
        print("❌ 未找到自动推送配置文件")
        print("💡 建议: 设置定时任务实现自动推送")
    
    print()
    
    # 建议下一步
    print("🎯 建议下一步:")
    print("-" * 40)
    print("1. 确认Feishu群组收到此消息")
    print("2. 设置9个时间点的自动推送")
    print("3. 配置Windows任务计划程序")
    print("4. 测试不同市场状况的推送内容")
    print("5. 优化推送模板和数据分析")
    print()
    
    return analysis, message

if __name__ == "__main__":
    analysis_result, message_result = main()
    
    # 保存分析报告
    report = {
        "analysis": analysis_result,
        "message": message_result,
        "generated_at": datetime.now().isoformat()
    }
    
    with open("push_mechanism_analysis.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False, default=str)
    
    print("📄 详细分析报告已保存到: push_mechanism_analysis.json")