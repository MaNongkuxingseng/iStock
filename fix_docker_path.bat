@echo off
echo ========================================
echo Docker PATH 修复工具
echo ========================================
echo.

echo [1/4] 查找Docker Desktop安装路径...
echo.

:: 常见Docker安装路径
set "PATHS_TO_CHECK=C:\Program Files\Docker\Docker\resources\bin;C:\Program Files\Docker\Docker\resources;%ProgramFiles%\Docker\Docker\resources\bin"

echo 检查以下路径:
for %%p in (%PATHS_TO_CHECK%) do (
    if exist "%%p\docker.exe" (
        echo ✅ 找到Docker: %%p\docker.exe
        set "DOCKER_PATH=%%p"
        goto :FOUND_DOCKER
    )
)

echo ❌ 未找到Docker，请检查是否已安装Docker Desktop
echo.
echo 请手动添加Docker路径到系统PATH:
echo 1. 右键点击"此电脑" -> 属性 -> 高级系统设置
echo 2. 点击"环境变量"
echo 3. 在"系统变量"中找到Path，点击编辑
echo 4. 添加Docker路径: C:\Program Files\Docker\Docker\resources\bin
echo 5. 重启命令行窗口
pause
exit /b 1

:FOUND_DOCKER
echo.
echo [2/4] 当前系统PATH检查...
echo %PATH% | find "%DOCKER_PATH%" >nul
if errorlevel 1 (
    echo ⚠️  Docker路径不在当前PATH中
) else (
    echo ✅  Docker路径已在PATH中
)

echo.
echo [3/4] 创建使用完整路径的脚本...
echo.

:: 创建使用完整Docker路径的脚本
echo @echo off > docker_fullpath.bat
echo set "DOCKER_EXE=%DOCKER_PATH%\docker.exe" >> docker_fullpath.bat
echo "%DOCKER_EXE%" %%* >> docker_fullpath.bat

echo @echo off > docker-compose_fullpath.bat
echo set "DOCKER_EXE=%DOCKER_PATH%\docker.exe" >> docker-compose_fullpath.bat
echo "%DOCKER_EXE%" compose %%* >> docker-compose_fullpath.bat

echo ✅ 已创建 docker_fullpath.bat 和 docker-compose_fullpath.bat
echo   这些脚本使用Docker的完整路径，避免PATH问题

echo.
echo [4/4] 更新项目中的Docker脚本...
echo.

:: 更新项目中的脚本使用完整路径
if exist "start_easy.bat" (
    powershell -Command "(Get-Content 'start_easy.bat') -replace 'docker ', '%DOCKER_PATH%\\docker ' | Set-Content 'start_easy_fixed.bat'"
    echo ✅ 更新 start_easy.bat -> start_easy_fixed.bat
)

if exist "docker-compose.yml" (
    echo # 使用完整Docker路径的启动命令 > start_docker_fixed.bat
    echo @echo off >> start_docker_fixed.bat
    echo echo 使用完整Docker路径启动服务... >> start_docker_fixed.bat
    echo "%DOCKER_PATH%\docker.exe" compose up -d >> start_docker_fixed.bat
    echo echo. >> start_docker_fixed.bat
    echo echo 服务状态: >> start_docker_fixed.bat
    echo "%DOCKER_PATH%\docker.exe" compose ps >> start_docker_fixed.bat
    echo pause >> start_docker_fixed.bat
    echo ✅ 创建 start_docker_fixed.bat
)

echo.
echo ========================================
echo 修复完成！
echo ========================================
echo.
echo 使用方法:
echo 1. 直接运行: docker_fullpath.bat [命令]
echo    示例: docker_fullpath.bat --version
echo 2. 运行: docker-compose_fullpath.bat [命令]
echo    示例: docker-compose_fullpath.bat up -d
echo 3. 或运行: start_docker_fixed.bat
echo.
echo 长期解决方案:
echo 请将 %DOCKER_PATH% 添加到系统PATH环境变量
echo.
pause