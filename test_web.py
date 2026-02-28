import subprocess
import time
import sys
import os

# 切换到web目录
web_dir = r"G:\openclaw\workspace\projects\active\myStock\instock\web"
os.chdir(web_dir)

# 启动web服务
print("Starting web service...")
process = subprocess.Popen([sys.executable, "web_service.py"], 
                          stdout=subprocess.PIPE, 
                          stderr=subprocess.PIPE,
                          text=True)

# 等待服务启动
print("Waiting for service to start...")
time.sleep(5)

# 检查端口
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
result = sock.connect_ex(('127.0.0.1', 9988))
if result == 0:
    print("Web service started successfully on port 9988")
    
    # 测试健康检查
    import urllib.request
    try:
        response = urllib.request.urlopen("http://127.0.0.1:9988/health", timeout=2)
        print(f"Health check: {response.read().decode()}")
    except Exception as e:
        print(f"Health check failed: {e}")
else:
    print("Web service failed to start on port 9988")
    
# 输出进程输出
print("\nProcess output:")
try:
    stdout, stderr = process.communicate(timeout=1)
    if stdout:
        print(f"STDOUT: {stdout}")
    if stderr:
        print(f"STDERR: {stderr}")
except subprocess.TimeoutExpired:
    process.terminate()
    print("Process is still running")