#!/usr/bin/env python3
"""
Docker环境验证脚本
验证Docker安装和iStock项目Docker配置
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def run_command(cmd):
    """运行命令并返回结果"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return 1, "", "命令执行超时"
    except Exception as e:
        return 1, "", str(e)

def check_docker_installation():
    """检查Docker安装"""
    print("🔍 检查Docker安装...")
    
    # 检查docker命令
    code, out, err = run_command("docker --version")
    
    if code == 0:
        print(f"✅ Docker已安装: {out.strip()}")
        return True
    else:
        print("❌ Docker未安装或不在PATH中")
        print("💡 解决方案:")
        print("  1. 确保Docker Desktop已启动")
        print("  2. 将Docker添加到系统PATH")
        print("  3. 重启命令行终端")
        return False

def check_docker_compose():
    """检查Docker Compose"""
    print("🔍 检查Docker Compose...")
    
    code, out, err = run_command("docker-compose --version")
    
    if code == 0:
        print(f"✅ Docker Compose已安装: {out.strip()}")
        return True
    else:
        # 尝试使用docker compose子命令
        code2, out2, err2 = run_command("docker compose version")
        if code2 == 0:
            print(f"✅ Docker Compose (插件版)已安装: {out2.strip()}")
            return True
        else:
            print("❌ Docker Compose未安装")
            return False

def check_docker_daemon():
    """检查Docker守护进程"""
    print("🔍 检查Docker守护进程...")
    
    code, out, err = run_command("docker info")
    
    if code == 0:
        print("✅ Docker守护进程运行正常")
        
        # 提取有用信息
        lines = out.split('\n')
        for line in lines[:10]:  # 显示前10行信息
            if line.strip():
                print(f"  {line}")
        return True
    else:
        print("❌ Docker守护进程未运行")
        print(f"错误信息: {err}")
        return False

def check_docker_images():
    """检查Docker镜像"""
    print("🔍 检查Docker镜像...")
    
    code, out, err = run_command("docker images")
    
    if code == 0:
        lines = out.strip().split('\n')
        if len(lines) > 1:
            print(f"✅ 找到 {len(lines)-1} 个Docker镜像")
            for line in lines[:5]:  # 显示前5个镜像
                print(f"  {line}")
        else:
            print("ℹ️  没有找到Docker镜像")
        return True
    else:
        print("❌ 无法获取Docker镜像列表")
        return False

