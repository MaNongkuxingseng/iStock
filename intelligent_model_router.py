#!/usr/bin/env python3
"""
智能模型路由系统
根据任务复杂度自动选择最佳模型
"""

import re
from typing import Dict, List, Tuple, Optional

class IntelligentModelRouter:
    """智能模型路由器"""
    
    def __init__(self):
        # 模型能力定义
        self.model_capabilities = {
            'deepseek/deepseek-chat': {
                'complexity_threshold': 70,  # 处理中等复杂度任务
                'strengths': ['代码生成', '逻辑推理', '中文理解', '常规对话'],
                'weaknesses': ['创意写作', '复杂分析', '多轮深度对话'],
                'cost': 'low',
                'speed': 'fast'
            },
            'openai-codex/gpt-5.3-codex': {
                'complexity_threshold': 90,  # 处理高复杂度任务
                'strengths': ['复杂分析', '创意写作', '深度推理', '多轮对话'],
                'weaknesses': ['成本较高', '可能限流'],
                'cost': 'high',
                'speed': 'medium'
            },
            'qwen/qwen-plus': {
                'complexity_threshold': 80,  # 处理中高复杂度任务
                'strengths': ['中文处理', '本地化内容', '常规分析'],
                'weaknesses': ['创意有限', '深度推理'],
                'cost': 'medium',
                'speed': 'medium'
            }
        }
        
        # 任务类型定义
        self.task_patterns = {
            'simple_chat': {
                'patterns': ['你好', '在吗', '谢谢', '早上好', '晚安'],
                'complexity': 10,
                'recommended_model': 'deepseek/deepseek-chat'
            },
            'stock_analysis': {
                'patterns': ['股票', '持仓', '分析', '盈亏', '技术指标', 'MACD', 'RSI', 'KDJ'],
                'complexity': 75,
                'recommended_model': 'openai-codex/gpt-5.3-codex'
            },
            'code_generation': {
                'patterns': ['代码', '编程', '函数', '算法', 'Python', 'JavaScript', 'bug', '调试'],
                'complexity': 80,
                'recommended_model': 'deepseek/deepseek-chat'
            },
            'complex_analysis': {
                'patterns': ['深度分析', '策略建议', '风险评估', '投资组合', '市场预测'],
                'complexity': 85,
                'recommended_model': 'openai-codex/gpt-5.3-codex'
            },
            'data_processing': {
                'patterns': ['数据', '处理', '分析', '统计', '报表', 'Excel', 'CSV'],
                'complexity': 65,
                'recommended_model': 'deepseek/deepseek-chat'
            },
            'creative_writing': {
                'patterns': ['写作', '创作', '故事', '文章', '文案', '营销', '广告'],
                'complexity': 90,
                'recommended_model': 'openai-codex/gpt-5.3-codex'
            },
            'research': {
                'patterns': ['研究', '调查', '报告', '论文', '学术', '文献'],
                'complexity': 88,
                'recommended_model': 'openai-codex/gpt-5.3-codex'
            }
        }
        
        # 当前模型状态（从监控系统获取）
        self.model_status = {
            'deepseek/deepseek-chat': {'available': True, 'performance': 85},
            'openai-codex/gpt-5.3-codex': {'available': True, 'performance': 0},  # 暂时不可用
            'qwen/qwen-plus': {'available': False, 'performance': 0}  # 欠费不可用
        }
        
        # 使用历史记录
        self.usage_history = []
    
    def analyze_task_complexity(self, task_text: str) -> Dict:
        """分析任务复杂度"""
        complexity_score = 30  # 基础分数
        
        # 长度因素
        text_length = len(task_text)
        if text_length > 500:
            complexity_score += 25
        elif text_length > 200:
            complexity_score += 15
        elif text_length > 100:
            complexity_score += 10
        
        # 任务类型匹配
        matched_tasks = []
        for task_name, task_info in self.task_patterns.items():
            for pattern in task_info['patterns']:
                if pattern.lower() in task_text.lower():
                    matched_tasks.append(task_name)
                    complexity_score = max(complexity_score, task_info['complexity'])
                    break
        
        # 特殊关键词加分
        complexity_keywords = [
            ('复杂', 20), ('深度', 25), ('详细', 15), ('全面', 20),
            ('策略', 25), ('优化', 20), ('算法', 30), ('模型', 25),
            ('分析', 20), ('预测', 25), ('评估', 20), ('建议', 15)
        ]
        
        for keyword, score in complexity_keywords:
            if keyword in task_text:
                complexity_score += score
        
        # 问题数量
        question_count = task_text.count('?') + task_text.count('？')
        complexity_score += min(question_count * 5, 20)
        
        # 限制在0-100之间
        complexity_score = max(10, min(complexity_score, 100))
        
        return {
            'score': complexity_score,
            'level': self._get_complexity_level(complexity_score),
            'matched_tasks': matched_tasks,
            'text_length': text_length,
            'question_count': question_count
        }
    
    def _get_complexity_level(self, score: int) -> str:
        """获取复杂度等级"""
        if score >= 80:
            return 'high'
        elif score >= 60:
            return 'medium_high'
        elif score >= 40:
            return 'medium'
        elif score >= 20:
            return 'low'
        else:
            return 'very_low'
    
    def select_best_model(self, complexity_analysis: Dict, available_models: List[str] = None) -> Tuple[str, Dict]:
        """选择最佳模型"""
        if available_models is None:
            available_models = [m for m, status in self.model_status.items() if status['available']]
        
        complexity_score = complexity_analysis['score']
        
        # 按能力排序可用模型
        suitable_models = []
        for model in available_models:
            if model in self.model_capabilities:
                capability = self.model_capabilities[model]
                
                # 检查是否能处理该复杂度
                if complexity_score <= capability['complexity_threshold']:
                    suitability_score = self._calculate_suitability_score(
                        model, complexity_analysis, capability
                    )
                    
                    suitable_models.append({
                        'model': model,
                        'suitability_score': suitability_score,
                        'capability': capability,
                        'performance': self.model_status.get(model, {}).get('performance', 50)
                    })
        
        if not suitable_models:
            # 没有完全合适的模型，选择能力最强的
            for model in available_models:
                if model in self.model_capabilities:
                    capability = self.model_capabilities[model]
                    suitability_score = self._calculate_suitability_score(
                        model, complexity_analysis, capability
                    )
                    
                    suitable_models.append({
                        'model': model,
                        'suitability_score': suitability_score,
                        'capability': capability,
                        'performance': self.model_status.get(model, {}).get('performance', 50)
                    })
        
        # 按适合度排序
        suitable_models.sort(key=lambda x: x['suitability_score'], reverse=True)
        
        if suitable_models:
            best_model = suitable_models[0]
            
            # 记录使用历史
            self.usage_history.append({
                'timestamp': 'now',  # 实际应该用datetime
                'task_complexity': complexity_score,
                'selected_model': best_model['model'],
                'suitability_score': best_model['suitability_score'],
                'available_models': available_models
            })
            
            return best_model['model'], {
                'reason': f"复杂度{complexity_score}/100，{best_model['model']}最适合",
                'suitability_score': best_model['suitability_score'],
                'alternative_models': [m['model'] for m in suitable_models[1:3]],
                'complexity_level': complexity_analysis['level']
            }
        else:
            # 没有可用模型
            return None, {'reason': '没有可用模型', 'error': '所有模型均不可用'}
    
    def _calculate_suitability_score(self, model: str, complexity_analysis: Dict, capability: Dict) -> float:
        """计算模型适合度分数"""
        score = 0.0
        
        # 复杂度匹配度 (40%)
        complexity_score = complexity_analysis['score']
        threshold = capability['complexity_threshold']
        
        if complexity_score <= threshold:
            # 在能力范围内，越接近阈值越好（留有余量）
            match_ratio = (threshold - complexity_score) / threshold
            score += (1.0 - match_ratio * 0.5) * 40
        else:
            # 超出能力范围，按超出比例扣分
            exceed_ratio = (complexity_score - threshold) / 100
            score += max(0, 40 - exceed_ratio * 40)
        
        # 任务类型匹配 (30%)
        matched_tasks = complexity_analysis['matched_tasks']
        if matched_tasks:
            # 检查模型是否擅长这些任务
            task_match_score = 0
            for task_name in matched_tasks:
                task_info = self.task_patterns[task_name]
                recommended_model = task_info['recommended_model']
                
                if model == recommended_model:
                    task_match_score += 10
                elif any(strength in capability['strengths'] for strength in ['分析', '推理', '代码']):
                    task_match_score += 5
            
            score += min(task_match_score, 30)
        else:
            # 没有明确任务类型，根据通用能力评分
            if '常规对话' in capability['strengths']:
                score += 20
            elif '中文理解' in capability['strengths']:
                score += 15
        
        # 性能因素 (20%)
        performance = self.model_status.get(model, {}).get('performance', 50)
        score += (performance / 100) * 20
        
        # 成本因素 (10%)
        if capability['cost'] == 'low':
            score += 10
        elif capability['cost'] == 'medium':
            score += 7
        else:  # high
            score += 3
        
        return score
    
    def get_recommendation_for_task(self, task_description: str) -> Dict:
        """获取任务推荐"""
        # 分析任务复杂度
        complexity = self.analyze_task_complexity(task_description)
        
        # 选择最佳模型
        best_model, selection_info = self.select_best_model(complexity)
        
        # 获取模型详情
        model_details = None
        if best_model and best_model in self.model_capabilities:
            model_details = self.model_capabilities[best_model]
        
        return {
            'task_analysis': complexity,
            'recommended_model': best_model,
            'selection_info': selection_info,
            'model_details': model_details,
            'available_models': [m for m, s in self.model_status.items() if s['available']],
            'timestamp': 'now'
        }
    
    def update_model_status(self, model: str, available: bool, performance: int = None):
        """更新模型状态"""
        if model in self.model_status:
            self.model_status[model]['available'] = available
            if performance is not None:
                self.model_status[model]['performance'] = performance
    
    def get_system_status(self) -> Dict:
        """获取系统状态"""
        available_count = sum(1 for s in self.model_status.values() if s['available'])
        total_count = len(self.model_status)
        
        return {
            'total_models': total_count,
            'available_models': available_count,
            'availability_rate': (available_count / total_count) * 100 if total_count > 0 else 0,
            'model_status': self.model_status,
            'recent_decisions': self.usage_history[-5:] if self.usage_history else [],
            'router_version': '1.0'
        }

