# Gate Authority Table

**B2 Runtime Gate – 权限裁决总表（v0.4.2+）**

**版本：** v0.4.2  
**状态：** FROZEN（架构护栏）  
**位置：** 架构文档

---

## 🎯 Gate 的唯一职责

> **Gate 决定 B 是否有资格在当前时刻发声，以及只能以什么姿态发声**
> 
> **Gate 不判断世界，不确认风险，不替 C 做决定。**

---

## Ⅰ. 运行级裁决（Run-Level Authority）

| 裁决项 | Gate 可否裁决 | 影响范围 | 说明 |
|--------|--------------|---------|------|
| B 是否运行 | ✅ 是 | 整个 B 模块 | 决定 B 是否 ACTIVE |
| B 是否只读 | ✅ 是 | 禁止输出 | READ_ONLY |
| B 是否完全沉默 | ✅ 是 | 禁止一切 | SUSPENDED |
| perception 是否执行 | ✅ 是 | 上游感知 | 可被 Gate 直接阻断 |
| aggregation 是否执行 | ✅ 是 | 中游逻辑 | 仅 ACTIVE 执行 |

### 裁决结果枚举

- **ACTIVE** - B 正常工作
- **READ_ONLY** - B 只读运行（不产生新判断）
- **SUSPENDED** - B 暂停（视角或条件不可信）

---

## Ⅱ. 输出级裁决（Output Authority）

| 裁决项 | Gate 可否裁决 | 说明 |
|--------|--------------|------|
| 是否允许向 C 输出 | ✅ 是 | Gate=SUSPENDED 时必须为否 |
| 是否允许写 timeline | ✅ 是 | NO_OP / READ_ONLY 时禁止 |
| 是否允许写 memory | ✅ 是 | 不稳定阶段禁止 |
| 是否允许生成 decision | ✅ 是 | READ_ONLY 可生成但不可发声 |

### ⚠️ 注意

**Gate 阻断 ≠ impact = NO_OP**

**Gate 阻断 = 禁止表达判断**

---

## Ⅲ. 行为姿态裁决（Intervention Authority）

| 裁决项 | Gate 权限 | 说明 |
|--------|----------|------|
| intervention_level | ✅ 可限制 | HARD / SOFT |
| 是否允许 HARD 干预 | ✅ 是 | 远距 + 稳定时才允许 |
| 是否强制降级为 SOFT | ✅ 是 | 视角不稳 / 证据不足 |
| advisory_only | ✅ 强制为 True | B 永远是提醒者 |

### 📌 硬规则

- **Gate 可以降级干预**
- **Gate 不能升级干预**

---

## Ⅳ. 时间 / 预测裁决（Temporal Authority）

| 裁决项 | Gate 权限 | 说明 |
|--------|----------|------|
| 是否允许未来风险措辞 | ✅ 是 | "可能会发生" |
| 是否允许确认性预测 | ❌ 禁止 | "一定会发生" |
| 是否允许跨时间断言 | ✅ 限制 | 必须加不确定性 |

### 👉 防越权预测的核心防线

---

## Ⅴ. 证据生命周期裁决（Evidence Authority）

| 裁决项 | Gate 权限 | 说明 |
|--------|----------|------|
| evidence 是否可进入 CONFIRMED | ✅ 是 | 依赖视角稳定 |
| 是否强制停留在 OBSERVING | ✅ 是 | 抗视角污染 |
| 是否降级为 DEGRADED | ✅ 是 | 抖动/遮挡 |
| 是否允许参与决策 | ✅ 是 | ENV 常被排除 |

### 📌 Gate 不生成证据，只裁决证据状态

---

## Ⅵ. Trace & 审计强制裁决（Audit Authority）

| 裁决项 | Gate 权限 | 说明 |
|--------|----------|------|
| 是否必须写 trace | ✅ 强制 | 每一帧 |
| trace 中必须字段 | ✅ 强制 | gate_mode / blocked_by / reason |
| 是否允许无 Gate Trace | ❌ 禁止 | 架构违规 |

### 最低 Trace 要求

```json
{
  "gate_mode": "ACTIVE | READ_ONLY | SUSPENDED",
  "blocked_by": "...",
  "stability_score": 0.xx,
  "human_readable": "..."
}
```

---

## Ⅶ. Gate 明确禁止裁决的内容（Hard NO）

**Gate 永远不允许：**

| 项目 | 状态 |
|------|------|
| 判断风险是否真实 | ❌ |
| 确认"前方一定有坑" | ❌ |
| 修改 impact 语义 | ❌ |
| 替 C 做最终决策 | ❌ |
| 引入学习 / 自适应 | ❌（v0.5+ 才允许） |

---

## Ⅷ. 一句话架构裁定（建议写进代码注释）

### 英文版

```
Gate decides whether B may speak, and how.
B suggests possible risks.
C verifies and decides action.
```

### 中文版

```
Gate 决定能不能说、怎么说；
B 负责提醒；
C 负责确认与行动。
```

---

**版本：** v0.4.2  
**最后更新：** 2025-01-12  
**状态：** ✅ FROZEN（架构护栏）
