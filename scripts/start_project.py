#!/usr/bin/env python3
"""
iStock项目启动脚本
一键启动和配置整个项目
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def run_command(cmd, cwd=None, timeout=60):
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

def check_prerequisites():
    """检查前置条件"""
    print("🔍 检查前置条件...")
    
    checks = [
        ("Python 3.10+", "python --version", "Python 3.10"),
        ("Git", "git --version", "git version"),
        ("Docker", "docker --version", "Docker version"),
        ("Docker Compose", "docker-compose --version", "docker-compose version"),
    ]
    
    all_passed = True
    for name, cmd, expected in checks:
        code, out, err = run_command(cmd, timeout=10)
        if code == 0 and expected in out:
            print(f"  ✅ {name}")
        else:
            print(f"  ❌ {name}")
            all_passed = False
    
    return all_passed

def setup_environment():
    """设置环境"""
    print("⚙️  设置环境...")
    
    project_root = Path(__file__).parent.parent
    
    # 1. 创建.env文件（如果不存在）
    env_example = project_root / ".env.example"
    env_file = project_root / ".env"
    
    if not env_file.exists() and env_example.exists():
        print("📄 创建.env配置文件...")
        import shutil
        shutil.copy(env_example, env_file)
        print("✅ .env文件已创建（请根据需要修改配置）")
    elif env_file.exists():
        print("✅ .env文件已存在")
    
    # 2. 创建必要的目录
    directories = [
        "backend/logs",
        "frontend/logs",
        "data/postgres",
        "data/redis",
        "data/celery",
    ]
    
    for directory in directories:
        dir_path = project_root / directory
        dir_path.mkdir(parents=True, exist_ok=True)
    
    print("✅ 目录结构已创建")
    return True

def install_dependencies():
    """安装依赖"""
    print("📦 安装依赖...")
    
    project_root = Path(__file__).parent.parent
    
    # 1. 创建虚拟环境（如果不存在）
    venv_path = project_root / ".venv"
    if not venv_path.exists():
        print("🐍 创建Python虚拟环境...")
        code, out, err = run_command("python -m venv .venv", cwd=project_root)
        if code != 0:
            print(f"❌ 创建虚拟环境失败: {err}")
            return False
        print("✅ 虚拟环境已创建")
    
    # 2. 激活虚拟环境并安装依赖
    print("📦 安装Python依赖...")
    
    # 根据操作系统确定激活脚本
    if sys.platform == "win32":
        pip_path = venv_path / "Scripts" / "pip.exe"
        python_path = venv_path / "Scripts" / "python.exe"
    else:
        pip_path = venv_path / "bin" / "pip"
        python_path = venv_path / "bin" / "python"
    
    # 安装后端依赖
    requirements_file = project_root / "requirements.txt"
    if requirements_file.exists():
        code, out, err = run_command(f'"{pip_path}" install -r requirements.txt', cwd=project_root)
        if code != 0:
            print(f"❌ 安装后端依赖失败: {err}")
            return False
        print("✅ 后端依赖已安装")
    
    # 安装开发依赖
    requirements_dev_file = project_root / "requirements-dev.txt"
    if requirements_dev_file.exists():
        code, out, err = run_command(f'"{pip_path}" install -r requirements-dev.txt', cwd=project_root)
        if code != 0:
            print(f"⚠️  安装开发依赖失败: {err}")
        else:
            print("✅ 开发依赖已安装")
    
    # 安装前端依赖
    frontend_dir = project_root / "frontend"
    package_json = frontend_dir / "package.json"
    if package_json.exists():
        print("📦 安装前端依赖...")
        code, out, err = run_command("npm install", cwd=frontend_dir, timeout=300)
        if code != 0:
            print(f"⚠️  安装前端依赖失败: {err}")
        else:
            print("✅ 前端依赖已安装")
    
    return True

def build_docker_images():
    """构建Docker镜像"""
    print("🐳 构建Docker镜像...")
    
    project_root = Path(__file__).parent.parent
    
    print("注意: 构建可能需要几分钟时间...")
    
    # 构建后端镜像
    print("🔨 构建后端镜像...")
    code, out, err = run_command("docker-compose build backend", cwd=project_root, timeout=300)
    if code != 0:
        print(f"❌ 构建后端镜像失败: {err[:500]}...")
        return False
    print("✅ 后端镜像构建完成")
    
    # 构建前端镜像
    print("🔨 构建前端镜像...")
    code, out, err = run_command("docker-compose build frontend", cwd=project_root, timeout=300)
    if code != 0:
        print(f"⚠️  构建前端镜像失败: {err[:500]}...")
    else:
        print("✅ 前端镜像构建完成")
    
    return True

def start_services():
    """启动服务"""
    print("🚀 启动服务...")
    
    project_root = Path(__file__).parent.parent
    
    # 启动所有服务
    print("启动Docker Compose服务...")
    code, out, err = run_command("docker-compose up -d", cwd=project_root, timeout=120)
    
    if code != 0:
        print(f"❌ 启动服务失败: {err[:500]}...")
        return False
    
    print("✅ 服务启动成功")
    
    # 等待服务启动
    print("⏳ 等待服务就绪...")
    time.sleep(10)
    
    # 检查服务状态
    code, out, err = run_command("docker-compose ps", cwd=project_root)
    if code == 0:
        print("📊 服务状态:")
        print(out)
    
    return True

def initialize_database():
    """初始化数据库"""
    print("🗄️  初始化数据库...")
    
    project_root = Path(__file__).parent.parent
    
    # 运行数据库迁移
    print("运行数据库迁移...")
    code, out, err = run_command(
        "docker-compose exec backend alembic upgrade head",
        cwd=project_root,
        timeout=60
    )
    
    if code != 0:
        print(f"❌ 数据库迁移失败: {err[:500]}...")
        return False
    
    print("✅ 数据库迁移完成")
    
    # 播种初始数据
    print("🌱 播种初始数据...")
    code, out, err = run_command(
        "docker-compose exec backend python backend/scripts/seed_data.py",
        cwd=project_root,
        timeout=120
    )
    
    if code != 0:
        print(f"⚠️  播种数据失败: {err[:500]}...")
    else:
        print("✅ 初始数据播种完成")
    
    return True

def verify_services():
    """验证服务"""
    print("🔍 验证服务...")
    
    import requests
    import time
    
    services = [
        ("后端API", "http://localhost:8000/health", 30),
        ("API文档", "http://localhost:8000/docs", 30),
        ("前端应用", "http://localhost:3000", 60),
    ]
    
    all_healthy = True
    for service_name, url, timeout in services:
        print(f"  检查 {service_name} ({url})...")
        
        start_time = time.time()
        healthy = False
        
        while time.time() - start_time < timeout:
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    healthy = True
                    break
            except:
                pass
            
            time.sleep(2)
        
        if healthy:
            print(f"    ✅ {service_name} 健康")
        else:
            print(f"    ❌ {service_name} 未响应")
            all_healthy = False
    
    return all_healthy

def show_project_info():
    """显示项目信息"""
    print("\n" + "=" * 60)
    print("🎉 iStock项目启动完成！")
    print("=" * 60)
    
    print("\n📊 项目信息:")
    print("-" * 40)
    print("项目名称: iStock - 智能股票分析系统")
    print("项目位置:", Path(__file__).parent.parent)
    print("启动时间:", time.strftime("%Y-%m-%d %H:%M:%S"))
    
    print("\n🌐 访问地址:")
    print("-" * 40)
    print("后端API:      http://localhost:8000")
    print("API文档:      http://localhost:8000/docs")
    print("前端应用:      http://localhost:3000")
    print("数据库管理:    localhost:5432")
    print("Redis管理:     localhost:6379")
    print("Celery监控:   http://localhost:5555")
    
    print("\n🔧 管理命令:")
    print("-" * 40)
    print("查看服务状态:  docker-compose ps")
    print("查看服务日志:  docker-compose logs -f")
    print("停止服务:      docker-compose down")
    print("重启服务:      docker-compose restart")
    print("重建镜像:      docker-compose build --no-cache")
    
    print("\n📁 项目结构:")
    print("-" * 40)
    project_root = Path(__file__).parent.parent
    for item in project_root.iterdir():
        if item.is_dir():
            print(f"📁 {item.name}/")
        elif item.suffix in ['.py', '.md', '.yml', '.toml']:
            print(f"📄 {item.name}")
    
    print("\n🚀 下一步:")
    print("-" * 40)
    print("1. 访问 http://localhost:3000 开始使用")
    print("2. 查看 http://localhost:8000/docs 了解API")
    print("3. 运行测试: docker-compose exec backend pytest")
    print("4. 查看日志: docker-compose logs -f backend")
    
    print("\n" + "=" * 60)

def run_full_setup():
    """运行完整设置"""
    print("🚀 iStock项目完整设置")
    print("=" * 60)
    
    steps = [
        ("检查前置条件", check_prerequisites),
        ("设置环境", setup_environment),
        ("安装依赖", install_dependencies),
        ("构建Docker镜像", build_docker_images),
        ("启动服务", start_services),
        ("初始化数据库", initialize_database),
        ("验证服务", verify_services),
    ]
    
    results = []
    for step_name, step_func in steps:
        print(f"\n[{step_name}]")
        try:
            success = step_func()
            results.append((step_name, success))
            print(f"结果: {'✅ 成功' if success else '❌ 失败'}")
            
            if not success and step_name != "验证服务":
                print("⚠️  设置失败，停止后续步骤")
                break
                
        except Exception as e:
            print(f"❌ 步骤异常: {e}")
            results.append((step_name, False))
            break
    
    print("\n" + "=" * 60)
    print("📊 设置总结:")
    print("=" * 60)
    
    successful = sum(1 for _, result in results if result)
    total = len(results)
    
    for step_name, result in results:
        status = "✅ 成功" if result else "❌ 失败"
        print(f"{step_name}: {status}")
    
    print(f"\n总计: {successful}/{total} 成功")
    
    if successful == total:
        show_project_info()
        return True
    else:
        print("\n⚠️  部分设置失败，请检查错误信息。")
        print("\n💡 常见问题解决:")
        print("1. Docker未启动: 启动Docker Desktop")
        print("2. 端口冲突: 修改docker-compose.yml中的端口")
        print("3. 依赖安装失败: 检查网络连接")
        print("4. 数据库连接失败: 检查.env文件配置")
        return False

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='iStock项目启动工具')
    parser.add_argument('--step', '-s', choices=[
        'prereq', 'env', 'deps', 'build', 'start', 
        'db', 'verify', 'info', 'all'
    ], default='all', help='要执行的步骤')
    
    args = parser.parse_args()
    
    if args.step == 'all':
        success = run_full_setup()
    elif args.step == 'prereq':
        success = check_prerequisites()
    elif args.step == 'env':
        success = setup_environment()
    elif args.step == 'deps':
        success = install_dependencies()
    elif args.step == 'build':
        success = build_docker_images()
    elif args.step == 'start':
        success = start_services()
    elif args.step == 'db':
        success = initialize_database()
    elif args.step == 'verify':
        success = verify_services()
    elif args.step == 'info':
        show_project_info()
        success = True
    else:
        print(f"❌ 未知步骤: {args.step}")
        sys.exit(1)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()