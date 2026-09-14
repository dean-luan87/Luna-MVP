# 主线 2 第二阶段：对象时空账本 M0 交付说明

**依据**：SpatialMap、Evidence Ledger、Hypothesis、Recheck、working/episode memory、用户命名/问询  
**目标**：在已有认知链上增加最小对象级时空账本，单对象优先，记录“最后确认位置、可见性、容器候选、假设摘要”，为“找药盒/找钥匙/找遥控器”等场景提供对象载体。不做完整目标识别学习、不做复杂 re-id、不做持久化多对象库、不做经验沉淀。

---

## 1. 修改文件清单

| 文件 | 变更摘要 |
|------|----------|
| `decision_monitor/object_temporal_ledger.py` | **新建**。ObjectTemporalEntry、LedgerEvent、ObjectTemporalLedger；VISIBILITY_STATUSES、EVENT_TYPES；build_object_temporal_ledger(focus_object_label, smap, ledger, hypothesis_layer, recheck_planner, pools, current_ts)。 |
| `decision_monitor/schema.py` | 引入 ObjectTemporalLedger；DecisionMonitorFrame 新增 object_temporal_ledger。 |
| `decision_monitor/builder.py` | 引入 object_temporal_ledger；build 中在 recheck_planner 之后调用 build_object_temporal_ledger，ctx.get("focus_object_label")，写入 frame.object_temporal_ledger。 |
| `runtime/context.py` | 新增 focus_object_label、object_last_confirmed_location、object_visibility_status、object_ledger_confidence、object_container_candidate。 |
| `main.py` | monitor_ctx 增加 focus_object_label（来自 runtime_ctx）；决策显示器块内将 object_temporal_ledger 摘要写入 runtime_ctx。 |
| `tools/decision_monitor_viewer.py` | 新增「对象时空账本 / Object Temporal Ledger (M0)」卡片；sections 增加 object_temporal_ledger。 |
| `decision_monitor/CONTRACT.md` | 补充 object_temporal_ledger 说明与未实现项。 |

---

## 2. 数据结构说明

### ObjectTemporalEntry（最小对象条目）

| 字段 | 类型 | 含义 |
|------|------|------|
| object_label | str | 对象标签（用户问询/关注或 current_focus） |
| object_profile_summary | str | 简要画像（如 last_location、working 数） |
| last_confirmed_location | str | 最后确认位置（smap focus/confirm 的 sector/band） |
| last_seen_ts | float | 最后可见时间戳 |
| visibility_status | str | visible / occluded / lost / container_candidate / unknown |
| current_container_candidate | str | 当前容器候选（来自 container_candidate 假设） |
| current_hypothesis_summary | str | 当前假设摘要 |
| ledger_confidence | float | 账本置信度 0～1 |

### LedgerEvent（最小事件）

| 字段 | 类型 | 含义 |
|------|------|------|
| event_type | str | object_seen / object_picked / object_lost_visibility / container_opened / object_candidate_in_container |
| timestamp | float | 时间戳 |
| summary | str | 可选摘要 |

### ObjectTemporalLedger

| 字段 | 类型 | 含义 |
|------|------|------|
| focus_object_entry | ObjectTemporalEntry | 当前关注单对象条目 |
| events | List[LedgerEvent] | 最小事件链（最多保留 5 条） |
| ledger_reason | str | 生成原因摘要 |

---

## 3. 最小事件链与生成规则

- **object_seen**：路径延续或交互目标假设、或有 last_location/working 证据时添加。
- **object_lost_visibility**：occluded_object_candidate 假设时添加。
- **object_candidate_in_container**：container_candidate 假设时添加。
- 每帧至多追加一条当前状态对应事件，events 保留最近 5 条。

---

## 4. 输入来源与单对象优先

- 输入仅来自：local_goal_spatial_map（位置）、evidence_ledger（置信度）、hypothesis_layer（可见性/容器/假设摘要）、recheck_planner（原因）、spatial_memory_pools（working 数）、focus_object_label（ctx，用户问询或当前关注）。
- 无 focus_object_label 时使用 "current_focus" 作为占位标签，仍产出一条条目便于展示与后续对接。

---

## 5. Viewer 展示说明

- **卡片标题**：对象时空账本 / Object Temporal Ledger (M0)。
- **第一行**：关注对象、可见性、置信度。
- **第二行**：最后确认位置、容器候选。
- **第三行**：事件数、ledger_reason。
- 专家折叠面板可展开 object_temporal_ledger 查看 focus_object_entry、events、ledger_reason。

---

## 6. 当前已真实化 vs 仍预留

| 项目 | 状态 |
|------|------|
| ObjectTemporalEntry、LedgerEvent、ObjectTemporalLedger、build_object_temporal_ledger、从 smap/ledger/hypothesis/pools/recheck 取数、frame/runtime_ctx/Viewer、focus_object_label 传递 | **真实化**。 |
| 完整目标识别学习、复杂 re-id、持久化多对象数据库、经验沉淀、多对象全场账本 | **未实现**，本轮不做。 |

---

## 7. 本轮是否通过

- **是**。验收满足：运行时可读对象时空账本；单对象条目含 label/location/visibility/confidence/container_candidate/hypothesis_summary；事件链含 object_seen/object_lost_visibility/object_candidate_in_container 等；Viewer 可展示；不破坏既有认知链。未实现项已在 CONTRACT 与本文档写明。
