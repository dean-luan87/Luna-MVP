# B2 v0.4.2：Gate + tick 主循环结构图（冻结版）

**版本：** v0.4.2  
**状态：** ✅ FROZEN（不可退化形态）  
**日期：** 2025-01-12

---

## 🎯 架构定位

> **Gate 是 B2 主循环的"最高裁决者"，它只裁决【是否允许 B2 在本帧产出新判断/写回】。**  
> **Gate 不改变因子算法，不引入新能力，只控制 B2 的运行模式与写回权限。**

---

## 📊 tick() 主循环完整结构图

```
tick(frame_ts, perception, frame_id)
│
├─┐
│ │ =====================================================
│ │ v0.4.2 Gate FIRST — runtime authority
│ │ =====================================================
│ │
│ ├─ 1. 提取 Gate 输入
│ │   ├─ stability_score (从 perception 或 imu_data)
│ │   ├─ range_m (从 perception 或 self.range_m)
│ │   ├─ pitch_deg, roll_deg (从 imu_data)
│ │   └─ visibility_score (从 perception 或默认 0.75)
│ │
│ ├─ 2. Gate 评估
│ │   └─ mode, gate_trace = self.gate.evaluate(...)
│ │
│ └─ 3. Gate 裁决（三态分流）
│     │
│     ├─┐ SUSPENDED (Hard Gate Fail)
│     │ │
│     │ ├─ 权限：完全禁止 B2 产出"新结论/新建议"
│     │ ├─ 行为：tick() 立即返回 None（SILENT）
│     │ ├─ 写回：禁止 timeline / memory / health 写入
│     │ └─ trace：写入最小 trace（gate_eval + decision_state）
│     │
│     │ → return None
│     │
│     ├─┐ READ_ONLY (Soft Gate Fail)
│     │ │
│     │ ├─ 权限：允许计算（factors/impact），但禁止"写回新事实"
│     │ ├─ 行为：tick() 可返回 summary（供 C 参考），但必须标记 readonly=True
│     │ ├─ 写回：禁止 timeline / memory（可允许 health/trace 记录）
│     │ └─ 目的：证据未稳定时，允许观察但不固化，不污染世界模型
│     │
│     │ → 继续执行（但后续写回被拦截）
│     │
│     └─┐ ACTIVE (All Pass)
│       │
│       ├─ 权限：允许正常产出 + 写回（timeline/memory/health）
│       └─ 行为：tick() 正常运行
│
│       → 继续执行完整流程
│
├─┐
│ │ =====================================================
│ │ v0.4.1 系统时间唯一性
│ │ =====================================================
│ │
│ └─ system_ts = time.time()
│    trace = {}
│
├─┐
│ │ =====================================================
│ │ Meta 信息 + 时间信息
│ │ =====================================================
│ │
│ └─ trace["meta"] = {...}
│    trace["time"] = {...}
│
├─┐
│ │ =====================================================
│ │ 正常因子计算（不因 Gate 改算法）
│ │ =====================================================
│ │
│ ├─ 1. 写入未来 buffer
│ │   └─ self._append_future_state(frame_ts, perception)
│ │
│ ├─ 2. 提取未来窗口
│ │   └─ future_states = self._collect_future_window(frame_ts)
│ │
│ ├─ 3. 感知阶段
│ │   └─ evidences = build_factor_evidences(future_states)
│ │
│ ├─ 4. Evidence Lifecycle
│ │   └─ evidence_state.update(...)
│ │
│ ├─ 5. 规则评估
│ │   └─ rule_hits = self._evaluate_rules(evidences)
│ │
│ └─ 6. Impact 计算
│     └─ summary = self._summarize_world_change(evidences, frame_ts, read_only=is_read_only)
│
├─┐
│ │ =====================================================
│ │ v0.4.2 READ_ONLY 拦截（写回前）
│ │ =====================================================
│ │
│ └─ if mode == "READ_ONLY":
│      return summary  # 允许计算，不允许留下系统痕迹
│
├─┐
│ │ =====================================================
│ │ NO_OP 沉默规则（v0.4.1 已有）
│ │ =====================================================
│ │
│ └─ if impact == "NO_OP":
│      trace["decision_state"] = "SILENT"
│      trace["silence_reason"] = ...
│      return None
│
├─┐
│ │ =====================================================
│ │ 写回（仅 ACTIVE 模式）
│ │ =====================================================
│ │
│ ├─ timeline_writer.write(summary)  # 仅 ACTIVE
│ ├─ health_logger.log(...)          # 仅 ACTIVE
│ └─ memory.write(...)               # 仅 ACTIVE
│
└─┐
  │ =====================================================
  │ Trace 写入（无条件执行）
  │ =====================================================
  │
  └─ trace_writer.write(trace)  # 每帧都写
     return summary (或 None)
```

