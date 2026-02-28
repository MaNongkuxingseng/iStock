#!/usr/bin/env python3
"""
iStock项目状态检查脚本
检查项目各个组件的状态和健康状况
"""

import os
import sys
import subprocess
import time
from pathlib import Path
from datetime import datetime

def run_command(cmd, cwd=None, timeout=30):
    """运行命令并返回结果"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            cwd=cwd,
            timeout=timeout
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return 1, "", "命令执行超时"
    except Exception as e:
        return 1, "", str(e)

def check_git_status():
    """检查Git状态"""
    print("📊 检查Git状态...")
    
    project_root = Path(__file__).parent.parent
    
    checks = [
        ("当前分支", "git branch --show-current"),
        ("远程仓库", "git remote -v"),
        ("未提交更改", "git status --porcelain"),
        ("最新提交", "git log --oneline -1"),
    ]
    
    all_good = True
    for check_name, cmd in checks:
        code, out, err = run_command(cmd, cwd=project_root)
        
        if code == 0:
            output = out.strip()
            if output:
                if check_name == "未提交更改" and output:
                    print(f"  ⚠️  {check_name}: 有未提交的更改")
                    all_good = False
                else:
                    print(f"  ✅ {check_name}: {output}")
            else:
                print(f"  ✅ {check_name}: 无")
        else:
            print(f"  ❌ {check_name}: 检查失败")
            all_good = False
    
    return all_good

def check_docker_status():
    """检查Docker状态"""
    print("🐳 检查Docker状态...")
    
    checks = [
        ("Docker版本", "docker --version"),
        ("Docker Compose", "docker-compose --version"),
        ("Docker守护进程", "docker info"),
        ("运行中的容器", "docker ps"),
        ("iStock容器", "docker-compose ps"),
    ]
    
    all_good = True
    for check_name, cmd in checks:
        code, out, err = run_command(cmd)
        
        if code == 0:
            if check_name == "iStock容器":
                lines = out.strip().split('\n')
                if len(lines) > 2:  # 有运行的容器
                    print(f"  ✅ {check_name}: {len(lines)-2} 个容器运行中")
                    for line in lines[2:]:
                        print(f"    {line}")
                else:
                    print(f"  ⚠️  {check_name}: 无运行中的容器")
                    all_good = False
            else:
                first_line = out.strip().split('\n')[0]
                print(f"  ✅ {check_name}: {first_line}")
        else:
            if check_name == "iStock容器":
                print(f"  ⚠️  {check_name}: 未运行或未配置")
            else:
                print(f"  ❌ {check_name}: 检查失败")
                all_good = False
    
    return all_good

def check_python_environment():
    """检查Python环境"""
    print("🐍 检查Python环境...")
    
    project_root = Path(__file__).parent.parent
    
    checks = [
        ("Python版本", "python --version"),
        ("Pip版本", "pip --version"),
        ("虚拟环境", f"cd {project_root} && python -c \"import sys; print(sys.prefix)\""),
        ("依赖包", f"cd {project_root} && pip list | grep -E '(fastapi|sqlalchemy|pandas)'"),
    ]
    
    all_good = True
    for check_name, cmd in checks:
        code, out, err = run_command(cmd)
        
        if code == 0:
            output = out.strip()
            if output:
                if check_name == "依赖包":
                    packages = [p for p in output.split('\n') if p]
                    print(f"  ✅ {check_name}: 找到 {len(packages)} 个关键包")
                    for pkg in packages[:3]:  # 显示前3个
                        print(f"    {pkg}")
                else:
                    print(f"  ✅ {check_name}: {output}")
            else:
                if check_name == "依赖包":
                    print(f"  ⚠️  {check_name}: 未找到关键依赖包")
                    all_good = False
                else:
                    print(f"  ✅ {check_name}: 正常")
        else:
            print(f"  ❌ {check_name}: 检查失败")
            all_good = False
    
    return all_good

def check_database_status():
    """检查数据库状态"""
    print("🗄️  检查数据库状态...")
    
    project_root = Path(__file__).parent.parent
    
    # 尝试连接数据库
    test_script = """
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))
try:
    from src.database.session import engine
    with engine.connect() as conn:
        result = conn.execute("SELECT 1")
        print("✅ 数据库连接成功")
