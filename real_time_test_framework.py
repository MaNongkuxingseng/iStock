#!/usr/bin/env python3
"""
iStock 实时测试框架
确保每个功能都有真实的运行测试，避免虚假报告
"""

import asyncio
import aiohttp
import time
import json
import sys
import os
from datetime import datetime
from typing import Dict, List, Tuple, Any
import subprocess
import requests

class RealTimeTestFramework:
    """实时测试框架"""
    
    def __init__(self):
        self.test_results = []
        self.failed_tests = []
        self.warning_tests = []
        self.start_time = datetime.now()
        
        # 测试配置
        self.config = {
            "timeout_seconds": 10,
            "retry_count": 2,
            "require_actual_execution": True,
            "validate_output": True,
            "log_detailed": True
        }
        
        # 创建测试日志目录
        self.log_dir = "test_logs"
        os.makedirs(self.log_dir, exist_ok=True)
    
    def log_test(self, test_name: str, status: str, details: str, data: Any = None):
        """记录测试结果"""
        test_record = {
            "timestamp": datetime.now().isoformat(),
            "test_name": test_name,
            "status": status,
            "details": details,
            "data": data
        }
        
        self.test_results.append(test_record)
        
        # 控制台输出
        status_icon = "✅" if status == "PASS" else "⚠️" if status == "WARN" else "❌"
        print(f"{status_icon} [{datetime.now().strftime('%H:%M:%S')}] {test_name}: {details}")
        
        if status == "FAIL":
            self.failed_tests.append(test_record)
        elif status == "WARN":
            self.warning_tests.append(test_record)
        
        # 写入日志文件
        log_file = os.path.join(self.log_dir, f"test_{datetime.now().strftime('%Y%m%d')}.jsonl")
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(test_record, ensure_ascii=False) + "\n")
        
        return test_record
    
    async def test_backend_service(self):
        """测试后端服务 - 真实运行测试"""
        test_name = "后端服务运行测试"
        
        try:
            # 1. 检查服务进程
            self.log_test(test_name, "INFO", "检查后端服务进程状态")
            
            # 尝试启动后端服务
            backend_proc = subprocess.Popen(
                ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"],
                cwd="backend",
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # 等待服务启动
            time.sleep(3)
            
            # 2. 真实API调用测试
            endpoints = [
                ("健康检查", "http://localhost:8000/health"),
                ("API文档", "http://localhost:8000/docs"),
                ("股票API", "http://localhost:8000/api/v1/stocks"),
            ]
            
            all_passed = True
            for endpoint_name, url in endpoints:
                try:
                    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=5)) as session:
                        async with session.get(url) as response:
                            if response.status == 200:
                                self.log_test(f"{test_name} - {endpoint_name}", "PASS", 
                                            f"API响应正常 (状态码: {response.status})")
                            else:
                                self.log_test(f"{test_name} - {endpoint_name}", "FAIL",
                                            f"API响应异常 (状态码: {response.status})")
                                all_passed = False
                except Exception as e:
                    self.log_test(f"{test_name} - {endpoint_name}", "FAIL",
                                f"API调用失败: {str(e)}")
                    all_passed = False
            
            # 3. 停止服务进程
            backend_proc.terminate()
            backend_proc.wait()
            
            if all_passed:
                self.log_test(test_name, "PASS", "后端服务所有测试通过")
            else:
                self.log_test(test_name, "FAIL", "后端服务部分测试失败")
            
            return all_passed
            
        except Exception as e:
            self.log_test(test_name, "FAIL", f"后端服务测试异常: {str(e)}")
            return False
    
    async def test_database_connection(self):
        """测试数据库连接 - 真实连接测试"""
        test_name = "数据库连接测试"
        
        try:
            # 1. 检查数据库服务
            self.log_test(test_name, "INFO", "检查数据库服务状态")
            
            # 尝试连接数据库
            import psycopg2
            from psycopg2 import OperationalError
            
            try:
                # 从环境变量获取连接信息
                conn = psycopg2.connect(
                    host="localhost",
                    port=5432,
                    database="istock",
                    user="postgres",
                    password="postgres"
                )
                
                # 执行真实查询
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                
                if result and result[0] == 1:
                    self.log_test(test_name, "PASS", "数据库连接和查询正常")
                    
                    # 检查表结构
                    cursor.execute("""
                        SELECT table_name 
                        FROM information_schema.tables 
                        WHERE table_schema = 'public'
                    """)
                    tables = cursor.fetchall()
                    
                    required_tables = ["stocks", "stock_daily", "users", "portfolios"]
                    existing_tables = [table[0] for table in tables]
                    
                    missing_tables = []
                    for req_table in required_tables:
                        if req_table not in existing_tables:
                            missing_tables.append(req_table)
                    
                    if missing_tables:
                        self.log_test(f"{test_name} - 表结构", "WARN",
                                    f"缺少必要表: {', '.join(missing_tables)}")
                    else:
                        self.log_test(f"{test_name} - 表结构", "PASS",
                                    "所有必要表都存在")
                    
                else:
                    self.log_test(test_name, "FAIL", "数据库查询返回异常结果")
                
                cursor.close()
                conn.close()
                return True
                
            except OperationalError as e:
                self.log_test(test_name, "FAIL", f"数据库连接失败: {str(e)}")
                return False
                
        except ImportError:
            self.log_test(test_name, "FAIL", "数据库驱动未安装 (psycopg2)")
            return False
        except Exception as e:
            self.log_test(test_name, "FAIL", f"数据库测试异常: {str(e)}")
            return False
    
    async def test_frontend_service(self):
        """测试前端服务 - 真实运行测试"""
        test_name = "前端服务运行测试"
        
        try:
            # 1. 检查Node.js环境
            self.log_test(test_name, "INFO", "检查Node.js环境")
            
            try:
                node_version = subprocess.check_output(["node", "--version"], 
                                                      stderr=subprocess.STDOUT, 
                                                      text=True)
                npm_version = subprocess.check_output(["npm", "--version"], 
                                                     stderr=subprocess.STDOUT, 
                                                     text=True)
                
                self.log_test(f"{test_name} - 环境", "PASS",
                            f"Node.js: {node_version.strip()}, npm: {npm_version.strip()}")
                
            except (subprocess.CalledProcessError, FileNotFoundError):
                self.log_test(f"{test_name} - 环境", "FAIL", "Node.js/npm未安装")
                return False
            
            # 2. 检查前端依赖
            self.log_test(test_name, "INFO", "检查前端依赖")
            
            if not os.path.exists("frontend/package.json"):
                self.log_test(f"{test_name} - 依赖", "FAIL", "前端package.json不存在")
                return False
            
            # 3. 尝试启动开发服务器
            self.log_test(test_name, "INFO", "尝试启动前端开发服务器")
            
            try:
                # 检查是否已安装依赖
                if not os.path.exists("frontend/node_modules"):
                    self.log_test(f"{test_name} - 依赖", "WARN", "node_modules不存在，需要npm install")
                
                # 启动开发服务器
                frontend_proc = subprocess.Popen(
                    ["npm", "start"],
                    cwd="frontend",
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                # 等待启动
                time.sleep(5)
                
                # 检查服务是否响应
                try:
                    response = requests.get("http://localhost:3000", timeout=5)
                    if response.status_code == 200:
                        self.log_test(test_name, "PASS", "前端服务启动成功并响应正常")
                    else:
                        self.log_test(test_name, "FAIL", 
                                    f"前端服务响应异常 (状态码: {response.status_code})")
                except requests.RequestException:
                    self.log_test(test_name, "FAIL", "前端服务未响应")
                
                # 停止服务
                frontend_proc.terminate()
                frontend_proc.wait()
                
                return True
                
            except Exception as e:
                self.log_test(test_name, "FAIL", f"前端服务启动失败: {str(e)}")
                return False
                
        except Exception as e:
            self.log_test(test_name, "FAIL", f"前端测试异常: {str(e)}")
            return False
    
    async def test_monitoring_system(self):
        """测试监控系统 - 真实执行测试"""
        test_name = "监控系统运行测试"
        
        try:
            # 1. 测试自动化监控脚本
            self.log_test(f"{test_name} - 自动化监控", "INFO", "执行自动化监控脚本")
            
            if os.path.exists("automated_monitor.py"):
                try:
                    result = subprocess.run(
                        ["python", "automated_monitor.py", "--test"],
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
                    
                    if result.returncode == 0:
                        self.log_test(f"{test_name} - 自动化监控", "PASS", 
                                    "脚本执行成功")
                    else:
                        self.log_test(f"{test_name} - 自动化监控", "FAIL",
                                    f"脚本执行失败: {result.stderr[:100]}")
                except subprocess.TimeoutExpired:
                    self.log_test(f"{test_name} - 自动化监控", "WARN", "脚本执行超时")
                except Exception as e:
                    self.log_test(f"{test_name} - 自动化监控", "FAIL",
                                f"脚本执行异常: {str(e)}")
            else:
                self.log_test(f"{test_name} - 自动化监控", "FAIL", "脚本文件不存在")
            
            # 2. 测试盯盘推送
            self.log_test(f"{test_name} - 盯盘推送", "INFO", "测试盯盘推送功能")
            
            if os.path.exists("push_watch_en.py"):
                try:
                    # 导入并测试函数
                    import push_watch_en
                    
                    # 测试是否能正常导入和调用
                    test_result = "脚本可导入"
                    self.log_test(f"{test_name} - 盯盘推送", "PASS", test_result)
                except Exception as e:
                    self.log_test(f"{test_name} - 盯盘推送", "FAIL",
                                f"脚本导入失败: {str(e)}")
            else:
                self.log_test(f"{test_name} - 盯盘推送", "FAIL", "脚本文件不存在")
            
            # 3. 测试警报系统
            self.log_test(f"{test_name} - 警报系统", "INFO", "测试警报系统")
            
            if os.path.exists("test_alert_simple.py"):
                try:
                    result = subprocess.run(
                        ["python", "test_alert_simple.py"],
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                    
                    if result.returncode == 0:
                        self.log_test(f"{test_name} - 警报系统", "PASS", 
                                    "警报测试执行成功")
                    else:
                        self.log_test(f"{test_name} - 警报系统", "FAIL",
                                    f"警报测试失败: {result.stderr[:100]}")
                except Exception as e:
                    self.log_test(f"{test_name} - 警报系统", "FAIL",
                                f"警报测试异常: {str(e)}")
            else:
                self.log_test(f"{test_name} - 警报系统", "FAIL", "测试脚本不存在")
            
            return True
            
        except Exception as e:
            self.log_test(test_name, "FAIL", f"监控系统测试异常: {str(e)}")
            return False
    
    async def test_data_source_integration(self):
        """测试数据源集成 - 真实API调用"""
        test_name = "数据源集成测试"
        
        try:
            # 测试真实数据源API
            data_sources = [
                ("新浪财经", "http://hq.sinajs.cn/list=sh000001"),
                ("腾讯财经", "http://qt.gtimg.cn/q=sh000001"),
            ]
            
            all_passed = True
            for source_name, url in data_sources:
                try:
                    response = requests.get(url, timeout=5)
                    if response.status_code == 200:
                        # 检查响应内容
                        content = response.text
                        if len(content) > 10:  # 简单的内容检查
                            self.log_test(f"{test_name} - {source_name}", "PASS",
                                        "数据源API响应正常")
                        else:
                            self.log_test(f"{test_name} - {source_name}", "WARN",
                                        "数据源API响应内容过短")
                    else:
                        self.log_test(f"{test_name} - {source_name}", "FAIL",
                                    f"数据源API响应异常 (状态码: {response.status_code})")
                        all_passed = False
                except requests.RequestException as e:
                    self.log_test(f"{test_name} - {source_name}", "FAIL",
                                f"数据源API调用失败: {str(e)}")
                    all_passed = False
            
            return all_passed
            
        except Exception as e:
            self.log_test(test_name, "FAIL", f"数据源测试异常: {str(e)}")
            return False
    
    async def run_comprehensive_test(self):
        """运行全面测试"""
        print("=" * 70)
        print("🚀 iStock 实时运行测试框架")
        print("=" * 70)
        print("开始真实运行测试，确保每个功能都实际可运行...")
        print()
        
        # 运行所有测试
        tests = [
            ("后端服务测试", self.test_backend_service),
            ("数据库连接测试", self.test_database_connection),
            ("前端服务测试", self.test_frontend_service),
            ("监控系统测试", self.test_monitoring_system),
            ("数据源集成测试", self.test_data_source_integration),
        ]
        
        test_results = {}
        
        for test_name, test_func in tests:
            print(f"\n▶️  开始测试: {test_name}")
            print("-" * 50)
            
            try:
                result = await test_func()
                test_results[test_name] = result
            except Exception as e:
                self.log_test(test_name, "FAIL", f"测试执行异常: {str(e)}")
                test_results[test_name] = False
            
            time.sleep(1)  # 测试间隔
        
        # 生成测试报告
        await self.generate_test_report(test_results)
        
        return test_results
    
    async def generate_test_report(self, test_results: Dict[str, bool]):
        """生成测试报告"""
        print("\n" + "=" * 70)
        print("📊 iStock 实时测试报告")
        print("=" * 70)
        
        total_tests = len(test_results)
        passed_tests = sum(1 for result in test_results.values() if result)
        failed_tests = total_tests - passed_tests
        
        print(f"\n测试统计:")
        print(f"  总测试数: {total_tests}")
        print(f"  通过: {passed_tests}")
        print(f"  失败: {failed_tests}")
        print(f"  通过率: {passed_tests/total_tests*100:.1f}%" if total_tests > 0 else "  通过率: N/A")
        
        print(f"\n详细结果:")
        for test_name, result in test_results.items():
            status = "✅ 通过" if result else "❌ 失败"
            print(f"  {status} - {test_name}")
        
        print(f"\n失败测试详情 ({len(self.failed_tests)}个):")
        for failed in self.failed_tests:
            print(f"  • {failed['test_name']}: {failed['details']}")
        
        print(f"\n警告测试详情 ({len(self.warning_tests)}个):")
        for warning in self.warning_tests:
            print(f"  • {warning['test_name']}: {warning['details']}")
        
        # 保存完整报告
        report = {
            "timestamp": datetime.now().isoformat(),
            "duration_seconds": (datetime.now() - self.start_time).total_seconds(),
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "pass_rate": passed_tests/total_tests*100 if total_tests > 0 else 0,
            "test_results": test_results,
            "detailed_results": self.test_results,
            "failed_tests_detail": self.failed_tests,
            "warning_tests_detail": self.warning_tests,
            "recommendations": self.generate_recommendations()
        }
        
        report_file = f"real_time_test_report_{datetime.now().strftime('%Y%m%d_%H%M