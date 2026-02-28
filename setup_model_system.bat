@echo off
chcp 65001 >nul
echo ========================================
echo OpenClaw模型管理系统一键配置
echo ========================================
echo.

set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

echo [1/4] 检查当前配置...
openclaw config get agents.defaults.model.primary
openclaw config get agents.defaults.model.fallbacks

echo.
echo [2/4] 更新模型配置...
echo 设置主模型为: deepseek/deepseek-chat
echo 设置备用模型为: openai-codex/gpt-5.3-codex, qwen/qwen-plus

REM 这里应该调用实际的配置更新命令
REM 由于openclaw config set有格式问题，我们直接编辑文件
echo 正在编辑配置文件...

python -c "
import json
config_path = r'C:\Users\Administrator\.openclaw\openclaw.json'
try:
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # 更新模型配置
    if 'agents' not in config:
        config['agents'] = {}
    if 'defaults' not in config['agents']:
        config['agents']['defaults'] = {}
    if 'model' not in config['agents']['defaults']:
        config['agents']['defaults']['model'] = {}
    
    config['agents']['defaults']['model']['primary'] = 'deepseek/deepseek-chat'
    config['agents']['defaults']['model']['fallbacks'] = ['openai-codex/gpt-5.3-codex', 'qwen/qwen-plus']
    
    # 保存配置
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print('配置更新成功！')
except Exception as e:
    print(f'配置更新失败: {e}')
"

echo.
echo [3/4] 重启Gateway服务...
openclaw gateway restart
timeout /t 3 /nobreak >nul

echo.
echo [4/4] 验证配置...
openclaw gateway status
echo.
echo 验证模型配置:
openclaw config get agents.defaults.model.primary
openclaw config get agents.defaults.model.fallbacks

echo.
echo ========================================
echo 配置完成！
echo ========================================
echo.
echo 下一步操作:
echo 1. 测试模型监控系统: python model_guard_bot.py
echo 2. 测试智能路由: python intelligent_model_router.py
echo 3. 启动完整监控: python model_management_system.py
echo.
echo 定时任务建议:
echo • 每5分钟检查模型状态
echo • 每天生成模型使用报告
echo • 异常时自动发送Feishu警报
echo.
pause