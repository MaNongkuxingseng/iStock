#!/usr/bin/env python3
"""
完整的模型管理系统
整合配置管理、监控告警、智能路由
"""

import json
import os
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import subprocess

class ModelManagementSystem:
    """模型管理系统"""
    
    def __init__(self, config_path: str = None):
        self.config_path = config_path or "C:\\Users\\Administrator\\.openclaw\\openclaw.json"
        self.backup_path = self.config_path + ".backup"
        
        # 加载配置
        self.config = self.load_config()
        
        # 模型配置
        self.model_config = self.extract_model_config()
        
        # 监控状态
        self.monitoring_status = {
            'last_check': None,
            'alerts_sent_today': 0,
            'model_tests_today': 0,
            'last_model_switch': None
        }
        
        # 创建日志目录
        self.log_dir = os.path.join(os.path.dirname(__file__), "logs", "model_management")
        os.makedirs(self.log_dir, exist_ok=True)
    
    def load_config(self) -> Dict:
        """加载OpenClaw配置"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"加载配置失败: {e}")
            return {}
    
    def save_config(self) -> bool:
        """保存配置"""
        try:
            # 创建备份
            if os.path.exists(self.config_path):
                import shutil
                shutil.copy2(self.config_path, self.backup_path)
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            
            print(f"配置已保存到: {self.config_path}")
            print(f"备份已创建: {self.backup_path}")
            return True
        except Exception as e:
            print(f"保存配置失败: {e}")
            return False
    
    def extract_model_config(self) -> Dict:
        """提取模型配置"""
        model_config = {
            'primary': None,
            'fallbacks': [],
            'available_models': []
        }
        
        try:
            # 从agents.defaults.model提取
            agents_config = self.config.get('agents', {}).get('defaults', {}).get('model', {})
            model_config['primary'] = agents_config.get('primary')
            model_config['fallbacks'] = agents_config.get('fallbacks', [])
            
            # 从models.providers提取可用模型
            providers = self.config.get('models', {}).get('providers', {})
            for provider, info in providers.items():
                models = info.get('models', [])
                for model in models:
                    model_id = model.get('id')
                    if model_id:
                        full_name = f"{provider}/{model_id}"
                        model_config['available_models'].append(full_name)
            
            return model_config
        except Exception as e:
            print(f"提取模型配置失败: {e}")
            return model_config
    
    def update_model_priority(self, primary_model: str, fallbacks: List[str] = None) -> bool:
        """更新模型优先级"""
        try:
            # 确保配置结构存在
            if 'agents' not in self.config:
                self.config['agents'] = {}
            if 'defaults' not in self.config['agents']:
                self.config['agents']['defaults'] = {}
            if 'model' not in self.config['agents']['defaults']:
                self.config['agents']['defaults']['model'] = {}
            
            # 更新主模型
            self.config['agents']['defaults']['model']['primary'] = primary_model
            
            # 更新备用模型
            if fallbacks is not None:
                self.config['agents']['defaults']['model']['fallbacks'] = fallbacks
            
            # 保存配置
            if self.save_config():
                print(f"模型优先级已更新:")
                print(f"  主模型: {primary_model}")
                print(f"  备用模型: {fallbacks}")
                
                # 记录更改
                self.log_change({
                    'action': 'update_priority',
                    'primary': primary_model,
                    'fallbacks': fallbacks,
                    'timestamp': datetime.now().isoformat()
                })
                
                return True
            else:
                return False
                
        except Exception as e:
            print(f"更新模型优先级失败: {e}")
            return False
    
    def test_model_availability(self, model_name: str) -> Dict:
        """测试模型可用性"""
        print(f"测试模型: {model_name}")
        
        # 这里应该调用实际的模型测试
        # 暂时使用模拟测试
        
        test_result = {
            'model': model_name,
            'timestamp': datetime.now().isoformat(),
            'success': True,
            'response_time': 1.5,
            'quality_score': 0.8,
            'error': None
        }
        
        # 模拟特定模型的失败
        if 'qwen' in model_name.lower():
            test_result['success'] = False
            test_result['error'] = "阿里云API欠费"
        elif 'openai-codex' in model_name.lower():
            test_result['success'] = True  # 假设可用但可能限流
            test_result['quality_score'] = 0.6
        
        return test_result
    
    def test_all_models(self) -> Dict:
        """测试所有模型"""
        print("开始测试所有模型...")
        
        results = {}
        models_to_test = [self.model_config['primary']] + self.model_config['fallbacks']
        
        for model in models_to_test:
            result = self.test_model_availability(model)
            results[model] = result
            
            # 记录测试
            self.monitoring_status['model_tests_today'] += 1
        
        self.monitoring_status['last_check'] = datetime.now()
        
        # 保存测试结果
        self.save_test_results(results)
        
        return results
    
    def analyze_test_results(self, results: Dict) -> Dict:
        """分析测试结果"""
        analysis = {
            'available_models': [],
            'unavailable_models': [],
            'performance_ranking': [],
            'recommendations': []
        }
        
        for model, result in results.items():
            if result['success']:
                analysis['available_models'].append({
                    'model': model,
                    'response_time': result['response_time'],
                    'quality_score': result['quality_score']
                })
            else:
                analysis['unavailable_models'].append({
                    'model': model,
                    'error': result['error']
                })
        
        # 按性能排序
        analysis['available_models'].sort(key=lambda x: x['quality_score'], reverse=True)
        
        # 生成推荐
        if analysis['available_models']:
            best_model = analysis['available_models'][0]
            
            # 检查是否需要切换主模型
            current_primary = self.model_config['primary']
            if current_primary != best_model['model']:
                analysis['recommendations'].append({
                    'type': 'switch_primary',
                    'current': current_primary,
                    'recommended': best_model['model'],
                    'reason': f"性能更好 (质量分: {best_model['quality_score']:.2f})"
                })
        
        # 检查是否有模型需要关注
        for unavailable in analysis['unavailable_models']:
            analysis['recommendations'].append({
                'type': 'model_unavailable',
                'model': unavailable['model'],
                'reason': unavailable['error'],
                'action': '检查API状态或账户余额'
            })
        
        return analysis
    
    def generate_alert(self, analysis: Dict, test_results: Dict) -> Optional[Dict]:
        """生成警报"""
        alerts = []
        
        # 检查主模型状态
        primary_model = self.model_config['primary']
        primary_result = test_results.get(primary_model, {})
        
        if not primary_result.get('success', False):
            alerts.append({
                'level': 'critical',
                'type': 'primary_model_down',
                'model': primary_model,
                'message': f'主模型 {primary_model} 不可用',
                'details': primary_result.get('error', '未知错误'),
                'action': '自动切换到备用模型'
            })
        
        # 检查备用模型状态
        unavailable_fallbacks = []
        for model in self.model_config['fallbacks']:
            result = test_results.get(model, {})
            if not result.get('success', False):
                unavailable_fallbacks.append(model)
        
        if unavailable_fallbacks:
            alerts.append({
                'level': 'warning',
                'type': 'fallback_models_down',
                'models': unavailable_fallbacks,
                'message': f'{len(unavailable_fallbacks)}个备用模型不可用',
                'details': '减少系统冗余度',
                'action': '检查并修复备用模型'
            })
        
        # 检查可用模型数量
        available_count = len(analysis['available_models'])
        if available_count == 0:
            alerts.append({
                'level': 'critical',
                'type': 'all_models_down',
                'message': '所有模型均不可用',
                'details': '系统无法正常工作',
                'action': '需要立即人工干预'
            })
        elif available_count == 1:
            alerts.append({
                'level': 'warning',
                'type': 'single_model_available',
                'model': analysis['available_models'][0]['model'],
                'message': '仅剩一个可用模型',
                'details': '系统冗余度不足',
                'action': '建议尽快修复其他模型'
            })
        
        # 检查性能问题
        for available in analysis['available_models']:
            if available['quality_score'] < 0.6:
                alerts.append({
                    'level': 'warning',
                    'type': 'model_performance_low',
                    'model': available['model'],
                    'message': f'模型 {available["model"]} 性能较低',
                    'details': f'质量分: {available["quality_score"]:.2f}',
                    'action': '监控性能变化'
                })
        
        return alerts if alerts else None
    
    def send_feishu_alert(self, alert: Dict) -> bool:
        """发送Feishu警报"""
        try:
            # 构建消息
            level_emoji = {
                'critical': '🔴',
                'warning': '🟡',
                'info': '🟢'
            }
            
            message = f"""{level_emoji.get(alert['level'], '⚪')} **模型管理警报**

