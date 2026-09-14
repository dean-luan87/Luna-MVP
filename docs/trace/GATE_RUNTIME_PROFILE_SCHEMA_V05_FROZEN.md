# Gate Runtime Profile Schema v0.5（冻结版）

**Status：** FROZEN / READ-ONLY  
**版本：** v0.5  
**日期：** 2025-01-12

---

## 📋 Schema 定位

本文档定义 Gate Runtime Profile 在 v0.5 中的唯一合法 JSON 结构。

这是 v0.5 的核心，不可省略。

---

## 1. GateRuntimeProfile 完整结构

```json
{
  "gate_mode": "ACTIVE | READ_ONLY | SUSPENDED",
  "runtime_profile": {
    "compute_level": "NONE | LIGHT | FULL",
    "tick_interval_ms": 100,
    "allow_future_probe": false,
    "authority_scope": "ADVISORY_ONLY"
  },
  "blocked_by": null,
  "human_reason": "镜头稳定，允许正常运行"
}
```

---

## 2. 字段逐项冻结说明

### 2.1 gate_mode（运行态裁决）

**类型：** `string`  
**枚举值：** `"ACTIVE" | "READ_ONLY" | "SUSPENDED"`  
**必填：** ✅

**语义：**
- `ACTIVE` - Gate 允许 B 正常运行
- `READ_ONLY` - Gate 允许只读运行
- `SUSPENDED` - Gate 禁止 B 运行

---

### 2.2 runtime_profile（调度裁决核心）

**类型：** `object`  
**必填：** ✅

#### 2.2.1 compute_level

**类型：** `string`  
**枚举值：** `"NONE" | "LIGHT" | "FULL"`  
**必填：** ✅

**语义：**
- `NONE` - 完全禁止，不运行任何 B 逻辑
- `LIGHT` - 低成本只读，轻量感知、状态更新、trace
- `FULL` - 完整运行，v0.4.x 已有全部 B 能力

**冻结规则：**
- `compute_level = NONE` ⇒ 必须等价于 `gate_mode = SUSPENDED`
- Gate 不得在 v0.5 中引入除上述三档以外的新等级

---

#### 2.2.2 tick_interval_ms

**类型：** `integer`  
**单位：** 毫秒（基于系统时间，不是帧）  
**必填：** ✅  
**最小值：** 1  
**典型值：** 33, 66, 100+

**语义：**
- B 允许被调度执行的最小时间间隔
- Gate 决定"多久跑一次"
- B 不得自行缩短该间隔
- C 不受此字段影响（C 仍逐帧）

**硬规则：**
```
实际 tick 时间 - 上次 tick 时间 >= tick_interval_ms
否则 → 不执行
```

这是 v0.5 最重要的"反作弊机制"，DCS 会审计这一条（RED）。

---

#### 2.2.3 allow_future_probe

**类型：** `boolean`  
**必填：** ✅  
**v0.5 固定值：** `false`

**冻结含义（v0.5）：**
- 明确保留接口
- v0.5 必须始终为 `false`
- 不允许 B 在 v0.5 做任何形式的未来预演

这是为 v0.6+ 预留的结构性接口，不是能力入口。

---

#### 2.2.4 authority_scope

**类型：** `string`  
**枚举值：** `"ADVISORY_ONLY"`  
**必填：** ✅  
**v0.5 固定值：** `"ADVISORY_ONLY"`

**冻结规则：**
- v0.5 中必须恒等于 `ADVISORY_ONLY`
- 任何试图改为 `CONFIRM` / `FORCE` / `EXECUTE` → 直接 DCS RED

---

### 2.3 blocked_by

**类型：** `string | null`  
**必填：** 仅在 `gate_mode != ACTIVE` 时必填

**语义：**
- Gate 阻断运行的唯一原因标识

**示例值：**
- `"camera_shake"`
- `"too_close"`
- `"missing_view_state"`
- `"insufficient_evidence"`

**规则：**
- 仅在 `gate_mode ≠ ACTIVE` 时允许非 null
- 必须与 Gate Authority Table 中定义的枚举一致

---

### 2.4 human_reason

**类型：** `string`  
**必填：** ✅

**语义：**
- 人类可读解释
- 用于 trace / Viewer / 审计
- 不参与任何计算或逻辑判断

**示例：**
- `"视角稳定，允许正常运行"`
- `"镜头晃动，暂停输出"`
- `"距离过近，交由 C 主导"`

---

## 3. Trace 集成要求

### 3.1 必须出现在 trace 中的位置

```json
{
  "gate": {
    "mode": "ACTIVE",
    "runtime_profile": {
      "compute_level": "FULL",
      "tick_interval_ms": 33,
      "allow_future_probe": false,
      "authority_scope": "ADVISORY_ONLY"
    },
    "blocked_by": null,
    "human_reason": "视角稳定，允许正常运行"
  }
}
```

### 3.2 DCS 审计要求

以下字段必须真实存在于 trace 中，否则 DCS 会判定为违规：

- ✅ `gate.runtime_profile.compute_level`
- ✅ `gate.runtime_profile.tick_interval_ms`
- ✅ `gate.runtime_profile.allow_future_probe`
- ✅ `gate.runtime_profile.authority_scope`
- ✅ `gate.blocked_by`（当 `gate.mode != ACTIVE` 时）
- ✅ `gate.human_reason`

---

## 4. 与 v0.4.x 的关系

| 项目 | v0.4.x | v0.5 |
|------|--------|------|
| gate_mode | ✅ | ✅ |
| runtime_profile | ❌ | ✅（新增） |
| compute_level | ❌ | ✅（新增） |
| tick_interval_ms | ❌ | ✅（新增） |
| allow_future_probe | ❌ | ✅（新增，固定 false） |
| authority_scope | ❌ | ✅（新增，固定 ADVISORY_ONLY） |

---

## 5. 冻结声明

- ✅ 本文档在 v0.5 生命周期内只读
- ✅ 不允许在实现阶段"边写边改语义"
- ✅ 所有新增能力必须**新开版本 + 新文档**

---

## ✅ 结论

GateRuntimeProfile 是 v0.5 的核心，不可省略。

它让 Gate 从"规则判断器"升级为"真实调度中枢"，并且能被 DCS 与 Web 完整审计。

---

**版本：** v0.5  
**状态：** FROZEN  
**最后更新：** 2025-01-12