# 使用示例
def main():
    """主函数示例"""
    router = IntelligentModelRouter()
    
    # 更新模型状态（模拟）
    router.update_model_status('openai-codex/gpt-5.3-codex', False)  # 暂时不可用
    router.update_model_status('qwen/qwen-plus', False)  # 欠费不可用
    router.update_model_status('deepseek/deepseek-chat', True, 85)
    
    # 测试任务
    test_tasks = [
        "你好，今天天气怎么样？",
        "请帮我分析一下我的股票持仓，包括技术指标和风险",
        "写一个Python函数计算斐波那契数列",
        "深度分析当前市场趋势和投资策略建议",
        "处理这个CSV文件并生成统计报表"
    ]
    
    print("智能模型路由系统测试")
    print("="*60)
    
    for i, task in enumerate(test_tasks, 1):
        print(f"\n任务{i}: {task[:50]}...")
        
        recommendation = router.get_recommendation_for_task(task)
        
        print(f"  复杂度: {recommendation['task_analysis']['score']}/100 ({recommendation['task_analysis']['level']})")
        print(f"  推荐模型: {recommendation['recommended_model']}")
        print(f"  理由: {recommendation['selection_info']['reason']}")
        
        if recommendation['model_details']:
            print(f"  模型能力: {', '.join(recommendation['model_details']['strengths'][:3])}")
    
    # 显示系统状态
    print("\n" + "="*60)
    print("系统状态:")
    status = router.get_system_status()
    print(f"  总模型数: {status['total_models']}")
    print(f"  可用模型: {status['available_models']}")
    print(f"  可用率: {status['availability_rate']:.1f}%")
    
    print("\n模型状态详情:")
    for model, info in status['model_status'].items():
        status_emoji = '🟢' if info['available'] else '🔴'
        print(f"  {status_emoji} {model}: {'可用' if info['available'] else '不可用'}")

if __name__ == "__main__":
    main()