**级别**: {alert['level'].upper()}
**类型**: {alert['type']}
**消息**: {alert['message']}
**详情**: {alert.get('details', '无')}
**建议操作**: {alert.get('action', '请检查')}

**时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**系统**: OpenClaw Model Management System
"""
            
            print(f"\n发送Feishu警报:")
            print(message)
            
            # 这里应该调用Feishu API发送消息
            # 暂时记录到日志
            
            self.log_alert(alert, message)
            self.monitoring_status['alerts_sent_today'] += 1
            
            return True
            
        except Exception as e:
            print(f"发送警报失败: {e}")
            return False
    
    def auto_switch_model(self, analysis: Dict) -> bool:
        """自动切换模型"""
        if not analysis['available_models']:
            print("没有可用模型，无法切换")
            return False
        
        # 选择最佳模型
        best_model = analysis['available_models'][0]['model']
        current_primary = self.model_config['primary']
        
        if best_model == current_primary:
            print(f"当前主模型 {current_primary} 已是最佳选择")
            return False
        
        print(f"准备切换主模型: {current_primary} -> {best_model}")
        
        # 构建新的fallback列表
        new_fallbacks = []
        for model in [current_primary] + self.model_config['fallbacks']:
            if model != best_model and model in [m['model'] for m in analysis['available_models']]:
                new_fallbacks.append(model)
        
        # 更新配置
        if self.update_model_priority(best_model, new_fallbacks):
            self.monitoring_status['last_model_switch'] = datetime.now()
            
            # 发送切换通知
            switch_alert = {
                'level': 'info',
                'type': 'model_switched',
                'model': best_model,
                'message': f'主模型已自动切换为 {best_model}',
                'details': f'从 {current_primary} 切换到 {best_model}',
                'action': '系统将继续监控模型状态'
            }
            
            self.send_feishu_alert(switch_alert)
            
            return True
        else:
            return False
    
    def run_monitoring_cycle(self, interval_minutes: int = 5):
        """运行监控周期"""
        print("="*60)
        print("模型管理系统 - 监控模式")
        print("="*60)
        
        cycle_count = 0
        
        while True:
            cycle_count += 1
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 监控周期 #{cycle_count}")
            
            try:
                # 1. 测试所有模型
                test_results = self.test_all_models()
                
                # 2. 分析结果
                analysis = self.analyze_test_results(test_results)
                
                # 3. 生成警报
                alerts = self.generate_alert(analysis, test_results)
                
                # 4. 发送警报
                if alerts:
                    for alert in alerts:
                        if alert['level'] in ['critical', 'warning']:
                            self.send_feishu_alert(alert)
                
                # 5. 自动切换（如果需要）
                if alerts and any(a['level'] == 'critical' and a['type'] == 'primary_model_down' for a in alerts):
                    print("检测到主模型故障，尝试自动切换...")
                    self.auto_switch_model(analysis)
                
                # 6. 显示状态
                self.display_status(analysis)
                
                # 7. 等待下一次检查
                print(f"\n等待 {interval_minutes} 分钟后再次检查...")
                time.sleep(interval_minutes * 60)
                
            except KeyboardInterrupt:
                print("\n监控已停止")
                break
            except Exception as e:
                print(f"监控循环错误: {e}")
                time.sleep(60)  # 出错后等待1分钟
    
    def display_status(self, analysis: Dict):
        """显示状态"""
        print("\n当前状态:")
        print(f"  主模型: {self.model_config['primary']}")
        print(f"  备用模型: {', '.join(self.model_config['fallbacks'])}")
        print(f"  可用模型: {len(analysis['available_models'])}个")
        print(f"  不可用模型: {len(analysis['unavailable_models'])}个")
        
        if analysis['available_models']:
            print("\n可用模型性能排名:")
            for i, model_info in enumerate(analysis['available_models'][:3], 1):
                print(f"  {i}. {model_info['model']} - 质量分: {model_info['quality_score']:.2f}")
        
        if analysis['recommendations']:
            print("\n建议:")
            for rec in analysis['recommendations']:
                print(f"  • {rec['reason']}")
    
    def log_change(self, change_data: Dict):
        """记录更改"""
        log_file = os.path.join(self.log_dir, f"changes_{datetime.now().strftime('%Y%m')}.jsonl")
        
        try:
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(change_data, ensure_ascii=False) + '\n')
        except Exception as e:
            print(f"记录更改失败: {e}")
    
    def log_alert(self, alert: Dict, message: str):
        """记录警报"""
        log_file = os.path.join(self.log_dir, f"alerts_{datetime.now().strftime('%Y%m%d')}.jsonl")
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'alert': alert,
            'message': message
        }
        
        try:
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
        except Exception as e:
            print(f"记录警报失败: {e}")
    
    def save_test_results(self, results: Dict):
        """保存测试结果"""
        log_file = os.path.join(self.log_dir, f"tests_{datetime.now().strftime('%Y%m%d')}.jsonl")
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'results': results
        }
        
        try:
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
        except Exception as e:
            print(f"保存测试结果失败: {e}")
    
    def get_daily_report(self) -> Dict:
        """获取日报"""
        today = datetime.now().strftime('%Y%m%d')
        
        report = {
            'date': today,
            'tests_today': self.monitoring_status['model_tests_today'],
            'alerts_today': self.monitoring_status['alerts_sent_today'],
            'last_check': self.monitoring_status['last_check'].isoformat() if self.monitoring_status['last_check'] else None,
            'last_switch': self.monitoring_status['last_model_switch'].isoformat() if self.monitoring_status['last_model_switch'] else None,
            'current_config': self.model_config
        }
        
        return report

def main():
    """主函数"""
    print("