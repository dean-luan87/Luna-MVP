# 🔧 Cursor Patch 指令：B2 v0.4.2（Gate 接入 tick 主循环）

**版本：** v0.4.2  
**状态：** 可直接丢给 Cursor 执行  
**目标：** 最小、可回滚、只接 Gate、不引入新能力

---

## 🎯 Patch 目标（不可偏离）

- **只做一件事：** 把 GateEvaluator 接入 tick() 主循环
- **Gate 成为 B 是否工作的唯一裁决者**
- **不修改 v0.4.1 的任何判定语义**
- **不引入 OCR / 多镜头 / 学习 / 新阈值**
- **所有 v0.4.1 行为回归测试必须保持通过**

---

## 🧩 Step 1：修改 b2_v03.py —— Gate-first tick 流程

### 📍 文件

`vision_pipeline/b2/v03/b2_v03.py`

---

### ✅ 1. 在 __init__ 中确认 GateEvaluator 已存在

如果没有：

```python
from vision_pipeline.b2.v03.gate_evaluator_v05 import GateEvaluator

self.gate = GateEvaluator(config_path="gate_config.yaml")
```

**不要在 GateEvaluator 内写日志 / timeline**

---

### ✅ 2. 修改 tick()：在最前面插入 Gate 裁决

**要求：Gate 必须是 tick 的第一裁决点**

在 `tick()` 的最开头插入：

```python
view_state = self._get_view_state(frame)
range_state = self._get_range_state()
evidence_state = self._evidence_state.snapshot()

gate_mode, gate_reason, gate_eval = self.gate.evaluate(
    view_state=view_state,
    range_state=range_state,
    evidence_state=evidence_state,
)

# 写入 runtime trace（每一帧都必须写）
self.runtime_trace["gate_eval"] = gate_eval

# Gate 强裁决
if gate_mode == "SUSPENDED":
    return None

read_only = (gate_mode == "READ_ONLY")
```

---

### ✅ 3. 保持 perception / aggregation 不变

**不要修改以下内容的内部逻辑：**
- `_perceive`
- `_aggregate`
- `_summarize_world_change`

**只在调用时传入 read_only：**

```python
summary = self._summarize_world_change(
    evidences,
    ts_now,
    read_only=read_only
)
```

---

### ✅ 4. Gate=READ_ONLY 时禁止对外输出

在 decision emit 前插入防护：

```python
if read_only:
    return None
```

---

## 🧩 Step 2：timeline 写入点加 Gate 防护

### 📍 文件

`vision_pipeline/b2/v03/b2_v03.py`

找到 timeline 写入的位置（`timeline_writer.write` 或等价逻辑）

在写入前增加：

```python
if gate_mode != "ACTIVE":
    return
```

**规则：**
Gate ≠ ACTIVE → 不允许写 timeline

---

## 🧩 Step 3：Health Log 增强（必须可追溯）

### 📍 文件

`vision_pipeline/b2/v03/b2_health_logger.py`

在 `B2HealthEvent` 中新增字段：

```python
gate_mode: str
gate_blocked_by: Optional[str]
```

在记录 health event 时写入：

```python
gate_mode=gate_mode,
gate_blocked_by=gate_eval.get("blocked_by"),
```

**目的：**

线上事故必须能回答：
**"B 当时为什么没提醒？"**

---

## 🧩 Step 4：Runtime Trace Schema 对齐

### 📍 文件

`runtime_trace_schema_v05.md`（或对应 schema）

确认并补齐字段：

```json
"gate_eval": {
  "gate_mode": "ACTIVE | READ_ONLY | SUSPENDED",
  "blocked_by": "camera_shake | too_close | insufficient_evidence | null",
  "human_readable": "string"
}
```

---

## 🧩 Step 5：新增最小测试（不改旧测试）

### 📍 新文件

`tests/test_b2_v042_gate_in_tick.py`

**测试断言必须包含：**
- Gate=SUSPENDED → tick() 返回 None
- Gate=READ_ONLY → 无 timeline 写入
- Gate=ACTIVE → 行为与 v0.4.1 完全一致
- ENV 不触发 decision
- impact=NO_OP 不写 timeline

---

## ❌ 明确禁止事项（Cursor 必须遵守）

- ❌ **不得修改 impact 判定逻辑**
- ❌ **不得新增任何阈值**
- ❌ **不得把 Gate 写进 world / summarize**
- ❌ **不得让 Gate 直接影响 decision 内容**
- ❌ **不得输出任何确认性风险语句**

---

## ✅ Patch 完成判定标准（自动验收）

Patch 完成后，必须满足：

- ✅ v0.4.1 行为回归测试 100% 通过
- ✅ 新 Gate 测试 全部通过
- ✅ Gate=SUSPENDED 时：
  - 无 decision
  - 无 timeline
  - 有 trace
- ✅ 所有"不提醒"的情况都能在 trace 中解释清楚

---

## 📌 Patch 结束语（给 Cursor）

**这是 v0.4.2 的最小接入 Patch。**

**不要做任何"优化""顺手重构""顺便增强"。**

**只做 Gate 接入与裁决权下沉。**

---

**版本：** v0.4.2  
**最后更新：** 2025-01-12  
**状态：** ✅ 可直接丢给 Cursor 执行
