# 🔧 修复Docker PATH问题指南

## 🚨 问题描述
Docker Desktop已安装并运行，但命令行中`docker`命令不可用，显示：
```
'docker' 不是内部或外部命令，也不是可运行的程序或批处理文件。
```

## 🎯 原因分析
Docker Desktop的可执行文件未添加到系统的PATH环境变量中。

## 🔧 解决方案

### 方案1: 重启Docker Desktop（最简单）
1. 右键点击系统托盘中的Docker图标
2. 选择 "Restart"
3. 等待Docker重新启动
4. 重新打开命令提示符或PowerShell
5. 测试: `docker --version`

### 方案2: 手动添加Docker到PATH

#### Windows 10/11步骤:
1. 右键点击"此电脑" → "属性"
2. 点击"高级系统设置"
3. 点击"环境变量"
4. 在"系统变量"部分，找到并选择"Path"
5. 点击"编辑"
6. 点击"新建"，添加以下路径:
   ```
   C:\Program Files\Docker\Docker\resources\bin
   ```
7. 点击"确定"保存所有更改
8. 重新打开命令提示符
9. 测试: `docker --version`

### 方案3: 使用完整路径
在批处理文件中使用Docker的完整路径:
```batch
REM 使用完整路径调用docker
"C:\Program Files\Docker\Docker\resources\bin\docker.exe" --version
"C:\Program Files\Docker\Docker\resources\bin\docker-compose.exe" --version
```

### 方案4: 创建快捷脚本
创建`docker_env.bat`:
```batch
@echo off
set PATH=C:\Program Files\Docker\Docker\resources\bin;%PATH%
cmd
```

## 🛠️ 验证步骤

### 步骤1: 检查Docker安装位置
```batch
where docker
where docker-compose
```

### 步骤2: 检查当前PATH
```batch
echo %PATH%
```

### 步骤3: 测试Docker命令
```batch
docker --version
docker-compose --version
docker info
```

### 步骤4: 测试iStock项目
```batch
cd /d "G:\openclaw\workspace\_system\agent-home\myStock-AI"
docker-compose version
```

## 📋 快速修复脚本

创建`fix_docker_path.bat`:
```batch
@echo off
echo Fixing Docker PATH issues...
echo.

REM 检查Docker是否在PATH中
where docker >nul 2>nul
if %errorlevel% equ 0 (
    echo Docker found in PATH
    docker --version
) else (
    echo Docker not in PATH, trying to fix...
    
    REM 尝试常见安装路径
    if exist "C:\Program Files\Docker\Docker\resources\bin\docker.exe" (
        echo Adding Docker to PATH temporarily...
        set PATH=C:\Program Files\Docker\Docker\resources\bin;%PATH%
        echo PATH updated
        docker --version
    ) else (
        echo ERROR: Docker not found in standard location
        echo Please ensure Docker Desktop is installed
    )
)

echo.
echo Testing Docker Compose...
where docker-compose >nul 2>nul
if %errorlevel% equ 0 (
    echo docker-compose found
    docker-compose --version
) else (
    echo Trying docker compose (plugin)...
    docker compose version
)

echo.
pause
```

## 🔍 诊断工具

运行以下PowerShell命令诊断问题:
```powershell
# 检查Docker进程
Get-Process | Where-Object {$_.ProcessName -like "*docker*"}

# 检查Docker安装
Get-ChildItem "C:\Program Files\Docker" -Recurse -Filter "docker.exe" -ErrorAction SilentlyContinue

# 检查PATH
$env:PATH -split ';' | Where-Object {$_ -like "*docker*"}

# 测试命令
try { docker --version } catch { "Docker command failed" }
try { docker-compose --version } catch { "Docker Compose command failed" }
```

## 🚀 iStock项目特定修复

### 修改启动脚本使用完整路径
编辑批处理文件，在开头添加:
```batch
REM 设置Docker路径
if not "%DOCKER_PATH%"=="" (
    set "DOCKER_PATH=C:\Program Files\Docker\Docker\resources\bin"
)
if exist "%DOCKER_PATH%\docker.exe" (
    set "PATH=%DOCKER_PATH%;%PATH%"
)
```

### 创建环境设置脚本
`setup_docker_env.bat`:
```batch
@echo off
echo Setting up Docker environment for iStock...
echo.

REM 设置Docker路径
set DOCKER_PATH=C:\Program Files\Docker\Docker\resources\bin

if exist "%DOCKER_PATH%\docker.exe" (
    echo Found Docker at %DOCKER_PATH%
    set PATH=%DOCKER_PATH%;%PATH%
    
    echo Testing Docker...
    docker --version
    docker-compose --version
    
    echo.
    echo Now you can run iStock commands:
    echo docker-compose up -d
    echo docker-compose ps
) else (
    echo ERROR: Docker not found at %DOCKER_PATH%
    echo Please check Docker Desktop installation
)

echo.
pause
```

## 📊 验证成功标准

完成修复后，应该能够:
- [ ] 运行 `docker --version` 无错误
- [ ] 运行 `docker-compose --version` 无错误
- [ ] 运行 `docker info` 显示Docker信息
- [ ] 在iStock目录运行 `docker-compose ps` 显示服务状态

## ⚠️ 常见问题

### Q1: 添加PATH后仍然无效
**A**: 需要重启命令提示符或PowerShell窗口使PATH更改生效。

### Q2: Docker Desktop显示已运行但命令无效
**A**: 可能需要以管理员身份运行命令提示符。

### Q3: 找不到docker-compose.exe
**A**: 新版本Docker使用`docker compose`（插件形式），而不是独立的`docker-compose.exe`。

### Q4: 权限被拒绝
**A**: 确保有权限修改系统环境变量，或以管理员身份运行。

## 🆘 紧急解决方案

如果以上方法都无效，使用:
1. **Docker Desktop内置终端**:
   - 打开Docker Desktop
   - 点击设置图标 ⚙️
   - 选择"Resources" → "WSL Integration"
   - 启用WSL 2集成
   - 使用WSL终端

2. **使用PowerShell Docker模块**:
   ```powershell
   Install-Module -Name DockerMsftProvider -Repository PSGallery -Force
   Install-Package -Name docker -ProviderName DockerMsftProvider
   ```

3. **联系支持**:
   - Docker官方文档: https://docs.docker.com/desktop/
   - Windows系统管理员

## 📞 获取帮助

如果问题仍未解决，请提供:
1. Windows版本
2. Docker Desktop版本
3. 错误消息截图
4. `where docker`命令输出
5. `echo %PATH%`输出（前几行）

---

**注意**: 修复PATH后，需要重新打开所有命令提示符窗口才能使更改生效。