#!/usr/bin/env python3
"""
iStock项目清理和整理脚本
清理临时文件、测试文件，整理项目结构
"""

import os
import shutil
import json
from datetime import datetime
from pathlib import Path

class ProjectCleaner:
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.cleanup_log = []
        self.backup_dir = self.project_root / "backup_cleanup"
        
    def log_action(self, action, path, status="INFO"):
        """记录清理操作"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "path": str(path),
            "status": status
        }
        self.cleanup_log.append(entry)
        print(f"[{status}] {action}: {path}")
    
    def create_backup(self):
        """创建备份目录"""
        if not self.backup_dir.exists():
            self.backup_dir.mkdir(parents=True)
            self.log_action("创建备份目录", self.backup_dir)
    
    def backup_file(self, file_path):
        """备份文件"""
        try:
            if file_path.exists():
                backup_path = self.backup_dir / file_path.relative_to(self.project_root)
                backup_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(file_path, backup_path)
                self.log_action("备份文件", file_path)
                return True
        except Exception as e:
            self.log_action(f"备份失败: {e}", file_path, "ERROR")
        return False
    
    def identify_temp_files(self):
        """识别临时文件"""
        temp_patterns = [
            "test_*.py", "test_*.bat", "test_*.ps1",
            "scratch_*.py", "scratch_*.sql",
            "check_*.py", "check_*.bat",
            "verify_*.py", "verify_*.bat",
            "fix_*.py", "fix_*.bat", "fix_*.ps1",
            "simple_*.py", "simple_*.bat",
            "quick_*.ps1", "quick_*.bat",
            "emergency_*.bat",
            "start_*.bat", "start_*.ps1",
            "run_*.py", "run_*.bat",
            "*.tmp", "*.temp", "*.bak", "*.backup",
            "temp_*", "tmp_*",
        ]
        
        temp_files = []
        for pattern in temp_patterns:
            temp_files.extend(self.project_root.rglob(pattern))
        
        # 添加特定文件
        specific_files = [
            "backfill_data.py", "backfill_data.sql", "batch_backfill.py",
            "check_database.py", "check_db.py", "check_pymysql.py",
            "check_table.bat", "check_table.py", "check_table2.bat",
            "create_minimal_frontend.bat", "direct_mysql_backfill.py",
            "emergency_fix.bat", "execute_backfill.py", "fix_all_issues.bat",
            "fix_all_issues.ps1", "fix_all_issues_fixed.bat", "fix_mysql_table.bat",
            "fix_table.py", "install_deps.py", "install_deps_simple.bat",
            "install_mystock_deps.py", "intelligent_model_router.py",
            "model_guard_bot.py", "model_management_system.py",
            "push_market_watch.py", "push_watch_en.py", "run_backfill.bat",
            "run_monitor_test.py", "scratch_check_tables.py",
            "scratch_query_xuelong.py", "scratch_xuelong_key.py",
            "setup_docker_mirror.bat", "setup_model_system.bat",
            "simple_backfill.bat", "simple_fix.bat", "simple_fix.sql",
            "simple_web_server.py", "start-dev.bat", "start_backfill.bat",
            "start_clean.bat", "start_easy.bat", "start_istock.bat",
            "start_istock_fixed.bat", "start_minimal.bat", "start_now.bat",
            "start_simple.ps1", "start_web.bat", "start_web_service.bat",
            "test_alert_simple.py", "test_backfill.py", "test_basic.bat",
            "test_db_connection.py", "test_direct_chat.py", "test_local.py",
            "test_quick.ps1", "test_simple.bat", "test_web.py",
            "verify_core.bat", "verify_deps.py", "verify_setup.ps1",
            "weather_fetcher.rs", "automated_monitor.py"
        ]
        
        for file in specific_files:
            file_path = self.project_root / file
            if file_path.exists():
                temp_files.append(file_path)
        
        # 去重
        temp_files = list(set(temp_files))
        
        # 分类
        categorized = {
            "test_scripts": [],
            "temporary_scripts": [],
            "backup_files": [],
            "duplicate_files": [],
            "old_versions": []
        }
        
        for file in temp_files:
            file_str = str(file)
            if "test" in file_str.lower():
                categorized["test_scripts"].append(file)
            elif "scratch" in file_str.lower() or "check" in file_str.lower():
                categorized["temporary_scripts"].append(file)
            elif "backup" in file_str.lower() or "old" in file_str.lower():
                categorized["backup_files"].append(file)
            elif "fixed" in file_str.lower() or "minimal" in file_str.lower():
                categorized["duplicate_files"].append(file)
            else:
                categorized["old_versions"].append(file)
        
        return categorized
    
    def identify_duplicate_dirs(self):
        """识别重复目录"""
        duplicate_dirs = []
        
        # 检查重复的目录
        dirs_to_check = [
            "myStock",  # 可能是旧版本
            "myStock-AI",  # 可能是重复
            "myStock._migrated_backup_20260226",  # 备份目录
        ]
        
        for dir_name in dirs_to_check:
            dir_path = self.project_root / dir_name
            if dir_path.exists() and dir_path.is_dir():
                duplicate_dirs.append(dir_path)
        
        return duplicate_dirs
    
    def identify_documentation_files(self):
        """识别文档文件"""
        doc_patterns = ["*.md", "*.txt", "*.rst"]
        doc_files = []
        
        for pattern in doc_patterns:
            doc_files.extend(self.project_root.rglob(pattern))
        
        # 分类文档
        categorized = {
            "project_docs": [],  # 项目文档
            "temporary_docs": [],  # 临时文档
            "guides": [],  # 指南
            "reports": []  # 报告
        }
        
        for file in doc_files:
            file_str = str(file)
            if any(name in file_str for name in ["README", "CONTRIBUTING", "LICENSE", "DEVELOPMENT", "WEEKLY"]):
                categorized["project_docs"].append(file)
            elif any(name in file_str for name in ["GUIDE", "MANUAL", "SETUP", "INSTALL"]):
                categorized["guides"].append(file)
            elif any(name in file_str for name in ["REPORT", "ANALYSIS", "CHECKLIST", "AUDIT"]):
                categorized["reports"].append(file)
            else:
                categorized["temporary_docs"].append(file)
        
        return categorized
    
    def clean_temp_files(self, categorized_files, dry_run=True):
        """清理临时文件"""
        cleaned = []
        kept = []
        
        # 需要保留的重要文件
        important_files = [
            "automated_monitor.py",  # 自动化监控
            "push_watch_en.py",  # 盯盘推送
            "test_alert_simple.py",  # 测试警报
        ]
        
        for category, files in categorized_files.items():
            for file in files:
                file_name = file.name
                
                # 检查是否重要文件
                is_important = any(important in str(file) for important in important_files)
                
                if is_important:
                    self.log_action(f"保留重要文件", file, "KEEP")
                    kept.append(file)
                    continue
                
                # 检查是否在项目结构中需要
                if self.is_in_project_structure(file):
                    self.log_action(f"保留项目结构文件", file, "KEEP")
                    kept.append(file)
                    continue
                
                if dry_run:
                    self.log_action(f"将清理 ({category})", file, "DRY_RUN")
                    cleaned.append(file)
                else:
                    # 先备份
                    if self.backup_file(file):
                        try:
                            if file.is_file():
                                file.unlink()
                                self.log_action(f"已清理 ({category})", file, "CLEANED")
                                cleaned.append(file)
                            elif file.is_dir():
                                shutil.rmtree(file)
                                self.log_action(f"已清理目录 ({category})", file, "CLEANED")
                                cleaned.append(file)
                        except Exception as e:
                            self.log_action(f"清理失败: {e}", file, "ERROR")
        
        return cleaned, kept
    
    def is_in_project_structure(self, file_path):
        """检查文件是否在项目结构中需要"""
        # 项目核心目录
        core_dirs = ["backend", "frontend", "docker", "scripts", ".github", "data", "local"]
        
        # 项目核心文件
        core_files = [
            "docker-compose.yml", "docker-compose-fixed.yml", "docker-compose-minimal.yml",
            "docker-compose.prod.yml", "Dockerfile.backend", "Dockerfile.frontend",
            "requirements.txt", "requirements-dev.txt", "pyproject.toml",
            ".gitignore", ".gitattributes", ".python-version", ".env.example",
            "Makefile", "LICENSE", "README.md"
        ]
        
        file_str = str(file_path)
        
        # 检查是否在核心目录中
        for core_dir in core_dirs:
            if f"/{core_dir}/" in file_str.replace("\\", "/"):
                return True
        
        # 检查是否核心文件
        if file_path.name in core_files:
            return True
        
        # 检查是否在项目根目录的重要文件
        if file_path.parent == self.project_root:
            # 项目文档
            if file_path.suffix in [".md", ".txt"]:
                return True
        
        return False
    
    def organize_documentation(self, categorized_docs):
        """整理文档"""
        docs_dir = self.project_root / "docs"
        if not docs_dir.exists():
            docs_dir.mkdir()
            self.log_action("创建docs目录", docs_dir)
        
        # 创建子目录
        subdirs = {
            "project": docs_dir / "project",
            "guides": docs_dir / "guides",
            "reports": docs_dir / "reports",
            "api": docs_dir / "api",
            "development": docs_dir / "development"
        }
        
        for name, path in subdirs.items():
            if not path.exists():
                path.mkdir()
                self.log_action(f"创建docs/{name}目录", path)
        
        # 移动文档文件
        moved = []
        
        for category, files in categorized_docs.items():
            for file in files:
                if file.parent == docs_dir:
                    continue  # 已经在docs目录中
                
                target_dir = None
                if category == "project_docs":
                    target_dir = subdirs["project"]
                elif category == "guides":
                    target_dir = subdirs["guides"]
                elif category == "reports":
                    target_dir = subdirs["reports"]
                else:
                    target_dir = docs_dir  # 临时文档放在docs根目录
                
                try:
                    target_path = target_dir / file.name
                    
                    # 处理重名文件
                    counter = 1
                    while target_path.exists():
                        stem = file.stem
                        suffix = file.suffix
                        target_path = target_dir / f"{stem}_{counter}{suffix}"
                        counter += 1
                    
                    shutil.move(str(file), str(target_path))
                    self.log_action(f"移动文档到 {target_dir.name}", file)
                    moved.append((file, target_path))
                    
                except Exception as e:
                    self.log_action(f"移动文档失败: {e}", file, "ERROR")
        
        return moved
    
    def create_project_structure_doc(self):
        """创建项目结构文档"""
        structure_file = self.project_root / "PROJECT_STRUCTURE.md"
        
        structure_content = """# 📁 iStock 项目结构

