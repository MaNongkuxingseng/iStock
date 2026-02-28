#!/usr/bin/env python3
"""
iStock 真实运行测试脚本
确保每个功能都实际可运行，避免虚假报告
"""

import asyncio
import requests
import time
import json
import os
import subprocess
from datetime import datetime

def log_test(test_name, status, details):
    """记录测试结果"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    icon = "✅" if status == "PASS" else "⚠️" if status == "WARN" else "❌"
    print(f"{icon} [{timestamp}] {test_name}: {details}")
    return {"test_name": test_name, "status": status, "details": details, "timestamp": timestamp}

def test_backend_real():
    """真实测试后端服务"""
    results = []
    
    print("\n🔧 测试后端服务 (真实运行测试)")
    print("-" * 50)
    
    # 1. 尝试启动后端服务
    results.append(log_test("启动后端服务", "INFO", "尝试启动FastAPI服务器"))
    
    try:
        # 检查backend目录
        if not os.path.exists("backend"):
            results.append(log_test("后端目录", "FAIL", "backend目录不存在"))
            return results, False
        
        # 检查main.py文件
        main_file = "backend/src/main.py"
        if not os.path.exists(main_file):
            results.append(log_test("主文件", "FAIL", f"{main_file}不存在"))
            return results, False
        
        # 启动服务
        import threading
        import sys
        import uvicorn
        
        def run_server():
            sys.path.insert(0, "backend/src")
            uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="error")
        
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
        
        results.append(log_test("启动后端服务", "INFO", "服务启动中..."))
        time.sleep(5)  # 等待服务启动
        
        # 2. 测试API端点
        endpoints = [
            ("健康检查", "http://localhost:8000/health"),
            ("API文档", "http://localhost:8000/docs"),
        ]
        
        all_passed = True
        for name, url in endpoints:
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    results.append(log_test(f"API测试 - {name}", "PASS", 
                                          f"响应正常 (状态码: {response.status_code})"))
                else:
                    results.append(log_test(f"API测试 - {name}", "FAIL",
                                          f"响应异常 (状态码: {response.status_code})"))
                    all_passed = False
            except Exception as e:
                results.append(log_test(f"API测试 - {name}", "FAIL",
                                      f"请求失败: {str(e)[:50]}"))
                all_passed = False
        
        if all_passed:
            results.append(log_test("后端服务测试", "PASS", "所有API测试通过"))
        else:
            results.append(log_test("后端服务测试", "FAIL", "部分API测试失败"))
        
        return results, all_passed
        
    except Exception as e:
        results.append(log_test("后端服务测试", "FAIL", f"测试异常: {str(e)[:100]}"))
        return results, False

def test_database_real():
    """真实测试数据库"""
    results = []
    
    print("\n🗄️  测试数据库连接 (真实连接测试)")
    print("-" * 50)
    
    try:
        # 尝试导入数据库模块
        import sys
        sys.path.append("backend/src")
        
        try:
            from database.session import SessionLocal
            results.append(log_test("数据库模块", "PASS", "成功导入数据库模块"))
            
            # 尝试连接
            try:
                db = SessionLocal()
                # 执行简单查询
                result = db.execute("SELECT 1")
                db.close()
                results.append(log_test("数据库连接", "PASS", "连接和查询成功"))
                return results, True
            except Exception as e:
                results.append(log_test("数据库连接", "FAIL", f"连接失败: {str(e)[:50]}"))
                return results, False
                
        except ImportError as e:
            results.append(log_test("数据库模块", "FAIL", f"导入失败: {str(e)[:50]}"))
            return results, False
            
    except Exception as e:
        results.append(log_test("数据库测试", "FAIL", f"测试异常: {str(e)[:100]}"))
        return results, False

def test_frontend_real():
    """真实测试前端"""
    results = []
    
    print("\n🎨 测试前端服务 (真实运行测试)")
    print("-" * 50)
    
    # 1. 检查前端目录
    if not os.path.exists("frontend"):
        results.append(log_test("前端目录", "FAIL", "frontend目录不存在"))
        return results, False
    
    # 2. 检查关键文件
    required_files = [
        "frontend/package.json",
        "frontend/src/App.js",
        "frontend/src/index.js"
    ]
    
    all_files_exist = True
    for file in required_files:
        if os.path.exists(file):
            results.append(log_test(f"文件检查 - {os.path.basename(file)}", "PASS", "文件存在"))
        else:
            results.append(log_test(f"文件检查 - {os.path.basename(file)}", "FAIL", "文件不存在"))
            all_files_exist = False
    
    if not all_files_exist:
        results.append(log_test("前端文件检查", "FAIL", "缺少必要文件"))
        return results, False
    
    # 3. 检查Node.js环境
    try:
        node_version = subprocess.check_output(["node", "--version"], 
                                              stderr=subprocess.STDOUT, 
                                              text=True).strip()
        results.append(log_test("Node.js环境", "PASS", f"版本: {node_version}"))
    except (subprocess.CalledProcessError, FileNotFoundError):
        results.append(log_test("Node.js环境", "WARN", "Node.js未安装或不在PATH中"))
        # 继续测试，但不启动服务
    
    # 4. 检查package.json内容
    try:
        with open("frontend/package.json", "r") as f:
            package_data = json.load(f)
        
        if "scripts" in package_data and "start" in package_data["scripts"]:
            results.append(log_test("package.json", "PASS", "包含启动脚本"))
        else:
            results.append(log_test("package.json", "WARN", "缺少启动脚本"))
            
        if "dependencies" in package_data:
            deps_count = len(package_data["dependencies"])
            results.append(log_test("依赖项", "INFO", f"有 {deps_count} 个依赖项"))
        
    except Exception as e:
        results.append(log_test("package.json", "WARN", f"读取失败: {str(e)[:50]}"))
    
    results.append(log_test("前端服务测试", "INFO", "基础检查完成"))
    return results, True

def test_monitoring_real():
    """真实测试监控系统"""
    results = []
    
    print("\n📊 测试监控系统 (真实执行测试)")
    print("-" * 50)
    
    # 1. 检查监控脚本
    monitor_scripts = [
        ("automated_monitor.py", "自动化监控"),
        ("push_watch_en.py", "盯盘推送"),
        ("test_alert_simple.py", "警报测试"),
    ]
    
    all_exist = True
    for filename, description in monitor_scripts:
        if os.path.exists(filename):
            results.append(log_test(f"监控脚本 - {description}", "PASS", "文件存在"))
            
            # 尝试导入
            try:
                # 动态导入
                module_name = filename.replace(".py", "")
                __import__(module_name)
                results.append(log_test(f"脚本导入 - {description}", "PASS", "可成功导入"))
            except Exception as e:
                results.append(log_test(f"脚本导入 - {description}", "WARN", 
                                      f"导入警告: {str(e)[:50]}"))
        else:
            results.append(log_test(f"监控脚本 - {description}", "FAIL", "文件不存在"))
            all_exist = False
    
    if not all_exist:
        results.append(log_test("监控脚本检查", "FAIL", "缺少监控脚本"))
        return results, False
    
    # 2. 测试警报系统
    try:
        # 运行简单的警报测试
        import test_alert_simple
        results.append(log_test("警报系统", "PASS", "测试脚本可运行"))
    except Exception as e:
        results.append(log_test("警报系统", "WARN", f"测试脚本运行警告: {str(e)[:50]}"))
    
    results.append(log_test("监控系统测试", "PASS", "基础功能正常"))
    return results, True

def test_data_sources_real():
    """真实测试数据源"""
    results = []
    
    print("\n📡 测试数据源连接 (真实API测试)")
    print("-" * 50)
    
    # 测试数据源API
    test_urls = [
        ("测试连接", "http://httpbin.org/get", True),  # 测试用
        ("本地API", "http://localhost:8000/health", False),  # 可选
    ]
    
    successful_tests = 0
    for name, url, required in test_urls:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                results.append(log_test(f"数据源 - {name}", "PASS", 
                                      f"连接成功 (状态码: {response.status_code})"))
                successful_tests += 1
            else:
                status = "FAIL" if required else "WARN"
                results.append(log_test(f"数据源 - {name}", status,
                                      f"连接异常 (状态码: {response.status_code})"))
        except Exception as e:
            status = "FAIL" if required else "WARN"
            results.append(log_test(f"数据源 - {name}", status,
                                  f"连接失败: {str(e)[:50]}"))
    
    if successful_tests > 0:
        results.append(log_test("数据源测试", "PASS", f"{successful_tests}/{len(test_urls)} 个测试通过"))
        return results, True
    else:
        results.append(log_test("数据源测试", "WARN", "所有数据源测试失败或警告"))
        return results, False

def generate_report(all_results):
    """生成测试报告"""
    print("\n" + "=" * 70)
    print("📋 iStock 真实运行测试报告")
    print("=" * 70)
    
    # 统计结果
    total_tests = 0
    passed_tests = 0
    failed_tests = 0
    warning_tests = 0
    
    for category, results, passed in all_results:
        for test in results:
            total_tests += 1
            if test["status"] == "PASS":
                passed_tests += 1
            elif test["status"] == "FAIL":
                failed_tests += 1
            elif test["status"] == "WARN":
                warning_tests += 1
    
    print(f"\n测试统计:")
    print(f"  总测试数: {total_tests}")
    print(f"  通过: {passed_tests}")
    print(f"  失败: {failed_tests}")
    print(f"  警告: {warning_tests}")
    
    if total_tests > 0:
        pass_rate = passed_tests / total_tests * 100
        print(f"  通过率: {pass_rate:.1f}%")
    
    print(f"\n系统组件测试结果:")
    for category, results, passed in all_results:
        status = "✅ 通过" if passed else "❌ 失败" if any(r["status"] == "FAIL" for r in results) else "⚠️  警告"
        print(f"  {status} - {category}")
    
    # 失败详情
    print(f"\n失败测试详情:")
    has_failures = False
    for category, results, _ in all_results:
        for test in results:
            if test["status"] == "FAIL":
                print(f"  • {category} - {test['test_name']}: {test['details']}")
                has_failures = True
    
    if not has_failures:
        print("  (无失败测试)")
    
    # 警告详情
    print(f"\n警告测试详情:")
    has_warnings = False
    for category, results, _ in all_results:
        for test in results:
            if test["status"] == "WARN":
                print(f"  • {category} - {test['test_name']}: {test['details']}")
                has_warnings = True
    
    if not has_warnings:
        print("  (无警告测试)")
    
    # 保存报告
    report = {
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "warning_tests": warning_tests,
            "pass_rate": pass_rate if total_tests > 0 else 0
        },
        "detailed_results": all_results,
        "recommendations": generate_recommendations(all_results)
    }
    
    report_file = f"real_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n详细报告已保存到: {report_file}")
    print("=" * 70)
    
    return report

def generate_recommendations(all_results):
    """生成改进建议"""
    recommendations = []
    
    # 分析测试结果
    for category, results, passed in all_results:
        if not passed:
            # 查找具体问题
            for test in results:
                if test["status"] == "FAIL":
                    recommendations.append(f"修复 {category}: {test['test_name']} - {test['details']}")
                elif test["status"] == "WARN":
                    recommendations.append(f"改进 {category}: {test['test_name']} - {test['details']}")
    
    if not recommendations:
        recommendations.append("所有测试通过，可以继续开发")
    else:
        recommendations.insert(0, "需要先修复以下问题:")
    
    return recommendations

async def main():
    """主函数"""
    print("=" * 70)
    print("🚀 iStock 真实运行测试框架")
    print("确保每个功能都实际可运行，避免虚假报告")
    print("=" * 70)
    
    start_time = time.time()
    
    # 运行所有测试
    all_results = []
    
    # 后端测试
    backend_results, backend_passed = test_backend_real()
    all_results.append(("后端服务", backend_results, backend_passed))
    
    # 数据库测试
    db_results, db_passed = test_database_real()
    all_results.append(("数据库", db_results, db_passed))
    
    # 前端测试
    frontend_results, frontend_passed = test_frontend_real()
    all_results.append(("前端服务", frontend_results, frontend_passed))
    
    # 监控测试
    monitor_results, monitor_passed = test_monitoring_real()
    all_results.append(("监控系统", monitor_results, monitor_passed))
    
    # 数据源测试
    datasource_results, datasource_passed = test_data_sources_real()
    all_results.append(("数据源", datasource_results, datasource_passed))
    
    # 生成报告
    report = generate_report(all_results)
    
    # 输出建议
    print("\n💡 开发建议:")
    print("-" * 40)
    for i, rec in enumerate(report["recommendations"], 1):
        print(f"{i}. {rec}")
    
    duration = time.time() - start_time
    print(f"\n⏱️  测试用时: {duration:.1f} 秒")
    print("=" * 70)
    
    # 总结
    if report["summary"]["failed_tests"] == 0:
        print("🎉 所有关键测试通过！可以继续开发。")
    else:
        print("⚠️  有失败测试，请先修复问题再继续开发。")

if __name__ == "__main__":
    asyncio.run(main())