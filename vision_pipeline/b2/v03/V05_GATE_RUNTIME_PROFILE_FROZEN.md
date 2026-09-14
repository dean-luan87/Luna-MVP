# B2 v0.5 Gate Runtime Profile 规范文档（冻结版）

**Status：** FROZEN / READ-ONLY  
**版本：** v0.5  
**日期：** 2025-01-12

---

## 📋 文档定位

本文档定义 Gate 在 v0.5 中对 B2 运行行为的唯一合法输出形态。

Gate 不产生 decision，不参与风险判断，不生成语义结论，仅负责**运行调度与算力裁决**。

---

## 1. 设计目标（v0.5 Only）

### Gate 在 v0.5 的唯一职责

> **决定 B 是否运行、以什么强度运行、多久运行一次**

### Gate 明确不做的事情

- ❌ 不生成 impact
- ❌ 不生成 decision / level
- ❌ 不确认风险
- ❌ 不预测未来结果
- ❌ 不干预 C 的行为逻辑

---

## 2. Gate Runtime Profile 总体结构

```json
{
  "gate_mode": "ACTIVE | READ_ONLY | SUSPENDED",
  "runtime_profile": {
    "compute_level": "NONE | LIGHT | FULL",
    "tick_interval_ms": 33,
    "allow_future_probe": false
  },
  "blocked_by": null,
  "human_reason": "视角稳定，允许正常运行"
}
```

---

## 3. 字段逐项冻结说明

### 3.1 gate_mode（运行态裁决）

| 值 | 含义 | 行为约束 |
|----|------|----------|
| ACTIVE | Gate 允许 B 正常运行 | 可能执行完整 B pipeline |
| READ_ONLY | Gate 允许只读运行 | 禁止产生 B→C 主动输出 |
| SUSPENDED | Gate 禁止 B 运行 | B 必须完全沉默 |

**强制规则：**
- `gate_mode = SUSPENDED` → B 不得执行任何感知、判断、输出
- `gate_mode = READ_ONLY` → B 仅允许读取状态、写 trace，不得输出 decision

---

### 3.2 runtime_profile（调度裁决核心）

#### 3.2.1 compute_level

| 值 | 语义 | 允许执行的内容 |
|----|------|----------------|
| NONE | 完全禁止 | 不运行任何 B 逻辑 |
| LIGHT | 低成本只读 | 轻量感知、状态更新、trace |
| FULL | 完整运行 | v0.4.x 已有全部 B 能力 |

**冻结规则：**
- `compute_level = NONE` ⇒ 必须等价于 `gate_mode = SUSPENDED`
- Gate 不得在 v0.5 中引入除上述三档以外的新等级

---

#### 3.2.2 tick_interval_ms

- **定义：** B 允许被调度执行的最小时间间隔
- **单位：** 毫秒（基于系统时间，不是帧）

**语义约束：**
- Gate 决定"多久跑一次"
- B 不得自行缩短该间隔
- C 不受此字段影响（C 仍逐帧）

**典型取值（非强制）：**
- `33ms` ≈ 30Hz（与视频帧同步）
- `66ms` ≈ 15Hz
- `100ms+` 用于节能 / 不稳定视角

---

#### 3.2.3 allow_future_probe

```json
"allow_future_probe": false
```

**冻结含义（v0.5）：**
- 明确保留接口
- v0.5 必须始终为 `false`
- 不允许 B 在 v0.5 做任何形式的未来预演

这是为 v0.6+ 预留的结构性接口，不是能力入口。

---

### 3.3 blocked_by

- **类型：** `string | null`
- **含义：** Gate 阻断运行的唯一原因标识

**示例：**
```json
"blocked_by": "camera_shake"
"blocked_by": "too_close"
"blocked_by": "missing_view_state"
```

**规则：**
- 仅在 `gate_mode ≠ ACTIVE` 时允许非 null
- 必须与 Gate Authority Table 中定义的枚举一致

---

### 3.4 human_reason

- 人类可读解释
- 用于 trace / Viewer / 审计
- 不参与任何计算或逻辑判断

---

## 4. Gate → B 的权威边界（冻结）

### Gate 有权决定

- ✅ B 是否运行
- ✅ B 运行频率
- ✅ B 运行强度（算力）

### Gate 无权决定

- ❌ B 的判断内容
- ❌ B 的语言
- ❌ B 的风险结论
- ❌ B 是否"提醒用户"

---

## 5. 与 v0.4.x 的关系

| 项目 | v0.4.x | v0.5 |
|------|--------|------|
| Gate 是否存在 | ✅ | ✅ |
| Gate 是否调度算力 | ❌ | ✅ |
| Gate 是否参与语义 | ❌ | ❌ |
| B 输出语义 | impact | impact（不变） |
| DCS 判定 | 基于行为 | 基于行为 + Gate |

---

## 6. DCS 强约束（自动红线）

以下任一情况，DCS 必须 RED：

1. `gate_mode = SUSPENDED` 但 B 仍执行逻辑
2. `compute_level = NONE` 但 B 仍产出 summary
3. `allow_future_probe = true`（v0.5 禁止）
4. B 自行修改 tick 频率，无视 Gate profile

---

## 7. 冻结声明

- ✅ 本文档在 v0.5 生命周期内只读
- ✅ 不允许在实现阶段"边写边改语义"
- ✅ 所有新增能力必须**新开版本 + 新文档**

---

## ✅ 结论

v0.5 Gate Runtime Profile 是"调度权力的封印"，不是能力扩张。

它让系统更稳、更省、更可控，但不会让 B 更聪明。

---

**版本：** v0.5  
**状态：** FROZEN  
**最后更新：** 2025-01-12
