#!/usr/bin/env python3
"""
iStock项目状态检查脚本
检查项目各个组件的运行状态
"""

import os
import sys
import subprocess
import time
import requests
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

def check_docker_status():
    """检查Docker状态"""
    print("🐳 检查Docker状态...")
    
    checks = [
        ("Docker守护进程", "docker info", "Server:"),
        ("Docker Compose", "docker-compose --version", "docker-compose version"),
        ("运行中的容器", "docker ps --format 'table {{.Names}}\\t{{.Status}}\\t{{.Ports}}'", "NAMES"),
    ]
    
    all_healthy = True
    for check_name, cmd, expected in checks:
        code, out, err = run_command(cmd)
        
        if code == 0 and expected in out:
            print(f"  ✅ {check_name}")
            if check_name == "运行中的容器":
                lines = out.strip().split('\n')
                if len(lines) > 1:
                    print("    运行中的容器:")
                    for line in lines[1:]:  # 跳过标题行
                        if line.strip():
                            print(f"      {line.strip()}")
        else:
            print(f"  ❌ {check_name}")
            if err:
                print(f"     错误: {err[:100]}")
            all_healthy = False
    
    return all_healthy

def check_iStock_services():
    """检查iStock服务状态"""
    print("🚀 检查iStock服务状态...")
    
    project_root = Path(__file__).parent.parent
    
    # 检查docker-compose服务
    code, out, err = run_command("docker-compose ps", cwd=project_root)
    
    if code == 0:
        lines = out.strip().split('\n')
        if len(lines) > 2:  # 有服务在运行
            print("  ✅ iStock服务正在运行")
            print("    服务状态:")
            for line in lines[2:]:  # 跳过标题行
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 4:
                        service_name = parts[0]
                        status = parts[1]
                        ports = " ".join(parts[3:]) if len(parts) > 3 else ""
                        print(f"      {service_name}: {status} {ports}")
        else:
            print("  ⚠️  iStock服务未运行")
            return False
    else:
        print("  ❌ 无法获取服务状态")
        return False
    
    return True

def check_service_health():
    """检查服务健康状态"""
    print("🏥 检查服务健康状态...")
    
    services = [
        ("后端API", "http://localhost:8000/health", 10),
        ("API文档", "http://localhost:8000/docs", 10),
        ("前端应用", "http://localhost:3000", 10),
        ("Celery监控", "http://localhost:5555", 10),
    ]
    
    all_healthy = True
    for service_name, url, timeout in services:
        try:
            response = requests.get(url, timeout=timeout)
            if response.status_code == 200:
                print(f"  ✅ {service_name}: {url}")
            else:
                print(f"  ⚠️  {service_name}: HTTP {response.status_code}")
                all_healthy = False
        except requests.exceptions.RequestException as e:
            print(f"  ❌ {service_name}: 无法连接 ({e})")
            all_healthy = False
    
    return all_healthy

def check_database_status():
    """检查数据库状态"""
    print("🗄️  检查数据库状态...")
    
    project_root = Path(__file__).parent.parent
    
    # 检查PostgreSQL
    try:
        code, out, err = run_command(
            "docker-compose exec postgres pg_isready -U mystock_user",
            cwd=project_root,
            timeout=10
        )
        
        if code == 0 and "accepting connections" in out:
            print("  ✅ PostgreSQL数据库: 运行正常")
            
            # 检查表数量
            code2, out2, err2 = run_command(
                """docker-compose exec postgres psql -U mystock_user -d mystock_ai -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';" """,
                cwd=project_root,
                timeout=10
            )
            
            if code2 == 0:
                try:
                    table_count = int(out2.strip().split('\n')[2].strip())
                    print(f"      表数量: {table_count}")
                except:
                    pass
        else:
            print("  ❌ PostgreSQL数据库: 未运行")
            return False
    except:
        print("  ❌ PostgreSQL数据库: 检查失败")
        return False
    
    # 检查Redis
    try:
        code, out, err = run_command(
            "docker-compose exec redis redis-cli ping",
            cwd=project_root,
            timeout=10
        )
        
        if code == 0 and "PONG" in out:
            print("  ✅ Redis缓存: 运行正常")
        else:
            print("  ❌ Redis缓存: 未运行")
            return False
    except:
        print("  ❌ Redis缓存: 检查失败")
        return False
    
    return True

def check_system_resources():
    """检查系统资源"""
    print("📊 检查系统资源...")
    
    # 检查Docker资源使用
    code, out, err = run_command("docker stats --no-stream --format 'table {{.Name}}\\t{{.CPUPerc}}\\t{{.MemUsage}}\\t{{.MemPerc}}'")
    
    if code == 0:
        lines = out.strip().split('\n')
        if len(lines) > 1:
            print("  📈 Docker容器资源使用:")
            for line in lines[1:]:  # 跳过标题行
                if line.strip() and "iStock" in line:
                    print(f"      {line.strip()}")
    
    # 检查磁盘空间
    code, out, err = run_command("docker system df")
    if code == 0:
        print("  💾 Docker磁盘使用:")
        lines = out.strip().split('\n')
        for line in lines:
            if line.strip():
                print(f"      {line.strip()}")
    
    return True

