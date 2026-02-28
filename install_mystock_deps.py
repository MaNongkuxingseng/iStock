#!/usr/bin/env python3
"""
安装mystock项目所需的所有依赖
"""

import subprocess
import sys

# mystock项目所需的所有依赖
DEPENDENCIES = [
    # Web框架
    "tornado",
    
    # 数据库
    "pymysql",
    "sqlalchemy",
    
    # 数据处理
    "pandas",
    "numpy",
    
    # 技术分析
    "talib",
    
    # 网络请求
    "requests",
    
    # 网页解析
    "beautifulsoup4",
    "lxml",
    
    # 进度显示
    "tqdm",
    
    # JavaScript引擎
    "py_mini_racer",
    
    # 其他
    "colorama",
    "soupsieve",
    "typing-extensions",
    "greenlet",
]

def install_dependency(dep):
    """安装单个依赖"""
    print(f"安装 {dep}...", end=" ")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", dep, "--target=D:\Program Files\Python\Lib\site-packages"],
            capture_output=True,
            text=True,
            timeout=120
        )
        if result.returncode == 0:
            print("✓ 成功")
            return True
        else:
            print(f"✗ 失败: {result.stderr[:100]}")
            return False
    except subprocess.TimeoutExpired:
        print("✗ 超时")
        return False
    except Exception as e:
        print(f"✗ 异常: {e}")
        return False

def verify_dependency(dep):
    """验证依赖是否安装成功"""
    module_name = dep.replace("-", "_")
    try:
        __import__(module_name)
        return True
    except ImportError:
        return False

def main():
    print("=" * 60)
    print("开始安装mystock项目依赖")
    print("=" * 60)
    
    success_count = 0
    fail_count = 0
    
    # 安装所有依赖
    for dep in DEPENDENCIES:
        if install_dependency(dep):
            success_count += 1
        else:
            fail_count += 1
    
    print("\n" + "=" * 60)
    print("安装完成统计:")
    print(f"  成功: {success_count}")
    print(f"  失败: {fail_count}")
    print("=" * 60)
    
    # 验证安装
    print("\n验证安装结果:")
    for dep in DEPENDENCIES:
        if verify_dependency(dep):
            print(f"  {dep}: ✓ 已安装")
        else:
            print(f"  {dep}: ✗ 未安装")
    
    print("\n" + "=" * 60)
    if fail_count == 0:
        print("所有依赖安装成功！可以运行mystock项目。")
    else:
        print(f"有 {fail_count} 个依赖安装失败，请手动安装。")
    print("=" * 60)

if __name__ == "__main__":
    main()