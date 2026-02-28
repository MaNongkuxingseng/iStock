#!/usr/bin/env python3
"""
iStock Git提交通知脚本
每次提交后自动发送详细信息到Feishu群组
"""

import argparse
import json
import os
import sys
from datetime import datetime
from typing import List, Dict, Any
import subprocess

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='发送Git提交通知到Feishu')
    parser.add_argument('--hash', required=True, help='提交哈希')
    parser.add_argument('--author', required=True, help='提交作者')
    parser.add_argument('--email', required=True, help='作者邮箱')
    parser.add_argument('--date', required=True, help='提交日期')
    parser.add_argument('--message', required=True, help='提交信息')
    parser.add_argument('--files', required=True, help='修改的文件列表（逗号分隔）')
    return parser.parse_args()

def analyze_commit_message(message: str) -> Dict[str, Any]:
    """分析提交信息"""
    lines = message.strip().split('\n')
    
    # 提取提交类型和主题
    commit_type = "其他"
    subject = ""
    
    if lines:
        first_line = lines[0].strip()
        if ':' in first_line:
            commit_type = first_line.split(':')[0].strip()
            subject = first_line.split(':', 1)[1].strip()
        else:
            subject = first_line
    
    # 提取详细描述
    description_lines = []
    in_description = False
    
    for line in lines[1:]:
        line = line.strip()
        if line:
            if line.startswith('- ') or line.startswith('* '):
                in_description = True
                description_lines.append(line)
            elif in_description:
                description_lines.append(line)
    
    return {
        'type': commit_type,
        'subject': subject,
        'description': '\n'.join(description_lines),
        'full_message': message
    }

def analyze_file_changes(files_str: str) -> Dict[str, Any]:
    """分析文件变更"""
    if not files_str:
        return {'total': 0, 'by_type': {}, 'files': []}
    
    files = [f.strip() for f in files_str.split(',') if f.strip()]
    
    # 按文件类型分类
    file_types = {}
    for file in files:
        if '.' in file:
            ext = file.split('.')[-1].lower()
        else:
            ext = '无扩展名'
        
        file_types[ext] = file_types.get(ext, 0) + 1
    
    return {
        'total': len(files),
        'by_type': file_types,
        'files': files[:20]  # 只显示前20个文件
    }

def get_branch_info() -> Dict[str, str]:
    """获取分支信息"""
    try:
        # 获取当前分支
        branch_result = subprocess.run(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        current_branch = branch_result.stdout.strip() if branch_result.returncode == 0 else "未知"
        
        # 获取远程分支
        remote_result = subprocess.run(
            ['git', 'remote', 'get-url', 'origin'],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        remote_url = remote_result.stdout.strip() if remote_result.returncode == 0 else "未设置"
        
        return {
            'current': current_branch,
            'remote': remote_url
        }
    except:
        return {'current': '未知', 'remote': '未知'}

def create_feishu_message(args, commit_analysis, file_analysis, branch_info) -> str:
    """创建Feishu消息内容"""
    
    # 提交类型图标映射
    type_icons = {
        'feat': '🆕',
        'fix': '🔧', 
        'docs': '📚',
        'style': '🎨',
        'refactor': '♻️',
        'test': '🧪',
        'chore': '🔧',
        'perf': '⚡',
        'ci': '🚀',
        'build': '📦',
        'revert': '↩️',
        '其他': '📝'
    }
    
    icon = type_icons.get(commit_analysis['type'], '📝')
    
    # 构建消息
    message_parts = []
    
    # 标题
    message_parts.append(f"{icon} **iStock Git提交通知**")
    message_parts.append("")
    
    # 基本信息
    message_parts.append("**📋 提交信息**")
    message_parts.append(f"- 哈希: `{args.hash[:8]}`")
    message_parts.append(f"- 分支: `{branch_info['current']}`")
    message_parts.append(f"- 作者: {args.author} ({args.email})")
    message_parts.append(f"- 时间: {args.date}")
    message_parts.append("")
    
    # 提交内容
    message_parts.append("**📝 提交内容**")
    message_parts.append(f"- 类型: `{commit_analysis['type']}`")
    message_parts.append(f"- 主题: {commit_analysis['subject']}")
    
    if commit_analysis['description']:
        message_parts.append("- 详细:")
        for line in commit_analysis['description'].split('\n'):
            if line.strip():
                message_parts.append(f"  {line}")
    
    message_parts.append("")
    
    # 文件变更
    message_parts.append("**📁 文件变更**")
    message_parts.append(f"- 总文件数: {file_analysis['total']}")
    
    if file_analysis['by_type']:
        message_parts.append("- 按类型:")
        for ext, count in sorted(file_analysis['by_type'].items()):
            message_parts.append(f"  - {ext}: {count}个")
    
    if file_analysis['files']:
        message_parts.append("- 修改的文件:")
        for i, file in enumerate(file_analysis['files'][:10], 1):
            message_parts.append(f"  {i}. {file}")
        
        if len(file_analysis['files']) > 10:
            message_parts.append(f"  ... 还有{len(file_analysis['files']) - 10}个文件")
    
    message_parts.append("")
    
    # GitHub链接
    if 'github.com' in branch_info['remote']:
        repo_path = branch_info['remote'].replace('https://github.com/', '').replace('.git', '')
        commit_url = f"https://github.com/{repo_path}/commit/{args.hash}"
        message_parts.append(f"**🔗 GitHub链接**")
        message_parts.append(f"- 提交详情: {commit_url}")
    
    return '\n'.join(message_parts)

def send_to_feishu(message: str):
    """发送消息到Feishu群组"""
    try:
        # 这里使用OpenClaw的message工具发送消息
        # 在实际环境中，这里会调用Feishu API
        # 由于我们在OpenClaw环境中，可以直接使用message工具
        
        print("📤 准备发送提交通知到Feishu...")
        print("=" * 50)
        print(message)
        print("=" * 50)
        
        # 在实际部署中，这里会调用真正的Feishu API
        # 暂时先打印到控制台
        print("✅ 提交通知已生成（实际部署时会发送到Feishu群组）")
        
        # 保存到日志文件供后续使用
        log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
        os.makedirs(log_dir, exist_ok=True)
        
        log_file = os.path.join(log_dir, f'commit_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write(message)
        
        print(f"📄 通知已保存到: {log_file}")
        
    except Exception as e:
        print(f"❌ 发送Feishu消息失败: {e}")

def main():
    """主函数"""
    print("🚀 iStock Git提交通知系统启动...")
    
    # 解析参数
    args = parse_arguments()
    
    # 分析提交信息
    print("📊 分析提交信息...")
    commit_analysis = analyze_commit_message(args.message)
    
    # 分析文件变更
    print("📁 分析文件变更...")
    file_analysis = analyze_file_changes(args.files)
    
    # 获取分支信息
    print("🌿 获取分支信息...")
    branch_info = get_branch_info()
    
    # 创建Feishu消息
    print("💬 创建通知消息...")
    feishu_message = create_feishu_message(args, commit_analysis, file_analysis, branch_info)
    
    # 发送到Feishu
    send_to_feishu(feishu_message)
    
    print("✅ 提交通知处理完成")

if __name__ == "__main__":
    main()