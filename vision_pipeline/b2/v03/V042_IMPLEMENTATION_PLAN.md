# B2 v0.4.2 实装方案

**版本：** v0.4.2  
**目标：** 将 Gate 正式接入 tick() 主循环  
**原则：** Gate 是最高裁判，永远高于 B 的任何判断

---

## ✅ 确认

**Gate 的裁决权是否"永远高于 B 的任何判断"？**

**答案：** ✅ **是，Gate 是最高裁判**

---

## 🎯 设计边界

### 本版本只允许做的事

- ✅ GateEvaluator 接入 tick()
- ✅ Gate 结果写入 Runtime Trace
- ✅ Gate 决定 ACTIVE / READ_ONLY / SUSPENDED
- ✅ Gate 对输出是否产生有绝对裁决权

### 本版本明确禁止

- ❌ 改 impact 语义
- ❌ 改 advisory_only / intervention_level
- ❌ 引入 OCR / 新感知
- ❌ 学习 / 进化 / 自适应
- ❌ 改 B/C 边界

---

## 📋 tick() 新结构（v0.4.2 标准）

### 原则

**Gate 在最前面，任何逻辑都不能绕过它。**

### 新 tick() 执行顺序（定死）

```
tick(frame):
 ├─ 0. build_tick_context()          # 构建上下文
 ├─ 1. gate_evaluator.evaluate()    ← 新增（最高优先级）
 │    ├─ ACTIVE
 │    ├─ READ_ONLY
 │    └─ SUSPENDED
 ├─ 2. write_gate_trace()            ← 无论如何都写
 ├─ 3. if SUSPENDED: return None     ← 直接结束
 ├─ 4. perception_step()             # 感知
 ├─ 5. evidence_update()              # 证据更新
 ├─ 6. world_change_aggregation()     # 世界变化聚合
 ├─ 7. decision & impact evaluation  # 决策和影响评估
 ├─ 8. if READ_ONLY: downgrade / no writeback  # READ_ONLY 处理
 ├─ 9. timeline / health / memory write  # 写入
 └─ 10. return advisory message (or None)  # 返回
```

**这条顺序是 v0.4.x 的"宪法"。**

---

## 🔒 Gate 在 tick() 中的"三权"

### 1️⃣ 生杀权（是否允许 B 工作）

```python
if gate_mode == "SUSPENDED":
    trace["to_c_message"] = {
        "sent": False,
        "reason": "gate_suspended"
    }
    return None
```

- ✅ SUSPENDED = 绝对沉默
- ✅ 不感知、不聚合、不决策
- ✅ 但 trace 一定要写

---

### 2️⃣ 降权权（READ_ONLY）

**READ_ONLY ≠ 不工作，而是：**

- ✅ **允许：**
  - 感知
  - 证据积累
- ❌ **禁止：**
  - 提升 impact 等级
  - 写 timeline
  - 写 memory（可选）

**实现原则：**

```python
if gate_mode == "READ_ONLY":
    decision["write_timeline"] = False
    decision["intervention_level"] = "SOFT"
```

**READ_ONLY 是"观察但不发声"。**

---

### 3️⃣ 可视权（必须写入 trace）

**无论 Gate 结果是什么，每一帧必须写：**

```json
"gate": {
  "mode": "SUSPENDED",
  "blocked_by": "camera_shake",
  "stability_score": 0.34,
  "human_readable": "镜头晃动过大，B暂停工作"
}
```

**这是你后面所有 Debug / 审判 / DCS 的根。**

---

## 📝 GateEvaluator 接入点

### 新增 / 使用文件

- ✅ `gate_evaluator_v05.py`（已有）
- ✅ `gate_config.yaml`（已冻结）

### 修改点（最小）

#### 1️⃣ b2_v03.py - tick() 方法

在 tick() 最开始：

```python
# =========================
# v0.4.2: Gate 作为第一裁判（最高优先级）
# =========================
# 1. 计算 view_state（用于 Gate 评估）
stability_score = compute_stability_score(...)
view_state = compute_view_state(...)

# 2. Gate 评估（在任何感知之前）
gate_mode, gate_trace = self.gate_evaluator_v05.evaluate(
    stability_score=stability_score,
    pitch_deg=view_state.get("pitch_deg", 0.0),
    roll_deg=view_state.get("roll_deg", 0.0),
    range_m=self.range_m or 10.0,
    visibility_score=view_state.get("visibility_score", 0.75),
    allow_runtime=True,  # 默认允许
    evidence_frames=0,  # 初始为 0，后续更新
    final_confidence=0.0,  # 初始为 0，后续更新
    now_ts=system_ts
)

# 3. 写入 Gate trace（无论如何都写）
trace["gate_eval"] = {
    "mode": gate_mode,
    "blocked_by": gate_trace.get("blocked_by"),
    "details": gate_trace.get("details", {}),
    "human_readable": gate_trace.get("human_readable", ""),
    "stability_score": stability_score
}

# 4. Gate=SUSPENDED → 直接返回 None
if gate_mode == "SUSPENDED":
    trace["decision_state"] = "SUSPENDED"
    trace["to_c_message"] = {"sent": False, "reason": "gate_suspended"}
    trace["writeback"] = {
        "timeline_written": False,
        "health_log_written": False,
        "memory_written": False
    }
    if self.trace_writer:
        self.trace_writer.write(trace)
    return None
```

---

## ✅ v0.4.2 的验收标准

**必须全部满足，否则 ❌**

- ✅ Gate=SUSPENDED → B 返回 None
- ✅ Gate=SUSPENDED → trace 有 gate 记录
- ✅ Gate=READ_ONLY → impact 不升级
- ✅ Gate=READ_ONLY → timeline 不写
- ✅ Gate=ACTIVE → 行为与 v0.4.1 完全一致
- ✅ 任一帧 trace 中必有 gate 字段

---

## 🔧 实施步骤

1. **初始化 GateEvaluatorV05**
   - 在 `__init__` 中初始化 `self.gate_evaluator_v05`

2. **重构 tick() 方法**
   - Gate 评估移到最前面
   - 在任何感知之前执行

3. **实现 Gate 三权**
   - 生杀权：SUSPENDED → return None
   - 降权权：READ_ONLY → 不写 timeline
   - 可视权：每帧写 gate trace

4. **补充回归测试**
   - 测试 Gate 三权
   - 测试 Gate trace 完整性

---

**版本：** v0.4.2  
**状态：** 📋 实施计划已就绪
