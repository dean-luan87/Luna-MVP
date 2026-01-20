# B2 v0.4.2：Gate 接入 tick 主循环顺序图（工程对齐版）

**版本：** v0.4.2  
**状态：** FROZEN（实现级语义顺序）  
**用途：** 可直接对照代码逐行落地

---

## 🎯 核心原则

> **先裁决"有没有资格看世界"，再谈"看到了什么"**

---

## 0️⃣ Tick 入口（系统时间锚点）

```python
tick(frame, ts_now)
```

### 强约束

- **ts_now = 系统当前时间（BC 唯一时间标尺）**
- **禁止使用缓存时间 / 帧时间做裁决**

---

## 1️⃣ Gate 评估（最高优先级，必须先执行）

```python
gate_result = Gate.evaluate(
    view_state, 
    range_state, 
    evidence_state
)
```

### Gate 输入

- **view_state**
  - `stability_score`
  - `camera_motion`
  - `camera_pose`
  - `fov_state`
- **range_state**
  - `min_distance`
  - `effective_range`
- **evidence_state**
  - 连续性 / 冷却 / 稳定度

### Gate 输出（必须写 trace）

```json
{
  "gate_mode": "ACTIVE | READ_ONLY | SUSPENDED",
  "blocked_by": "...",
  "human_readable": "..."
}
```

---

## 2️⃣ Gate Mode 分流（硬分支，不可合并）

### ⛔ SUSPENDED

```
- perception: ❌ 不执行
- aggregation: ❌ 不执行
- decision: ❌ 不生成
- output to C: ❌
- timeline: ❌
- trace: ✅（必须）
→ return None
```

**含义：** 当前视角不配看世界

---

### 👁 READ_ONLY

```
- perception: ✅（可执行）
- aggregation: ✅（仅内部）
- decision: ⚠️ 可生成
- output to C: ❌
- timeline: ❌
- memory: ⚠️（只读复用）
- trace: ✅
```

**含义：** 可以看，但不许说

---

### ▶️ ACTIVE

```
→ 进入完整 B2 流程
```

---

## 3️⃣ Perception（仅 ACTIVE / READ_ONLY）

```python
perception = perceive(frame)
```

### 规则

- **只产出 raw evidence**
- **不允许语义判断**
- **不允许 risk 结论**

---

## 4️⃣ Evidence Lifecycle（抗视角污染）

```python
evidence_state.update(perception)
```

### 状态机

```
OBSERVING → CONFIRMED → DEGRADED → DROPPED
```

### Gate 可强制

- **卡在 OBSERVING**
- **从 CONFIRMED 降级**

---

## 5️⃣ Impact 评估（仅 ACTIVE / READ_ONLY）

```python
impact = summarize_world_change(evidences)
```

### 硬约束

**只回答一句话：**
> **👉「如果继续前进，可能会发生什么」**

**禁止确认性语义**

### 允许的 impact

- `NEED_SLOW_DOWN`
- `PATH_UNCERTAIN`
- `NEED_STOP`
- `NO_OP`

---

## 6️⃣ Intervention 裁决（Gate 参与）

```python
intervention = {
    "level": "HARD | SOFT",
    "advisory_only": True
}
```

### 规则

- **Gate 可降级 HARD → SOFT**
- **Gate 不可升级**
- **advisory_only = True 永久为真**

---

## 7️⃣ Output 分流（关键）

### `impact == NO_OP`

```
- 不写 timeline
- 不发给 C
- 只写 trace
```

### `Gate == READ_ONLY`

```
- 不发给 C
- 不写 timeline
- trace + 内部日志
```

### `Gate == ACTIVE && impact ≠ NO_OP`

```
- 发给 C（advisory）
- 写 timeline
- 写 health log
- 写 trace
```

---

## 8️⃣ Trace（无条件执行）

**每一帧必须有 trace**

### 最低字段

```json
{
  "time": ts_now,
  "gate_mode": "...",
  "impact": "...",
  "intervention_level": "...",
  "advisory_only": true,
  "human_interpretation": "..."
}
```

---

## 📋 一句话总结（写进 README / 代码注释）

```
Gate decides whether B may speak.
B suggests possible future risks.
C verifies reality and decides action.
```

**中文版：**
```
Gate 决定 B 是否能说话。
B 提醒可能的未来风险。
C 核验现实并决定行动。
```

---

## 🔄 完整流程图（文字版）

```
tick(frame, ts_now)
  │
  ├─ 0. 系统时间锚点（ts_now）
  │
  ├─ 1. Gate 评估（最高优先级）
  │   └─ gate_result = Gate.evaluate(...)
  │
  ├─ 2. Gate Mode 分流
  │   ├─ SUSPENDED → return None（只写 trace）
  │   ├─ READ_ONLY → 继续（但不输出）
  │   └─ ACTIVE → 继续完整流程
  │
  ├─ 3. Perception（仅 ACTIVE / READ_ONLY）
  │   └─ perception = perceive(frame)
  │
  ├─ 4. Evidence Lifecycle
  │   └─ evidence_state.update(perception)
  │
  ├─ 5. Impact 评估
  │   └─ impact = summarize_world_change(evidences)
  │
  ├─ 6. Intervention 裁决
  │   └─ intervention = {level, advisory_only}
  │
  ├─ 7. Output 分流
  │   ├─ NO_OP → 只写 trace
  │   ├─ READ_ONLY → trace + 内部日志
  │   └─ ACTIVE + impact → 完整输出
  │
  └─ 8. Trace（无条件执行）
      └─ 每帧必须有 trace
```

---

## ✅ 实现检查清单

### Gate 评估位置

- [ ] Gate 评估是否在 tick() 最前面？
- [ ] Gate 输入是否包含 view_state / range_state / evidence_state？
- [ ] Gate 输出是否写入 trace？

### Gate Mode 分流

- [ ] SUSPENDED 是否直接 return None？
- [ ] SUSPENDED 是否仍写 trace？
- [ ] READ_ONLY 是否不写 timeline？
- [ ] READ_ONLY 是否不发给 C？
- [ ] ACTIVE 是否进入完整流程？

### Perception & Evidence

- [ ] Perception 是否只产出 raw evidence？
- [ ] Evidence 状态机是否正确实现？
- [ ] Gate 是否可强制证据状态？

### Impact & Intervention

- [ ] Impact 是否只回答"如果继续前进，可能会发生什么"？
- [ ] 是否禁止确认性语义？
- [ ] Gate 是否可降级 HARD → SOFT？
- [ ] advisory_only 是否永久为 True？

### Output & Trace

- [ ] NO_OP 是否不写 timeline？
- [ ] READ_ONLY 是否不发给 C？
- [ ] 每帧是否都有 trace？
- [ ] Trace 是否包含最低字段？

---

**版本：** v0.4.2  
**最后更新：** 2025-01-12  
**状态：** ✅ FROZEN（实现级语义顺序）