def check_iStock_docker_files():
    """检查iStock项目的Docker文件"""
    print("🔍 检查iStock Docker文件...")
    
    project_root = Path(__file__).parent.parent
    required_files = [
        ("docker-compose.yml", "开发环境配置"),
        ("docker-compose.prod.yml", "生产环境配置"),
        ("Dockerfile.backend", "后端Dockerfile"),
        ("Dockerfile.frontend", "前端Dockerfile"),
        ("docker/nginx/nginx.conf", "Nginx配置"),
        ("docker/postgres/init.sql", "数据库初始化脚本"),
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

def validate_docker_compose_config():
    """验证docker-compose配置"""
    print("🔍 验证docker-compose配置...")
    
    project_root = Path(__file__).parent.parent
    compose_file = project_root / "docker-compose.yml"
    
    if not compose_file.exists():
        print("❌ docker-compose.yml文件不存在")
        return False
    
    try:
        with open(compose_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查关键服务
        required_services = ['postgres', 'redis', 'backend', 'frontend']
        missing_services = []
        
        for service in required_services:
            if service in content:
                print(f"  ✅ {service}服务配置")
            else:
                print(f"  ❌ {service}服务配置 (缺失)")
                missing_services.append(service)
        
        if missing_services:
            print(f"⚠️  缺失服务: {', '.join(missing_services)}")
            return False
        else:
            print("✅ docker-compose配置完整")
            return True
            
    except Exception as e:
        print(f"❌ 读取docker-compose文件失败: {e}")
        return False

def test_docker_compose_build():
    """测试Docker Compose构建"""
    print("🔨 测试Docker Compose构建...")
    
    project_root = Path(__file__).parent.parent
    
    print("注意: 构建可能需要几分钟时间...")
    code, out, err = run_command("docker-compose build --no-cache backend")
    
    if code == 0:
        print("✅ Docker Compose构建成功")
        return True
    else:
        print("❌ Docker Compose构建失败")
        print(f"错误信息: {err[:500]}...")  # 只显示前500字符
        return False

def test_docker_compose_up():
    """测试Docker Compose启动"""
    print("🚀 测试Docker Compose启动...")
    
    print("启动服务（这可能需要一些时间）...")
    code, out, err = run_command("docker-compose up -d")
    
    if code == 0:
        print("✅ Docker Compose启动成功")
        
        # 检查服务状态
        code2, out2, err2 = run_command("docker-compose ps")
        if code2 == 0:
            print("📊 服务状态:")
            print(out2)
        
        return True
    else:
        print("❌ Docker Compose启动失败")
        print(f"错误信息: {err[:500]}...")
        return False

def check_service_health():
    """检查服务健康状态"""
    print("🏥 检查服务健康状态...")
    
    import time
    import requests
    
    services = [
        ("后端API", "http://localhost:8000/health", 30),
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

def cleanup_test():
    """清理测试环境"""
    print("🧹 清理测试环境...")
    
    code, out, err = run_command("docker-compose down")
    
    if code == 0:
        print("✅ 测试环境清理完成")
        return True
    else:
        print("❌ 清理失败")
        return False

def run_comprehensive_test():
    """运行全面测试"""
    print("🧪 Docker环境全面测试")
    print("=" * 60)
    
    tests = [
        ("Docker安装", check_docker_installation),
        ("Docker Compose", check_docker_compose),
        ("Docker守护进程", check_docker_daemon),
        ("Docker镜像", check_docker_images),
        ("iStock Docker文件", check_iStock_docker_files),
        ("docker-compose配置", validate_docker_compose_config),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n[{test_name}]")
        try:
            success = test_func()
            results.append((test_name, success))
            print(f"结果: {'✅ 通过' if success else '❌ 失败'}")
        except Exception as e:
            print(f"❌ 测试异常: {e}")
            results.append((test_name, False))
    
    # 检查是否所有基础测试都通过
    all_basic_passed = all(result for _, result in results)
    
    if all_basic_passed:
        print("\n🎉 所有基础测试通过，开始构建测试...")
        
        build_tests = [
            ("Docker Compose构建", test_docker_compose_build),
            ("Docker Compose启动", test_docker_compose_up),
            ("服务健康检查", check_service_health),
        ]
        
        for test_name, test_func in build_tests:
            print(f"\n[{test_name}]")
            try:
                success = test_func()
                results.append((test_name, success))
                print(f"结果: {'✅ 通过' if success else '❌ 失败'}")
            except Exception as e:
                print(f"❌ 测试异常: {e}")
                results.append((test_name, False))
        
        # 清理
        print("\n[环境清理]")
        cleanup_success = cleanup_test()
        results.append(("环境清理", cleanup_success))
    
    print("\n" + "=" * 60)
    print("📊 测试总结:")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name}: {status}")
    
    print(f"\n总计: {passed}/{total} 通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！Docker环境配置正确。")
        print("\n下一步:")
        print("1. 启动开发环境: docker-compose up -d")
        print("2. 访问后端API: http://localhost:8000/docs")
        print("3. 访问前端应用: http://localhost:3000")
        return True
    else:
        print("\n⚠️  部分测试失败，请根据错误信息进行修复。")
        return False

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Docker环境验证工具')
    parser.add_argument('--test', '-t', choices=['basic', 'build', 'full'], default='full', help='测试类型')
    
    args = parser.parse_args()
    
    if args.test == 'full':
        success = run_comprehensive_test()
    elif args.test == 'basic':
        # 只运行基础测试
        tests = [
            check_docker_installation,
            check_docker_compose,
            check_docker_daemon,
            check_iStock_docker_files,
            validate_docker_compose_config,
        ]
        
        success = all(test() for test in tests)
    elif args.test == 'build':
        # 运行构建测试
        success = test_docker_compose_build() and test_docker_compose_up()
    else:
        print(f"❌ 未知测试类型: {args.test}")
        sys.exit(1)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()