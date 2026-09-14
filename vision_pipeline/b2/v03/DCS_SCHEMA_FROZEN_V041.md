# DCS × Web 仪表盘 Schema（Frozen v0.4.1）

**状态：** FROZEN（不可随意修改）  
**修改本文件 = 架构变更，需单独评审**

**用途：**
- 系统级观察
- 架构越权审判
- 历史回放与事故复盘
- 不对用户暴露

---

## ⚠️ 冻结声明（必须写进 Cursor）

> **This document defines the frozen schema for DCS and its Web Dashboard.**
> 
> **Any modification must be reviewed as an architecture-level change.**
> 
> **No runtime logic should depend on DCS outputs.**
> 
> **DCS is strictly observational and retrospective.**

---

## 一、DCS 的定位（先定性，防走样）

### DCS 是什么

- **Decision Consistency System**
- 是一个 "事后审判 + 持续监察"系统
- 不参与实时决策
- 不影响 B / C 主链路

### DCS 不是什么

- ❌ 不是风控
- ❌ 不是学习模块
- ❌ 不是产品功能
- ❌ 不做任何在线干预

---

## 二、DCS 输入 Schema（Decision 审判单元）

### 每一条 B / C 决策，都可以被 DCS 单独审判

#### 1️⃣ DecisionRecord（最小审判单元）

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

### Schema 字段说明

| 字段路径 | 类型 | 说明 | 必填 |
|---------|------|------|------|
| `meta.version` | string | 版本号（v0.4.1） | ✅ |
| `meta.module` | string | 模块标识（"B" 或 "C"） | ✅ |
| `meta.ts` | float | 系统时间戳（秒） | ✅ |
| `meta.frame_id` | int | 帧编号 | ✅ |
| `meta.human_time` | string | 人类可读时间（MM:SS） | ✅ |
| `decision.impact` | string | 行为影响枚举 | ✅ |
| `decision.decision_level` | string | 决策级别 | ✅ |
| `decision.main_factor` | string | 主因子类型 | ⚠️ |
| `gate_state.mode` | string | Gate 状态 | ✅ |
| `gate_state.blocked_by` | string | 阻止原因 | ⚠️ |
| `gate_state.stability_score` | float | 稳定性分数（0.0-1.0） | ✅ |
| `view_state.camera_motion` | string | 相机运动状态 | ✅ |
| `view_state.camera_pose` | string | 相机姿态状态 | ✅ |
| `view_state.fov_state` | string | 视野状态 | ✅ |
| `trace_explain.trigger_reason` | string | 触发原因 | ✅ |
| `trace_explain.rule_path` | array | 规则路径 | ✅ |
| `trace_explain.human_interpretation` | string | 人类可读解释 | ✅ |

---

## 三、DCS 输出 Schema（审判结果）

#### 2️⃣ DCSJudgement

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

### Schema 字段说明

| 字段路径 | 类型 | 说明 | 必填 |
|---------|------|------|------|
| `dcs_judgement.level` | string | 判定级别（GREEN/YELLOW/RED） | ✅ |
| `dcs_judgement.violated_rules` | array | 违规规则列表 | ✅ |
| `dcs_judgement.reason` | string | 违规原因（人类可读） | ✅ |
| `dcs_judgement.confidence` | float | 判定置信度（0.0-1.0） | ✅ |
| `dcs_judgement.score` | int | DCS 分数（0-100） | ✅ |

---

## 四、DCS 硬判定规则（冻结）

### 🟥 RED（硬违规，必须修）

| 编号 | 判定条件 | 扣分 |
|------|---------|------|
| **DCS-R1** | B 输出确认性风险结论 | -20 |
| **DCS-R2** | B 替 C 完成风险核验 | -20 |
| **DCS-R3** | Gate = SUSPENDED 仍输出非 NO_OP | -20 |
| **DCS-R4** | B 在 ≤3m 或室内主导决策 | -20 |
| **DCS-R5** | 使用非系统当前时间 | -20 |

**➡ 出现任一条：版本判定不合格**

---

### 🟨 YELLOW（设计风险，需关注）

| 编号 | 判定条件 | 扣分 |
|------|---------|------|
| **DCS-Y1** | 高频唤醒但长期无有效 impact | -5 |
| **DCS-Y2** | 世界模型长期只读且无记忆更新 | -5 |
| **DCS-Y3** | C 长期过度保守影响体验 | -5 |

---

### 🟩 GREEN（符合设计）

| 编号 | 判定条件 | 加分 |
|------|---------|------|
| **DCS-G1** | 仅条件式风险预警 | +0（通过） |
| **DCS-G2** | C 完成靠近核验并回写 | +0（通过） |
| **DCS-G3** | 熟悉场景 B 自动降权 | +0（通过） |
| **DCS-G4** | 时间 / 距离标尺一致 | +0（通过） |

