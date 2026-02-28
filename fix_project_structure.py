#!/usr/bin/env python3
"""
修复iStock项目结构
根据真实测试结果重新组织文件
"""

import os
import shutil
from pathlib import Path

def analyze_current_structure():
    """分析当前项目结构"""
    print("Analyzing current project structure...")
    
    project_root = Path(".")
    
    # 检查backend目录
    backend_dir = project_root / "backend"
    if backend_dir.exists():
        print(f"\nbackend目录内容:")
        for item in backend_dir.rglob("*"):
            if item.is_file():
                print(f"  {item.relative_to(backend_dir)}")
    else:
        print("\nbackend目录不存在")
    
    # 检查frontend目录
    frontend_dir = project_root / "frontend"
    if frontend_dir.exists():
        print(f"\nfrontend目录内容:")
        for item in frontend_dir.rglob("*"):
            if item.is_file():
                print(f"  {item.relative_to(frontend_dir)}")
    else:
        print("\nfrontend目录不存在")
    
    # 检查根目录
    print(f"\n根目录关键文件:")
    for pattern in ["*.py", "*.md", "*.json", "*.bat", "*.ps1"]:
        for file in project_root.glob(pattern):
            print(f"  {file.name}")

def fix_backend_structure():
    """修复后端结构"""
    print("\nFixing backend structure...")
    
    backend_dir = Path("backend")
    backend_src_dir = backend_dir / "src"
    
    # 创建标准后端结构
    backend_src_dir.mkdir(parents=True, exist_ok=True)
    
    # 创建必要的子目录
    subdirs = ["api", "database", "models", "services", "utils"]
    for subdir in subdirs:
        (backend_src_dir / subdir).mkdir(exist_ok=True)
    
    # 检查是否有main.py文件
    main_py_files = list(Path(".").glob("**/main.py"))
    if main_py_files:
        # 移动第一个找到的main.py到正确位置
        source = main_py_files[0]
        target = backend_src_dir / "main.py"
        if not target.exists():
            shutil.move(str(source), str(target))
            print(f"  Moved main.py to {target}")
    
    # 创建默认的main.py如果不存在
    if not (backend_src_dir / "main.py").exists():
        create_default_main_py(backend_src_dir / "main.py")
    
    # 移动数据库相关文件
    move_database_files(backend_src_dir)
    
    print("  Backend structure fixed")

def create_default_main_py(filepath):
    """创建默认的main.py"""
    content = '''#!/usr/bin/env python3
"""
iStock Backend Main Application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Create FastAPI app
app = FastAPI(
    title="iStock API",
    description="Intelligent Stock Analysis System",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "iStock API is running"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "iStock API"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"  Created default main.py at {filepath}")

def move_database_files(backend_src_dir):
    """移动数据库文件"""
    # 查找数据库相关文件
    db_patterns = ["*database*.py", "*model*.py", "*session*.py"]
    
    for pattern in db_patterns:
        for file in Path(".").glob(f"**/{pattern}"):
            if file.is_file() and "frontend" not in str(file):
                # 移动到backend/src/database/
                target_dir = backend_src_dir / "database"
                target_dir.mkdir(exist_ok=True)
                target = target_dir / file.name
                
                if not target.exists():
                    shutil.move(str(file), str(target))
                    print(f"  Moved database file: {file.name}")

def fix_frontend_structure():
    """修复前端结构"""
    print("\nFixing frontend structure...")
    
    frontend_dir = Path("frontend")
    
    # 清理frontend目录，只保留前端文件
    frontend_files_to_keep = [
        "package.json", "README.md", "index.html",
        "App.css", "App.js", "index.css", "index.js",
        "Header.js", "StockTable.js", "AuthContext.js"
    ]
    
    # 创建src目录
    src_dir = frontend_dir / "src"
    src_dir.mkdir(exist_ok=True)
    
    # 创建子目录
    subdirs = ["components", "pages", "services", "contexts", "styles"]
    for subdir in subdirs:
        (src_dir / subdir).mkdir(exist_ok=True)
    
    # 移动前端文件到src目录
    for file in frontend_dir.glob("*"):
        if file.is_file() and file.name in frontend_files_to_keep:
            # 根据文件类型移动到不同目录
            if file.name.endswith(".js"):
                if "App.js" in file.name:
                    target = src_dir / "App.js"
                elif "index.js" in file.name:
                    target = src_dir / "index.js"
                elif "Header.js" in file.name or "StockTable.js" in file.name:
                    target = src_dir / "components" / file.name
                elif "AuthContext.js" in file.name:
                    target = src_dir / "contexts" / file.name
                else:
                    target = src_dir / file.name
            elif file.name.endswith(".css"):
                target = src_dir / "styles" / file.name
            else:
                target = src_dir / file.name
            
            # 确保目标目录存在
            target.parent.mkdir(parents=True, exist_ok=True)
            
            if not target.exists():
                shutil.move(str(file), str(target))
                print(f"  Moved frontend file: {file.name} -> {target.relative_to(frontend_dir)}")
    
    # 移动后端文件出frontend目录
    backend_files_in_frontend = [
        "alembic.ini", "pyproject.toml", "requirements-dev.txt",
        "__init__.py", "env.py", "script.py.mako", 
        "001_initial_tables.py", "data_sources.py", "db_migrate.py"
    ]
    
    for file in frontend_dir.glob("*"):
        if file.is_file() and file.name in backend_files_in_frontend:
            # 移动到项目根目录
            target = Path(".") / file.name
            if not target.exists():
                shutil.move(str(file), str(target))
                print(f"  Moved backend file out of frontend: {file.name}")
    
    print("  Frontend structure fixed")

def create_missing_files():
    """创建缺失的重要文件"""
    print("\nCreating missing important files...")
    
    # 1. 创建backend/requirements.txt如果不存在
    backend_req = Path("backend") / "requirements.txt"
    if not backend_req.exists():
        content = '''fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
