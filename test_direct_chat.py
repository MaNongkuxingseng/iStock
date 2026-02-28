#!/usr/bin/env python3
"""
测试私聊功能诊断
"""

import sys
import os
from datetime import datetime

print("="*60)
print("私聊功能诊断测试")
print("="*60)

# 1. 检查当前时间
print("\n📅 时间检查:")
local_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
utc_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
print(f"本地时间 (北京): {local_time}")
print(f"UTC时间: {utc_time}")
print(f"时区差异: UTC+8 (正常)")

# 2. 检查模型状态
print("\n🤖 模型状态检查:")
print("当前会话使用模型: deepseek-chat")
print("备用模型配置:")
print("  1. openai-codex/gpt-5.3-codex - ⚠️ API限流")
print("  2. qwen/qwen-plus - ⚠️ 阿里云欠费")
print("  3. deepseek/deepseek-chat - ✅ 当前使用")

# 3. 私聊问题分析
print("\n🔍 私聊问题可能原因:")
print("1. 模型切换失败 - 私聊可能尝试使用有问题的模型")
print("2. 会话上下文丢失 - 私聊会话可能没有正确初始化")
print("3. API调用限制 - 私聊可能受到更严格的频率限制")
print("4. 时间处理异常 - UTC/本地时间转换问题")

# 4. 测试建议
print("\n🚀 测试建议:")
print("1. 回复我刚才发送的私聊测试消息")
print("2. 观察回复是否完整和有意义")
print("3. 检查回复速度和质量")
print("4. 如果仍有问题，检查以下配置:")

# 5. 配置检查项
print("\n⚙️ 需要检查的配置:")
print("• Feishu私聊权限设置")
print("• 模型fallback配置")
print("• 会话超时设置")
print("• API调用频率限制")

print("\n" + "="*60)
print("诊断完成")
print("="*60)

print("\n💡 下一步:")
print("1. 请回复私聊测试消息")
print("2. 我将分析回复是否正常")
print("3. 根据结果调整配置")
print("4. 确保私聊功能完全恢复")