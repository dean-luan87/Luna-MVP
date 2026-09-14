# V1.8.1 CI 集成指南

**版本**: V1.8.1  
**创建日期**: 2025-12-29  
**目标**: 将自动化测试集成到 CI 流程

---

## 一、CI 集成建议（非常关键）

### 核心测试

**这两条测试**：
- ✅ **不允许 skip**
- ✅ **不允许 flaky**
- ✅ **它们的失败优先级**：
  - 高于单测失败
  - 高于 lint

### 测试用例

1. **TC-06**: 回滚等价性测试
   - 文件: `tests/v1_8_1/test_rollback_equivalence.py::test_observer_disabled_equals_v18`
   - 失败 = 版本不可存在

2. **TC-07**: 日志零污染测试
   - 文件: `tests/v1_8_1/test_logging_isolation.py::test_no_observer_logs_when_disabled`
   - 失败 = 版本不可存在

---

## 二、GitHub Actions 示例

### 完整 CI 配置

```yaml
# .github/workflows/v1_8_1_equivalence.yml
name: V1.8.1 Equivalence Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  equivalence-tests:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.8'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run TC-06: Rollback Equivalence
      run: |
        pytest tests/v1_8_1/test_rollback_equivalence.py::test_observer_disabled_equals_v18 -v
      continue-on-error: false  # 不允许失败
    
    - name: Run TC-07: Logging Isolation
      run: |
        pytest tests/v1_8_1/test_logging_isolation.py::test_no_observer_logs_when_disabled -v
      continue-on-error: false  # 不允许失败
    
    - name: Run other tests
      run: |
        pytest tests/v1_8_1/ -v
      continue-on-error: true  # 其他测试允许失败
```

---

## 三、CI 执行顺序

### 推荐顺序

1. **Lint / Format** (快速失败)
2. **TC-06 / TC-07** (核心等价性测试)
3. **其他单元测试**
4. **集成测试**

### 失败处理

- **TC-06 / TC-07 失败**: 立即终止，不允许继续
- **其他测试失败**: 允许继续，但标记为警告

---

## 四、CI 状态检查

### PR 合并要求

**必须满足**:
- ✅ TC-06 通过
- ✅ TC-07 通过
- ✅ Lint 通过

**可选**:
- ⚠️ 其他测试通过（警告，不阻断）

---

## 五、CI 监控

### 关键指标

- **TC-06 通过率**: 必须 100%
- **TC-07 通过率**: 必须 100%
- **执行时间**: 监控趋势，避免变慢

### 告警设置

**建议告警**:
- TC-06 / TC-07 失败 → 立即告警
- 执行时间异常 → 告警

---

## 六、本地开发建议

### 提交前检查

```bash
# 运行核心等价性测试
pytest tests/v1_8_1/test_rollback_equivalence.py::test_observer_disabled_equals_v18 -v
pytest tests/v1_8_1/test_logging_isolation.py::test_no_observer_logs_when_disabled -v
```

### 快速验证

```bash
# 运行所有 v1.8.1 测试
pytest tests/v1_8_1/ -v
```

---

## 七、总结

### 核心原则

- ✅ **TC-06 / TC-07 不允许 skip**
- ✅ **TC-06 / TC-07 不允许 flaky**
- ✅ **失败优先级高于其他测试**

### 工程价值

**任何未来改动，只要破坏 v1.8 等价性，CI 会第一时间把它杀掉。**

这在多版本并行时价值极高。

---

**最后更新**: 2025-12-29  
**维护者**: V1.8.1 开发团队


