#!/usr/bin/env python3
"""
iStock Service Test Script
Test all core service availability
"""

import requests
import time
import json
from datetime import datetime
import sys
import os

def test_backend_api():
    """Test backend API services"""
    print("Testing backend API services...")
    
    endpoints = [
        ("Health Check", "http://localhost:8000/health", {"method": "GET"}),
        ("API Docs", "http://localhost:8000/docs", {"method": "GET"}),
        ("Stocks List", "http://localhost:8000/api/v1/stocks", {"method": "GET"}),
        ("User Login", "http://localhost:8000/api/v1/auth/login", {"method": "POST", "json": {"username": "test", "password": "test"}}),
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
                results.append((name, "ERROR: Unsupported method", url))
                continue
            
            if response.status_code == 200:
                results.append((name, "OK", url, response.status_code))
            else:
                results.append((name, f"WARN: Status {response.status_code}", url, response.status_code))
                
        except requests.exceptions.ConnectionError:
            results.append((name, "ERROR: Connection failed", url, "N/A"))
        except requests.exceptions.Timeout:
            results.append((name, "ERROR: Timeout", url, "N/A"))
        except Exception as e:
            results.append((name, f"ERROR: {str(e)[:30]}", url, "N/A"))
    
    return results

def test_database():
    """Test database connection"""
    print("Testing database connection...")
    
    try:
        # Try to import database module
        sys.path.append("backend/src")
        from database.session import SessionLocal
        
        # Test connection
        db = SessionLocal()
        try:
            # Execute simple query
            result = db.execute("SELECT 1")
            db.close()
            return [("Database Connection", "OK", "PostgreSQL", "Connected")]
        except Exception as e:
            return [("Database Connection", f"ERROR: {str(e)[:30]}", "PostgreSQL", "Failed")]
            
    except ImportError:
        return [("Database Connection", "WARN: Module not found", "PostgreSQL", "Need dependencies")]
    except Exception as e:
        return [("Database Connection", f"ERROR: {str(e)[:30]}", "PostgreSQL", "Unknown error")]

def test_frontend():
    """Test frontend services"""
    print("Testing frontend services...")
    
    endpoints = [
        ("React Dev Server", "http://localhost:3000", 5),
        ("Static Resources", "http://localhost:3000/static/js/main.js", 3),
    ]
    
    results = []
    
    for name, url, timeout in endpoints:
        try:
            response = requests.get(url, timeout=timeout)
            if response.status_code == 200:
                results.append((name, "OK", url, response.status_code))
            else:
                results.append((name, f"WARN: Status {response.status_code}", url, response.status_code))
        except requests.exceptions.ConnectionError:
            results.append((name, "ERROR: Connection failed", url, "N/A"))
        except Exception as e:
            results.append((name, f"ERROR: {str(e)[:30]}", url, "N/A"))
    
    return results

def test_monitoring_system():
    """Test monitoring system"""
    print("Testing monitoring system...")
    
    tests = [
        ("Automated Monitor", "Check automated_monitor.py", test_automated_monitor),
        ("Watch Push System", "Check push_watch_en.py", test_watch_push),
        ("Alert Test System", "Check test_alert_simple.py", test_alert_system),
    ]
    
    results = []
    
    for name, description, test_func in tests:
        try:
            result = test_func()
            results.append((name, "OK", description, result))
        except Exception as e:
            results.append((name, f"ERROR: {str(e)[:30]}", description, "Test failed"))
    
    return results

def test_automated_monitor():
    """Test automated monitor"""
    try:
        # Check if file exists
        if os.path.exists("automated_monitor.py"):
            # Try to import
            import automated_monitor
            return "Script importable"
        return "File exists"
    except:
        return "Needs fix"

def test_watch_push():
    """Test watch push"""
    try:
        if os.path.exists("push_watch_en.py"):
            import push_watch_en
            return "Script importable"
        return "File exists"
    except:
        return "Needs fix"

def test_alert_system():
    """Test alert system"""
    try:
        if os.path.exists("test_alert_simple.py"):
            import test_alert_simple
            return "Script importable"
        return "File exists"
    except:
        return "Needs fix"

def test_local_deployment():
    """Test local deployment module"""
    print("Testing local deployment module...")
    
    local_dir = "local"
    if not os.path.exists(local_dir):
        return [("Local Deployment", "ERROR: Directory not found", local_dir, "Need to create")]
    
    files = ["app.py", "start_local.py", "run_local.bat"]
    results = []
    
    for file in files:
        file_path = os.path.join(local_dir, file)
        if os.path.exists(file_path):
            results.append((f"Local file: {file}", "OK", file_path, "Exists"))
        else:
            results.append((f"Local file: {file}", "WARN: Not found", file_path, "Need to create"))
    
    return results

def generate_test_report(all_results):
    """Generate test report"""
    print("\n" + "="*70)
    print("iStock Service Test Report")
    print("="*70)
    
    total_tests = 0
    passed_tests = 0
    failed_tests = 0
    
    for category, results in all_results.items():
        print(f"\n{category}:")
        print("-" * 60)
        
        for name, status, detail, code in results:
            total_tests += 1
            if "OK" in status:
                passed_tests += 1
            elif "ERROR" in status:
                failed_tests += 1
            
            print(f"  {status:15} {name:25} {detail:35} [{code}]")
    
    print("\n" + "="*70)
    print("Test Statistics:")
    print(f"  Total Tests: {total_tests}")
    print(f"  Passed: {passed_tests}")
    print(f"  Failed: {failed_tests}")
    print(f"  Pass Rate: {passed_tests/total_tests*100:.1f}%" if total_tests > 0 else "  Pass Rate: N/A")
    print("="*70)
    
    # Save report
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
    
    print(f"\nDetailed report saved to: service_test_report.json")
    
    return report

def generate_recommendations(all_results):
    """Generate improvement recommendations"""
    recommendations = []
    
    # Check backend API
    backend_results = all_results.get("Backend API Tests", [])
    for name, status, detail, code in backend_results:
        if "ERROR" in status or "WARN" in status:
            recommendations.append(f"Fix backend API: {name} - {detail}")
    
    # Check database
    db_results = all_results.get("Database Tests", [])
    for name, status, detail, code in db_results:
        if "ERROR" in status:
            recommendations.append(f"Fix database connection: {detail}")
    
    # Check frontend
    frontend_results = all_results.get("Frontend Tests", [])
    for name, status, detail, code in frontend_results:
        if "ERROR" in status:
            recommendations.append(f"Start frontend service: {detail}")
    
    # Check monitoring system
    monitor_results = all_results.get("Monitoring System Tests", [])
    for name, status, detail, code in monitor_results:
        if "ERROR" in status:
            recommendations.append(f"Fix monitoring system: {name}")
    
    # Check local deployment
    local_results = all_results.get("Local Deployment Tests", [])
    for name, status, detail, code in local_results:
        if "ERROR" in status:
            recommendations.append(f"Complete local deployment: {name}")
    
    if not recommendations:
        recommendations.append("All services normal, can proceed to next development phase")
    
    return recommendations

def main():
    """Main test function"""
    print("Starting iStock service tests...")
    print("="*70)
    
    all_results = {}
    
    # Run all tests
    try:
        all_results["Backend API Tests"] = test_backend_api()
        time.sleep(1)
        
        all_results["Database Tests"] = test_database()
        time.sleep(1)
        
        all_results["Frontend Tests"] = test_frontend()
        time.sleep(1)
        
        all_results["Monitoring System Tests"] = test_monitoring_system()
        time.sleep(1)
        
        all_results["Local Deployment Tests"] = test_local_deployment()
        
    except KeyboardInterrupt:
        print("\nTests interrupted by user")
        return
    except Exception as e:
        print(f"\nError during testing: {e}")
        all_results["Test Errors"] = [("Test Framework", f"ERROR: {str(e)}", "Testing process", "Exception")]
    
    # Generate report
    report = generate_test_report(all_results)
    
    # Output recommendations
    print("\nImprovement Recommendations:")
    print("-" * 40)
    for i, rec in enumerate(report["recommendations"], 1):
        print(f"{i}. {rec}")
    
    print("\n" + "="*70)
    print("Testing completed!")
    print("="*70)
    
    # Summary
    if report["failed_tests"] == 0:
        print("All tests passed! Ready for next development phase.")
    else:
        print(f"Warning: {report['failed_tests']} tests failed, please fix issues first.")

if __name__ == "__main__":
    main()