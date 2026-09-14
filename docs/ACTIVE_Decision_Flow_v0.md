# ACTIVE 决策系统工程流图（v0 冻结版）

**用途**：工程实现 / 长期运行 / Shadow → Real 灰度  
**状态**：冻结版（v0）

**设计目标**：在复杂真实环境中，稳定、可解释地决定 **是否介入、何时介入、介入多重、介入谁**，并支持长期体检与灰度上线。

---

## 0. 设计总原则（写死）

1. **短期决策 ≠ 长期判断**
2. **实时系统只读长期统计，不自我修正**
3. **所有异常必须能在 trace 中被解释**
4. **Shadow 与 Real 使用同一决策链**

---

## 1. 输入层（Perception / Context）

### 1.1 视角事实层（View Fact Layer）

- `frame_quality`: GOOD / DEGRADED / INVALID
- `view_confidence`: 0–1
- **硬约束**：
  - `frame_quality != GOOD` → 禁止风险升级
  - `view_confidence < 0.4` → 强制 GUARDED

### 1.2 世界结构信号（冻结）

- `motion_instability`
- `path_instability`
- `branch_load`
- `roi_count` / `roi_load`

这四项构成「世界复杂度主干」，不学习、不自适应。

---

## 2. A3 复杂度计算（只算不控）

### 2.1 原始复杂度

```
complexity_raw = f(motion, path, branch, roi)
```

### 2.2 视角调制

```
complexity_effective = complexity_raw × view_confidence
```

### 2.3 控制模式

- ASSISTED
- GUARDED（低 VC / 视角不可信）

---

## 3. 主线 A：介入资格门禁（Eligibility v0）

**判断**：这一刻有没有资格「考虑介入」

**条件（冻结）**

- ACTIVE 任务态
- `complexity_effective` ≥ 阈值
- `control_mode != GUARDED`

**输出**

- `eligible`: true | false
- `reason`: LOW_COMPLEXITY | GUARDED | ACTIVE_AND_HIGH_COMPLEXITY

---

## 4. PAL v0（前瞻难度评估）

- **输入**：motion / path / branch / roi
- **输出**：`pal_horizon_difficulty`
- **特性**：EMA 平滑、慢于 complexity

PAL 不决定是否介入，只决定：

> 「如果要介入，现在是不是一个合适的节奏点」

---

## 5. ACTIVE × PAL 节律（Rhythm v0）

**状态机**

```
IDLE → PREPARE → ENGAGED → IDLE
```

**进入条件（冻结）**

- PREPARE：PAL ≥ 0.15
- ENGAGED：PAL ≥ 0.20

**时间约束**

- T_prepare_min = 2s
- T_engaged_min = 5s
- T_cooldown = 5s

**输出**

- `rhythm.state`: IDLE | PREPARE | ENGAGED

---

## 6. ENGAGED 介入强度（Engagement v0）

**决定**：介入「多重」，不决定内容。

**等级**

- L0：非 ENGAGED
- L1 / L2 / L3

**判定（冻结）**

- 基于 PAL + complexity + VC
- GUARDED 禁止 L3

**输出参数**

- `advice_scale`
- `pal_lookahead_m`
- `speak_cooldown_s`

**防抖**

- 升级立即
- 降级需 2 tick

---

## 7. Advice 类型节律（E v0）

**决定**：这段时间内「允许哪类 Advice 出现」

**类型**

- NAVIGATION_HINT
- ENV_AWARENESS
- TASK_STATE
- SAFETY_REMINDER（不受限）

**配额（30s 窗口）**

| 类型 | 每 30s 最大次数 |
|------|----------------|
| NAV  | 2              |
| ENV  | 2              |
| TASK | 1              |
| SAFETY | ∞           |

---

## 8. 多任务并行仲裁（Arbitration v0）

**候选任务**

- 来自：VISION / VOICE / TASK

**仲裁评分**

```
score = base_score × cooldown + fairness_boost
```

**规则**

- SAFETY 直通
- 其余选最高分 1 个
- 分数 < 0.25 → 本 tick 不介入

**输出**

- `winner` / `deferred` / `scores`

---

## 9. 跨 tick 公平性（Fairness v0）

**状态**

- `missed_count`

**补偿**

```
fairness_boost = min(missed_count × 0.1, 0.3)
```

- 只在 ENGAGED 内生效
- ENGAGED 结束清零

---

## 10. 多模态冲突处理（K v0）

**来源优先级**

```
SAFETY > VOICE > VISION > TASK
```

- VOICE 提升优先级，但不绕过节律/预算

**输出**

- `multimodal_conflict`: {selected_source, reason}

---

## 11. 执行 / Shadow 分流（L v0）

**Shadow Mode**

- 全算不说
- 输出 `shadow_decision`

**Real Mode**

- 执行 Advice
- 保留 Shadow 统计

---

## 12. 失败回退诊断（D v0）

在 ENGAGED 且未说时记录：

- FAIL_LOW_CONFIDENCE
- FAIL_COOLDOWN_ACTIVE
- FAIL_NO_ADVICE_MATCH
- FAIL_BUDGET_EXHAUSTED
- FAIL_SAFETY_SUPPRESSED

---

## 13. 长期体检与上传（M v0）

**本地聚合**

- 5 min 窗口

**上传内容**

- engaged_ratio
- level_dist
- arbitration_stats
- failure_stats
- multimodal_stats

**不上传**：内容、事件序列、用户标识

---

## 14. Shadow → Real 灰度规则（N v0）

**三道门**

1. 稳定性
2. 保守性
3. 结构健康

**灰度阶段**

| 阶段    | 行为       |
|---------|------------|
| Shadow  | 全算不说   |
| Real-L1 | 只允许 L1  |
| Real-L2 | 允许 L1+L2 |
| Real-L3 | 全部       |

---

## 15. 冻结声明

**本文档描述的所有 v0 规则：**

- 不学习
- 不在线自适应
- 只通过版本升级调整

---

> 这是一个可长期运行、可解释、可灰度的 ACTIVE 决策系统工程蓝图。
