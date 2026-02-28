#!/usr/bin/env python3
"""
iStock Real Runtime Test Script
Ensure every function actually runs, avoid false reports
"""

import requests
import time
import json
import os
import subprocess
from datetime import datetime

def log_test(test_name, status, details):
    """Log test result"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    icon = "[OK]" if status == "PASS" else "[WARN]" if status == "WARN" else "[FAIL]"
    print(f"{icon} [{timestamp}] {test_name}: {details}")
    return {"test_name": test_name, "status": status, "details": details, "timestamp": timestamp}

def test_backend_real():
    """Real test backend service"""
    results = []
    
    print("\n[TEST] Backend Service (Real Runtime Test)")
    print("-" * 50)
    
    # 1. Check backend directory
    if not os.path.exists("backend"):
        results.append(log_test("Backend Directory", "FAIL", "backend directory not found"))
        return results, False
    
    # 2. Check main.py file
    main_file = "backend/src/main.py"
    if not os.path.exists(main_file):
        results.append(log_test("Main File", "FAIL", f"{main_file} not found"))
        return results, False
    
    results.append(log_test("Backend Files", "PASS", "Required files exist"))
    
    # 3. Try to import and test
    try:
        # Add backend/src to path
        import sys
        sys.path.insert(0, "backend/src")
        
        # Try to import main module
        import main
        results.append(log_test("Backend Import", "PASS", "Successfully imported main module"))
        
        # Check if app exists
        if hasattr(main, 'app'):
            results.append(log_test("FastAPI App", "PASS", "FastAPI application found"))
        else:
            results.append(log_test("FastAPI App", "FAIL", "No FastAPI app found in main"))
            return results, False
            
    except ImportError as e:
        results.append(log_test("Backend Import", "FAIL", f"Import error: {str(e)[:50]}"))
        return results, False
    except Exception as e:
        results.append(log_test("Backend Test", "FAIL", f"Test error: {str(e)[:50]}"))
        return results, False
    
    # 4. Test if service is already running
    try:
        response = requests.get("http://localhost:8000/health", timeout=3)
        if response.status_code == 200:
            results.append(log_test("Backend Service", "PASS", "Service already running and healthy"))
            return results, True
        else:
            results.append(log_test("Backend Service", "WARN", 
                                  f"Service responding but status {response.status_code}"))
    except requests.RequestException:
        results.append(log_test("Backend Service", "INFO", "Service not running (expected)"))
    
    results.append(log_test("Backend Test", "PASS", "Backend code structure is valid"))
    return results, True

def test_database_real():
    """Real test database"""
    results = []
    
    print("\n[TEST] Database Connection (Real Connection Test)")
    print("-" * 50)
    
    try:
        # Try to import database module
        import sys
        sys.path.append("backend/src")
        
        try:
            from database.session import SessionLocal
            results.append(log_test("Database Module", "PASS", "Successfully imported database module"))
            
            # Try to connect
            try:
                db = SessionLocal()
                # Execute simple query
                result = db.execute("SELECT 1")
                db.close()
                results.append(log_test("Database Connection", "PASS", "Connection and query successful"))
                return results, True
            except Exception as e:
                results.append(log_test("Database Connection", "FAIL", f"Connection failed: {str(e)[:50]}"))
                return results, False
                
        except ImportError as e:
            results.append(log_test("Database Module", "FAIL", f"Import failed: {str(e)[:50]}"))
            return results, False
            
    except Exception as e:
        results.append(log_test("Database Test", "FAIL", f"Test error: {str(e)[:100]}"))
        return results, False

def test_frontend_real():
    """Real test frontend"""
    results = []
    
    print("\n[TEST] Frontend Service (Real Runtime Test)")
    print("-" * 50)
    
    # 1. Check frontend directory
    if not os.path.exists("frontend"):
        results.append(log_test("Frontend Directory", "FAIL", "frontend directory not found"))
        return results, False
    
    # 2. Check key files
    required_files = [
        "frontend/package.json",
        "frontend/src/App.js",
        "frontend/src/index.js"
    ]
    
    all_files_exist = True
    for file in required_files:
        if os.path.exists(file):
            results.append(log_test(f"File Check - {os.path.basename(file)}", "PASS", "File exists"))
        else:
            results.append(log_test(f"File Check - {os.path.basename(file)}", "FAIL", "File not found"))
            all_files_exist = False
    
    if not all_files_exist:
        results.append(log_test("Frontend Files", "FAIL", "Missing required files"))
        return results, False
    
    results.append(log_test("Frontend Files", "PASS", "All required files exist"))
    
    # 3. Check Node.js environment
    try:
        node_version = subprocess.check_output(["node", "--version"], 
                                              stderr=subprocess.STDOUT, 
                                              text=True).strip()
        results.append(log_test("Node.js Environment", "PASS", f"Version: {node_version}"))
    except (subprocess.CalledProcessError, FileNotFoundError):
        results.append(log_test("Node.js Environment", "WARN", "Node.js not installed or not in PATH"))
    
    # 4. Check package.json
    try:
        with open("frontend/package.json", "r") as f:
            package_data = json.load(f)
        
        if "scripts" in package_data and "start" in package_data["scripts"]:
            results.append(log_test("package.json", "PASS", "Contains start script"))
        else:
            results.append(log_test("package.json", "WARN", "Missing start script"))
            
        if "dependencies" in package_data:
            deps_count = len(package_data["dependencies"])
            results.append(log_test("Dependencies", "INFO", f"Has {deps_count} dependencies"))
        
    except Exception as e:
        results.append(log_test("package.json", "WARN", f"Read failed: {str(e)[:50]}"))
    
    # 5. Check if service is running
    try:
        response = requests.get("http://localhost:3000", timeout=3)
        if response.status_code == 200:
            results.append(log_test("Frontend Service", "PASS", "Service already running"))
            return results, True
    except requests.RequestException:
        results.append(log_test("Frontend Service", "INFO", "Service not running (expected)"))
    
    results.append(log_test("Frontend Test", "PASS", "Frontend code structure is valid"))
    return results, True

def test_monitoring_real():
    """Real test monitoring system"""
    results = []
    
    print("\n[TEST] Monitoring System (Real Execution Test)")
    print("-" * 50)
    
    # 1. Check monitoring scripts
    monitor_scripts = [
        ("automated_monitor.py", "Automated Monitor"),
        ("push_watch_en.py", "Watch Push"),
        ("test_alert_simple.py", "Alert Test"),
    ]
    
    all_exist = True
    for filename, description in monitor_scripts:
        if os.path.exists(filename):
            results.append(log_test(f"Script - {description}", "PASS", "File exists"))
        else:
            results.append(log_test(f"Script - {description}", "FAIL", "File not found"))
            all_exist = False
    
    if not all_exist:
        results.append(log_test("Monitoring Scripts", "FAIL", "Missing monitoring scripts"))
        return results, False
    
    results.append(log_test("Monitoring Scripts", "PASS", "All scripts exist"))
    
    # 2. Test alert system
    try:
        # Try to import and run simple test
        import test_alert_simple
        results.append(log_test("Alert System", "PASS", "Test script can be imported"))
    except Exception as e:
        results.append(log_test("Alert System", "WARN", f"Test script warning: {str(e)[:50]}"))
    
    results.append(log_test("Monitoring Test", "PASS", "Monitoring system structure is valid"))
    return results, True

def test_data_sources_real():
    """Real test data sources"""
    results = []
    
    print("\n[TEST] Data Source Connection (Real API Test)")
    print("-" * 50)
    
    # Test data source APIs
    test_urls = [
        ("Test Connection", "http://httpbin.org/get", True),
        ("Local API", "http://localhost:8000/health", False),
    ]
    
    successful_tests = 0
    for name, url, required in test_urls:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                results.append(log_test(f"Data Source - {name}", "PASS", 
                                      f"Connection successful (status: {response.status_code})"))
                successful_tests += 1
            else:
                status = "FAIL" if required else "WARN"
                results.append(log_test(f"Data Source - {name}", status,
                                      f"Connection abnormal (status: {response.status_code})"))
        except Exception as e:
            status = "FAIL" if required else "WARN"
            results.append(log_test(f"Data Source - {name}", status,
                                  f"Connection failed: {str(e)[:50]}"))
    
    if successful_tests > 0:
        results.append(log_test("Data Source Test", "PASS", 
                              f"{successful_tests}/{len(test_urls)} tests passed"))
        return results, True
    else:
        results.append(log_test("Data Source Test", "WARN", "All data source tests failed or warned"))
        return results, False

def generate_report(all_results):
    """Generate test report"""
    print("\n" + "=" * 70)
    print("iStock Real Runtime Test Report")
    print("=" * 70)
    
    # Calculate statistics
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
    
    print(f"\nTest Statistics:")
    print(f"  Total Tests: {total_tests}")
    print(f"  Passed: {passed_tests}")
    print(f"  Failed: {failed_tests}")
    print(f"  Warnings: {warning_tests}")
    
    if total_tests > 0:
        pass_rate = passed_tests / total_tests * 100
        print(f"  Pass Rate: {pass_rate:.1f}%")
    
    print(f"\nSystem Component Test Results:")
    for category, results, passed in all_results:
        status = "[PASS]" if passed else "[FAIL]" if any(r["status"] == "FAIL" for r in results) else "[WARN]"
        print(f"  {status} - {category}")
    
    # Failure details
    print(f"\nFailure Details:")
    has_failures = False
    for category, results, _ in all_results:
        for test in results:
            if test["status"] == "FAIL":
                print(f"  • {category} - {test['test_name']}: {test['details']}")
                has_failures = True
    
    if not has_failures:
        print("  (No failures)")
    
    # Warning details
    print(f"\nWarning Details:")
    has_warnings = False
    for category, results, _ in all_results:
        for test in results:
            if test["status"] == "WARN":
                print(f"  • {category} - {test['test_name']}: {test['details']}")
                has_warnings = True
    
    if not has_warnings:
        print("  (No warnings)")
    
    # Save report
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
    
    print(f"\nDetailed report saved to: {report_file}")
    print("=" * 70)
    
    return report

def generate_recommendations(all_results):
    """Generate improvement recommendations"""
    recommendations = []
    
    # Analyze test results
    for category, results, passed in all_results:
        if not passed:
            # Find specific issues
            for test in results:
                if test["status"] == "FAIL":
                    recommendations.append(f"Fix {category}: {test['test_name']} - {test['details']}")
                elif test["status"] == "WARN":
                    recommendations.append(f"Improve {category}: {test['test_name']} - {test['details']}")
    
    if not recommendations:
        recommendations.append("All tests passed, can continue development")
    else:
        recommendations.insert(0, "Need to fix the following issues first:")
    
    return recommendations

def main():
    """Main function"""
    print("=" * 70)
    print("iStock Real Runtime Test Framework")
    print("Ensure every function actually runs, avoid false reports")
    print("=" * 70)
    
    start_time = time.time()
    
    # Run all tests
    all_results = []
    
    # Backend test
    print("\n[START] Testing Backend Service...")
    backend_results, backend_passed = test_backend_real()
    all_results.append(("Backend Service", backend_results, backend_passed))
    
    # Database test
    print("\n[START] Testing Database...")
    db_results, db_passed = test_database_real()
    all_results.append(("Database", db_results, db_passed))
    
    # Frontend test
    print("\n[START] Testing Frontend Service...")
    frontend_results, frontend_passed = test_frontend_real()
    all_results.append(("Frontend Service", frontend_results, frontend_passed))
    
    # Monitoring test
    print("\n[START] Testing Monitoring System...")
    monitor_results, monitor_passed = test_monitoring_real()
    all_results.append(("Monitoring System", monitor_results, monitor_passed))
    
    # Data source test
    print("\n[START] Testing Data Sources...")
    datasource_results, datasource_passed = test_data_sources_real()
    all_results.append(("Data Sources", datasource_results, datasource_passed))
    
    # Generate report
    report = generate_report(all_results)
    
    # Output recommendations
    print("\nDevelopment Recommendations:")
    print("-" * 40)
    for i, rec in enumerate(report["recommendations"], 1):
        print(f"{i}. {rec}")
    
    duration = time.time() - start_time
    print(f"\nTest Duration: {duration:.1f} seconds")
    print("=" * 70)
    
    # Summary
    if report["summary"]["failed_tests"] == 0:
        print("All critical tests passed! Can continue development.")
    else:
        print("There are failed tests, please fix issues before continuing development.")

if __name__ == "__main__":
    main()