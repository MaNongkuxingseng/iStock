#!/usr/bin/env python3
"""
iStock Git Commit Notification Script
Send commit details to Feishu after each commit
"""

import argparse
import os
import sys
from datetime import datetime
import subprocess

def parse_arguments():
    parser = argparse.ArgumentParser(description='Send Git commit notification')
    parser.add_argument('--hash', required=True, help='Commit hash')
    parser.add_argument('--author', required=True, help='Commit author')
    parser.add_argument('--email', required=True, help='Author email')
    parser.add_argument('--date', required=True, help='Commit date')
    parser.add_argument('--message', required=True, help='Commit message')
    parser.add_argument('--files', required=True, help='Modified files')
    return parser.parse_args()

def create_message(args):
    """Create notification message"""
    
    # Type mapping
    type_map = {
        'feat': 'NEW',
        'fix': 'FIX',
        'docs': 'DOCS',
        'style': 'STYLE',
        'refactor': 'REFACTOR',
        'test': 'TEST',
        'chore': 'CHORE',
        'perf': 'PERF',
        'ci': 'CI',
        'build': 'BUILD',
        'revert': 'REVERT'
    }
    
    # Get commit type
    commit_type = 'OTHER'
    subject = args.message.split('\n')[0] if args.message else ''
    
    if ':' in subject:
        possible_type = subject.split(':')[0].strip()
        if possible_type in type_map:
            commit_type = type_map[possible_type]
    
    # Get branch info
    try:
        project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        branch_result = subprocess.run(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
            capture_output=True,
            text=True,
            cwd=project_dir
        )
        branch = branch_result.stdout.strip() if branch_result.returncode == 0 else 'unknown'
    except:
        branch = 'unknown'
    
    # Count files
    file_count = len([f for f in args.files.split(',') if f.strip()])
    
    # Create message
    message = f"""iStock Git Commit Notification
================================

Commit: {args.hash[:8]}
Branch: {branch}
Type: {commit_type}
Author: {args.author}
Time: {args.date}

Subject: {subject}

Files changed: {file_count}
"""
    
    # Add file list if not too many
    files = [f.strip() for f in args.files.split(',') if f.strip()]
    if files and len(files) <= 10:
        message += "\nFiles:\n"
        for i, file in enumerate(files[:10], 1):
            message += f"  {i}. {file}\n"
    
    return message

def main():
    print("Processing Git commit notification...")
    
    args = parse_arguments()
    message = create_message(args)
    
    print("\n" + "="*50)
    print("COMMIT NOTIFICATION READY")
    print("="*50)
    print(message)
    print("="*50)
    
    # Save to file
    log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f'commit_{timestamp}.txt')
    
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write(message)
    
    print(f"\nNotification saved to: {log_file}")
    print("\nThis message would be sent to Feishu group in production.")

if __name__ == "__main__":
    main()