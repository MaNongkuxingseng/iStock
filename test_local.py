#!/usr/bin/env python3
"""
本地测试脚本 - 不依赖Docker
"""

import sys
import os
import subprocess
import time
import requests

def check_python():
    """检查Python环境"""
    print("检查Python环境...")
    try:
        result = subprocess.run([sys.executable, "--version"], 
                              capture_output=True, text=True)
        print(f"✓ Python版本: {result.stdout.strip()}")
        return True
    except Exception as e:
        print(f"✗ Python检查失败: {e}")
        return False

def check_dependencies():
    """检查依赖"""
    print("\n检查Python依赖...")
    requirements_file = "backend/requirements.txt"
    
    if not os.path.exists(requirements_file):
        print(f"✗ 依赖文件不存在: {requirements_file}")
        return False
    
    try:
        # 检查主要依赖
        import fastapi
        import sqlalchemy
        import uvicorn
        print("✓ 主要依赖已安装")
        return True
    except ImportError as e:
        print(f"✗ 依赖缺失: {e}")
        print("请运行: pip install -r backend/requirements.txt")
        return False

def start_local_server():
    """启动本地开发服务器"""
    print("\n启动本地开发服务器...")
    
    # 切换到backend目录
    original_dir = os.getcwd()
    backend_dir = os.path.join(original_dir, "backend")
    
    if not os.path.exists(backend_dir):
        print(f"✗ backend目录不存在: {backend_dir}")
        return False
    
    os.chdir(backend_dir)
    
    try:
        # 启动服务器（在后台）
        server_process = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "src.api.main:app", 
             "--host", "0.0.0.0", "--port", "8000", "--reload"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        print("✓ 服务器进程已启动 (PID: {})".format(server_process.pid))
        
        # 等待服务器启动
        print("等待服务器启动 (10秒)...")
        time.sleep(10)
        
        # 测试服务器
        test_url = "http://localhost:8000/health"
        try:
            response = requests.get(test_url, timeout=5)
            if response.status_code == 200:
                print(f"✓ 服务器响应正常: {response.json()}")
                return True, server_process
            else:
                print(f"✗ 服务器响应异常: {response.status_code}")
                return False, server_process
        except requests.RequestException as e:
            print(f"✗ 服务器连接失败: {e}")
            return False, server_process
            
    except Exception as e:
        print(f"✗ 启动服务器失败: {e}")
        return False, None
    finally:
        os.chdir(original_dir)

def test_api_endpoints():
    """测试API端点"""
    print("\n测试API端点...")
    
    endpoints = [
        ("/health", "健康检查"),
        ("/docs", "API文档"),
        ("/api/v1/docs", "API文档v1"),
        ("/", "根端点")
    ]
    
    for endpoint, description in endpoints:
        url = f"http://localhost:8000{endpoint}"
        try:
            response = requests.get(url, timeout=5)
            print(f"✓ {description}: {response.status_code}")
        except requests.RequestException:
            print(f"✗ {description}: 连接失败")

def main():
    """主函数"""
    print("=" * 50)
    print("iStock 本地测试脚本")
    print("=" * 50)
    
    # 检查环境
    if not check_python():
        return 1
    
    if not check_dependencies():
        return 1
    
    # 启动服务器
    success, server_process = start_local_server()
    
    if success:
        print("\n" + "=" * 50)
        print("✅ 本地测试成功!")
        print("=" * 50)
        print("\n可用链接:")
        print("1. 后端API: http://localhost:8000")
        print("2. API文档: http://localhost:8000/docs")
        print("3. 健康检查: http://localhost:8000/health")
        print("\n测试API端点...")
        test_api_endpoints()
        
        print("\n" + "=" * 50)
        print("服务器正在运行...")
        print("按 Ctrl+C 停止服务器")
        print("=" * 50)
        
        try:
            # 保持服务器运行
            server_process.wait()
        except KeyboardInterrupt:
            print("\n正在停止服务器...")
            server_process.terminate()
            server_process.wait()
            print("服务器已停止")
            
    else:
        print("\n" + "=" * 50)
        print("❌ 本地测试失败")
        print("=" * 50)
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())