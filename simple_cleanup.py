#!/usr/bin/env python3
"""
iStock项目简单清理工具
"""

import os
import json
from datetime import datetime
from pathlib import Path

def analyze_project():
    """分析项目结构"""
    project_root = Path(".")
    
    print("=" * 70)
    print("iStock项目结构分析")
    print("=" * 70)
    
    # 统计文件
    all_files = list(project_root.rglob("*"))
    
    categories = {
        "python_files": [],
        "batch_files": [],
        "powershell_files": [],
        "document_files": [],
        "config_files": [],
        "temp_files": [],
        "backup_dirs": []
    }
    
    for file in all_files:
        if file.is_file():
            suffix = file.suffix.lower()
            name = file.name.lower()
            
            if suffix == ".py":
                categories["python_files"].append(file)
            elif suffix == ".bat":
                categories["batch_files"].append(file)
            elif suffix == ".ps1":
                categories["powershell_files"].append(file)
            elif suffix in [".md", ".txt", ".rst"]:
                categories["document_files"].append(file)
            elif suffix in [".yml", ".yaml", ".toml", ".json", ".env", ".gitignore"]:
                categories["config_files"].append(file)
            elif any(keyword in name for keyword in ["test", "scratch", "check", "verify", "fix", "simple", "quick"]):
                categories["temp_files"].append(file)
        
        elif file.is_dir():
            dir_name = file.name.lower()
            if any(keyword in dir_name for keyword in ["backup", "old", "temp", "tmp"]):
                categories["backup_dirs"].append(file)
    
    # 打印统计
    print("\n文件统计:")
    print("-" * 40)
    for category, files in categories.items():
        print(f"{category:20}: {len(files)} 个")
    
    return categories

def create_cleanup_plan(categories):
    """创建清理计划"""
    print("\n" + "=" * 70)
    print("清理计划")
    print("=" * 70)
    
    plan = {
        "keep": [],
        "archive": [],
        "delete": []
    }
    
    # 需要保留的核心文件
    core_files = [
        # 配置文件
        "docker-compose.yml", "docker-compose-fixed.yml", 
        "docker-compose-minimal.yml", "docker-compose.prod.yml",
        "Dockerfile.backend", "Dockerfile.frontend",
        "requirements.txt", "requirements-dev.txt", "pyproject.toml",
        ".gitignore", ".gitattributes", ".python-version", ".env.example",
        "Makefile", "LICENSE",
        
        # 项目文档
        "README.md", "DEVELOPMENT_PLAN.md", "WEEKLY_PLAN.md",
        "WEEK3_PLAN.md", "DATA_ACCURACY_PLAN.md",
        "GIT_BRANCH_MANAGEMENT.md", "GIT_COMMIT_ZH.md",
        
        # 重要脚本
        "automated_monitor.py", "push_watch_en.py", "test_alert_simple.py",
        
        # 报告文档
        "CODE_COMPLETENESS_CHECKLIST.md", "COMPLETE_DELIVERY_CHECKLIST.md",
        "PUSH_MECHANISM_ANALYSIS.md", "AUTOMATED_MONITOR_SETUP.md",
        
        # 项目结构文件
        "PROJECT_STRUCTURE.md", "PROGRESS_REPORT.md"
    ]
    
    # 需要归档的测试文件
    test_files_patterns = ["test_", "check_", "verify_", "scratch_"]
    
    # 可以删除的临时文件
    temp_files_patterns = ["fix_", "simple_", "quick_", "emergency_", "start_"]
    
    all_files = []
    for file_list in categories.values():
        all_files.extend(file_list)
    
    for file in all_files:
        if file.is_file():
            file_name = file.name
            
            # 检查是否核心文件
            if file_name in core_files:
                plan["keep"].append(str(file))
                print(f"[KEEP] 核心文件: {file}")
            
            # 检查是否测试文件
            elif any(pattern in file_name.lower() for pattern in test_files_patterns):
                plan["archive"].append(str(file))
                print(f"[ARCHIVE] 测试文件: {file}")
            
            # 检查是否临时文件
            elif any(pattern in file_name.lower() for pattern in temp_files_patterns):
                plan["delete"].append(str(file))
                print(f"[DELETE] 临时文件: {file}")
            
            else:
                # 默认保留
                plan["keep"].append(str(file))
    
    return plan

