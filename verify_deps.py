import sys

deps = [
    "tornado",
    "pymysql",
    "sqlalchemy",
    "talib",
    "requests",
    "numpy",
    "pandas"
]

print("Verifying dependencies...")
all_ok = True
for dep in deps:
    try:
        __import__(dep.replace("-", "_"))
        print(f"  {dep}: ✓ OK")
    except ImportError as e:
        print(f"  {dep}: ✗ FAILED - {e}")
        all_ok = False

if all_ok:
    print("\nAll dependencies are installed successfully!")
    print("Now you can start the web service with:")
    print('  python "G:\\openclaw\\workspace\\projects\\active\\myStock\\instock\\web\\web_service.py"')
else:
    print("\nSome dependencies are missing.")
    print("Please install missing dependencies with:")
    print('  pip install <missing_package> --target="D:\\Program Files\\Python\\Lib\\site-packages"')