except Exception as e:
    print(f"❌ 数据库连接失败: {e}")
"""
    
    test_file = project_root / "backend" / "test_db_connection.py"
    with open(test_file, "w", encoding="utf-8") as f:
        f.write(test_script)
    
    code, out, err = run_command(f"python {test_file}", cwd=project_root / "backend")
    
    # 清理临时文件
    if test_file.exists():
        test_file.unlink()
    
    if code == 0 and "✅" in out:
        print(f"  {out.strip()}")
        return True
    else:
        print(f"  ❌ 数据库连接失败")
        if err:
            print(f"    错误: {err[:100]}")
        return False

def check_service_health():
    """检查服务健康状态"""
    print("🏥 检查服务健康状态...")
    
    import requests
    import socket
    
    services = [
        {
            "name": "后端API",
            "type": "http",
            "endpoint": "http://localhost:8000",
            "timeout": 5
        },
        {
            "name": "API文档",
            "type": "http", 
            "endpoint": "http://localhost:8000/docs",
            "timeout": 5
        },
        {
            "name": "前端应用",
            "type": "http",
            "endpoint": "http://localhost:3000",
            "timeout": 5
        },
        {
            "name": "PostgreSQL",
            "type": "tcp",
            "host": "localhost",
            "port": 5432,
            "timeout": 5
        },
        {
            "name": "Redis",
            "type": "tcp",
            "host": "localhost",
            "port": 6379,
            "timeout": 5
        },
    ]
    
    all_healthy = True
    for service in services:
        print(f"  检查 {service['name']}...")
        
        if service["type"] == "http":
            try:
                response = requests.get(service["endpoint"], timeout=service["timeout"])
                if response.status_code < 500:
                    print(f"    ✅ {service['name']}: HTTP {response.status_code}")
                else:
                    print(f"    ⚠️  {service['name']}: HTTP {response.status_code}")
                    all_healthy = False
            except requests.exceptions.RequestException as e:
                print(f"    ❌ {service['name']}: 无法连接 - {str(e)[:50]}")
                all_healthy = False
        elif service["type"] == "tcp":
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(service["timeout"])
                result = sock.connect_ex((service["host"], service["port"]))
                if result == 0:
                    print(f"    ✅ {service['name']}: 端口开放")
                else:
                    print(f"    ❌ {service['name']}: 端口关闭")
                    all_healthy = False
                sock.close()
            except Exception as e:
                print(f"    ❌ {service['name']}: 检查失败 - {str(e)[:50]}")
                all_healthy = False
    
    return all_healthy

def check_project_structure():
    """检查项目结构"""
    print("📁 检查项目结构...")
    
    project_root = Path(__file__).parent.parent
    
    required_dirs = [
        ("backend/", "后端代码"),
        ("backend/src/", "后端源码"),
        ("backend/src/database/", "数据库模块"),
        ("frontend/", "前端代码"),
        ("docker/", "Docker配置"),
        ("docker/nginx/", "Nginx配置"),
        ("docker/postgres/", "数据库配置"),
        ("local/", "本地开发"),
        ("scripts/", "工具脚本"),
    ]
    
    required_files = [
        ("docker-compose.yml", "开发环境配置"),
        ("docker-compose.prod.yml", "生产环境配置"),
        ("Dockerfile.backend", "后端Dockerfile"),
        ("Dockerfile.frontend", "前端Dockerfile"),
        (".env.example", "环境变量示例"),
        ("requirements.txt", "Python依赖"),
        ("pyproject.toml", "项目配置"),
        ("README.md", "项目说明"),
    ]
    
    all_good = True
    
    print("  目录结构:")
    for dir_path, description in required_dirs:
        full_path = project_root / dir_path
        if full_path.exists():
            print(f"    ✅ {dir_path} - {description}")
        else:
            print(f"    ❌ {dir_path} - {description} (缺失)")
            all_good = False
    
    print("\n  关键文件:")
    for file_path, description in required_files:
        full_path = project_root / file_path
        if full_path.exists():
            size = full_path.stat().st_size
            print(f"    ✅ {file_path} - {description} ({size} bytes)")
        else:
            print(f"    ❌ {file_path} - {description} (缺失)")
            all_good = False
    
    return all_good

def generate_report():
    """生成检查报告"""
    print("\n📋 生成检查报告...")
    
    project_root = Path(__file__).parent.parent
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "project": "iStock",
        "project_root": str(project_root),
        "checks": {}
    }
    
    # 运行所有检查
    checks = [
        ("Git状态", check_git_status),
        ("Docker状态", check_docker_status),
        ("Python环境", check_python_environment),
        ("数据库状态", check_database_status),
        ("服务健康", check_service_health),
        ("项目结构", check_project_structure),
    ]
    
    results = []
    for check_name, check_func in checks:
        print(f"\n[{check_name}]")
        try:
            success = check_func()
            results.append((check_name, success))
            report["checks"][check_name] = {
                "status": "pass" if success else "fail",
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            print(f"❌ 检查异常: {e}")
            results.append((check_name, False))
            report["checks"][check_name] = {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    # 保存报告
    import json
    report_file = project_root / "project_status_report.json"
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 报告已保存: {report_file}")
    
    return results

def show_summary(results):
    """显示检查总结"""
    print("\n" + "=" * 60)
    print("📊 检查总结:")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for check_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{check_name}: {status}")
    
    print(f"\n总计: {passed}/{total} 通过")
    
    if passed == total:
        print("\n🎉 所有检查通过！项目状态良好。")
        print("\n💡 下一步:")
        print("  1. 启动开发: python scripts/start_project.py")
        print("  2. 运行测试: python -m pytest backend/tests/")
        print("  3. 访问应用: http://localhost:8000/docs")
    else:
        print("\n⚠️  部分检查失败，请根据错误信息进行修复。")
        print("\n🔧 常见问题解决:")
        print("  1. Docker未运行: 启动Docker Desktop")
        print("  2. 端口冲突: 修改docker-compose.yml中的端口")
        print("  3. 依赖缺失: pip install -r requirements.txt")
        print("  4. 数据库连接: 检查.env文件配置")
    
    return passed == total

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='iStock项目状态检查工具')
    parser.add_argument('--check', '-c', choices=['git', 'docker', 'python', 'db', 'services', 'structure', 'all'], default='all', help='检查类型')
    parser.add_argument('--report', '-r', action='store_true', help='生成详细报告')
    
    args = parser.parse_args()
    
    print("🔍 iStock项目状态检查")
    print("=" * 60)
    
    if args.check == 'all':
        results = generate_report()
        success = show_summary(results)
        sys.exit(0 if success else 1)
    else:
        checks = {
            'git': ("Git状态", check_git_status),
            'docker': ("Docker状态", check_docker_status),
            'python': ("Python环境", check_python_environment),
            'db': ("数据库状态", check_database_status),
            'services': ("服务健康", check_service_health),
            'structure': ("项目结构", check_project_structure),
        }
        
        if args.check in checks:
            check_name, check_func = checks[args.check]
            print(f"[{check_name}]")
            success = check_func()
            
            if args.report:
                import json
                report = {
                    "timestamp": datetime.now().isoformat(),
                    "check": check_name,
                    "status": "pass" if success else "fail"
                }
                
                project_root = Path(__file__).parent.parent
                report_file = project_root / f"check_{args.check}_report.json"
                with open(report_file, "w", encoding="utf-8") as f:
                    json.dump(report, f, indent=2, ensure_ascii=False)
                
                print(f"\n📄 报告已保存: {report_file}")
            
            sys.exit(0 if success else 1)
        else:
            print(f"❌ 未知检查类型: {args.check}")
            sys.exit(1)

if __name__ == "__main__":
    main()