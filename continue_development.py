#!/usr/bin/env python3
"""
继续iStock开发任务
在环境准备期间进行代码整理和交付准备
"""

import os
import json
import shutil
from datetime import datetime
from pathlib import Path

def organize_code_for_delivery():
    """整理代码准备交付"""
    print("Organizing code for delivery...")
    
    project_root = Path(".")
    delivery_dir = project_root / "delivery_prepared"
    delivery_dir.mkdir(exist_ok=True)
    
    # 创建交付目录结构
    dirs_to_create = [
        "source_code",
        "documentation", 
        "configuration",
        "scripts",
        "test_reports"
    ]
    
    for dir_name in dirs_to_create:
        (delivery_dir / dir_name).mkdir(exist_ok=True)
    
    # 1. 整理源代码
    print("\n1. Organizing source code...")
    
    # 后端代码
    backend_files = [
        "backend/src/main.py",
        "backend/src/api/",
        "backend/src/database/",
        "backend/src/models/",
        "backend/src/services/",
        "backend/src/utils/",
        "backend/requirements.txt"
    ]
    
    for item in backend_files:
        source = project_root / item
        if source.exists():
            if source.is_file():
                target = delivery_dir / "source_code" / "backend" / source.relative_to(project_root / "backend")
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target)
                print(f"  Copied: {item}")
            elif source.is_dir():
                # 复制整个目录
                target = delivery_dir / "source_code" / "backend" / source.relative_to(project_root / "backend")
                shutil.copytree(source, target, dirs_exist_ok=True)
                print(f"  Copied directory: {item}")
    
    # 前端代码
    frontend_files = [
        "frontend/package.json",
        "frontend/src/",
        "frontend/public/"
    ]
    
    for item in frontend_files:
        source = project_root / item
        if source.exists():
            if source.is_file():
                target = delivery_dir / "source_code" / "frontend" / source.name
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target)
                print(f"  Copied: {item}")
            elif source.is_dir():
                target = delivery_dir / "source_code" / "frontend" / source.relative_to(project_root / "frontend")
                shutil.copytree(source, target, dirs_exist_ok=True)
                print(f"  Copied directory: {item}")
    
    # 2. 整理文档
    print("\n2. Organizing documentation...")
    
    doc_sources = [
        "docs/",
        "knowledge/",
        "README.md",
        "DEVELOPMENT_PLAN.md",
        "PROJECT_STRUCTURE.md"
    ]
    
    for item in doc_sources:
        source = project_root / item
        if source.exists():
            if source.is_file():
                target = delivery_dir / "documentation" / source.name
                shutil.copy2(source, target)
                print(f"  Copied: {item}")
            elif source.is_dir():
                target = delivery_dir / "documentation" / source.name
                shutil.copytree(source, target, dirs_exist_ok=True)
                print(f"  Copied directory: {item}")
    
    # 3. 整理配置文件
    print("\n3. Organizing configuration files...")
    
    config_files = [
        "docker-compose.yml",
        "docker-compose-fixed.yml",
        "docker-compose-minimal.yml",
        "docker-compose.prod.yml",
        "Dockerfile.backend",
        "Dockerfile.frontend",
        ".env.example",
        ".gitignore",
        "pyproject.toml",
        "requirements.txt",
        "requirements-dev.txt"
    ]
    
    for file in config_files:
        source = project_root / file
        if source.exists():
            target = delivery_dir / "configuration" / file
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
            print(f"  Copied: {file}")
    
    # 4. 整理脚本
    print("\n4. Organizing scripts...")
    
    script_files = [
        "run_real_tests_en.py",
        "test_services_en.py",
        "automated_monitor.py",
        "push_watch_en.py",
        "test_alert_simple.py",
        "fix_docker_path.bat",
        "start_backend.bat"
    ]
    
    for file in script_files:
        source = project_root / file
        if source.exists():
            target = delivery_dir / "scripts" / file
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
            print(f"  Copied: {file}")
    
    # 5. 整理测试报告
    print("\n5. Organizing test reports...")
    
    test_reports = list(project_root.glob("*test*report*.json"))
    for report in test_reports:
        target = delivery_dir / "test_reports" / report.name
        shutil.copy2(report, target)
        print(f"  Copied: {report.name}")
    
    print(f"\nDelivery preparation completed in: {delivery_dir}")
    return delivery_dir