def organize_documentation():
    """整理文档"""
    print("\n" + "=" * 70)
    print("整理文档")
    print("=" * 70)
    
    docs_dir = Path("docs")
    if not docs_dir.exists():
        docs_dir.mkdir()
        print("创建 docs/ 目录")
    
    # 创建子目录
    subdirs = ["project", "guides", "reports", "api", "development"]
    for subdir in subdirs:
        subdir_path = docs_dir / subdir
        if not subdir_path.exists():
            subdir_path.mkdir()
            print(f"创建 docs/{subdir}/ 目录")
    
    # 移动文档文件
    doc_files = list(Path(".").glob("*.md")) + list(Path(".").glob("*.txt"))
    
    moved_count = 0
    for doc in doc_files:
        if doc.name == "README.md":
            continue  # 保留根目录的README
        
        target_dir = None
        
        # 根据内容分类
        doc_name = doc.name.lower()
        
        if any(keyword in doc_name for keyword in ["plan", "structure", "progress"]):
            target_dir = docs_dir / "project"
        elif any(keyword in doc_name for keyword in ["guide", "manual", "setup", "install"]):
            target_dir = docs_dir / "guides"
        elif any(keyword in doc_name for keyword in ["report", "analysis", "checklist", "audit"]):
            target_dir = docs_dir / "reports"
        elif any(keyword in doc_name for keyword in ["git", "commit", "branch"]):
            target_dir = docs_dir / "development"
        else:
            target_dir = docs_dir / "project"
        
        try:
            target_path = target_dir / doc.name
            doc.rename(target_path)
            print(f"移动: {doc.name} -> docs/{target_dir.name}/")
            moved_count += 1
        except Exception as e:
            print(f"移动失败 {doc.name}: {e}")
    
    print(f"\n共移动 {moved_count} 个文档文件")

def create_knowledge_base():
    """创建知识库"""
    print("\n" + "=" * 70)
    print("创建知识库")
    print("=" * 70)
    
    knowledge_dir = Path("knowledge")
    if not knowledge_dir.exists():
        knowledge_dir.mkdir()
        print("创建 knowledge/ 目录")
    
    # 创建知识库文件
    knowledge_files = {
        "project_overview.md": """# iStock 项目概述

## 项目简介
iStock是一个智能股票分析系统，提供实时盯盘、技术分析、投资组合管理和自动化交易建议。

## 核心功能
1. 实时市场监控
2. 技术指标分析
3. 投资组合管理
4. 自动化交易建议
5. 风险控制

## 技术栈
- 后端: Python + FastAPI + PostgreSQL
- 前端: React + TypeScript
- 部署: Docker + Nginx
- 监控: 自定义监控系统

## 开发状态
- 当前版本: v0.1.0
- 完成度: ~85%
- 最后更新: 2026-02-28
""",
        
        "development_workflow.md": """# 开发工作流

## 代码规范
1. 使用中文提交消息
2. 遵循PEP 8代码风格
3. 编写单元测试
4. 及时更新文档

## Git流程
1. `main`分支: 生产环境
2. `develop`分支: 开发环境
3. `feature/*`分支: 功能开发

## 提交规范
```
feat: 添加新功能
fix: 修复bug
docs: 更新文档
style: 代码格式调整
refactor: 代码重构
test: 添加测试
chore: 构建过程或辅助工具变动
```

## 自动化
- CI/CD: GitHub Actions
- 代码检查: pre-commit hooks
- 文档生成: 自动生成API文档
""",
        
        "api_documentation.md": """# API 文档

## 基础信息
- 基础URL: `http://localhost:8000`
- API版本: `v1`
- 文档地址: `http://localhost:8000/docs`

## 认证
所有API需要JWT token认证:
```
Authorization: Bearer <token>
```

## 主要端点

### 健康检查
```
GET /health
```

### 股票数据
```
GET /api/v1/stocks
GET /api/v1/stocks/{symbol}
POST /api/v1/stocks/analyze
```

### 用户管理
```
POST /api/v1/auth/login
POST /api/v1/auth/register
GET /api/v1/users/me
```

### 投资组合
```
GET /api/v1/portfolio
POST /api/v1/portfolio/add
PUT /api/v1/portfolio/update
```

## 数据格式
所有请求和响应使用JSON格式。
""",
        
        "deployment_guide.md": """# 部署指南

## 开发环境
```bash
# 1. 克隆项目
git clone https://github.com/MaNongkuxingseng/iStock.git

# 2. 安装依赖
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 3. 配置环境变量
cp .env.example .env
# 编辑 .env 文件

# 4. 启动服务
docker-compose up -d

# 5. 访问应用
# 后端API: http://localhost:8000
# 前端应用: http://localhost:3000
```

## 生产环境
```bash
# 使用生产配置
docker-compose -f docker-compose.prod.yml up -d

# 或使用Docker Swarm/Kubernetes
```

## 监控和维护
1. 查看日志: `docker-compose logs`
2. 健康检查: `http://localhost:8000/health`
3. 性能监控: 使用Grafana + Prometheus
4. 备份策略: 定期备份数据库
"""
    }
    
    created_count = 0
    for filename, content in knowledge_files.items():
        file_path = knowledge_dir / filename
        if not file_path.exists():
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"创建: knowledge/{filename}")
            created_count += 1
    
    print(f"\n共创建 {created_count} 个知识库文件")