**➡ 失败扣 -10 分**

---

## 五、Web 仪表盘 Schema（只读）

### 不写代码，只定义结构

#### 页面结构（逻辑层）

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

#### Timeline Marker Schema

```json
{
  "ts": 300.02,
  "frame_id": 8997,
  "color": "RED | YELLOW | GREEN",
  "impact": "NEED_STOP",
  "rule_hit": ["DCS-R3"]
}
```

### Schema 字段说明

| 字段 | 类型 | 说明 | 必填 |
|------|------|------|------|
| `ts` | float | 系统时间戳（秒） | ✅ |
| `frame_id` | int | 帧编号 | ✅ |
| `color` | string | 颜色标识（RED/YELLOW/GREEN） | ✅ |
| `impact` | string | 行为影响 | ✅ |
| `rule_hit` | array | 触发的规则列表 | ✅ |

---

#### GlobalHealth Schema

```json
{
  "overall_status": "RED | YELLOW | GREEN",
  "dcs_score": 85,
  "summary_counts": {
    "total_decisions": 145,
    "red_count": 0,
    "yellow_count": 2,
    "green_count": 143
  },
  "time_range": {
    "start": 0.0,
    "end": 402.5
  }
}
```

---

#### ViolationStats Schema

```json
{
  "red_count": 0,
  "yellow_count": 2,
  "rule_distribution": [
    {
      "rule_id": "DCS-R1",
      "count": 0,
      "level": "RED"
    },
    {
      "rule_id": "DCS-Y1",
      "count": 2,
      "level": "YELLOW"
    }
  ]
}
```

---

#### DecisionDrilldown Schema

```json
{
  "decision_record": {
    // DecisionRecord 完整结构
  },
  "dcs_judgement": {
    // DCSJudgement 完整结构
  },
  "rule_explanation": {
    "rule_id": "DCS-R3",
    "description": "Gate = SUSPENDED 仍输出非 NO_OP",
    "evidence": {
      "gate_state": "SUSPENDED",
      "impact": "NEED_STOP"
    },
    "suggested_fix": "Gate SUSPENDED 时 B 必须返回 None"
  }
}
```

---

## 六、评分规则（冻结）

### 初始分数：100 分

### 扣分规则

- **RED 违规：** 每个 -20 分
- **YELLOW 风险：** 每个 -5 分
- **GREEN 失败：** 每个 -10 分

### 判定标准

- **≥ 85 分：** 合格（GREEN）
- **70-84 分：** 警告（YELLOW）
- **< 70 分：** 不合格（RED）

---

## 七、最终裁定（非常重要）

### 从这一刻起：

- 所有"B 是否越权"的争论
- 所有"C 是否被误导"的讨论
- 所有"为什么当时这么判断"的复盘

**都必须回到 DCS + 仪表盘 Schema 上来。**

### 这一步完成，意味着：

- ✅ **架构边界 已经封死**
- ✅ **学习系统 未来才有资格接管**
- ✅ **出问题 一定能被抓出来**

---

## 八、使用约束（必须遵守）

### 1. Schema 不可随意修改

- 任何修改必须经过架构评审
- 修改必须记录变更原因
- 修改必须更新版本号

### 2. DCS 不参与实时决策

- DCS 输出不得影响 B / C 主链路
- DCS 不得修改任何运行时状态
- DCS 只做观察和记录

### 3. Web 仪表盘只读

- 仪表盘不得修改任何数据
- 仪表盘不得触发任何操作
- 仪表盘只做展示和查询

---

## 九、版本历史

| 版本 | 日期 | 变更说明 |
|------|------|---------|
| v0.4.1 | 2025-01-12 | 初始冻结版本 |

---

## 十、相关文档

- `dcs_hard_rules_v041.py` - DCS 硬判定项实现
- `dcs_hard_rules_v041.md` - DCS 硬判定项规则说明
- `dcs_web_dashboard_schema.md` - Web 仪表盘详细 Schema
- `dcs_history_audit_v01_v03.md` - DCS 回审历史版本

---

**版本：** v0.4.1（FROZEN）  
**最后更新：** 2025-01-12  
**状态：** ✅ **已冻结，后续所有工程、审计、可视化都必须服从此 Schema 基线**

---

## ⚠️ 再次强调冻结声明

> **This document defines the frozen schema for DCS and its Web Dashboard.**
> 
> **Any modification must be reviewed as an architecture-level change.**
> 
> **No runtime logic should depend on DCS outputs.**
> 
> **DCS is strictly observational and retrospective.**