def create_delivery_summary(delivery_dir):
    """创建交付摘要"""
    print("\nCreating delivery summary...")
    
    summary = {
        "project": "iStock - Intelligent Stock Analysis System",
        "version": "0.1.0",
        "delivery_date": datetime.now().isoformat(),
        "components": {
            "backend": {
                "status": "structure_ready",
                "dependencies_needed": ["fastapi", "sqlalchemy", "psycopg2-binary"],
                "files_count": count_files(delivery_dir / "source_code" / "backend")
            },
            "frontend": {
                "status": "structure_ready", 
                "dependencies_needed": ["react", "react-dom", "react-scripts"],
                "files_count": count_files(delivery_dir / "source_code" / "frontend")
            },
            "documentation": {
                "status": "complete",
                "files_count": count_files(delivery_dir / "documentation")
            },
            "configuration": {
                "status": "complete",
                "files_count": count_files(delivery_dir / "configuration")
            },
            "scripts": {
                "status": "complete",
                "files_count": count_files(delivery_dir / "scripts")
            }
        },
        "test_results": {
            "real_test_pass_rate": 68.8,
            "monitoring_system": "fully_passed",
            "data_sources": "connection_verified",
            "issues_found": [
                "backend_dependencies_missing",
                "database_module_import_error", 
                "frontend_file_organization_needed"
            ]
        },
        "next_steps": [
            "Install backend dependencies: pip install -r backend/requirements.txt",
            "Fix database module import errors",
            "Organize frontend files correctly",
            "Install frontend dependencies: cd frontend && npm install",
            "Run complete test suite: python run_real_tests_en.py",
            "Start services and verify functionality"
        ],
        "environment_requirements": {
            "python": "3.8+",
            "nodejs": "14+",
            "docker": "20.10+ (optional)",
            "postgresql": "13+ (optional, SQLite supported)",
            "system": "Windows/Linux/macOS"
        }
    }
    
    summary_file = delivery_dir / "DELIVERY_SUMMARY.json"
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print(f"Delivery summary created: {summary_file}")
    
    # 创建README
    readme_content = f"""# iStock Delivery Package

## Project Overview
iStock is an intelligent stock analysis system providing real-time market monitoring, technical analysis, and automated trading suggestions.

## Delivery Contents

### 1. Source Code
- **Backend**: Python + FastAPI application
- **Frontend**: React application
- **Database**: SQLAlchemy models and migrations

### 2. Documentation
- Project documentation in `docs/` directory
- Knowledge base in `knowledge/` directory
- Development plans and architecture documents

### 3. Configuration
- Docker configurations for multiple environments
- Environment variable templates
- Build and deployment configurations

### 4. Scripts
- Real runtime test framework
- Service startup scripts
- Monitoring and alert scripts
- Docker PATH fix tools

### 5. Test Reports
- Real test execution reports
- Service validation results
- Issue identification reports

## Current Status

### Test Results
- Real test pass rate: 68.8%
- Monitoring system: ✅ Fully passed
- Data sources: ✅ Connection verified

### Known Issues
1. Backend dependencies need installation
2. Database module import errors need fixing
3. Frontend file organization needed

## Setup Instructions

### 1. Environment Preparation
```bash
# Install Python dependencies
pip install -r source_code/backend/requirements.txt

# Install Node.js dependencies
cd source_code/frontend
npm install
```

### 2. Fix Known Issues
- Run: `python scripts/run_real_tests_en.py` to identify issues
- Fix database module import errors
- Organize frontend files as needed

### 3. Start Services
```bash
# Start backend
cd source_code/backend
python -m uvicorn src.main:app --reload

# Start frontend
cd source_code/frontend
npm start
```

### 4. Run Tests
```bash
# Run complete test suite
python scripts/run_real_tests_en.py

# Check test reports in test_reports/ directory
```

## Next Development Phase

### Priority Tasks
1. Complete data source API integration
2. Implement machine learning models
3. Enhance user interface
4. Optimize performance

### Quality Assurance
- All new code must pass real runtime tests
- Test coverage target: > 80%
- Continuous integration setup required

## Support

For issues or questions:
1. Check test reports for identified problems
2. Review documentation for setup guidance
3. Run real tests to verify functionality

---

**Delivery Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Version**: 0.1.0
**Status**: Ready for environment setup and testing
"""
    
    readme_file = delivery_dir / "README.md"
    with open(readme_file, "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print(f"README created: {readme_file}")
    
    return summary

def count_files(directory):
    """统计目录中的文件数量"""
    if not directory.exists():
        return 0
    return sum(1 for _ in directory.rglob("*") if _.is_file())

def create_git_commit_plan():
    """创建Git提交计划"""
    print("\nCreating Git commit plan...")
    
    commit_plan = {
        "commits": [
            {
                "type": "feat",
                "message": "建立真实运行测试机制和框架",
                "files": [
                    "run_real_tests_en.py",
                    "real_time_test_framework.py",
                    "REAL_TEST_SUMMARY.md"
                ]
            },
            {
                "type": "fix", 
                "message": "修复项目结构问题，重新组织文件",
                "files": [
                    "fix_project_structure.py",
                    "backend/src/",
                    "frontend/src/"
                ]
            },
            {
                "type": "docs",
                "message": "更新项目文档和知识库",
                "files": [
                    "docs/",
                    "knowledge/",
                    "README.md"
                ]
            },
            {
                "type": "chore",
                "message": "添加Docker PATH修复工具和配置",
                "files": [
                    "fix_docker_path.bat",
                    "docker_fullpath.bat",
                    "docker-compose_fullpath.bat"
                ]
            },
            {
                "type": "test",
                "message": "添加服务测试脚本和报告",
                "files": [
                    "test_services_en.py",
                    "service_test_report.json",
                    "real_test_report_*.json"
                ]
            }
        ],
        "branch": "develop",
        "remote": "origin",
        "push_command": "git push origin develop"
    }
    
    plan_file = Path(".") / "GIT_COMMIT_PLAN.json"
    with open(plan_file, "w", encoding="utf-8") as f:
        json.dump(commit_plan, f, indent=2, ensure_ascii=False)
    
    print(f"Git commit plan created: {plan_file}")
    
    # 创建提交脚本
    create_commit_script(commit_plan)
    
    return commit_plan

def create_commit_script(commit_plan):
    """创建提交脚本"""
    script_content = """@echo off
echo iStock Git提交脚本
echo ========================================
echo.

echo [1/4] 检查Git状态...
git status

echo.
echo [2/4] 添加文件到暂存区...
git add .

echo.
echo [3/4] 提交更改...
"""
    
    for i, commit in enumerate(commit_plan["commits"], 1):
        commit_type = commit["type"]
        commit_msg = commit["message"]
        script_content += f'echo Commit {i}: {commit_type}: {commit_msg}\n'
        script_content += f'git commit -m "{commit_type}: {commit_msg}"\n\n'
    
    script_content += f"""echo [4/4] 推送到远程仓库...
git push {commit_plan["remote"]} {commit_plan["branch"]}

echo.
echo ========================================
echo 提交完成！
echo ========================================
pause
"""
    
    script_file = Path(".") / "git_commit_script.bat"
    with open(script_file, "w", encoding="utf-8") as f:
        f.write(script_content)
    
    print(f"Git commit script created: {script_file}")

def main():
    """主函数"""
    print("=" * 70)
    print("继续iStock开发任务 - 代码整理和交付准备")
    print("=" * 70)
    
    # 整理代码准备交付
    delivery_dir = organize_code_for_delivery()
    
    # 创建交付摘要
    summary = create_delivery_summary(delivery_dir)
    
    # 创建Git提交计划
    commit_plan = create_git_commit_plan()
    
    print("\n" + "=" * 70)
    print("任务完成!")
    print("=" * 70)
    
    print(f"\n交付包位置: {delivery_dir}")
    print(f"包含文件: {count_files(delivery_dir)} 个文件")
    
    print(f"\n下一步:")
    print("1. 处理环境准备问题 (已通过valenbot私聊发送)")
    print("2. 安装依赖: pip install -r backend/requirements.txt")
    print("3. 运行提交脚本: git_commit_script.bat")
    print("4. 继续功能开发和测试")
    
    print(f"\nGit提交计划:")
    for i, commit in enumerate(commit_plan["commits"], 1):
        print(f"  {i}. {commit['type']}: {commit['message']}")
    
    print(f"\n测试状态: {summary['test_results']['real_test_pass_rate']}% 通过率")
    print(f"已知问题: {len(summary['test_results']['issues_found'])} 个")

if __name__ == "__main__":
    main()