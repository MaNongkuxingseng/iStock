"""
iStock本地模式启动脚本
"""

import os
import sys
import subprocess
import time
import webbrowser


def check_python():
    """检查Python环境"""
    try:
        import sys
        if sys.version_info < (3, 10):
            print("❌ Python版本过低，请安装Python 3.10+")
            return False
        print("✅ Python环境检查通过")
        return True
    except Exception as e:
        print(f"❌ Python环境检查失败: {e}")
        return False

def install_dependencies():
    """安装依赖"""
    try:
        print("📦 正在安装依赖...")
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "--upgrade", "pip"
        ], capture_output=True, text=True)
        
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "local/requirements.txt"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ 依赖安装成功")
            return True
        else:
            print(f"❌ 依赖安装失败: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ 依赖安装异常: {e}")
        return False

def start_server():
    """启动服务器"""
    try:
        print("🌐 正在启动iStock服务...")
        # 打开浏览器
        webbrowser.open("http://localhost:8000/docs")
        
        # 启动FastAPI
        os.system(f"{sys.executable} local/app.py")
        
        return True
    except Exception as e:
        print(f"❌ 服务启动失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 启动iStock本地化运行模式...")
    print("==================================")
    
    if not check_python():
        return
    
    if not install_dependencies():
        return
    
    print("✅ 本地模式部署完成！")
    print("💡 访问 http://localhost:8000/docs 查看API文档")
    print("💡 访问 http://localhost:3000 查看前端界面（需单独启动）")
    
    # 启动服务器
    start_server()

if __name__ == "__main__":
    main()