def check_project_files():
    """检查项目文件"""
    print("📁 检查项目文件...")
    
    project_root = Path(__file__).parent.parent
    
    required_files = [
        ("docker-compose.yml", "开发环境配置"),
        (".env", "环境变量配置"),
        ("requirements.txt", "Python依赖"),
        ("backend/src/database/models.py", "数据模型"),
        ("frontend/package.json", "前端配置"),
    ]
    
    all_exist = True
    for file_path, description in required_files:
        full_path = project_root / file_path
        if full_path.exists():
            print(f"  ✅ {file_path} - {description}")
        else:
            print(f"  ❌ {file_path} - {description} (缺失)")
            all_exist = False
    
    return all_exist

def check_git_status():
    """检查Git状态"""
    print("🔀 检查Git状态...")
    
    project_root = Path(__file__).parent.parent
    
    # 检查当前分支
    code, out, err = run_command("git branch --show-current", cwd=project_root)
    if code == 0:
        current_branch = out.strip()
        print(f"  当前分支: {current_branch}")
    
    # 检查是否有未提交的更改
    code, out, err = run_command("git status --porcelain", cwd=project_root)
    if code == 0:
        changes = out.strip().split('\n')
        if changes and changes[0]:
            print(f"  ⚠️  有 {len([c for c in changes if c])} 个未提交的更改")
        else:
            print("  ✅ 工作区干净")
    
    # 检查最后一次提交
    code, out, err = run_command("git log --oneline -1", cwd=project_root)
    if code == 0:
        last_commit = out.strip()
        print(f"  最后一次提交: {last_commit}")
    
    return True

def generate_status_report():
    """生成状态报告"""
    print("\n" + "=" * 60)
    print("📋 iStock项目状态报告")
    print("=" * 60)
    print(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    checks = [
        ("Docker状态", check_docker_status),
        ("iStock服务", check_iStock_services),
        ("服务健康", check_service_health),
        ("数据库状态", check_database_status),
        ("系统资源", check_system_resources),
        ("项目文件", check_project_files),
        ("Git状态", check_git_status),
    ]
    
    results = []
    for check_name, check_func in checks:
        print(f"\n[{check_name}]")
        try:
            success = check_func()
            results.append((check_name, success))
            print(f"结果: {'✅ 正常' if success else '❌ 异常'}")
        except Exception as e:
            print(f"❌ 检查异常: {e}")
            results.append((check_name, False))
    
    print("\n" + "=" * 60)
    print("📊 状态总结:")
    print("=" * 60)
    
    healthy = sum(1 for _, result in results if result)
    total = len(results)
    
    for check_name, result in results:
        status = "✅ 正常" if result else "❌ 异常"
        print(f"{check_name}: {status}")
    
    print(f"\n健康度: {healthy}/{total} ({healthy/total*100:.1f}%)")
    
    if healthy == total:
        print("\n🎉 所有系统正常！")
        print("\n🌐 访问地址:")
        print("  后端API: http://localhost:8000")
        print("  前端应用: http://localhost:3000")
        print("  API文档: http://localhost:8000/docs")
    else:
        print(f"\n⚠️  有 {total - healthy} 个问题需要修复")
        
        # 提供修复建议
        print("\n🔧 修复建议:")
        for check_name, result in results:
            if not result:
                if "Docker" in check_name:
                    print(f"  • {check_name}: 启动Docker Desktop并检查PATH")
                elif "服务" in check_name:
                    print(f"  • {check_name}: 运行 'docker-compose up -d'")
                elif "数据库" in check_name:
                    print(f"  • {check_name}: 检查数据库连接配置")
                elif "文件" in check_name:
                    print(f"  • {check_name}: 检查项目文件完整性")
    
    print("\n" + "=" * 60)
    
    return healthy == total

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='iStock项目状态检查工具')
    parser.add_argument('--check', '-c', choices=[
        'docker', 'services', 'health', 'database', 
        'resources', 'files', 'git', 'all'
    ], default='all', help='要检查的项目')
    
    args = parser.parse_args()
    
    if args.check == 'all':
        success = generate_status_report()
    elif args.check == 'docker':
        success = check_docker_status()
    elif args.check == 'services':
        success = check_iStock_services()
    elif args.check == 'health':
        success = check_service_health()
    elif args.check == 'database':
        success = check_database_status()
    elif args.check == 'resources':
        success = check_system_resources()
    elif args.check == 'files':
        success = check_project_files()
    elif args.check == 'git':
        success = check_git_status()
    else:
        print(f"❌ 未知检查项: {args.check}")
        sys.exit(1)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()