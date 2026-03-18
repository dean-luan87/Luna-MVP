# 主线 2 第二阶段：Experience / Evidence Evolution M1 交付说明

**依据**：Experience / Evidence Evolution M0 已完成；从单轮审计推进为多轮经验候选治理。  
**目标**：同类经验候选聚合、contradiction_sources、watchlist/promotable/blocked/rejected 细化、evolution_confidence_band、future_use_scope、审计报告式 reason。  
**约束**：不做学习系统、不做长期经验库、不做自动策略更新、不跨会话持久化、不反写 hypothesis/object_ledger/recheck。

---

## 1. 修改文件清单

| 文件 | 变更摘要 |
|------|----------|
| `decision_monitor/experience_evolution.py` | M1 常量 LAST_OUTCOME_TYPES、CONTRADICTION_SOURCES、EVOLUTION_CONFIDENCE_BANDS、FUTURE_USE_SCOPES；EVOLUTION_HINTS 增 cautious、review_required；ExperienceCandidate 新增 experience_group_key、aggregated_source_paths、repeated_pattern_count、last_observed_ts、last_outcome_type、contradiction_sources、watchlist_reason、promotable_score、evolution_confidence_band、future_use_scope；ExperienceEvolutionResult 新增 snapshot_for_next；_flow_stem、_last_outcome_type、_contradiction_sources、_governance_m1；build_experience_evolution 新增 prev_candidates_snapshot、current_ts，聚合与治理逻辑，返回 snapshot_for_next。 |
| `decision_monitor/builder.py` | 从 ctx 解析 experience_evolution_prev_snapshot，传入 prev_candidates_snapshot、current_ts。 |
| `runtime/context.py` | 新增 experience_evolution_group、experience_evolution_score、experience_evolution_scope、experience_evolution_confidence_band、experience_evolution_hint、experience_evolution_prev_snapshot。 |
| `main.py` | monitor_ctx 增加 experience_evolution_prev_snapshot；写回 M1 字段与 snapshot（JSON）。 |
| `tools/decision_monitor_viewer.py` | 经验演化卡片升级为 M1：展示 group、repeated、contradiction_sources、score、scope、confidence_band、watchlist_reason。 |
| `decision_monitor/CONTRACT.md` | experience_evolution 段落补充 M1 与不做项。 |
| `docs/MAINLINE_2_EXPERIENCE_EVIDENCE_EVOLUTION_M1_DELIVERY.md` | **新建**。本文档。 |

---

## 2. M1 数据结构升级说明

### ExperienceCandidate 新增字段

| 字段 | 类型 | 含义 |
|------|------|------|
| experience_group_key | str | 聚合键，如 object_search_path_pattern:container |
| aggregated_source_paths | List[str] | 同组最近 2~3 条 path 摘要 |
| repeated_pattern_count | int | 同组模式重复次数 |
| last_observed_ts | float | 最近观测时间戳 |
| last_outcome_type | str | found / unresolved / fallback / user_confirmed / user_denied / cancelled |
| contradiction_sources | List[str] | user_denied, repeated_fallback, blocked_context, unresolved_after_recheck, container_candidate_rejected, pocket_check_failed |
| watchlist_reason | str | 进入 watchlist 原因 |
| promotable_score | float | 0~1 升格倾向分 |
| evolution_confidence_band | str | low / medium / high |
| future_use_scope | str | local_only / same_flow_only / same_object_type_only / review_required |

### ExperienceEvolutionResult

- snapshot_for_next：List[dict]，供下一帧 build 时做聚合（group_key, source_path, repeated_pattern_count, experience_type, aggregated_source_paths）。

---

## 3. 经验候选聚合规则说明

- **experience_group_key**：`{experience_type}:{flow_stem}`，flow_stem 由 _flow_stem(path_list) 得到（container / occlusion / pocket / last_location / description / recheck / generic）。  
- **aggregated_source_paths**：上一轮同 group_key 的 aggregated_source_paths 加当前 path_str，取最近 3 条。  
- **repeated_pattern_count**：上一轮同 group_key 的 repeated_pattern_count + 1；无上一轮则为 1。  
- **prev_candidates_snapshot**：由 main 将上一帧 snapshot_for_next 写入 runtime_ctx（JSON），本帧 build 时从 ctx 传入并解析为 prev_by_key。  

