# V1.8.1 自动化测试骨架

**版本**: V1.8.1  
**创建日期**: 2025-12-29  
**状态**: 🚧 骨架就绪，待实现具体逻辑

---

## 自动化范围优先级

### 第一优先级（必须自动化）

- ✅ **TC-06**: 全局回滚等价性测试
  - 文件: `test_rollback_equivalence.py`
  - 目标: 验证 observer_mode=false 时，行为必须等价 v1.8

- ✅ **TC-07**: 日志零污染测试
  - 文件: `test_logging_isolation.py`
  - 目标: 验证 observer_mode=false 时，不得写 observer_* 日志

### 第二优先级（半自动 / 模拟）

- ✅ **TC-03**: 危险场景强打断
  - 文件: `test_intervene_safety.py`
  - 目标: 验证 INTERVENE 行为正确性

- ✅ **TC-05**: 等待态安全行为
  - 文件: `test_waiting_state_safety.py`
  - 目标: 验证 waiting_state 下只允许 INTERVENE

### 暂不自动化

- ⏳ **TC-01**: 后台观察（BACKGROUND）- 交互复杂，先人工
- ⏳ **TC-02**: 关键节点确认（CONFIRM）- 交互复杂，先人工
- ⏳ **TC-04**: 连续 CONFIRM 失败 - 交互复杂，先人工
- ⏳ **TC-08**: 人工求助触发 - 交互复杂，先人工
- ⏳ **TC-09**: 人工求助不越权 - 交互复杂，先人工

---

## 文件结构

```
tests/v1_8_1/
├── conftest.py                    # pytest 配置和 Fixtures
├── test_rollback_equivalence.py  # TC-06: 回滚等价性测试
├── test_logging_isolation.py     # TC-07: 日志零污染测试
├── test_intervene_safety.py      # TC-03: 危险场景强打断
├── test_waiting_state_safety.py  # TC-05: 等待态安全行为
└── README.md                      # 本文件
```

---

## 运行方式

### 运行所有测试

```bash
pytest tests/v1_8_1/
```

### 运行特定测试

```bash
# 运行回滚等价性测试
pytest tests/v1_8_1/test_rollback_equivalence.py

# 运行日志零污染测试
pytest tests/v1_8_1/test_logging_isolation.py
```

### 运行特定测试用例

```bash
# 运行 TC-06 主测试
pytest tests/v1_8_1/test_rollback_equivalence.py::test_observer_mode_disabled_equivalence
```

---

## 工程意义

### 不是形式，而是保障

这套自动化不是为了：
- ❌ 提升覆盖率
- ❌ 追求"看起来很高级"

而是为了：

**任何未来改动，只要破坏 v1.8 等价性，CI 会第一时间把它杀掉。**

这在多版本并行时价值极高。

---

## 实现状态

### 已完成

- ✅ 测试骨架结构
- ✅ pytest 配置和 Fixtures
- ✅ TC-06 测试框架
- ✅ TC-07 测试框架
- ✅ TC-03 测试框架（半自动）
- ✅ TC-05 测试框架（半自动）

### 待实现

- ⏳ 系统运行器（SystemRunner）的具体实现
- ⏳ 日志收集器（LogCollector）的具体实现
- ⏳ v1.8 基线版本的运行逻辑
- ⏳ 场景模拟逻辑
- ⏳ 行为对比逻辑

---

## 注意事项

### 合同测试

TC-06 和 TC-07 是"合同测试"，不是功能测试。

**失败就意味着：版本不可存在**

### CI 集成

建议在 CI 中集成这些测试：

```yaml
# .github/workflows/v1_8_1_equivalence.yml
- name: Run V1.8.1 Equivalence Tests
  run: |
    pytest tests/v1_8_1/test_rollback_equivalence.py
    pytest tests/v1_8_1/test_logging_isolation.py
```

---

## 参考文档

- `docs/V1_8_1_TEST_SUITE.md` - 完整测试脚本总集
- `docs/V1_8_1_TEST_EXECUTION_LOG.md` - 测试执行记录模板
- `docs/V1_8_1_LOGGING_METRICS.md` - 日志与指标文档

---

**最后更新**: 2025-12-29  
**维护者**: V1.8.1 开发团队