## 🏗️ 项目架构

```
iStock/
├── 📁 backend/                    # 后端服务
│   ├── 📁 src/                   # 源代码
│   │   ├── 📁 api/              # API接口
│   │   ├── 📁 database/         # 数据库相关
│   │   ├── 📁 models/           # 数据模型
│   │   ├── 📁 services/         # 业务服务
│   │   └── 📁 utils/            # 工具函数
│   ├── 📁 scripts/              # 管理脚本
│   └── requirements.txt         # Python依赖
│
├── 📁 frontend/                  # 前端应用
│   ├── 📁 public/               # 静态资源
│   ├── 📁 src/                  # 源代码
│   │   ├── 📁 components/       # 组件
│   │   ├── 📁 pages/            # 页面
│   │   ├── 📁 services/         # API服务
│   │   └── 📁 contexts/         # 上下文
│   └── package.json             # Node.js依赖
│
├── 📁 docker/                    # Docker配置
│   ├── 📁 nginx/                # Nginx配置
│   ├── 📁 postgres/             # PostgreSQL初始化
│   └── nginx.conf               # Nginx主配置
│
├── 📁 scripts/                   # 项目脚本
│   ├── git_commit_notify.py     # Git提交通知
│   └── project_management.py    # 项目管理
│
├── 📁 docs/                      # 项目文档
│   ├── 📁 project/              # 项目文档
│   ├── 📁 guides/               # 使用指南
│   ├── 📁 reports/              # 分析报告
│   ├── 📁 api/                  # API文档
│   └── 📁 development/          # 开发文档
│
├── 📁 data/                      # 数据文件
│   ├── 📁 raw/                  # 原始数据
│   ├── 📁 processed/            # 处理后的数据
│   └── 📁 models/               # 机器学习模型
│
├── 📁 local/                     # 本地开发环境
│   ├── app.py                   # 本地应用
│   └── start_local.py           # 本地启动脚本
│
├── 📁 .github/                   # GitHub配置
│   └── 📁 workflows/            # CI/CD工作流
│
├── docker-compose.yml           # Docker开发环境
├── docker-compose.prod.yml      # Docker生产环境
├── requirements.txt             # Python主依赖
├── requirements-dev.txt         # Python开发依赖
├── pyproject.toml               # 项目配置
├── Makefile                     # 构建命令
├── .env.example                 # 环境变量示例
├── .gitignore                   # Git忽略文件
├── LICENSE                      # 许可证
└── README.md                    # 项目说明
```

