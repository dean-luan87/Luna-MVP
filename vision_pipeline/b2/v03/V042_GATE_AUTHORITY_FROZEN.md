# Gate Authority Table — B2 v0.4.2 (Frozen)

**版本：** v0.4.2  
**状态：** ✅ 已冻结  
**日期：** 2025-01-12

---

## ✅ 已完成的改动

### 1. Gate Authority Table 已添加到代码注释

- ✅ `gate_evaluator_v05.py` 顶部（完整版本）
- ✅ `b2_v03.py` 的 `tick()` 方法 docstring（简化版本）

### 2. Gate 集成状态检查

**当前实现：**
- ✅ Gate 已在 `tick()` 最开始评估
- ✅ SUSPENDED 时返回 None
- ✅ READ_ONLY 时禁止 timeline 和 B→C message
- ✅ view_state 缺失时降级为 READ_ONLY

---

## 📋 Gate Authority Table（完整版）

### Gate 决策维度（只此四项）

1. 是否允许 B 输出（can_trigger）
2. B 的运行模式（ACTIVE / READ_ONLY / SUSPENDED）
3. 是否允许写入 timeline / trace
4. 是否允许向 C 发送 advisory

### Gate Mode 权限表

**[ACTIVE]**
- B 可以计算 impact
- B 可以输出 advisory（advisory_only = True）
- B 可以写 timeline / trace
- B 不得确认风险（禁止 certainty 语义）
- B 不得覆盖 C 的即时判断

**[READ_ONLY]**
- B 可以计算 impact（用于内部观察）
- B **不得**向 C 发送 advisory
- B **不得**写 timeline
- B **只允许**写 trace（用于审计）
- 用途：证据未稳定、视角不充分

**[SUSPENDED]**
- B **不得**计算 impact
- B **不得**输出任何 decision
- B **不得**写 timeline
- B **只写** gate trace（说明为什么沉默）
- 用途：视角污染 / 距离过近 / 严重不可信

### Gate 绝对裁决项（任何情况下优先）

- `camera_shake` → SUSPENDED
- `too_close` (进入 C 主导) → SUSPENDED
- `missing_view_state` → READ_ONLY（v0.4.2 起）
- `insufficient_evidence` → READ_ONLY

### 禁止事项（一旦出现 = 架构错误）

- Gate = SUSPENDED 但仍有 B 输出
- Gate = READ_ONLY 但写 timeline
- Gate 未 ACTIVE 却向 C 发送 advisory
- 没有 view_state 却 ACTIVE
- B 输出"确认性风险结论"

---

## 🎯 这个 patch 带来的确定性结果

- ✅ Gate 永远先于 B 决策
- ✅ 没有 view_state → 不可能 ACTIVE
- ✅ SUSPENDED / READ_ONLY 永远不会污染 timeline
- ✅ v0.4.1 的 30 个 RED 根因被结构性封死
- ✅ v0.5 可以在此基础上安全进化

---

## 📋 后续版本规则

**这张表可以原封不动贴进代码注释**

**后续版本只允许：**
- ✅ 新增 Gate Mode（如果有新的运行状态）
- ✅ 新增裁决项（如果有新的前提条件）

**不允许：**
- ❌ 修改已有语义
- ❌ 降低 Gate 的裁决权
- ❌ 允许在 SUSPENDED / READ_ONLY 时输出

---

**版本：** v0.4.2  
**最后更新：** 2025-01-12  
**状态：** ✅ 已冻结
