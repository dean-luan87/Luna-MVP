# V1.8.1 人工测试执行指南

**版本**: V1.8.1  
**创建日期**: 2025-12-29  
**用途**: QA 团队人工测试执行指南

---

## 测试执行总原则

### 硬规则

- **TC-06 / TC-07 任一 FAIL → 测试立即终止**
- **不允许"先看看功能好不好"**
- **必须与 v1.8 完全一致**

---

## Phase 1: 回滚等价性（生死线）

### TC-06: 全局回滚测试

#### 测试目标

验证 `observer_mode=false` 时，行为必须等价 v1.8

#### 执行步骤

1. **准备测试环境**
   ```bash
   # 设置 observer_mode=false
   export OBSERVER_MODE_ENABLED=false
   # 或修改配置文件
   ```

2. **运行完整流程**
   - 导航流程
   - 医院挂号流程
   - 其他核心流程

3. **对比 v1.8 基线版本**
   - 播报内容对比
   - 任务流对比
   - 交互流程对比

4. **记录结果**
   - 使用 `docs/V1_8_1_TEST_EXECUTION_LOG.md` 记录
   - 必须明确：PASS 或 FAIL

#### 判定标准

- ✅ **所有行为与 v1.8 完全一致** → PASS
- ❌ **任何差异** → FAIL（阻断版本）

#### 检查清单

- [ ] 设置 OBSERVER_MODE_ENABLED=false
- [ ] 运行完整导航流程
- [ ] 运行医院挂号流程
- [ ] 对比 v1.8 基线版本的行为
- [ ] 检查播报内容是否一致
- [ ] 检查任务流是否一致
- [ ] 检查交互流程是否一致

---

### TC-07: 日志回滚测试

#### 测试目标

验证 `observer_mode=false` 时，不得写 observer_* 日志

#### 执行步骤

1. **准备测试环境**
   ```bash
   # 设置 observer_mode=false
   export OBSERVER_MODE_ENABLED=false
   ```

2. **运行系统，触发所有场景**
   - 导航场景
   - 医院场景
   - 其他场景

3. **检查日志**
   ```bash
   # 检查日志文件
   grep -r "observer_" logs/
   
   # 或使用辅助脚本
   python3 scripts/manual_test_tc06_tc07.py
   ```

4. **记录结果**
   - 使用 `docs/V1_8_1_TEST_EXECUTION_LOG.md` 记录
   - 必须明确：PASS 或 FAIL

#### 判定标准

- ✅ **日志中无 observer_* 字段** → PASS
- ❌ **存在 observer_* 字段** → FAIL（阻断版本）

#### 检查清单

- [ ] 设置 OBSERVER_MODE_ENABLED=false
- [ ] 运行系统，触发所有场景
- [ ] 检查日志文件（logs/ 目录）
- [ ] 检查控制台输出
- [ ] 搜索 observer_* 字段
- [ ] 确认不存在 observer_* 字段

---

## 辅助工具

### 快速验证脚本

```bash
# 代码层面快速检查
python3 scripts/quick_test_rollback.py
```

### 人工测试辅助脚本

```bash
# 辅助执行 TC-06 / TC-07
python3 scripts/manual_test_tc06_tc07.py
```

---

## 测试记录

### 记录位置

`docs/V1_8_1_TEST_EXECUTION_LOG.md`

### 记录模板

#### TC-06 记录

```markdown
### TC-06: 全局回滚测试

- **执行人**：
- **日期**：
- **版本 / Commit**：
- **OBSERVER_MODE_ENABLED**：
  - [x] false
  - [ ] true

#### 执行结果
- **Pass / Fail**：
- **与 v1.8 是否完全一致（是 / 否）**：

#### 证据
- **日志截图 / 输出摘要**：

#### 结论
- [ ] 允许继续
- [x] **阻断版本**（如 Fail，必须选择此项）
```

#### TC-07 记录

```markdown
### TC-07: 日志回滚测试

- **执行人**：
- **日期**：
- **版本 / Commit**：
- **OBSERVER_MODE_ENABLED**：
  - [x] false
  - [ ] true

#### 执行结果
- **Pass / Fail**：
- **与 v1.8 是否完全一致（是 / 否）**：

#### 证据
- **日志截图 / 输出摘要**：

#### 结论
- [ ] 允许继续
- [x] **阻断版本**（如 Fail，必须选择此项）
```

---

## 重要提醒

### TC-06 / TC-07 的结论栏

**只能二选一，不能模糊描述**

- ✅ 允许继续
- ❌ **阻断版本**（如 Fail，必须选择此项）

### 如果失败

- **立即终止测试**
- **版本冻结**
- **不允许"先看看功能好不好"**

---

## 下一步

### 如果 TC-06 和 TC-07 都通过

✅ **可以继续 Phase 2: 高风险安全测试**

### 如果任一失败

❌ **立即终止测试，版本冻结**

---

**最后更新**: 2025-12-29  
**维护者**: QA 团队


