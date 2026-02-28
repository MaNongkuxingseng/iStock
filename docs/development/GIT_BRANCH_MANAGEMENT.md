# iStock项目 - Git分支管理规范

## 📋 分支管理策略

### 目标
- 保持代码库整洁有序
- 支持并行开发
- 确保生产代码稳定
- 简化合并和部署流程

## 🌳 分支结构

### 主要分支
```
main (稳定生产分支)
    ↑
develop (集成开发分支)
    ↑
feature/* (功能开发分支)
```

### 分支说明

| 分支 | 用途 | 生命周期 | 保护规则 |
|------|------|----------|----------|
| **main** | 生产环境代码 | 永久 | 受保护，只接受从develop合并 |
| **develop** | 集成测试环境 | 永久 | 受保护，只接受从feature分支合并 |
| **feature/** | 功能开发 | 1-2周 | 临时分支，完成后删除 |
| **hotfix/** | 紧急修复 | 1-3天 | 临时分支，修复后删除 |
| **release/** | 版本发布 | 1-2周 | 临时分支，发布后删除 |

## 🚀 工作流程

### 1. 功能开发流程
```
1. 从develop创建功能分支
   git checkout develop
   git pull origin develop
   git checkout -b feature/week{周数}-{功能名}

2. 在功能分支上开发
   git add .
   git commit -m "feat: 功能描述"

3. 推送到远程
   git push -u origin feature/week{周数}-{功能名}

4. 创建Pull Request到develop
   - 代码审查
   - 自动化测试
   - 合并批准

5. 合并到develop
   git checkout develop
   git merge feature/week{周数}-{功能名}

6. 删除功能分支
   git branch -d feature/week{周数}-{功能名}
   git push origin --delete feature/week{周数}-{功能名}
```

### 2. 发布流程
```
1. 从develop创建发布分支
   git checkout develop
   git checkout -b release/v{版本号}

2. 在发布分支上进行最终测试和修复

3. 合并到main和develop
   git checkout main
   git merge release/v{版本号} --no-ff
   git tag -a v{版本号} -m "发布版本{版本号}"
   
   git checkout develop
   git merge release/v{版本号}

4. 删除发布分支
   git branch -d release/v{版本号}
```

### 3. 热修复流程
```
1. 从main创建热修复分支
   git checkout main
   git checkout -b hotfix/{问题描述}

2. 修复问题并测试

3. 合并到main和develop
   git checkout main
   git merge hotfix/{问题描述}
   git tag -a v{版本号.修复号} -m "热修复: {问题描述}"
   
   git checkout develop
   git merge hotfix/{问题描述}

4. 删除热修复分支
   git branch -d hotfix/{问题描述}
```

## 📅 每周分支管理计划

### 第1周：项目初始化 ✅
- **分支**: `feature/week1-initialization`
- **状态**: 已完成，已合并到develop，分支已删除
- **内容**: 项目基础设施、Docker配置、CI/CD流水线

### 第2周：数据模型设计 🔄
- **分支**: `feature/week2-data-models`
- **状态**: 进行中，预计3月1日完成
- **内容**: 数据库模型、迁移脚本、数据验证

### 第3周：数据源接入 📝
- **分支**: `feature/week3-data-sources`
- **计划**: 3月3日-3月7日
- **内容**: 新浪/腾讯/东方财富API、数据采集调度器

### 第4周：数据验证 📝
- **分支**: `feature/week4-data-validation`
- **计划**: 3月10日-3月14日
- **内容**: 数据质量检查、异常检测、清洗规则

## 🏷️ 分支命名规范

### 功能分支
```
feature/week{周数}-{功能名}
```
**示例**:
- `feature/week2-data-models`
- `feature/week3-data-sources`
- `feature/week4-data-validation`

### 热修复分支
```
hotfix/{问题描述}
```
**示例**:
- `hotfix/db-connection-timeout`
- `hotfix/api-auth-bug`

### 发布分支
```
release/v{版本号}
```
**示例**:
- `release/v1.0.0`
- `release/v1.1.0`

## 🔒 分支保护规则

### main分支
- ✅ 受GitHub保护
- ✅ 只允许从develop合并
- ✅ 需要Pull Request审查
- ✅ 需要所有检查通过
- ✅ 禁止强制推送

### develop分支
- ✅ 受GitHub保护
- ✅ 只允许从feature分支合并
- ✅ 需要Pull Request审查
- ✅ 需要自动化测试通过
- ✅ 禁止直接推送

## 📊 当前分支状态

| 分支 | 状态 | 最后更新 | 下一步 |
|------|------|----------|--------|
| **main** | 🟢 稳定 | 2026-02-28 | 等待第2周完成 |
| **develop** | 🟡 开发中 | 2026-02-28 | 集成第2周功能 |
| **feature/week2-data-models** | 🟡 进行中 | 2026-02-28 | 完成后合并到develop |
| **feature/week1-initialization** | 🔴 已删除 | 2026-02-28 | 已合并到develop |

## 🛠️ 管理脚本

### 创建功能分支
```bash
#!/bin/bash
# create_feature.sh
week=$1
feature=$2
branch_name="feature/week${week}-${feature}"

git checkout develop
git pull origin develop
git checkout -b $branch_name
echo "✅ 创建功能分支: $branch_name"
```

### 合并功能分支
```bash
#!/bin/bash
# merge_feature.sh
branch_name=$1

git checkout develop
git pull origin develop
git merge $branch_name
git push origin develop
git branch -d $branch_name
git push origin --delete $branch_name
echo "✅ 已合并并删除分支: $branch_name"
```

### 创建发布分支
```bash
#!/bin/bash
# create_release.sh
version=$1
branch_name="release/v${version}"

git checkout develop
git pull origin develop
git checkout -b $branch_name
echo "✅ 创建发布分支: $branch_name"
```

## 📈 合并计划

### 近期合并计划
1. **2026-03-01**: 合并`feature/week2-data-models`到develop
2. **2026-03-08**: 合并`feature/week3-data-sources`到develop
3. **2026-03-15**: 合并`feature/week4-data-validation`到develop
4. **2026-03-22**: 从develop合并到main，发布v1.0.0

### 里程碑发布
- **v0.1.0**: 第1周完成（项目初始化）
- **v0.2.0**: 第2周完成（数据模型）
- **v0.3.0**: 第3周完成（数据源）
- **v0.4.0**: 第4周完成（数据验证）
- **v1.0.0**: MVP版本发布

## 🚨 注意事项

1. **及时删除分支**: 功能完成后立即删除分支
2. **保持develop稳定**: develop分支应始终可部署
3. **小步提交**: 频繁提交，每次提交一个明确的功能
4. **代码审查**: 所有合并都需要Pull Request和审查
5. **自动化测试**: 合并前必须通过所有测试
6. **文档更新**: 分支变更时更新相关文档

## 🔄 分支清理策略

### 自动清理规则
- 功能分支：合并后7天内删除
- 热修复分支：修复后3天内删除
- 发布分支：发布后14天内删除

### 手动清理命令
```bash
# 查看已合并的分支
git branch --merged develop | grep feature/

# 删除已合并的本地分支
git branch --merged develop | grep feature/ | xargs git branch -d

# 删除已合并的远程分支
git branch -r --merged develop | grep origin/feature/ | sed 's/origin\///' | xargs -I {} git push origin --delete {}
```

---

**最后更新**: 2026-02-28  
**维护者**: iStock开发团队  
**状态**: 正式实施