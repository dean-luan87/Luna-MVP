# Luna-2 开发工作流程

## ⚠️ 重要说明

**V1.0.0 代码已锁定，禁止直接修改！**

所有后续开发必须在分支上进行，不允许直接修改以下分支：
- `main` 分支（V1.0.0稳定版本）
- `release/v1.0.0` 分支（V1.0.0发布分支）

## 🔀 分支说明

### 主分支 (main)
- **用途**: 稳定版本代码
- **当前版本**: V1.0.0
- **状态**: 🔒 **锁定** - 禁止直接修改
- **更新方式**: 仅通过release分支合并

### 发布分支 (release/v1.0.0)
- **用途**: V1.0.0版本备份
- **状态**: 🔒 **锁定** - 禁止修改
- **用途**: 用于版本回滚和参考

### 开发分支 (develop)
- **用途**: 日常开发主分支
- **状态**: ✅ **可开发** - 用于集成新功能
- **更新方式**: 从feature分支合并

### 功能分支 (feature/xxx)
- **用途**: 新功能开发
- **状态**: ✅ **可开发** - 从develop创建
- **命名规范**: `feature/功能名称`

## 📋 开发流程

### 1. 开始新功能开发

```bash
# 1. 确保在develop分支
git checkout develop
git pull origin develop

# 2. 创建功能分支
git checkout -b feature/your-feature-name

# 3. 开始开发
# ... 编写代码 ...
```

### 2. 提交代码

```bash
# 在功能分支上提交
git add .
git commit -m "feat: 添加新功能描述"

# 推送到远程
git push origin feature/your-feature-name
```

### 3. 合并到develop

```bash
# 1. 切换到develop分支
git checkout develop
git pull origin develop

# 2. 合并功能分支
git merge feature/your-feature-name

# 3. 解决冲突（如果有）
# ... 解决冲突 ...

# 4. 推送到远程
git push origin develop

# 5. 删除本地功能分支（可选）
git branch -d feature/your-feature-name

# 6. 删除远程功能分支（可选）
git push origin --delete feature/your-feature-name
```

### 4. 创建新版本

```bash
# 1. 从develop创建版本分支
git checkout develop
git checkout -b release/v1.1.0

# 2. 更新版本号
# - 修改 VERSION 文件
# - 更新 CHANGELOG.md
# - 更新模块版本号
# - 更新文档

# 3. 提交版本更新
git add .
git commit -m "chore: 准备发布v1.1.0"

# 4. 测试和修复
# ... 进行测试和bug修复 ...

# 5. 合并到main分支
git checkout main
git merge release/v1.1.0

# 6. 创建标签
git tag -a v1.1.0 -m "Release version 1.1.0"

# 7. 合并回develop
git checkout develop
git merge release/v1.1.0

# 8. 推送所有更改
git push origin main
git push origin develop
git push origin v1.1.0
git push origin release/v1.1.0
```

### 5. 紧急Bug修复

```bash
# 1. 从main创建hotfix分支
git checkout main
git checkout -b hotfix/critical-bug-fix

# 2. 修复bug
# ... 修复代码 ...

# 3. 提交修复
git add .
git commit -m "fix: 修复严重bug描述"

# 4. 合并到main和develop
git checkout main
git merge hotfix/critical-bug-fix

git checkout develop
git merge hotfix/critical-bug-fix

# 5. 推送
git push origin main
git push origin develop
```

## 🚫 禁止操作

### ❌ 禁止直接修改main分支
```bash
# ❌ 错误示例
git checkout main
# 直接修改代码
git commit -m "xxx"  # 禁止！

# ✅ 正确做法
git checkout develop
git checkout -b feature/xxx
# 开发完成后合并到develop
```

### ❌ 禁止直接修改release/v1.0.0分支
```bash
# ❌ 错误示例
git checkout release/v1.0.0
# 修改代码  # 禁止！

# ✅ release分支是只读的，用于版本备份
```

### ❌ 禁止强制推送
```bash
# ❌ 错误示例
git push --force origin main  # 绝对禁止！

# ✅ 使用正常的合并流程
```

## 📝 提交信息规范

使用语义化提交信息：

- `feat`: 新功能
- `fix`: Bug修复
- `docs`: 文档更新
- `style`: 代码格式（不影响功能）
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建/工具相关
- `perf`: 性能优化

示例：
```bash
git commit -m "feat: 添加新的语音识别功能"
git commit -m "fix: 修复YOLO检测精度问题"
git commit -m "docs: 更新API文档"
```

## 🔍 检查当前状态

### 查看当前分支
```bash
git branch
```

### 查看所有分支（包括远程）
```bash
git branch -a
```

### 查看版本标签
```bash
git tag -l
```

### 查看版本信息
```bash
python3 scripts/check_versions.py
```

## 📊 分支关系图

```
main (V1.0.0) ──────────────┐
                            │
release/v1.0.0 ─────────────┤ (锁定)
                            │
develop ────────────────────┼─── feature/xxx ────┐
                            │                     │
                            │                     │ (合并)
                            │                     ▼
                            │              develop (更新)
                            │
                            └─── release/v1.1.0 ──→ main (V1.1.0)
```

## 🎯 快速参考

### 日常开发
```bash
# 1. 创建功能分支
git checkout develop && git pull
git checkout -b feature/my-feature

# 2. 开发并提交
git add . && git commit -m "feat: xxx"

# 3. 推送
git push origin feature/my-feature

# 4. 合并到develop（通过PR或直接合并）
git checkout develop
git merge feature/my-feature
git push origin develop
```

### 查看V1.0.0代码
```bash
# 查看V1.0.0标签的代码
git checkout v1.0.0

# 查看release分支
git checkout release/v1.0.0

# 返回开发分支
git checkout develop
```

## ⚠️ 重要提醒

1. **永远不要直接修改main分支**
2. **永远不要直接修改release/v1.0.0分支**
3. **所有开发都在feature分支上进行**
4. **使用规范的提交信息**
5. **定期同步develop分支**
6. **发布前进行充分测试**

---

**最后更新**: 2025-11-05  
**维护者**: Luna开发团队

