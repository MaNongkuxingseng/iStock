#!/usr/bin/env python3
"""
iStock项目启动脚本
提供多种启动方式和环境配置
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def run_command(cmd, cwd=None, timeout=300):
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

def check_requirements():
    """检查系统要求"""
    print("🔍 检查系统要求...")
    
    requirements = [
        ("Python 3.8+", "python --version"),
        ("Git", "git --version"),
        ("Docker", "docker --version"),
        ("Docker Compose", "docker-compose --version"),
    ]
    
    all_met = True
    for req_name, cmd in requirements:
        code, out, err = run_command(cmd)
        if code == 0:
            print(f"  ✅ {req_name}: {out.strip()}")
        else:
            print(f"  ❌ {req_name}: 未安装")
            all_met = False
    
    return all_met

def setup_environment():
    """设置环境"""
    print("⚙️  设置环境...")
    
    project_root = Path(__file__).parent.parent
    
    # 创建.env文件（如果不存在）
    env_example = project_root / ".env.example"
    env_file = project_root / ".env"
    
    if not env_file.exists() and env_example.exists():
        import shutil
        shutil.copy(env_example, env_file)
        print(f"  ✅ 创建.env文件: {env_file}")
    elif env_file.exists():
        print(f"  ✅ .env文件已存在: {env_file}")
    else:
        print(f"  ⚠️  未找到.env.example文件")
    
    # 检查Python虚拟环境
    venv_dir = project_root / ".venv"
    if not venv_dir.exists():
        print(f"  ℹ️  Python虚拟环境未创建")
        print(f"    建议: python -m venv .venv")
    else:
        print(f"  ✅ Python虚拟环境已存在")
    
    return True

def start_docker_development():
    """启动Docker开发环境"""
    print("🐳 启动Docker开发环境...")
    
    project_root = Path(__file__).parent.parent
    
    # 构建镜像
    print("🔨 构建Docker镜像...")
    code, out, err = run_command("docker-compose build", cwd=project_root, timeout=600)
    
    if code != 0:
        print(f"❌ Docker构建失败: {err[:500]}...")
        return False
    
    print("✅ Docker镜像构建完成")
    
    # 启动服务
    print("🚀 启动服务...")
    code, out, err = run_command("docker-compose up -d", cwd=project_root, timeout=300)
    
    if code != 0:
        print(f"❌ 启动服务失败: {err[:500]}...")
        return False
    
    print("✅ 服务启动成功")
    
    # 检查服务状态
    print("📊 检查服务状态...")
    time.sleep(10)  # 给服务一些启动时间
    
    code, out, err = run_command("docker-compose ps", cwd=project_root)
    if code == 0:
        print("服务状态:")
        print(out)
    else:
        print(f"❌ 无法获取服务状态: {err}")
    
    return True

def start_local_development():
    """启动本地开发环境"""
    print("💻 启动本地开发环境...")
    
    project_root = Path(__file__).parent.parent
    
    # 检查本地开发目录
    local_dir = project_root / "local"
    if not local_dir.exists():
        print(f"❌ 本地开发目录不存在: {local_dir}")
        return False
    
    # 启动本地服务
    print("🚀 启动本地服务...")
    
    # 检查启动脚本
    start_scripts = [
        local_dir / "run_local.bat",
        local_dir / "start_local.py",
        local_dir / "app.py",
    ]
    
    for script in start_scripts:
        if script.exists():
            print(f"📄 找到启动脚本: {script.name}")
            
            if script.suffix == ".bat":
                code, out, err = run_command(f"start cmd /k \"{script}\"", cwd=local_dir)
            elif script.suffix == ".py":
                code, out, err = run_command(f"python {script.name}", cwd=local_dir)
            else:
                continue
            
            if code == 0:
                print(f"✅ 成功启动脚本: {script.name}")
                return True
            else:
                print(f"❌ 启动脚本失败: {err}")
    
    print("❌ 未找到可用的启动脚本")
    return False

def check_services():
    """检查服务状态"""
    print("🏥 检查服务状态...")
    
    import requests
    
    services = [
        ("后端API", "http://localhost:8000"),
        ("后端API文档", "http://localhost:8000/docs"),
        ("前端应用", "http://localhost:3000"),
        ("数据库", "localhost:5432"),
        ("Redis", "localhost:6379"),
        ("Celery监控", "http://localhost:5555"),
    ]
    
    all_healthy = True
    for service_name, endpoint in services:
        print(f"  检查 {service_name} ({endpoint})...")
        
        if "http" in endpoint:
            try:
                response = requests.get(endpoint, timeout=5)
                if response.status_code < 500:
                    print(f"    ✅ {service_name} 响应正常")
                else:
                    print(f"    ⚠️  {service_name} 响应异常: {response.status_code}")
                    all_healthy = False
            except requests.exceptions.RequestException:
                print(f"    ❌ {service_name} 无法连接")
                all_healthy = False
        else:
            # 检查TCP端口
            import socket
            host, port = endpoint.split(":")
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                result = sock.connect_ex((host, int(port)))
                if result == 0:
                    print(f"    ✅ {service_name} 端口开放")
                else:
                    print(f"    ❌ {service_name} 端口关闭")
                    all_healthy = False
                sock.close()
            except:
                print(f"    ❌ {service_name} 检查失败")
                all_healthy = False
    
    return all_healthy

def show_usage_instructions():
    """显示使用说明"""
    print("\n📚 使用说明:")
    print("=" * 60)
    
    print("\n🔗 访问地址:")
    print("  🌐 后端API:      http://localhost:8000")
    print("  📖 API文档:      http://localhost:8000/docs")
    print("  🎨 前端应用:     http://localhost:3000")
    print("  📊 Celery监控:   http://localhost:5555")
    
    print("\n🔧 常用命令:")
    print("  📦 构建镜像:     docker-compose build")
    print("  🚀 启动服务:     docker-compose up -d")
    print("  ⏸️  停止服务:     docker-compose down")
    print("  📊 查看日志:     docker-compose logs -f")
    print("  🏥 服务状态:     docker-compose ps")
    
    print("\n🐍 本地开发:")
    print("  📁 目录:         myStock-AI/local/")
    print("  🏃 启动:         cd local && python app.py")
    print("  🏃 Windows:      cd local && run_local.bat")
    
    print("\n📁 项目结构:")
    print("  📂 backend/      - 后端代码 (FastAPI)")
    print("  📂 frontend/     - 前端代码 (React)")
    print("  📂 docker/       - Docker配置")
    print("  📂 local/        - 本地开发配置")
    print("  📂 scripts/      - 工具脚本")
    
    print("\n🚀 快速开始:")
    print("  1. 确保Docker已安装并运行")
    print("  2. 运行: python scripts/start_project.py --mode docker")
    print("  3. 访问: http://localhost:8000/docs")

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='iStock项目启动工具')
    parser.add_argument('--mode', '-m', choices=['docker', 'local', 'check', 'all'], default='all', help='启动模式')
    parser.add_argument('--setup', '-s', action='store_true', help='只进行环境设置')
    parser.add_argument('--check', '-c', action='store_true', help='只检查服务状态')
    
    args = parser.parse_args()
    
    print("🚀 iStock项目启动工具")
    print("=" * 60)
    
    # 检查系统要求
    if not check_requirements():
        print("\n❌ 系统要求不满足，请先安装必要的软件")
        sys.exit(1)
    
    # 设置环境
    setup_environment()
    
    if args.setup:
        print("\n✅ 环境设置完成")
        sys.exit(0)
    
    if args.check:
        check_services()
        sys.exit(0)
    
    # 根据模式启动
    success = False
    
    if args.mode == 'docker':
        success = start_docker_development()
    elif args.mode == 'local':
        success = start_local_development()
    elif args.mode == 'all':
        print("\n🔍 尝试多种启动方式...")
        
        # 先尝试Docker
        print("\n[尝试Docker启动]")
        if start_docker_development():
            success = True
        else:
            print("\n[尝试本地启动]")
            success = start_local_development()
    
    if success:
        print("\n" + "=" * 60)
        print("🎉 iStock项目启动成功！")
        
        # 检查服务状态
        time.sleep(5)
        check_services()
        
        # 显示使用说明
        show_usage_instructions()
        
        print("\n💡 提示: 服务可能需要几分钟完全启动")
        print("       请耐心等待并刷新浏览器")
    else:
        print("\n❌ iStock项目启动失败")
        print("\n💡 故障排除:")
        print("  1. 检查Docker是否运行: docker info")
        print("  2. 检查端口是否被占用: netstat -ano | findstr :8000")
        print("  3. 查看日志: docker-compose logs")
        print("  4. 尝试手动启动: cd myStock-AI && docker-compose up")
        
        sys.exit(1)

if __name__ == "__main__":
    main()