---

## 🔒 Gate 三态权限表（冻结）

| Gate 状态 | B 工作权限 | 写回权限 | 返回行为 |
|-----------|-----------|---------|---------|
| **SUSPENDED** | ❌ 完全禁止 | ❌ 禁止所有写回 | `return None` |
| **READ_ONLY** | ✅ 允许计算 | ❌ 禁止 timeline/memory | `return summary` (readonly=True) |
| **ACTIVE** | ✅ 正常工作 | ✅ 允许所有写回 | `return summary` (正常) |

---

## 🎯 Gate 裁决内容（冻结）

### ✅ Gate 裁决的 4 件事

1. **是否允许 B 工作**
   - ACTIVE / READ_ONLY / SUSPENDED

2. **是否允许写 timeline**
   - READ_ONLY / SUSPENDED 禁止

3. **是否允许写 health / memory**
   - READ_ONLY / SUSPENDED 禁止

4. **是否必须立即沉默**
   - SUSPENDED = 必须

### ❌ Gate 不裁决的内容

- ❌ impact 是什么
- ❌ factor 怎么算
- ❌ world 是否变化
- ❌ 用户该不该信

---

## 📋 关键执行顺序（不可改变）

```
1. Gate 评估（必须最先）
   ↓
2. Gate=SUSPENDED → return None
   ↓
3. trace 初始化
   ↓
4. 正常因子计算
   ↓
5. Gate=READ_ONLY → return summary（写回前拦截）
   ↓
6. NO_OP 沉默规则
   ↓
7. 写回（仅 ACTIVE）
   ↓
8. Trace 写入（无条件）
```

---

## 🔐 Non-Negotiables（不可协商）

1. **Gate 评估必须在 tick() 最顶部**
   - 在任何 factor / impact / window 计算之前

2. **Gate=SUSPENDED 必须直接 return None**
   - 不进入任何 B2 逻辑
   - 但仍写最小 trace

3. **Gate=READ_ONLY 必须拦截写回**
   - 允许计算，但不允许留下系统痕迹
   - summary 必须包含 `readonly=True`

4. **Gate=ACTIVE 仍受 NO_OP 沉默规则约束**
   - impact=NO_OP → 不写 timeline
   - 这是 v0.4.1 的规则，v0.4.2 不改

---

## 📊 数据流图

```
perception (输入)
    ↓
Gate 评估 (第一裁决)
    ↓
    ├─ SUSPENDED → return None
    ├─ READ_ONLY → 继续计算 → return summary (readonly=True)
    └─ ACTIVE → 继续计算 → 写回 → return summary
         ↓
    factors / evidences
         ↓
    summary (impact + advisory_only)
         ↓
    ┌─ NO_OP → return None (v0.4.1 规则)
    └─ 其他 → 写回 (仅 ACTIVE)
         ↓
    trace (无条件写入)
```

---

## 🎯 架构原则（冻结）

### 1. Gate 是运行许可裁决器

> Gate 决定"能不能说、怎么说"，不决定"说什么"

### 2. Gate 不改算法

> Gate 不改变因子算法、不引入新能力，只控制运行模式与写回权限

### 3. Gate 不越权

> Gate 不判断世界、不确认风险、不替 C 做决定

---

## 📝 版本演进约束

### v0.4.2 → v0.5 允许的改动

- ✅ 在 Gate 之后添加新能力（stability_score 实装、evidence 生命周期）
- ✅ 增强 Gate 输入（更精确的 stability_score 计算）
- ✅ 扩展 trace 字段（为 Web 可视化准备）

### v0.4.2 → v0.5 禁止的改动

- ❌ 改变 Gate 评估位置（必须在 tick() 最顶部）
- ❌ 改变 Gate 三态语义（SUSPENDED / READ_ONLY / ACTIVE）
- ❌ 绕过 Gate 写回（任何写回都必须经过 Gate 检查）
- ❌ 改变 Gate 裁决内容（只裁决运行权限，不裁决业务逻辑）

---

## 🔒 冻结声明

**此结构图定义了 v0.4.2 的"不可退化形态"。**

**任何未来改动都必须：**
1. 尊重 Gate 的第一裁决地位
2. 保持 Gate 三态语义不变
3. 不绕过 Gate 写回检查
4. 不改变 Gate 裁决内容

**违反以上任一原则 → 架构违规**

---

**版本：** v0.4.2  
**最后更新：** 2025-01-12  
**状态：** ✅ FROZEN（不可退化形态）
