# Git提交通知测试文件

这个文件用于测试Git提交后自动发送通知到Feishu的功能。

## 测试步骤

1. 添加这个文件到Git
2. 提交更改
3. 检查是否触发post-commit钩子
4. 验证通知消息格式

## 预期结果

提交后应该：
- 触发post-commit钩子脚本
- 运行git_commit_notify.py
- 生成格式化的提交通知
- （实际部署时）发送到Feishu群组

## 功能说明

### 通知内容包含：
- ✅ 提交哈希（短格式）
- ✅ 分支信息
- ✅ 作者信息
- ✅ 提交时间
- ✅ 提交类型和主题
- ✅ 详细描述（如果有）
- ✅ 修改的文件统计
- ✅ GitHub链接（如果配置了远程仓库）

### 提交类型图标：
- 🆕 feat: 新功能
- 🔧 fix: 修复bug
- 📚 docs: 文档更新
- 🎨 style: 代码格式
- ♻️ refactor: 代码重构
- 🧪 test: 测试相关
- 🔧 chore: 构建工具
- ⚡ perf: 性能优化
- 🚀 ci: 持续集成
- 📦 build: 构建系统
- ↩️ revert: 回退提交
- 📝 其他: 其他类型

## 配置说明

### Git钩子位置：
- `.git/hooks/post-commit` (Linux/macOS)
- `.git/hooks/post-commit.bat` (Windows)

### 通知脚本：
- `scripts/git_commit_notify.py`

### 依赖：
- Python 3.6+
- Git命令行工具

## 后续优化

1. 添加真正的Feishu API集成
2. 支持自定义消息模板
3. 添加提交统计功能
4. 支持多种通知渠道（邮件、Slack等）
5. 添加提交质量检查

---

**创建时间**: 2026-02-28  
**用途**: 测试Git提交通知功能