def update_readme():
    """更新README.md"""
    print("\n" + "=" * 70)
    print("更新README.md")
    print("=" * 70)
    
    readme_content = """# iStock - 智能股票分析系统

![版本](https://img.shields.io/badge/版本-v0.1.0-blue)
![状态](https://img.shields.io/badge/状态-开发中-orange)
![许可证](https://img.shields.io/badge/许可证-MIT-green)

## 📖 项目简介

iStock是一个基于人工智能的智能股票分析系统，提供实时盯盘、技术分析、投资组合管理和自动化交易建议。

## ✨ 核心功能

- 📈 **实时市场监控**: 9个时间点的盯盘消息推送
- 🤖 **智能分析**: 基于机器学习的技术分析
- 💼 **投资组合管理**: 个人持仓管理和分析
- 🔔 **风险预警**: 实时风险检测和警报
- 📊 **数据可视化**: 交互式图表和报表
- 🔄 **自动化交易**: 基于策略的自动化建议

## 🏗️ 技术架构

### 后端技术栈
- **框架**: Python + FastAPI
- **数据库**: PostgreSQL + Redis
- **ORM**: SQLAlchemy + Alembic
- **认证**: JWT + OAuth2
- **任务队列**: Celery + RabbitMQ

### 前端技术栈
- **框架**: React + TypeScript
- **状态管理**: Redux Toolkit
- **UI组件**: Ant Design
- **图表**: Recharts / ECharts
- **路由**: React Router

### 基础设施
- **容器化**: Docker + Docker Compose
- **Web服务器**: Nginx
- **CI/CD**: GitHub Actions
- **监控**: 自定义监控系统 + Grafana

## 🚀 快速开始

### 开发环境
```bash
# 1. 克隆项目
git clone https://github.com/MaNongkuxingseng/iStock.git
cd iStock

# 2. 安装依赖
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 3. 配置环境
cp .env.example .env
# 编辑 .env 文件设置您的配置

# 4. 启动服务
docker-compose up -d

# 5. 访问应用
# 后端API: http://localhost:8000
# API文档: http://localhost:8000/docs
# 前端应用: http://localhost:3000
```

### 生产部署
```bash
# 使用生产配置
docker-compose -f docker-compose.prod.yml up -d
```

## 📁 项目结构

```
iStock/
├── backend/          # 后端服务
├── frontend/         # 前端应用
├── docker/           # Docker配置
├── docs/             # 项目文档
├── knowledge/        # 知识库
├── scripts/          # 管理脚本
├── data/             # 数据文件
└── local/            # 本地开发
```

详细结构请查看 [PROJECT_STRUCTURE.md](docs/project/PROJECT_STRUCTURE.md)

## 📚 文档

- [开发计划](docs/project/DEVELOPMENT_PLAN.md) - 14周开发计划
- [API文档](docs/api/API_DOCUMENTATION.md) - 完整的API参考
- [部署指南](docs/guides/DEPLOYMENT_GUIDE.md) - 部署和运维指南
- [开发规范](docs/development/DEVELOPMENT_WORKFLOW.md) - 代码规范和流程

## 🔧 开发

### 代码规范
- 使用中文提交消息
- 遵循PEP 8和ESLint规范
- 编写单元测试
- 及时更新文档

### Git流程
- `main`: 生产环境
- `develop`: 开发环境  
- `feature/*`: 功能开发分支

### 提交规范
```
feat: 添加新功能
fix: 修复bug
docs: 更新文档
style: 代码格式调整
refactor: 代码重构
test: 添加测试
chore: 构建过程或辅助工具变动
```

## 🤝 贡献

欢迎贡献！请查看 [CONTRIBUTING.md](docs/development/CONTRIBUTING.md) 了解如何参与开发。

## 📄 许可证

本项目基于 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 支持

- 问题反馈: [GitHub Issues](https://github.com/MaNongkuxingseng/iStock/issues)
- 功能建议: 通过Issue提交
- 紧急问题: 联系项目维护者

## 🚧 开发状态

### 当前进度 (~85%)
- ✅ 项目基础架构
- ✅ 数据库设计
- ✅ 后端API服务
- ✅ 前端React应用
- ✅ 自动化监控系统
- 🔄 数据源集成
- 🔄 机器学习模型
- 🔄 生产环境优化

### 近期计划
1. 完成数据源API集成
2. 实现机器学习预测模型
3. 优化前端用户体验
4. 完善生产环境部署

---

**最后更新**: 2026-02-28
**版本**: v0.1.0
"""
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print("README.md 已更新")

def main():
    """主函数"""
    print("开始iStock项目整理工作...")
    print()
    
    # 分析项目
    categories = analyze_project()
    
    # 创建清理计划
    plan = create_cleanup_plan(categories)
    
    # 整理文档
    organize_documentation()
    
    # 创建知识库
    create_knowledge_base()
    
    # 更新README
    update_readme()
    
    # 保存清理计划
    with open("cleanup_plan.json", "w", encoding="utf-8") as f:
        json.dump(plan, f, indent=2, ensure_ascii=False)
    
    print("\n" + "=" * 70)
    print("整理完成!")
    print("=" * 70)
    
    print("\n下一步:")
    print("1. 查看 cleanup_plan.json 了解清理建议")
    print("2. 检查 docs/ 目录中的文档整理")
    print("3. 检查 knowledge/ 目录中的知识库")
    print("4. 查看更新的 README.md")
    print("5. 提交Git更改")
    
    return plan

if __name__ == "__main__":
    main()