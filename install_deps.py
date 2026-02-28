import subprocess
import sys

dependencies = [
    "tornado",
    "pymysql",
    "sqlalchemy",
    "pandas",
    "numpy"
]

print("Installing dependencies for mystock web service...")
for dep in dependencies:
    print(f"Installing {dep}...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", dep, "--target=D:\Program Files\Python\Lib\site-packages"], 
                      check=True, capture_output=True, text=True)
        print(f"  {dep} installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"  Failed to install {dep}: {e.stderr}")

print("\nVerifying installations...")
for dep in dependencies:
    try:
        __import__(dep.replace("-", "_"))
        print(f"  {dep}: OK")
    except ImportError:
        print(f"  {dep}: FAILED")

print("\nDependency installation completed.")