## 🔧 核心文件说明

### 后端服务 (`backend/`)
- `src/api/` - FastAPI路由和端点
- `src/database/` - 数据库连接和会话管理
- `src/models/` - SQLAlchemy数据模型
- `src/services/` - 业务逻辑服务层
- `src/utils/` - 工具函数和辅助类

### 前端应用 (`frontend/`)
- `src/components/` - React组件
- `src/pages/` - 页面组件
- `src/services/` - API调用服务
- `src/contexts/` - React上下文

### Docker配置 (`docker/`)
- `nginx/` - Web服务器配置
- `postgres/` - 数据库初始化脚本
- 多环境Docker Compose配置

### 文档 (`docs/`)
- `project/` - 项目规划和设计文档
- `guides/` - 用户指南和操作手册
- `reports/` - 分析报告和审计文档
- `api/` - API接口文档
- `development/` - 开发文档和规范

## 🚀 开发工作流

### 1. 环境设置
```bash
# 复制环境变量
cp .env.example .env

# 安装依赖
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 启动开发环境
docker-compose up -d
```

### 2. 代码开发
```bash
# 后端开发
cd backend
python -m uvicorn src.main:app --reload

# 前端开发
cd frontend
npm start
```

### 3. 测试验证
```bash
# 运行测试
pytest

# 代码检查
black .
flake8 .
mypy .
```

### 4. 提交代码
```bash
# 使用中文提交消息
git commit -m "feat: 添加新功能"

# 推送到远程
git push origin develop
```

## 📊 项目状态

### 当前版本: v0.1.0
### 完成度: ~85%
### 最后更新: {update_date}

## 🔗 相关链接

- [GitHub仓库](https://github.com/MaNongkuxingseng/iStock)
- [开发计划](docs