---

## 4. contradiction_sources / watchlist / promotable / blocked / rejected 治理规则说明

- **contradiction_sources**：user_denied（用户否认）、repeated_fallback（fallback_count>=2）、blocked_context（高风险或 terminal==blocked）、unresolved_after_recheck（补证后仍未解决）、container_candidate_rejected（用户答否在容器）、pocket_check_failed（口袋流且发生回退）。  
- **rejected**：user_denied 明确；或 container_candidate_rejected 且 pocket_check_failed 同时存在。  
- **blocked**：repeated_fallback、blocked_context、unresolved_after_recheck。  
- **promotable**：repeated_pattern_count >= 2、support >= 1、user_confirmed >= 1、contradiction <= 0、fallback <= 1、非高风险。  
- **watchlist**：support >= 1 且（confirm >= 1 或 repeated_pattern >= 1）且 fallback <= 1，但不足 promotable；watchlist_reason 写明“有一定支撑或重复度但尚不足升格”。  

---

## 5. evolution_confidence_band / future_use_scope 规则说明

- **evolution_confidence_band**：repeated_pattern>=2 且 support/confirm 足且无冲突且 fallback 低 → high；有支撑且冲突或 fallback 未清零 → medium；单次成功/高频 fallback/用户否认 → low。  
- **future_use_scope**：高风险或 blocked_context → review_required；repeated_pattern>=2 且无冲突 → same_flow_only；container/pocket 且 confirm>=1 → same_object_type_only；否则 local_only。  

---

## 6. evolution_reason / promotion_block_reason 增强说明

- evolution_reason 为审计报告式多句：是否重复、重复次数、支撑来源、冲突来源、为何 watchlist/promotable/blocked/rejected、为何 future_use_scope 受限；并追加“聚合路径数”“冲突来源：…”。  
- promotion_block_reason 取值：user_denied、repeated_fallback、blocked_context、unresolved_after_recheck、single_success_with_confirm_or_repeat、single_success_not_enough 等。  

---

## 7. Viewer 展示说明

- 卡片标题：经验演化 / Experience Evolution (M1)。  
- 展示：experience_type、experience_group_key、evolution_status、confidence_trend、evolution_confidence_band；repeated_pattern_count、supporting_events_count、contradiction_count、contradiction_sources、user_confirmed_count、fallback_count；promotable_score、future_use_scope、watchlist_reason；source、evolution_reason、promotion_block_reason；共 N 条候选。  
- sections 保留 experience_evolution 完整展开。  

---

## 8. 样本运行结果

- **首帧无 prev**：repeated_pattern_count=1，aggregated_source_paths=[当前 path]，snapshot_for_next 写入 runtime_ctx。  
- **次帧同 group**：repeated_pattern_count=2，aggregated_source_paths 含上帧与本帧 path；若 support+confirm 足则可为 promotable。  
- **user_denied**：contradiction_sources 含 user_denied，status=rejected。  
- **fallback_count>=2**：contradiction_sources 含 repeated_fallback，status=blocked。  

---

## 9. 真实化与预留

| 项目 | 状态 |
|------|------|
| group_key、aggregated_source_paths、repeated_pattern_count、last_outcome_type、contradiction_sources、watchlist_reason、promotable_score、evolution_confidence_band、future_use_scope、snapshot_for_next、prev 聚合、治理规则、Viewer、runtime_ctx | **真实化** |
| 长期经验库、自动策略更新、跨会话沉淀、经验层反写主策略 | **未实现**（本轮不做） |

---

## 10. 验收与本轮是否通过

- **验收**：运行时存在可读的 Experience Evolution M1；至少支持同类经验候选的最小聚合；contradiction_sources 可区分若干具体来源；watchlist/promotable/blocked/rejected 判定比 M0 更细；evolution_confidence_band、future_use_scope 存在；Viewer 能展示增强结果；仍不直接改写 hypothesis/object_ledger/recheck；不破坏既有链路。  
- **本轮是否通过**：实现与文档满足上述要求即通过。
