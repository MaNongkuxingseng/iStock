#!/usr/bin/env python3
"""
iStock 自动化监控与分析系统
提供自动化的服务监控、分析反馈和消息推送
"""

import asyncio
import aiohttp
import schedule
import time
import json
import logging
from datetime import datetime, date
from typing import Dict, Any, List, Optional
import sys
import os

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('automated_monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AutomatedMonitor:
    """自动化监控器"""
    
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.health_endpoint = f"{self.base_url}/health"
        self.docs_endpoint = f"{self.base_url}/docs"
        self.api_base = f"{self.base_url}/api/v1"
        
        # 监控状态
        self.monitor_state = {
            "last_check": None,
            "service_status": {},
            "error_count": 0,
            "success_count": 0,
            "alerts_sent": 0
        }
        
        # 加载状态文件
        self.state_file = "monitor_state.json"
        self.load_state()
    
    def load_state(self):
        """加载监控状态"""
        try:
            if os.path.exists(self.state_file):
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    self.monitor_state = json.load(f)
                logger.info(f"加载监控状态: {self.monitor_state['last_check']}")
        except Exception as e:
            logger.error(f"加载状态文件失败: {e}")
    
    def save_state(self):
        """保存监控状态"""
        try:
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(self.monitor_state, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"保存状态文件失败: {e}")
    
    async def check_service_health(self) -> Dict[str, Any]:
        """检查服务健康状态"""
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
                # 检查健康端点
                async with session.get(self.health_endpoint) as response:
                    health_status = await response.json() if response.status == 200 else None
                
                # 检查API文档
                async with session.get(self.docs_endpoint) as response:
                    docs_status = response.status == 200
                
                # 检查股票API
                stocks_url = f"{self.api_base}/stocks"
                async with session.get(stocks_url) as response:
                    stocks_status = response.status == 200
                
                result = {
                    "timestamp": datetime.now().isoformat(),
                    "health_endpoint": {
                        "status": response.status if 'response' in locals() else "error",
                        "data": health_status
                    },
                    "docs_endpoint": docs_status,
                    "stocks_api": stocks_status,
                    "overall": health_status is not None and docs_status and stocks_status
                }
                
                self.monitor_state["success_count"] += 1
                logger.info(f"服务检查成功: {result['overall']}")
                
                return result
                
        except Exception as e:
            self.monitor_state["error_count"] += 1
            logger.error(f"服务检查失败: {e}")
            
            return {
                "timestamp": datetime.now().isoformat(),
                "error": str(e),
                "overall": False
            }
    
    def analyze_service_status(self, health_data: Dict[str, Any]) -> Dict[str, Any]:
        """分析服务状态"""
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "status": "healthy" if health_data.get("overall", False) else "unhealthy",
            "issues": [],
            "recommendations": [],
            "severity": "low"
        }
        
        if not health_data.get("overall", False):
            analysis["issues"].append("服务不可用或部分不可用")
            analysis["severity"] = "high"
            
            if "error" in health_data:
                analysis["issues"].append(f"错误: {health_data['error']}")
            
            analysis["recommendations"].append("检查Docker Desktop是否运行")
            analysis["recommendations"].append("查看服务日志: docker-compose logs")
            analysis["recommendations"].append("重启服务: docker-compose restart")
        
        # 检查响应时间
        if health_data.get("health_endpoint", {}).get("data"):
            response_time = health_data.get("response_time_ms", 0)
            if response_time > 1000:
                analysis["issues"].append(f"响应时间过长: {response_time}ms")
                analysis["severity"] = "medium"
                analysis["recommendations"].append("优化数据库查询")
                analysis["recommendations"].append("检查服务器负载")
        
        return analysis
    
    async def send_alert(self, analysis: Dict[str, Any], is_test: bool = False):
        """发送警报消息"""
        try:
            # 构建消息
            if is_test:
                title = "🚨 iStock 测试警报"
                message = "这是一条严重的测试警报消息，用于验证监控系统工作正常。"
                severity = "critical"
            else:
                title = f"⚠️ iStock 服务{alysis['severity'].upper()}警报"
                message = self._format_alert_message(analysis)
                severity = analysis["severity"]
            
            alert_data = {
                "title": title,
                "message": message,
                "severity": severity,
                "timestamp": analysis["timestamp"],
                "is_test": is_test,
                "monitor_state": {
                    "error_count": self.monitor_state["error_count"],
                    "success_count": self.monitor_state["success_count"],
                    "alerts_sent": self.monitor_state["alerts_sent"] + 1
                }
            }
            
            # 在实际实现中，这里应该调用消息推送API
            # 这里先记录到日志和文件
            
            logger.warning(f"发送警报: {title}")
            logger.warning(f"消息内容: {message}")
            
            # 保存警报记录
            self._save_alert_record(alert_data)
            
            # 更新状态
            self.monitor_state["alerts_sent"] += 1
            self.monitor_state["last_alert"] = datetime.now().isoformat()
            
            # 发送到Feishu（模拟）
            await self._send_to_feishu(alert_data)
            
            return True
            
        except Exception as e:
            logger.error(f"发送警报失败: {e}")
            return False
    
    def _format_alert_message(self, analysis: Dict[str, Any]) -> str:
        """格式化警报消息"""
        lines = []
        
        lines.append(f"📊 iStock 服务状态分析")
        lines.append(f"时间: {analysis['timestamp']}")
        lines.append(f"状态: {analysis['status'].upper()}")
        lines.append(f"严重程度: {analysis['severity'].upper()}")
        
        if analysis["issues"]:
            lines.append("")
            lines.append("❌ 发现问题:")
            for issue in analysis["issues"]:
                lines.append(f"  • {issue}")
        
        if analysis["recommendations"]:
            lines.append("")
            lines.append("💡 建议操作:")
            for rec in analysis["recommendations"]:
                lines.append(f"  • {rec}")
        
        lines.append("")
        lines.append("📈 监控统计:")
        lines.append(f"  成功检查: {self.monitor_state['success_count']}")
        lines.append(f"  失败检查: {self.monitor_state['error_count']}")
        lines.append(f"  警报发送: {self.monitor_state['alerts_sent']}")
        
        return "\n".join(lines)
    
    def _save_alert_record(self, alert_data: Dict[str, Any]):
        """保存警报记录"""
        try:
            alert_file = "alerts_history.json"
            alerts = []
            
            if os.path.exists(alert_file):
                with open(alert_file, 'r', encoding='utf-8') as f:
                    alerts = json.load(f)
            
            alerts.append(alert_data)
            
            # 只保留最近100条记录
            if len(alerts) > 100:
                alerts = alerts[-100:]
            
            with open(alert_file, 'w', encoding='utf-8') as f:
                json.dump(alerts, f, indent=2, default=str)
                
        except Exception as e:
            logger.error(f"保存警报记录失败: {e}")
    
    async def _send_to_feishu(self, alert_data: Dict[str, Any]):
        """发送到Feishu（模拟实现）"""
        try:
            # 在实际实现中，这里应该调用Feishu API
            # 这里模拟发送
            
            feishu_message = {
                "msg_type": "interactive",
                "card": {
                    "config": {
                        "wide_screen_mode": True
                    },
                    "header": {
                        "title": {
                            "tag": "plain_text",
                            "content": alert_data["title"]
                        },
                        "template": "red" if alert_data["severity"] in ["high", "critical"] else "yellow"
                    },
                    "elements": [
                        {
                            "tag": "div",
                            "text": {
                                "tag": "lark_md",
                                "content": alert_data["message"]
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
                                    "content": f"iStock 自动化监控系统 | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                                }
                            ]
                        }
                    ]
                }
            }
            
            logger.info(f"模拟发送到Feishu: {alert_data['title']}")
            
            # 在实际实现中，这里应该调用Feishu API
            # import requests
            # webhook_url = "YOUR_FEISHU_WEBHOOK_URL"
            # response = requests.post(webhook_url, json=feishu_message)
            
            return True
            
        except Exception as e:
            logger.error(f"发送到Feishu失败: {e}")
            return False
    
    def is_trading_day(self) -> bool:
        """判断是否为交易日"""
        today = date.today()
        weekday = today.weekday()  # 0=Monday, 6=Sunday
        
        # 简单判断：周一到周五为交易日
        if weekday < 5:  # 0-4 = Monday to Friday
            # 检查是否为节假日（这里需要实际的节假日数据）
            # 暂时简单返回True
            return True
        
        return False
    
    async def run_stock_analysis(self):
        """运行股票分析"""
        if not self.is_trading_day():
            logger.info("非交易日，跳过股票分析")
            return
        
        try:
            logger.info("开始股票分析...")
            
            # 模拟分析结果
            analysis_result = {
                "timestamp": datetime.now().isoformat(),
                "market_status": "open",
                "analyzed_stocks": 10,
                "alerts_found": 3,
                "recommendations": [
                    {"symbol": "AAPL", "action": "BUY", "reason": "技术指标向好"},
                    {"symbol": "TSLA", "action": "HOLD", "reason": "波动较大，建议观望"},
                    {"symbol": "MSFT", "action": "SELL", "reason": "达到目标价位"}
                ],
                "portfolio_health": "good",
                "risk_level": "medium"
            }
            
            # 保存分析结果
            self._save_analysis_result(analysis_result)
            
            # 如果有重要发现，发送警报
            if analysis_result["alerts_found"] > 0:
                await self.send_stock_alert(analysis_result)
            
            logger.info(f"股票分析完成: {analysis_result}")
            
        except Exception as e:
            logger.error(f"股票分析失败: {e}")
    
    def _save_analysis_result(self, analysis: Dict[str, Any]):
        """保存分析结果"""
        try:
            analysis_file = "stock_analysis_history.json"
            analyses = []
            
            if os.path.exists(analysis_file):
                with open(analysis_file, 'r', encoding='utf-8') as f:
                    analyses = json.load(f)
            
            analyses.append(analysis)
            
            # 只保留最近50条记录
            if len(analyses) > 50:
                analyses = analyses[-50:]
            
            with open(analysis_file, 'w', encoding='utf-8') as f:
                json.dump(analyses, f, indent=2, default=str)
                
        except Exception as e:
            logger.error(f"保存分析结果失败: {e}")
    
    async def send_stock_alert(self, analysis: Dict[str, Any]):
        """发送股票警报"""
        try:
            title = "📈 股票分析警报"
            
            message_lines = []
            message_lines.append("📊 今日股票分析结果")
            message_lines.append(f"时间: {analysis['timestamp']}")
            message_lines.append(f"分析股票数: {analysis['analyzed_stocks']}")
            message_lines.append(f"发现警报: {analysis['alerts_found']}个")
            message_lines.append(f"投资组合健康度: {analysis['portfolio_health'].upper()}")
            message_lines.append(f"风险等级: {analysis['risk_level'].upper()}")
            
            if analysis["recommendations"]:
                message_lines.append("")
                message_lines.append("💡 交易建议:")
                for rec in analysis["recommendations"]:
                    action_emoji = "🟢" if rec["action"] == "BUY" else "🟡" if rec["action"] == "HOLD" else "🔴"
                    message_lines.append(f"  {action_emoji} {rec['symbol']}: {rec['action']} - {rec['reason']}")
            
            message = "\n".join(message_lines)
            
            alert_data = {
                "title": title,
                "message": message,
                "severity": "medium",
                "type": "stock_analysis",
                "timestamp": analysis["timestamp"]
            }
            
            # 发送警报
            await self._send_to_feishu(alert_data)
            
            logger.info(f"发送股票分析警报: {title}")
            
        except Exception as e:
            logger.error(f"发送股票警报失败: {e}")
    
    async def run_monitoring_cycle(self, is_test: bool = False):
        """运行监控周期"""
        logger.info("开始监控周期..." if not is_test else "开始测试监控周期...")
        
        # 更新状态
        self.monitor_state["last_check"] = datetime.now().isoformat()
        
        # 检查服务健康
        health_data = await self.check_service_health()
        
        # 分析状态
        analysis = self.analyze_service_status(health_data)
        
        # 保存状态
        self.save_state()
        
        # 如果需要发送警报
        if not analysis["overall"] or is_test:
            await self.send_alert(analysis, is_test=is_test)
        
        # 如果是交易日，运行股票分析
        if self.is_trading_day() and not is_test:
            await self.run_stock_analysis()
        
        logger.info(f"监控周期完成: 状态={analysis['status']}, 严重程度={analysis['severity']}")
        
        return analysis
    
    def setup_schedule(self):
        """设置定时任务"""
        # 每30分钟检查一次服务健康
        schedule.every(30).minutes.do(
            lambda: asyncio.create_task(self.run_monitoring_cycle())
        )
        
        # 交易日每天9:30、13:00运行股票分析
        schedule.every().day.at("09:30").do(
            lambda: asyncio.create_task(self.run_stock_analysis() if self.is_trading_day() else None)
        )
        schedule.every().day.at("13:00").do(
            lambda: asyncio.create_task(self.run_stock_analysis() if self.is_trading_day() else None)
        )
        
        # 每天23:00发送日报
        schedule.every().day.at("23:00").do(
            lambda: asyncio.create_task(self.send_daily_report())
        )
        
        logger.info("定时任务设置完成")
    
    async def send_daily_report(self):
        """发送日报"""
        try:
            today = date.today().isoformat()
            
            report = {
                "date": today,
                "checks_today": self.monitor_state["success_count"] + self.monitor_state["error_count"],
                "success_rate": self.monitor_state["success_count"] / (self.monitor_state["success_count"] + self.monitor_state["error_count"]) * 100 if (self.monitor_state["success_count"] + self.monitor_state["error_count"]) > 0 else 0,
                "alerts_sent": self.monitor_state["alerts_sent"],
                "trading_day": self.is_trading_day(),
                "last_check": self.monitor_state["last_check"]
            }
            
            title = f"📅 iStock 每日报告 ({today})"
            
            message_lines = []
            message_lines.append(f"📊 {today} 监控报告")
            message_lines.append(f"检查次数: {report['checks_today']}")
            message_lines.append(f"成功率: {report['success_rate']:.1f}%")
            message_lines.append(f"警报发送: {report['alerts_sent']}")
            message_lines.append(f"交易日: {'是' if report['trading_day'] else '否'}")
            message_lines.append(f"最后检查: {report['last_check']}")
            
            message = "\n".join(message_lines)
            
            await self._send_to_feishu({
                "title": title,
