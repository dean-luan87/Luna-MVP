# 主线 2 第二阶段：空间遗忘 M0 交付说明

**依据**：SPATIAL_MEMORY_POLICY_CONSTITUTION.md v1.0 + Spatial Memory Pooling M0  
**目标**：在记忆分池 M0 基础上为四层空间记忆池增加最小出池规则，使 working / episode 不再只进不出，形成最小可见、可记录、可测试的空间遗忘闭环。本轮只做最小遗忘，不做 Value Decay、长期证据门槛、学习、情感记忆。

---

## 1. 修改文件清单

| 文件 | 变更摘要 |
|------|----------|
| `decision_monitor/spatial_forgetting.py` | **新建**。SpatialForgettingSummary；apply_spatial_forgetting(pools, goal, state, current_ts, prev_goal_type, prev_goal_status, prev_dominant) 实现 Working TTL、Episode Task-End Collapse、Episode 最小过期；返回 (更新后 pools, summary)。 |
| `decision_monitor/schema.py` | 引入 SpatialForgettingSummary；DecisionMonitorFrame 新增 spatial_forgetting。 |
| `decision_monitor/builder.py` | 引入 spatial_forgetting；build 中在 spatial_memory_pools 之后调用 apply_spatial_forgetting，用更新后 pools 与 forgetting_summary 写入 frame。 |
| `runtime/context.py` | 新增 last_goal_type、last_goal_status、last_dominant_skeleton（供下一帧遗忘判定）；spatial_forgetting_working_expired、spatial_forgetting_episode_collapsed、spatial_forgetting_episode_expired、spatial_forgetting_reason、spatial_forgetting_actions。 |
| `main.py` | monitor_ctx 增加 prev_goal_type、prev_goal_status、prev_dominant（来自 runtime_ctx）；本帧写 spatial_forgetting 与 last_goal_type/last_goal_status/last_dominant_skeleton 到 runtime_ctx。 |
| `tools/decision_monitor_viewer.py` | 新增「空间遗忘 / Spatial Forgetting (M0)」卡片；sections 增加 spatial_forgetting。 |
| `decision_monitor/CONTRACT.md` | 补充 spatial_forgetting 说明与未实现项（Value Decay、Evidence Replacement、stable/anchor 长期遗忘、学习型 policy）。 |

---

## 2. Forgetting 结果结构说明

### SpatialForgettingSummary

| 字段 | 类型 | 含义 |
|------|------|------|
| working_expired_count | int | 本帧 working 因 TTL 过期移除的数量 |
| episode_collapsed_count | int | 本帧 episode 因 Task-End/上下文切换塌缩移除的数量 |
| episode_expired_count | int | 本帧 episode 因时间过期移除的数量 |
| forgetting_reason_summary | str | 遗忘原因摘要（分号分隔） |
| forgetting_actions_applied | List[str] | 已应用动作：working_ttl / episode_collapse / episode_expiry |

---

## 3. Working TTL 规则说明

- **规则**：对 working_memory_items 中每项，若 (current_ts * 1000 - item.timestamp * 1000) > WORKING_TTL_MS，则从 working 中移除。
- **默认 TTL**：WORKING_TTL_MS = 5000 ms（5 秒），可测、规则明确。
- **统计**：移除数量写入 working_expired_count；forgetting_actions_applied 含 "working_ttl"。
- **说明**：当前每帧从 smap/relations 重建 pools，同帧内新写入项 timestamp=now，故同帧内通常无过期；当后续引入跨帧池或注入旧 timestamp 时，TTL 会生效。

---

## 4. Episode Task-End Collapse 规则说明

- **触发条件**（满足任一即塌缩）：  
  - goal_status 为 paused 或 completed；  
  - goal_type 与上一帧 prev_goal_type 不同；  
  - goal_status 与上一帧 prev_goal_status 不同且当前为 paused/completed；  
  - dominant_skeleton 与上一帧 prev_dominant 不同。
- **动作**：清空 episode_memory_items；episode_collapsed_count = 清空前的数量；forgetting_actions_applied 含 "episode_collapse"。
- **实现**：规则型，prev_* 由 main 从 runtime_ctx（上一帧写入的 last_goal_type、last_goal_status、last_dominant_skeleton）传入 ctx。

---

## 5. Episode 最小过期规则说明

- **规则**：当未触发 Task-End Collapse 时，对 episode_memory_items 按时间过滤：(current_ts * 1000 - item.timestamp * 1000) > EPISODE_TTL_MS 的项移除。
- **默认 TTL**：EPISODE_TTL_MS = 30000 ms（30 秒），保守占位。
- **与 Task-End 区分**：Task-End Collapse 为上下文切换触发；Episode 过期为时间触发。
- **统计**：移除数量写入 episode_expired_count；forgetting_actions_applied 含 "episode_expiry"。

---

## 6. Stable / Anchor：继续不做复杂遗忘

- stable_memory_items、anchor_memory_items 当前阶段保持占位或弱占位。
- **不做**：证据门槛、replacement、冲突替换、长期衰减。
- **文档**：此为预留设计，非遗漏；后续 Evidence Ledger / 长期记忆再接入。

---

## 7. Viewer 展示说明

- **卡片标题**：空间遗忘 / Spatial Forgetting (M0)。
- **第一行**：working 过期：&lt;working_expired_count&gt; · episode 塌缩：&lt;episode_collapsed_count&gt; · episode 过期：&lt;episode_expired_count&gt;。
- **第二行**：原因：&lt;forgetting_reason_summary&gt;。
- **第三行**：已应用：&lt;forgetting_actions_applied 逗号分隔&gt;（无则为「无」）。
- 专家折叠面板可展开 spatial_forgetting 查看全部字段。

---

## 8. 样本运行结果（验收）

- 运行时存在可读的 forgetting summary（frame.spatial_forgetting、runtime_ctx 各字段）。
- Working memory 能发生 TTL 过期（可通过注入旧 timestamp 的 pools 或跨帧池验证）。
- Episode memory 能发生 Task-End Collapse（prev_goal_type ≠ goal_type 或 goal_status paused 等）。
- Episode memory 能发生最小时间过期（同上，注入旧 timestamp 可验证）。
- Viewer 能显示遗忘结果。
- 不破坏主线 A、主线 2 第一阶段、M0、M1、M1.5、M2、Skeleton Mix M0、Skeleton Filter M0、Spatial Memory Pooling M0 链路。

---

## 9. 当前哪些遗忘字段已真实化，哪些仍预留

| 项目 | 状态 |
|------|------|
| SpatialForgettingSummary、apply_spatial_forgetting、Working TTL、Episode Task-End Collapse、Episode 最小过期、frame/runtime_ctx/Viewer、prev_* 传递与 last_* 回写 | **真实化**。 |
| Value Decay、Evidence Replacement、Stable/Anchor 长期遗忘、学习型 forgetting policy、情感记忆遗忘、Hypothesis Layer 联动、数据库/持久化 | **未实现**，本轮不做。 |

---

## 10. 本轮是否通过

- **是**。验收满足：运行时存在可读的 forgetting summary；Working/Episode 出池规则可测；Viewer 能显示；不破坏既有链路。未实现项已在 CONTRACT 与本文档写明。
