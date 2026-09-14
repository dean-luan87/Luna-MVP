# B2 v0.4 decision enum → DTL.ActionImpact 映射表（冻结版）

## 设计原则（裁判标准）

- **DTL 只关心"是否影响 C 的行为"**
- **不影响行为 = NO_OP**
- **世界描述 ≠ 行为影响**

---

## 一、世界 / 环境类 decision（全部废弃，不翻译）

这些是 v0.1–v0.3 的核心问题来源。

| v0.4 decision enum | 处理方式 | 原因 |
|-------------------|---------|------|
| `WORLD_SHIFT` | ❌ 废弃 | 世界变化≠行为影响 |
| `ENV_TRANSITION` | ❌ 废弃 | 环境分类非法 |
| `STAGE_CHANGE` | ❌ 废弃 | 抽象阶段非法 |
| `SCENE_CHANGE` | ❌ 废弃 | B 不允许描述世界 |
| `ENTER_MARKET` / `OUTDOOR` | ❌ 废弃 | 非行为语义 |

**📌 说明：**
- 这些 decision **不允许映射**
- 不要试图"翻译得更好"
- 只能：
  - 写入 internal log
  - 写入 evidence 作为背景

---

## 二、路况 / 条件变化类 decision（条件映射）

这些 decision 是否能输出，取决于是否影响 C 的行为。

---

### 1️⃣ CONDITION_CHANGE

这是最容易"误用"的一个。

**❌ 错误用法（旧）：**
> 路况变化了 → 输出 CONDITION_CHANGE

**✅ 正确映射（新）：**

| 内部评估结果 | DTL 输出 |
|------------|---------|
| 路况变化，但仍可安全通过 | `NO_OP` |
| 路况变化，舒适性下降 | `NEED_SLOW_DOWN` |
| 路况变化，通行性不确定 | `PATH_UNCERTAIN` |
| 路况变化，明确不可通行 | `NEED_STOP` 或 `NEED_DETOUR` |

**📌 关键点：**
- `CONDITION_CHANGE` 本身**不允许作为输出**
- 只能作为 **internal signal**

---

### 2️⃣ PATH_CHANGE

| 内部含义 | DTL.ActionImpact |
|---------|------------------|
| 路面轻微变化 | `NO_OP` |
| 路面变差但可走 | `NEED_SLOW_DOWN` |
| 台阶 / 不连续 | `PATH_UNCERTAIN` |
| 完全阻断 | `NEED_STOP` |

---

## 三、人流 / 车流相关 decision（行为优先）

---

### 3️⃣ CROWD_INCREASE / PEOPLE_DENSITY_UP

| 情况 | DTL.ActionImpact |
|-----|------------------|
| 人多但不影响当前路线 | `NO_OP` |
| 人多影响舒适性 | `NEED_SLOW_DOWN` |
| 人流与行进方向冲突 | `NEED_DETOUR` |
| 人流严重阻断 | `NEED_STOP` |

**📌 注意：**
- "人多"不是理由
- "是否影响行为"才是理由

---

### 4️⃣ VEHICLE_APPROACH / TRAFFIC_FLOW

| 情况 | DTL.ActionImpact |
|-----|------------------|
| 远处车辆，无交叉 | `NO_OP` |
| 可能交叉，需谨慎 | `NEED_SLOW_DOWN` |
| 明确交叉风险 | `NEED_STOP` |

---

## 四、突发 / 事件类 decision（严格行为导向）

---

### 5️⃣ INTERRUPT / EVENT_DETECTED

这类在 v0.4 里通常最混乱。

**正确拆解方式：**

| 内部事件含义 | DTL.ActionImpact |
|------------|------------------|
| 事件发生，但不在 t_horizon | `NO_OP` |
| 事件可能影响未来路线 | `PATH_UNCERTAIN` |
| 事件阻断当前路线 | `NEED_STOP` |
| 事件需提前绕行 | `NEED_DETOUR` |

**📌 INTERRUPT 不能直接输出**

必须先回答一句话：

> **"如果 C 继续现在的行为，会发生什么？"**

---

## 五、默认兜底规则（非常重要）

### 🔒 统一兜底映射规则

```python
if cannot_explain_how_it_affects_behavior:
    return NO_OP
```

**这条规则 比任何阈值都重要。**

---

## 六、映射优先级规则（写进代码注释）

当多个内部 decision 同时触发时：

