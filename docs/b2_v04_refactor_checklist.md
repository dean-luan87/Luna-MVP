# B2 v0.4 重构 Checklist（DTL 对齐版）

## 目标

让 B2 v0.4 成为第一版"合法说话"的 B。

**不追求判断更准，  
只追求 说的话 C 听得懂、用得上、不被污染。**

---

## 一、必须【删除 / 禁用】的内容（零妥协）

这些内容 **不允许再对外出现**，不翻译、不兼容。

---

### ❌ 1. 所有"世界状态类 decision / enum"

包括但不限于：
- `WORLD_SHIFT`
- `ENV_TRANSITION`
- `STAGE_CHANGE`
- `SCENE_CHANGE`
- `CONDITION_CHANGE`（如果语义是"世界变了"）

**📌 动作：**
- 从对外接口中彻底移除
- 不再写入 timeline 作为"决策"
- 只允许存在于：
  - legacy 代码
  - debug 日志（internal-only）

---

### ❌ 2. B2 自行定义的时间窗口逻辑（作为决策依据）

包括：
- `Δ_pre / Δ_post`
- "变化发生在 t±x"
- "稳定确认后触发 decision"

**📌 动作：**
- 禁止这些逻辑 **直接触发输出**
- 允许它们：
  - 继续作为内部 signal
  - 写入 evidence（解释用）

---

## 二、必须【重构】的内容（v0.4 核心工作）

这些是 v0.4 **唯一需要你动手改的地方**。

---

### ✅ 3. 所有 decision 输出 → 改为 DTL.ActionImpact / NO_OP

**你现在大概率有类似逻辑：**

```python
if score > threshold:
    decision = WORLD_SHIFT
```

**必须改为：**

```python
impact = map_to_action_impact(
    internal_signals,
    c_context,        # t_horizon, task, motion
    dtl_rules
)

if impact is None:
    output = NO_OP
else:
    output = DTL.ActionImpact(...)
```

**📌 验收标准：**
- B2 v0.4 的对外输出 **只可能是**：
  - `DTL.ActionImpact`
  - `NO_OP`
- **不存在第三种可能**

---

### ✅ 4. 引入 DTL gating（发言资格判断）

在 B2 输出前，必须统一加一层 gate：

```python
if not dtl_gate.is_b2_allowed(scene, distance, stability):
    return NO_OP
```

**gate 条件至少包括：**
- 是否室内（室内 → NO_OP）
- 是否超过 3m（≤3m → NO_OP）
- 镜头是否稳定
- 是否在 C 请求的 t_horizon 内

**📌 验收标准：**
- 晃动 / 室内 / 近场 → B2 完全沉默
- 没有"误插嘴"的情况

---

### ✅ 5. ActionImpact 的生成必须以"行为"为中心

**禁止这种逻辑：**

> "我看到市场 / 施工 / 人多，所以我要说话"

**必须改成：**

> "如果你保持当前行为，在 t_horizon 内是否存在风险？"

**映射示例（强制）：**

| 内部信号 | 输出 |
|---------|------|
| 人流 ↑ + MID | `NEED_SLOW_DOWN` |
| 路面不确定 | `PATH_UNCERTAIN` |
| 明确阻断 | `NEED_STOP` |
| 无影响 | `NO_OP` |

**📌 验收标准：**
- ActionImpact 描述的是 **行为后果**
- 而不是 **世界状态**

---

## 三、可以【完整保留】的内容（不动）

这些不是问题来源，**千万别误删**。

---

### 🟢 6. 感知因子 / 连续性判断

包括：
- `crowd density`
- `vehicle flow`
- `surface change score`
- `continuity / stability / occlusion`

**📌 定位：**
- 全部降级为 **B-Lang internal**
- 只作为 ActionImpact 的"证据来源"

---

### 🟢 7. Evidence / Timeline / Record 体系

**📌 只改用途，不改结构：**
- ❌ 不再用于证明"世界判断正确"
- ✅ 用于解释：
  - 为什么给出这个 ActionImpact
  - 为什么选择 NO_OP

---

### 🟢 8. param_vector（但用途已变）

**📌 保留，但禁止用于实时判断**
- 只用于：
  - 离线分析
  - 权重回归
  - 人工 vs 系统差异分析

---

## 四、明确【现在不做】的事情（防止范围失控）

### 🚫 9. 现在不做的事

- 不引入学习 / 自我修复
- 不调阈值
- 不追求"更准"
- 不回改 v0.1–v0.3
- 不统一历史版本

**📌 理由：**

> 接口没对齐之前，所有精度优化都是假进步。

---

## 五、v0.4 重构完成后的"验收清单"

你可以用这 6 条直接验收：

1. ✅ B2 不再输出任何"世界判断类 decision"
2. ✅ 所有对外输出都能映射到 DTL
3. ✅ 室内 / 近场 / 晃动时，B2 保持沉默
4. ✅ 输出内容看起来像"给 C 的建议"，不是"系统日志"
5. ✅ Evidence 能解释"为什么建议你这么做"
6. ✅ 判断不准时，能明确是：
   - NO_OP 太保守
   - 还是 ActionImpact 类型不合适

---

## 六、强烈建议的执行方式（工程节奏）

**不要全局重构，一次只改一个点：**

1. **先让 v0.4 只输出 NO_OP**
2. **再逐个打开：**
   - `NEED_SLOW_DOWN`
   - `NEED_STOP`
   - `PATH_UNCERTAIN`
3. **最后才加 `NEED_DETOUR`**

这样你会非常清楚：
**是"哪个建议类型"在制造误差。**

---

## 七、最后一句（非常重要）

你现在不是在"修 Bug"，  
而是在"纠正 B 的表达方式"。

一旦 v0.4 重构完成，你会明显感觉到：
- ✅ B2 不再吵
- ✅ 时间点自然靠近人类感知
- ✅ C 的行为变得可解释

---

