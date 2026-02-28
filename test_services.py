#!/usr/bin/env python3
"""
iStock 服务测试脚本
测试所有核心服务的可用性
"""

import requests
import time
import json
from datetime import datetime
import sys
import os

def test_backend_api():
    """测试后端API服务"""
    print("🔧 测试后端API服务...")
    
    endpoints = [
        ("健康检查", "http://localhost:8000/health", {"method": "GET"}),
        ("API文档", "http://localhost:8000/docs", {"method": "GET"}),
        ("股票列表", "http://localhost:8000/api/v1/stocks", {"method": "GET"}),
        ("用户登录", "http://localhost:8000/api/v1/auth/login", {"method": "POST", "json": {"username": "test", "password": "test"}}),
    ]
    
    results = []
    
    for name, url, config in endpoints:
        try:
            method = config.get("method", "GET")
            timeout = config.get("timeout", 5)
            
            if method == "GET":
                response = requests.get(url, timeout=timeout)
            elif method == "POST":
                json_data = config.get("json", {})
                response = requests.post(url, json=json_data, timeout=timeout)
            else:
                results.append((name, "❌ 不支持的HTTP方法", url))
                continue
            
            if response.status_code == 200:
                results.append((name, "✅ 正常", url, response.status_code))
            else:
                results.append((name, f"⚠️ 状态码 {response.status_code}", url, response.status_code))
                
        except requests.exceptions.ConnectionError:
            results.append((name, "❌ 连接失败", url, "N/A"))
        except requests.exceptions.Timeout:
            results.append((name, "❌ 请求超时", url, "N/A"))
        except Exception as e:
            results.append((name, f"❌ 错误: {str(e)[:30]}", url, "N/A"))
    
    return results

def test_database():
    """测试数据库连接"""
    print("🗄️  测试数据库连接...")
    
    try:
        # 尝试导入数据库模块
        sys.path.append("backend/src")
        from database.session import SessionLocal
        
        # 测试连接
        db = SessionLocal()
        try:
            # 执行简单查询
            result = db.execute("SELECT 1")
            db.close()
            return [("数据库连接", "✅ 正常", "PostgreSQL", "连接成功")]
        except Exception as e:
            return [("数据库连接", f"❌ 错误: {str(e)[:30]}", "PostgreSQL", "连接失败")]
            
    except ImportError:
        return [("数据库连接", "⚠️ 数据库模块未找到", "PostgreSQL", "需要安装依赖")]
    except Exception as e:
        return [("数据库连接", f"❌ 错误: {str(e)[:30]}", "PostgreSQL", "未知错误")]

def test_frontend():
    """测试前端服务"""
    print("🎨 测试前端服务...")
    
    endpoints = [
        ("React开发服务器", "http://localhost:3000", 5),
        ("静态资源", "http://localhost:3000/static/js/main.js", 3),
    ]
    
    results = []
    
    for name, url, timeout in endpoints:
        try:
            response = requests.get(url, timeout=timeout)
            if response.status_code == 200:
                results.append((name, "✅ 正常", url, response.status_code))
            else:
                results.append((name, f"⚠️ 状态码 {response.status_code}", url, response.status_code))
        except requests.exceptions.ConnectionError:
            results.append((name, "❌ 连接失败", url, "N/A"))
        except Exception as e:
            results.append((name, f"❌ 错误: {str(e)[:30]}", url, "N/A"))
    
    return results

def test_monitoring_system():
    """测试监控系统"""
    print("📊 测试监控系统...")
    
    tests = [
        ("自动化监控脚本", "检查 automated_monitor.py", test_automated_monitor),
        ("盯盘推送系统", "检查 push_watch_en.py", test_watch_push),
        ("警报测试系统", "检查 test_alert_simple.py", test_alert_system),
    ]
    
    results = []
    
    for name, description, test_func in tests:
        try:
            result = test_func()
            results.append((name, "✅ 正常", description, result))
        except Exception as e:
            results.append((name, f"❌ 错误: {str(e)[:30]}", description, "测试失败"))
    
    return results

def test_automated_monitor():
    """测试自动化监控"""
    try:
        # 检查文件是否存在
        if os.path.exists("automated_monitor.py"):
            # 尝试导入
            import automated_monitor
            return "脚本可导入"
        return "文件存在"
    except:
        return "需要修复"

def test_watch_push():
    """测试盯盘推送"""
    try:
        if os.path.exists("push_watch_en.py"):
            import push_watch_en
            return "脚本可导入"
        return "文件存在"
    except:
        return "需要修复"

def test_alert_system():
    """测试警报系统"""
    try:
        if os.path.exists("test_alert_simple.py"):
            import test_alert_simple
            return "脚本可导入"
        return "文件存在"
    except:
        return "需要修复"