1. `NEED_STOP`（最高优先级）
2. `NEED_DETOUR`
3. `PATH_UNCERTAIN`
4. `NEED_SLOW_DOWN`
5. `NO_OP`（最低优先级）

**📌 价值排序依据：**

> **安全 > 舒适 > 距离**

---

## 七、工程里可以直接用的"映射伪代码"

```python
def map_decision_to_actionimpact(signals, c_ctx):
    """
    将 B2 内部信号映射为 DTL.ActionImpact
    
    Args:
        signals: B2 内部感知信号
        c_ctx: C 的上下文（t_horizon, task, motion）
    
    Returns:
        DTL.ActionImpact 或 NO_OP
    """
    # 1. DTL gating（发言资格判断）
    if not dtl_gate.allow_b2(c_ctx):
        return NO_OP
    
    # 2. 优先级映射（安全 > 舒适 > 距离）
    if signals.blocked or signals.critical_risk:
        return ActionImpact(
            impact_type="NEED_STOP",
            confidence=signals.confidence,
            effective_zone="MID",
            path_state="BLOCKED",
            reasons=signals.reasons,
            time_horizon=c_ctx.t_horizon,
            t_valid_until=signals.t_valid_until
        )
    
    if signals.requires_detour:
        return ActionImpact(
            impact_type="NEED_DETOUR",
            confidence=signals.confidence,
            effective_zone="MID",
            path_state="BLOCKED",
            reasons=["TEMP_OBSTACLE"],
            time_horizon=c_ctx.t_horizon,
            t_valid_until=signals.t_valid_until
        )
    
    if signals.path_uncertain or signals.surface_irregular:
        return ActionImpact(
            impact_type="PATH_UNCERTAIN",
            confidence=signals.confidence,
            effective_zone="MID",
            path_state="UNCERTAIN",
            reasons=["SURFACE_CHANGE"],
            time_horizon=c_ctx.t_horizon,
            t_valid_until=signals.t_valid_until
        )
    
    if signals.comfort_drop or signals.crowd_up or signals.traffic_flow:
        return ActionImpact(
            impact_type="NEED_SLOW_DOWN",
            confidence=signals.confidence,
            effective_zone="MID",
            path_state="DEGRADED",
            reasons=["CROWD"] if signals.crowd_up else ["VEHICLE_FLOW"],
            time_horizon=c_ctx.t_horizon,
            t_valid_until=signals.t_valid_until
        )
    
    # 3. 兜底规则
    return NO_OP
```

---

## 八、映射表总结

### ✅ 可以映射的 decision（条件映射）

| 原 decision | 映射条件 | DTL 输出 |
|------------|---------|---------|
| `CONDITION_CHANGE` | 影响行为 | `NEED_SLOW_DOWN` / `PATH_UNCERTAIN` / `NEED_STOP` |
| `PATH_CHANGE` | 影响行为 | `NEED_SLOW_DOWN` / `PATH_UNCERTAIN` / `NEED_STOP` |
| `CROWD_INCREASE` | 影响行为 | `NEED_SLOW_DOWN` / `NEED_DETOUR` / `NEED_STOP` |
| `VEHICLE_APPROACH` | 影响行为 | `NEED_SLOW_DOWN` / `NEED_STOP` |
| `INTERRUPT` | 影响行为 | `PATH_UNCERTAIN` / `NEED_STOP` / `NEED_DETOUR` |

### ❌ 必须废弃的 decision（不可映射）

| 原 decision | 处理方式 |
|------------|---------|
| `WORLD_SHIFT` | ❌ 废弃，只写 internal log |
| `ENV_TRANSITION` | ❌ 废弃，只写 internal log |
| `STAGE_CHANGE` | ❌ 废弃，只写 internal log |
| `SCENE_CHANGE` | ❌ 废弃，只写 internal log |
| `ENTER_MARKET` / `OUTDOOR` | ❌ 废弃，只写 internal log |

---

## 九、最重要的一句话（请记住）

> **"世界变了"不是 B 该说的话，  
> "你接下来这样走还行不行"才是。**

---

## 十、使用指南

### 工程重构时：

1. **先找所有使用废弃 decision 的地方**
   - 标记为 `@deprecated`
   - 改为只写 internal log

2. **逐个替换条件映射的 decision**
   - 先判断是否影响行为
   - 再映射到对应的 DTL.ActionImpact

3. **使用映射优先级规则**
   - 多个信号同时触发时，选择优先级最高的

4. **使用兜底规则**
   - 无法解释如何影响行为 → `NO_OP`

---

