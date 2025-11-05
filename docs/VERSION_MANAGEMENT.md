# Luna-2 版本管理规范

## 📋 版本号规则

采用 [语义化版本](https://semver.org/lang/zh-CN/) 规范：

```
主版本号.次版本号.修订号
例如: 1.0.0
```

- **主版本号**: 不兼容的API修改
- **次版本号**: 向下兼容的功能性新增
- **修订号**: 向下兼容的问题修正

## 🏷️ 当前版本

**V1.0.0** - 硬件Demo测试版本 (2025-11-05)

## 📁 版本文件

### VERSION
存储当前版本号，格式：`1.0.0`

### CHANGELOG.md
详细记录每个版本的变更内容

### docs/VERSION_1.0.0.md
版本详细说明文档

## 🔀 分支管理

### 主分支 (main/master)
- 稳定版本代码
- 仅接受来自release分支的合并
- 当前版本: V1.0.0

### 开发分支 (develop)
- 日常开发分支
- 新功能开发
- Bug修复

### 版本分支 (release/v1.0.0)
- 版本发布分支
- 从develop分支创建
- 版本测试和修复
- 完成后合并到main和develop

### 功能分支 (feature/xxx)
- 新功能开发
- 从develop分支创建
- 完成后合并回develop

### 修复分支 (hotfix/xxx)
- 紧急Bug修复
- 从main分支创建
- 完成后合并到main和develop

## 📝 版本发布流程

### 1. 创建版本分支

```bash
# 从develop分支创建版本分支
git checkout develop
git pull origin develop
git checkout -b release/v1.0.0
git push origin release/v1.0.0
```

### 2. 更新版本信息

- 更新 `VERSION` 文件
- 更新 `CHANGELOG.md`
- 更新模块中的 `__version__` 属性
- 创建版本说明文档 `docs/VERSION_X.X.X.md`

### 3. 版本测试

- 运行完整测试套件
- 进行集成测试
- 性能测试
- 文档检查

### 4. 合并到主分支

```bash
# 合并到main分支
git checkout main
git merge release/v1.0.0
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin main
git push origin v1.0.0

# 合并回develop分支
git checkout develop
git merge release/v1.0.0
git push origin develop
```

### 5. 删除版本分支

```bash
git branch -d release/v1.0.0
git push origin --delete release/v1.0.0
```

## 🔖 Git标签规范

### 创建标签

```bash
# 创建带注释的标签
git tag -a v1.0.0 -m "Release version 1.0.0"

# 推送标签
git push origin v1.0.0
```

### 标签命名

- 格式: `v主版本号.次版本号.修订号`
- 示例: `v1.0.0`, `v1.1.0`, `v2.0.0`

## 📦 模块版本管理

### 模块版本标识

每个核心模块都应包含版本信息：

```python
# 在模块文件开头添加
__version__ = "1.0.0"
__version_info__ = (1, 0, 0)
```

### 模块版本列表

#### Luna_Badge 核心模块
- `system_orchestrator.py`: 1.0.0
- `system_orchestrator_enhanced.py`: 1.0.0
- `whisper_recognizer.py`: 1.0.0
- `tts_manager.py`: 1.0.0
- `vision_ocr_engine.py`: 1.0.0
- `step_detector.py`: 1.0.0
- `navigation_manager.py`: 1.0.0
- `task_engine.py`: 1.0.0
- `memory_store.py`: 1.0.0
- `log_manager.py`: 1.0.0

#### Luna-mid 学习模块
- `error_learning.py`: 1.0.0
- `task_optimizer.py`: 1.0.0
- `user_habit_analyzer.py`: 1.0.0
- `visual_learning.py`: 1.0.0
- `learning_manager.py`: 1.0.0

## 📋 版本检查清单

### 发布前检查

- [ ] 所有测试通过
- [ ] 文档更新完成
- [ ] 版本号更新
- [ ] CHANGELOG更新
- [ ] 模块版本标记
- [ ] 依赖版本检查
- [ ] 性能基准测试
- [ ] 安全审计

### 发布后检查

- [ ] 版本标签创建
- [ ] 发布说明发布
- [ ] 文档站点更新
- [ ] 团队通知

## 🔄 版本兼容性

### V1.0.0 兼容性说明

- **API兼容性**: 首次发布，无兼容性问题
- **数据格式**: 使用JSON格式，向前兼容
- **配置文件**: YAML格式，可向后扩展

### 升级策略

- 主版本升级: 需要迁移指南
- 次版本升级: 平滑升级
- 修订版本: 直接替换

## 📚 相关文档

- `CHANGELOG.md` - 变更日志
- `docs/VERSION_1.0.0.md` - V1.0.0版本说明
- `docs/ARCHITECTURE.md` - 系统架构文档（待创建）

## 🛠️ 工具脚本

### 版本检查脚本

```bash
# 检查所有模块版本
python3 scripts/check_versions.py

# 更新版本号
python3 scripts/update_version.py 1.0.0
```

---

**最后更新**: 2025-11-05  
**维护者**: Luna开发团队