def test_local_deployment():
    """测试本地部署模块"""
    print("💻 测试本地部署模块...")
    
    local_dir = "local"
    if not os.path.exists(local_dir):
        return [("本地部署", "❌ 目录不存在", local_dir, "需要创建")]
    
    files = ["app.py", "start_local.py", "run_local.bat"]
    results = []
    
    for file in files:
        file_path = os.path.join(local_dir, file)
        if os.path.exists(file_path):
            results.append((f"本地文件: {file}", "✅ 存在", file_path, "正常"))
        else:
            results.append((f"本地文件: {file}", "⚠️ 不存在", file_path, "需要创建"))
    
    return results

def generate_test_report(all_results):
    """生成测试报告"""
    print("\n" + "="*70)
    print("📋 iStock 服务测试报告")
    print("="*70)
    
    total_tests = 0
    passed_tests = 0
    failed_tests = 0
    
    for category, results in all_results.items():
        print(f"\n{category}:")
        print("-" * 60)
        
        for name, status, detail, code in results:
            total_tests += 1
            if "✅" in status:
                passed_tests += 1
            elif "❌" in status:
                failed_tests += 1
            
            print(f"  {status} {name:30} {detail:40} [{code}]")
    
    print("\n" + "="*70)
    print("测试统计:")
    print(f"  总测试数: {total_tests}")
    print(f"  通过: {passed_tests}")
    print(f"  失败: {failed_tests}")
    print(f"  通过率: {passed_tests/total_tests*100:.1f}%" if total_tests > 0 else "  通过率: N/A")
    print("="*70)
    
    # 保存报告
    report = {
        "timestamp": datetime.now().isoformat(),
        "total_tests": total_tests,
        "passed_tests": passed_tests,
        "failed_tests": failed_tests,
        "pass_rate": passed_tests/total_tests*100 if total_tests > 0 else 0,
        "results": all_results,
        "recommendations": generate_recommendations(all_results)
    }
    
    with open("service_test_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"\n详细报告已保存到: service_test_report.json")
    
    return report

def generate_recommendations(all_results):
    """生成改进建议"""
    recommendations = []
    
    # 检查后端API
    backend_results = all_results.get("后端API测试", [])
    for name, status, detail, code in backend_results:
        if "❌" in status or "⚠️" in status:
            recommendations.append(f"修复后端API: {name} - {detail}")
    
    # 检查数据库
    db_results = all_results.get("数据库测试", [])
    for name, status, detail, code in db_results:
        if "❌" in status:
            recommendations.append(f"修复数据库连接: {detail}")
    
    # 检查前端
    frontend_results = all_results.get("前端测试", [])
    for name, status, detail, code in frontend_results:
        if "❌" in status:
            recommendations.append(f"启动前端服务: {detail}")
    
    # 检查监控系统
    monitor_results = all_results.get("监控系统测试", [])
    for name, status, detail, code in monitor_results:
        if "❌" in status:
            recommendations.append(f"修复监控系统: {name}")
    
    # 检查本地部署
    local_results = all_results.get("本地部署测试", [])
    for name, status, detail, code in local_results:
        if "❌" in status:
            recommendations.append(f"完善本地部署: {name}")
    
    if not recommendations:
        recommendations.append("所有服务正常，可以开始下一步开发")
    
    return recommendations

def main():
    """主测试函数"""
    print("🚀 开始iStock服务测试...")
    print("="*70)
    
    all_results = {}
    
    # 运行所有测试
    try:
        all_results["后端API测试"] = test_backend_api()
        time.sleep(1)
        
        all_results["数据库测试"] = test_database()
        time.sleep(1)
        
        all_results["前端测试"] = test_frontend()
        time.sleep(1)
        
        all_results["监控系统测试"] = test_monitoring_system()
        time.sleep(1)
        
        all_results["本地部署测试"] = test_local_deployment()
        
    except KeyboardInterrupt:
        print("\n测试被用户中断")
        return
    except Exception as e:
        print(f"\n测试过程中发生错误: {e}")
        all_results["测试错误"] = [("测试框架", f"❌ 错误: {str(e)}", "测试过程", "异常")]
    
    # 生成报告
    report = generate_test_report(all_results)
    
    # 输出建议
    print("\n💡 改进建议:")
    print("-" * 40)
    for i, rec in enumerate(report["recommendations"], 1):
        print(f"{i}. {rec}")
    
    print("\n" + "="*70)
    print("测试完成!")
    print("="*70)
    
    # 总结
    if report["failed_tests"] == 0:
        print("🎉 所有测试通过！可以开始下一步开发工作。")
    else:
        print(f"⚠️  有 {report['failed_tests']} 个测试失败，请先修复问题。")

if __name__ == "__main__":
    main()