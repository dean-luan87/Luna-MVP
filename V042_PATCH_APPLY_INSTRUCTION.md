# B2 v0.4.2 Patch 应用说明

**Patch 文件：** `b2_v042_gate.patch`  
**目标文件：** `vision_pipeline/b2/v03/b2_v03.py`  
**版本：** v0.4.1 → v0.4.2

---

## 📋 Patch 内容

### 1. 添加 `self.gate` 别名

在 `__init__` 方法中（第 154 行后）：
```python
self.gate = self.gate_evaluator_v05  # v0.4.2: 简化别名
```

### 2. Gate 评估移到 tick() 最顶部

在 `tick()` 方法中，在 `trace = {}` 之前（第 198 行前）：
- 从 perception 中提取 Gate 所需信息
- 调用 `self.gate.evaluate()`
- SUSPENDED 时直接返回 None（但仍写最小 trace）

### 3. 简化 READ_ONLY 处理

在写回之前（第 743 行前）：
```python
if mode == "READ_ONLY":
    return summary
```

---

## 🚀 应用方式

### 方法 1: 使用 git apply

```bash
git apply b2_v042_gate.patch
```

### 方法 2: 手动应用

按照 patch 文件中的行号指示，逐行修改代码。

---

## ✅ 应用后验证

### 1. 运行测试

```bash
# v0.4.1 回归测试（应全部 PASS）
python3 -m pytest tests/test_b2_v041_gate_behavior_standalone.py -v

# v0.4.2 集成测试
python3 -m pytest tests/test_b2_v042_tick_gate_integration.py -v
```

### 2. 检查 trace

- ✅ trace 中新增 `gate_eval` 节点
- ✅ Gate=SUSPENDED 时，trace 包含 `decision_state: "SUSPENDED"`
- ✅ Gate=READ_ONLY 时，summary 包含 `readonly: True`

### 3. 检查行为

- ✅ Gate=SUSPENDED → tick() 返回 None
- ✅ Gate=READ_ONLY → 有 summary，但无 timeline / health / memory
- ✅ Gate=ACTIVE → 行为与 v0.4.1 完全一致

---

## ⚠️ 注意事项

1. **Gate 评估位置**：必须在 `trace = {}` 之前，确保 SUSPENDED 时能提前返回
2. **变量作用域**：`mode` 变量需要在后续代码中可用（READ_ONLY 检查）
3. **向后兼容**：保留 `self.gate_evaluator_v05`，只添加 `self.gate` 别名

---

**版本：** v0.4.2  
**最后更新：** 2025-01-12
