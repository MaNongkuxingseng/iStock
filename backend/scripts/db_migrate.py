#!/usr/bin/env python3
"""
数据库迁移管理脚本
用于初始化、升级和回滚数据库
"""

import os
import sys
import subprocess
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

def run_command(cmd, cwd=None):
    """运行命令并返回结果"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            cwd=cwd
        )
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return 1, "", str(e)

def init_database():
    """初始化数据库"""
    print("🔧 初始化数据库...")
    
    # 检查Alembic配置
    alembic_ini = project_root / "backend" / "alembic.ini"
    if not alembic_ini.exists():
        print("❌ 未找到alembic.ini配置文件")
        return False
    
    # 运行Alembic初始化（如果未初始化）
    alembic_dir = project_root / "backend" / "alembic"
    if not (alembic_dir / "env.py").exists():
        print("📦 初始化Alembic迁移环境...")
        code, out, err = run_command("alembic init alembic", cwd=project_root / "backend")
        if code != 0:
            print(f"❌ Alembic初始化失败: {err}")
            return False
    
    # 创建初始迁移
    print("📝 创建初始迁移...")
    code, out, err = run_command(
        "alembic revision --autogenerate -m 'Initial tables'",
        cwd=project_root / "backend"
    )
    
    if code != 0:
        print(f"❌ 创建迁移失败: {err}")
        return False
    
    # 应用迁移
    print("🚀 应用数据库迁移...")
    code, out, err = run_command(
        "alembic upgrade head",
        cwd=project_root / "backend"
    )
    
    if code == 0:
        print("✅ 数据库初始化完成")
        return True
    else:
        print(f"❌ 数据库迁移失败: {err}")
        return False

def upgrade_database():
    """升级数据库到最新版本"""
    print("🔼 升级数据库...")
    
    code, out, err = run_command(
        "alembic upgrade head",
        cwd=project_root / "backend"
    )
    
    if code == 0:
        print("✅ 数据库升级完成")
        return True
    else:
        print(f"❌ 数据库升级失败: {err}")
        return False

def downgrade_database(version="-1"):
    """回滚数据库版本"""
    print("🔽 回滚数据库...")
    
    code, out, err = run_command(
        f"alembic downgrade {version}",
        cwd=project_root / "backend"
    )
    
    if code == 0:
        print(f"✅ 数据库回滚到版本 {version} 完成")
        return True
    else:
        print(f"❌ 数据库回滚失败: {err}")
        return False

def show_migration_history():
    """显示迁移历史"""
    print("📜 迁移历史:")
    
    code, out, err = run_command(
        "alembic history",
        cwd=project_root / "backend"
    )
    
    if code == 0:
        print(out)
    else:
        print(f"❌ 获取迁移历史失败: {err}")

def create_migration(message):
    """创建新的迁移"""
    print(f"📝 创建迁移: {message}")
    
    code, out, err = run_command(
        f'alembic revision --autogenerate -m "{message}"',
        cwd=project_root / "backend"
    )
    
    if code == 0:
        print("✅ 迁移创建成功")
        return True
    else:
        print(f"❌ 迁移创建失败: {err}")
        return False

def check_database_status():
    """检查数据库状态"""
    print("🔍 检查数据库状态...")
    
    # 检查当前版本
    code, out, err = run_command(
        "alembic current",
        cwd=project_root / "backend"
    )
    
    if code == 0:
        print(f"当前版本: {out.strip()}")
    else:
        print(f"❌ 获取当前版本失败: {err}")
    
    # 检查是否有待应用的迁移
    code, out, err = run_command(
        "alembic heads",
        cwd=project_root / "backend"
    )
    
    if code == 0:
        heads = out.strip().split('\n')
        current_code, current_out, current_err = run_command(
            "alembic current",
            cwd=project_root / "backend"
        )
        
        if current_code == 0:
            current = current_out.strip()
            if current not in heads:
                print("⚠️  有未应用的迁移")
                show_migration_history()
            else:
                print("✅ 数据库已是最新版本")
        else:
            print("❌ 无法确定数据库状态")
    else:
        print(f"❌ 检查迁移头失败: {err}")

def seed_initial_data():
    """播种初始数据"""
    print("🌱 播种初始数据...")
    
    # 这里可以添加初始数据插入逻辑
    # 例如：创建默认用户、测试股票数据等
    
    seed_script = """
# 初始数据播种脚本
# 这里可以添加SQL插入语句或调用Python脚本
print("初始数据播种功能待实现")
"""
    
    seed_file = project_root / "backend" / "scripts" / "seed_data.py"
    seed_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(seed_file, "w", encoding="utf-8") as f:
        f.write(seed_script)
    
    print(f"📄 播种脚本已创建: {seed_file}")
    print("💡 请编辑此文件添加具体的初始数据逻辑")
    
    return True

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='数据库迁移管理工具')
    parser.add_argument('action', choices=[
        'init', 'upgrade', 'downgrade', 'history', 
        'create', 'status', 'seed', 'all'
    ], help='执行的操作')
    parser.add_argument('--message', '-m', help='迁移描述信息')
    parser.add_argument('--version', '-v', default='-1', help='回滚到的版本')
    
    args = parser.parse_args()
    
    actions = {
        'init': init_database,
        'upgrade': upgrade_database,
        'downgrade': lambda: downgrade_database(args.version),
        'history': show_migration_history,
        'create': lambda: create_migration(args.message or 'Auto-generated migration'),
        'status': check_database_status,
        'seed': seed_initial_data,
    }
    
    if args.action == 'all':
        # 执行所有初始化步骤
        print("🚀 执行完整数据库初始化流程...")
        success = True
        success = success and init_database()
        success = success and seed_initial_data()
        success = success and check_database_status()
        
        if success:
            print("🎉 数据库完整初始化完成")
        else:
            print("❌ 数据库初始化过程中出现错误")
            sys.exit(1)
    else:
        if args.action in actions:
            func = actions[args.action]
            success = func()
            
            if not success:
                sys.exit(1)
        else:
            print(f"❌ 未知操作: {args.action}")
            sys.exit(1)

if __name__ == "__main__":
    main()