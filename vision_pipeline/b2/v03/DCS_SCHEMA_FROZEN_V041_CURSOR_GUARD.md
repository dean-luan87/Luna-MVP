# Cursor Guard: DCS Schema Frozen v0.4.1

**用途：** Cursor 只读 Guard 文档  
**状态：** FROZEN（不可随意修改）

---

## ⚠️ 冻结声明

> **This document defines the frozen schema for DCS and its Web Dashboard.**
> 
> **Any modification must be reviewed as an architecture-level change.**
> 
> **No runtime logic should depend on DCS outputs.**
> 
> **DCS is strictly observational and retrospective.**

---

## 🎯 核心约束（Cursor 必须遵守）

### 1. Schema 不可随意修改

**规则：**
- 任何修改必须经过架构评审
- 修改必须记录变更原因
- 修改必须更新版本号

**Cursor 检查点：**
- 如果修改 `DCS_SCHEMA_FROZEN_V041.md`，必须：
  1. 说明变更原因
  2. 更新版本号
  3. 记录变更历史

---

### 2. DCS 不参与实时决策

**规则：**
- DCS 输出不得影响 B / C 主链路
- DCS 不得修改任何运行时状态
- DCS 只做观察和记录

**Cursor 检查点：**
- 如果代码中 DCS 输出被用于决策逻辑 → ❌ 拒绝
- 如果 DCS 修改运行时状态 → ❌ 拒绝
- 如果 DCS 触发任何操作 → ❌ 拒绝

---

### 3. Web 仪表盘只读

**规则：**
- 仪表盘不得修改任何数据
- 仪表盘不得触发任何操作
- 仪表盘只做展示和查询

**Cursor 检查点：**
- 如果仪表盘有写操作 → ❌ 拒绝
- 如果仪表盘触发任何操作 → ❌ 拒绝

---

## 📋 Schema 核心结构（快速参考）

### DecisionRecord（最小审判单元）

```json
{
  "meta": {
    "version": "v0.4.1",
    "module": "B | C",
    "ts": 300.02,
    "frame_id": 8997,
    "human_time": "05:00"
  },
  "decision": {
    "impact": "NO_OP | NEED_SLOW_DOWN | PATH_UNCERTAIN | NEED_DETOUR | NEED_STOP",
    "decision_level": "NOTICE | CONDITION_CHANGE | INTERRUPT",
    "main_factor": "path | event | people | null"
  },
  "gate_state": {
    "mode": "ACTIVE | READ_ONLY | SUSPENDED",
    "blocked_by": "camera_shake | angle_invalid | range_invalid | none",
    "stability_score": 0.82
  },
  "view_state": {
    "camera_motion": "LOW | MEDIUM | HIGH",
    "camera_pose": "STABLE | TILTED | UNKNOWN",
    "fov_state": "NORMAL | ZOOMED | UNKNOWN"
  },
  "trace_explain": {
    "trigger_reason": "why B/C triggered",
    "rule_path": ["RULE-B1", "RULE-B3"],
    "human_interpretation": "条件风险预警，不构成确认"
  }
}
```

### DCSJudgement（审判结果）

```json
{
  "dcs_judgement": {
    "level": "GREEN | YELLOW | RED",
    "violated_rules": ["DCS-R1", "DCS-R3"],
    "reason": "视角不稳定但仍输出 NEED_STOP",
    "confidence": 0.94,
    "score": 80
  }
}
```

---

## 🔍 DCS 硬判定规则（快速参考）

### 🟥 RED（硬违规，必须修）

- **DCS-R1:** B 输出确认性风险结论
- **DCS-R2:** B 替 C 完成风险核验
- **DCS-R3:** Gate = SUSPENDED 仍输出非 NO_OP
- **DCS-R4:** B 在 ≤3m 或室内主导决策
- **DCS-R5:** 使用非系统当前时间

### 🟨 YELLOW（设计风险，需关注）

- **DCS-Y1:** 高频唤醒但长期无有效 impact
- **DCS-Y2:** 世界模型长期只读且无记忆更新
- **DCS-Y3:** C 长期过度保守影响体验

### 🟩 GREEN（符合设计）

- **DCS-G1:** 仅条件式风险预警
- **DCS-G2:** C 完成靠近核验并回写
- **DCS-G3:** 熟悉场景 B 自动降权
- **DCS-G4:** 时间 / 距离标尺一致

---

## 📊 Web 仪表盘结构（快速参考）

```
Dashboard
├─ GlobalHealth
│   ├─ overall_status (RED | YELLOW | GREEN)
│   └─ summary_counts
│
├─ TimelineView
│   ├─ time_axis
│   ├─ decision_markers[]
│   └─ gate_markers[]
│
├─ ViolationStats
│   ├─ red_count
│   ├─ yellow_count
│   └─ rule_distribution[]
│
└─ DecisionDrilldown
    ├─ DecisionRecord
    ├─ DCSJudgement
    └─ RuleExplanation
```

---

## ✅ Cursor 检查清单

### 修改 DCS 相关代码时

- [ ] 是否修改了 Schema 结构？
  - 如果是，是否经过架构评审？
- [ ] DCS 输出是否被用于决策逻辑？
  - 如果是，❌ 拒绝
- [ ] DCS 是否修改运行时状态？
  - 如果是，❌ 拒绝
- [ ] 仪表盘是否有写操作？
  - 如果是，❌ 拒绝

### 实现 DCS 功能时

- [ ] 是否遵循 DecisionRecord Schema？
- [ ] 是否遵循 DCSJudgement Schema？
- [ ] 是否遵循硬判定规则？
- [ ] 是否遵循评分规则？

---

## 📌 最终裁定

### 从这一刻起：

- 所有"B 是否越权"的争论 → 回到 DCS Schema
- 所有"C 是否被误导"的讨论 → 回到 DCS Schema
- 所有"为什么当时这么判断"的复盘 → 回到 DCS Schema

### 这一步完成，意味着：

- ✅ **架构边界 已经封死**
- ✅ **学习系统 未来才有资格接管**
- ✅ **出问题 一定能被抓出来**

---

**版本：** v0.4.1（FROZEN）  
**最后更新：** 2025-01-12  
**状态：** ✅ **已冻结，Cursor 必须遵守此 Schema 基线**