alembic==1.12.1
psycopg2-binary==2.9.9
pydantic==2.5.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
'''
        with open(backend_req, "w", encoding="utf-8") as f:
            f.write(content)
        print("  Created backend/requirements.txt")
    
    # 2. 创建frontend/package.json如果不存在或内容不对
    frontend_package = Path("frontend") / "package.json"
    if not frontend_package.exists() or frontend_package.stat().st_size < 100:
        content = '''{
  "name": "istock-frontend",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-scripts": "5.0.1"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "eslintConfig": {
    "extends": [
      "react-app"
    ]
  },
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  }
}
'''
        with open(frontend_package, "w", encoding="utf-8") as f:
            f.write(content)
        print("  Created/updated frontend/package.json")
    
    # 3. 确保监控脚本在正确位置
    monitor_scripts = ["automated_monitor.py", "push_watch_en.py", "test_alert_simple.py"]
    for script in monitor_scripts:
        script_path = Path(script)
        if not script_path.exists():
            # 从其他地方查找
            found = list(Path(".").glob(f"**/{script}"))
            if found:
                # 复制到根目录
                shutil.copy(str(found[0]), script)
                print(f"  Copied {script} to root directory")
    
    print("  Missing files created")

def update_test_config():
    """更新测试配置"""
    print("\nUpdating test configuration...")
    
    # 更新run_real_tests_en.py中的路径
    test_file = Path("run_real_tests_en.py")
    if test_file.exists():
        with open(test_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 更新后端主文件路径
        content = content.replace('main_file = "backend/src/main.py"', 
                                 'main_file = "backend/src/main.py"')
        
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(content)
        
        print("  Updated test configuration")

def main():
    """主函数"""
    print("=" * 70)
    print("iStock Project Structure Fix")
    print("=" * 70)
    
    # 分析当前结构
    analyze_current_structure()
    
    # 修复结构
    fix_backend_structure()
    fix_frontend_structure()
    create_missing_files()
    update_test_config()
    
    print("\n" + "=" * 70)
    print("Project structure fixed!")
    print("=" * 70)
    
    print("\nNext steps:")
    print("1. Run real tests again: python run_real_tests_en.py")
    print("2. Install backend dependencies: pip install -r backend/requirements.txt")
    print("3. Install frontend dependencies: cd frontend && npm install")
    print("4. Start services and test functionality")

if __name__ == "__main__":
    main()