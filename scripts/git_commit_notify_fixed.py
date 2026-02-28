#!/usr/bin/env python3
"""
iStock Git提交通知脚本 - 修复编码版本
每次提交后自动发送详细信息到Feishu群组
"""

import argparse
import json
import os
import sys
from datetime import datetime
from typing import List, Dict, Any
import subprocess

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Send Git commit notification to Feishu')
    parser.add_argument('--hash', required=True, help='Commit hash')
    parser.add_argument('--author', required=True, help='Commit author')
    parser.add_argument('--email', required=True, help='Author email')
    parser.add_argument('--date', required=True, help='Commit date')
    parser.add_argument('--message', required=True, help='Commit message')
    parser.add_argument('--files', required=True, help='Modified files (comma separated)')
    return parser.parse_args()

def analyze_commit_message(message: str) -> Dict[str, Any]:
    """Analyze commit message"""
    lines = message.strip().split('\n')
    
    # Extract commit type and subject
    commit_type = "other"
    subject = ""
    
    if lines:
        first_line = lines[0].strip()
        if ':' in first_line:
            commit_type = first_line.split(':')[0].strip()
            subject = first_line.split(':', 1)[1].strip()
        else:
            subject = first_line
    
    # Extract description
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
    """Analyze file changes"""
    if not files_str:
        return {'total': 0, 'by_type': {}, 'files': []}
    
    files = [f.strip() for f in files_str.split(',') if f.strip()]
    
    # Categorize by file type
    file_types = {}
    for file in files:
        if '.' in file:
            ext = file.split('.')[-1].lower()
        else:
            ext = 'no_extension'
        
        file_types[ext] = file_types.get(ext, 0) + 1
    
    return {
        'total': len(files),
        'by_type': file_types,
        'files': files[:20]  # Show only first 20 files
    }

def get_branch_info() -> Dict[str, str]:
    """Get branch information"""
    try:
        # Get current branch
        project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        branch_result = subprocess.run(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
            capture_output=True,
            text=True,
            cwd=project_dir
        )
        current_branch = branch_result.stdout.strip() if branch_result.returncode == 0 else "unknown"
        
        # Get remote URL
        remote_result = subprocess.run(
            ['git', 'remote', 'get-url', 'origin'],
            capture_output=True,
            text=True,
            cwd=project_dir
        )
        remote_url = remote_result.stdout.strip() if remote_result.returncode == 0 else "not_set"
        
        return {
            'current': current_branch,
            'remote': remote_url
        }
    except:
        return {'current': 'unknown', 'remote': 'unknown'}

def create_feishu_message(args, commit_analysis, file_analysis, branch_info) -> str:
    """Create Feishu message content"""
    
    # Commit type icons
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
        'other': '📝'
    }
    
    icon = type_icons.get(commit_analysis['type'], '📝')
    
    # Build message
    message_parts = []
    
    # Title
    message_parts.append(f"{icon} **iStock Git Commit Notification**")
    message_parts.append("")
    
    # Basic info
    message_parts.append("**📋 Commit Information**")
    message_parts.append(f"- Hash: `{args.hash[:8]}`")
    message_parts.append(f"- Branch: `{branch_info['current']}`")
    message_parts.append(f"- Author: {args.author} ({args.email})")
    message_parts.append(f"- Time: {args.date}")
    message_parts.append("")
    
    # Commit content
    message_parts.append("**📝 Commit Content**")
    message_parts.append(f"- Type: `{commit_analysis['type']}`")
    message_parts.append(f"- Subject: {commit_analysis['subject']}")
    
    if commit_analysis['description']:
        message_parts.append("- Details:")
        for line in commit_analysis['description'].split('\n'):
            if line.strip():
                message_parts.append(f"  {line}")
    
    message_parts.append("")
    
    # File changes
    message_parts.append("**📁 File Changes**")
    message_parts.append(f"- Total files: {file_analysis['total']}")
    
    if file_analysis['by_type']:
        message_parts.append("- By file type:")
        for ext, count in sorted(file_analysis['by_type'].items()):
            message_parts.append(f"  - {ext}: {count} files")
    
    if file_analysis['files']:
        message_parts.append("- Modified files:")
        for i, file in enumerate(file_analysis['files'][:10], 1):
            message_parts.append(f"  {i}. {file}")
        
        if len(file_analysis['files']) > 10:
            message_parts.append(f"  ... and {len(file_analysis['files']) - 10} more files")
    
    message_parts.append("")
    
    # GitHub link
    if 'github.com' in branch_info['remote']:
        repo_path = branch_info['remote'].replace('https://github.com/', '').replace('.git', '')
        commit_url = f"https://github.com/{repo_path}/commit/{args.hash}"
        message_parts.append(f"**🔗 GitHub Link**")
        message_parts.append(f"- Commit details: {commit_url}")
    
    return '\n'.join(message_parts)

def send_to_feishu(message: str):
    """Send message to Feishu group"""
    try:
        print("=" * 50)
        print("Git Commit Notification")
        print("=" * 50)
        print(message)
        print("=" * 50)
        
        # In actual deployment, this would call Feishu API
        # For now, we'll also send via OpenClaw message tool
        
        # Save to log file
        log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
        os.makedirs(log_dir, exist_ok=True)
        
        log_file = os.path.join(log_dir, f'commit_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write(message)
        
        print(f"Notification saved to: {log_file}")
        
        # Also send via OpenClaw message tool
        try:
            import subprocess
            # This would be the actual Feishu message sending
            # For demonstration, we'll just print
            print("📤 This message would be sent to Feishu group in production")
        except Exception as e:
            print(f"Note: Feishu sending not configured: {e}")
        
    except Exception as e:
        print(f"Error sending Feishu message: {e}")

def main():
    """Main function"""
    print("Starting iStock Git commit notification system...")
    
    # Parse arguments
    args = parse_arguments()
    
    # Analyze commit
    print("Analyzing commit information...")
    commit_analysis = analyze_commit_message(args.message)
    
    # Analyze file changes
    print("Analyzing file changes...")
    file_analysis = analyze_file_changes(args.files)
    
    # Get branch info
    print("Getting branch information...")
    branch_info = get_branch_info()
    
    # Create Feishu message
    print("Creating notification message...")
    feishu_message = create_feishu_message(args, commit_analysis, file_analysis, branch_info)
    
    # Send to Feishu
    send_to_feishu(feishu_message)
    
    print("Commit notification processing completed")

if __name__ == "__main__":
    main()