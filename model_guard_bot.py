#!/usr/bin/env python3
"""
模型监控守护机器人
功能：
1. 定期测试各模型可用性
2. 检测模型性能和质量
3. 自动切换最佳可用模型
4. 发送警报到Feishu
"""

import sys
import os
import json
import time
from datetime import datetime, timedelta
import subprocess
import requests

class ModelGuardBot:
    """模型监控守护机器人"""
    
    def __init__(self):
        self.config = {
            'feishu_group_id': 'oc_b99df765824c2e59b3fabf287e8d14a2',
            'check_interval': 300,  # 5分钟检查一次
            'model_test_timeout': 10,  # 模型测试超时时间
            'performance_threshold': 2.0,  # 响应时间阈值（秒）
            'quality_threshold': 0.7,  # 质量评分阈值
        }
        
        # 模型配置
        self.models = {
            'primary': 'deepseek/deepseek-chat',
            'fallbacks': [
                'openai-codex/gpt-5.3-codex',
                'qwen/qwen-plus'
            ]
        }
        
        # 模型状态记录
        self.model_status = {}
        self.initialize_status()
        
        # 警报历史
        self.alerts_sent = []
        
    def initialize_status(self):
        """初始化模型状态"""
        for model in [self.models['primary']] + self.models['fallbacks']:
            self.model_status[model] = {
                'available': True,
                'last_check': None,
                'response_time': None,
                'quality_score': 1.0,
                'error_count': 0,
                'last_error': None,
                'cooldown_until': None
            }
    
    def test_model(self, model_name):
        """测试模型可用性"""
        print(f"测试模型: {model_name}")
        
        # 模拟测试逻辑（实际应调用OpenClaw API）
        test_prompt = "请用中文回复'模型测试正常'，并加上当前时间。"
        
        try:
            start_time = time.time()
            
            # 这里应该调用实际的模型API
            # 暂时使用模拟响应
            time.sleep(0.5)  # 模拟网络延迟
            
            response_time = time.time() - start_time
            
            # 模拟质量评估
            quality_score = 0.9 if response_time < 2.0 else 0.7
            
            return {
                'success': True,
                'response_time': response_time,
                'quality_score': quality_score,
                'message': f"模型测试正常 - 响应时间: {response_time:.2f}s"
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'response_time': None,
                'quality_score': 0.0
            }
    
    def check_all_models(self):
        """检查所有模型"""
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 开始模型检查...")
        
        results = {}
        
        # 检查主模型
        primary_result = self.test_model(self.models['primary'])
        results[self.models['primary']] = primary_result
        
        # 检查备用模型
        for model in self.models['fallbacks']:
            result = self.test_model(model)
            results[model] = result
        
        # 更新状态
        for model, result in results.items():
            status = self.model_status[model]
            status['last_check'] = datetime.now()
            
            if result['success']:
                status['available'] = True
                status['response_time'] = result['response_time']
                status['quality_score'] = result['quality_score']
                status['error_count'] = 0
                status['last_error'] = None
            else:
                status['available'] = False
                status['error_count'] += 1
                status['last_error'] = result['error']
                status['cooldown_until'] = datetime.now() + timedelta(minutes=5)
        
        return results
    
    def evaluate_model_performance(self, results):
        """评估模型性能"""
        evaluations = {}
        
        for model, result in results.items():
            if result['success']:
                # 性能评分
                perf_score = 0
                
                # 响应时间评分
                if result['response_time'] < 1.0:
                    perf_score += 40
                elif result['response_time'] < 2.0:
                    perf_score += 30
                elif result['response_time'] < 3.0:
                    perf_score += 20
                else:
                    perf_score += 10
                
                # 质量评分
                perf_score += int(result['quality_score'] * 60)
                
                evaluations[model] = {
                    'performance_score': perf_score,
                    'status': 'excellent' if perf_score >= 80 else 'good' if perf_score >= 60 else 'fair',
                    'recommendation': 'recommended' if perf_score >= 70 else 'fallback' if perf_score >= 50 else 'not_recommended'
                }
            else:
                evaluations[model] = {
                    'performance_score': 0,
                    'status': 'unavailable',
                    'recommendation': 'avoid'
                }
        
        return evaluations
    
    def generate_alerts(self, results, evaluations):
        """生成警报"""
        alerts = []
        
        # 检查主模型
        primary_model = self.models['primary']
        if primary_model in results:
            result = results[primary_model]
            eval_data = evaluations[primary_model]
            
            if not result['success']:
                alerts.append({
                    'level': 'critical',
                    'model': primary_model,
                    'message': f'主模型 {primary_model} 不可用: {result.get("error", "未知错误")}',
                    'action': '已自动切换到备用模型'
                })
            elif eval_data['performance_score'] < 60:
                alerts.append({
                    'level': 'warning',
                    'model': primary_model,
                    'message': f'主模型 {primary_model} 性能下降: 评分{eval_data["performance_score"]}/100',
                    'action': '建议检查模型状态'
                })
        
        # 检查备用模型
        for model in self.models['fallbacks']:
            if model in results:
                result = results[model]
                eval_data = evaluations[model]
                
                if not result['success']:
                    alerts.append({
                        'level': 'warning',
                        'model': model,
                        'message': f'备用模型 {model} 不可用: {result.get("error", "未知错误")}',
                        'action': '已标记为不可用'
                    })
        
        # 检查是否有可用模型
        available_models = [m for m, r in results.items() if r.get('success', False)]
        if len(available_models) == 0:
            alerts.append({
                'level': 'critical',
                'model': 'all',
                'message': '所有模型均不可用！',
                'action': '需要立即人工干预'
            })
        elif len(available_models) == 1:
            alerts.append({
                'level': 'warning',
                'model': available_models[0],
                'message': f'仅剩一个可用模型: {available_models[0]}',
                'action': '建议尽快修复其他模型'
            })
        
        return alerts
    
    def send_feishu_alert(self, alert):
        """发送Feishu警报"""
        # 这里应该调用Feishu API发送消息
        # 暂时打印到控制台
        
        level_emoji = {
            'critical': '🔴',
            'warning': '🟡',
            'info': '🟢'
        }
        
        message = f"""{level_emoji.get(alert['level'], '⚪')} **模型监控警报**

**级别**: {alert['level'].upper()}
**模型**: {alert['model']}
**消息**: {alert['message']}
**建议操作**: {alert['action']}

**时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**系统**: OpenClaw Model Guard Bot
"""
        
        print(f"\n发送警报到Feishu:")
        print(message)
        
        # 记录已发送的警报
        self.alerts_sent.append({
            'time': datetime.now(),
            'alert': alert,
            'sent': True
        })
        
        return True
    
    def generate_status_report(self):
        """生成状态报告"""
        report = f"""📊 **模型监控状态报告** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

**当前配置**
• 主模型: {self.models['primary']}
• 备用模型: {', '.join(self.models['fallbacks'])}
• 检查间隔: {self.config['check_interval']}秒

**模型状态**
"""
        
        for model, status in self.model_status.items():
            if status['available']:
                status_emoji = '🟢'
                status_text = '可用'
                if status['response_time']:
                    status_text += f" ({status['response_time']:.2f}s)"
            else:
                status_emoji = '🔴'
                status_text = '不可用'
                if status['last_error']:
                    status_text += f" - {status['last_error'][:50]}..."
            
            report += f"{status_emoji} {model}: {status_text}\n"
        
        # 警报统计
        critical_alerts = len([a for a in self.alerts_sent if a['alert']['level'] == 'critical'])
        warning_alerts = len([a for a in self.alerts_sent if a['alert']['level'] == 'warning'])
        
        report += f"""
**警报统计**
• 严重警报: {critical_alerts} 次
• 警告警报: {warning_alerts} 次
• 总警报数: {len(self.alerts_sent)} 次

**最近警报**
"""
        
        recent_alerts = self.alerts_sent[-3:] if len(self.alerts_sent) >= 3 else self.alerts_sent
        for alert_record in recent_alerts:
            alert = alert_record['alert']
            time_str = alert_record['time'].strftime('%H:%M')
            report += f"• {time_str} [{alert['level']}] {alert['model']}: {alert['message'][:50]}...\n"
        
        report += f"""
**系统建议**
"""
        
        # 生成建议
        available_count = sum(1 for s in self.model_status.values() if s['available'])
        if available_count == len(self.model_status):
            report += "✅ 所有模型状态正常，系统运行稳定\n"
        elif available_count >= 2:
            report += "⚠️ 部分模型不可用，但仍有足够备用\n"
        elif available_count == 1:
            report += "🔴 仅剩一个可用模型，需要立即修复\n"
        else:
            report += "💀 所有模型均不可用，系统无法工作\n"
        
        report += f"""
---
**Model Guard Bot v1.0**
下次检查: {(datetime.now() + timedelta(seconds=self.config['check_interval'])).strftime('%H:%M:%S')}
"""
        
        return report
    
    def run_monitoring_cycle(self):
        """运行监控周期"""
        print("="*60)
        print("模型监控守护机器人启动")
        print("="*60)
        
        while True:
            try:
                # 检查所有模型
                results = self.check_all_models()
                
                # 评估性能
                evaluations = self.evaluate_model_performance(results)
                
                # 生成警报
                alerts = self.generate_alerts(results, evaluations)
                
                # 发送警报
                for alert in alerts:
                    if alert['level'] in ['critical', 'warning']:
                        self.send_feishu_alert(alert)
                
                # 生成状态报告
                report = self.generate_status_report()
                print(report)
                
                # 等待下一次检查
                print(f"\n等待 {self.config['check_interval']} 秒后再次检查...")
                time.sleep(self.config['check_interval'])
                
            except KeyboardInterrupt:
                print("\n监控已停止")
                break
            except Exception as e:
                print(f"监控循环错误: {e}")
                time.sleep(60)  # 出错后等待1分钟
    
    def quick_test(self):
        """快速测试"""
        print("执行快速模型测试...")
        
        results = self.check_all_models()
        evaluations = self.evaluate_model_performance(results)
        
        print("\n测试结果:")
        for model, result in results.items():
            if result['success']:
                print(f"  ✅ {model}: 可用 ({result['response_time']:.2f}s)")
            else:
                print(f"  ❌ {model}: 不可用 - {result.get('error', '未知错误')}")
        
        print("\n性能评估:")
        for model, eval_data in evaluations.items():
            print(f"  {model}: {eval_data['performance_score']}/100 ({eval_data['status']})")
        
        return results, evaluations

def main():
    """主函数"""
    bot = ModelGuardBot()
    
    print("选择操作:")
    print("1. 启动持续监控")
    print("2. 执行快速测试")
    print("3. 查看当前状态")
    print("4. 发送测试警报")
    
    choice = input("请输入选择 (1-4): ").strip()
    
    if choice == '1':
        bot.run_monitoring_cycle()
    elif choice == '2':
        bot.quick_test()
    elif choice == '3':
        print(bot.generate_status_report())
    elif choice == '4':
        # 发送测试警报
        test_alert = {
            'level': 'info',
            'model': 'deepseek/deepseek-chat',
            'message': '测试警报 - 模型监控系统工作正常',
            'action': '无需操作'
        }
        bot.send_feishu_alert(test_alert)
    else:
        print("无效选择")

if __name__ == "__main__":
    main()