# 主线 2 第二阶段：Experience / Evidence Evolution M0 交付说明

**依据**：Evidence Ledger、Hypothesis Layer、Recheck Planner、Object Temporal Ledger、Object Search Interaction M1.5 已完成；增加经验演化约束层，区分能力进化与幸运污染。  
**目标**：经验候选的记账、审计与约束；单次成功不自动升格；多次支撑+低冲突+用户确认才可能 promotable；fallback/否认过多则 blocked/rejected。  
**约束**：不做学习系统、不做长期经验库、不做自动策略更新、不反写 hypothesis/object_ledger/recheck、不做跨会话持久化。

---

## 1. 修改文件清单

| 文件 | 变更摘要 |
|------|----------|
| `decision_monitor/experience_evolution.py` | **新建**。ExperienceCandidate、ExperienceEvolutionResult；EXPERIENCE_TYPES、EVOLUTION_STATUSES、CONFIDENCE_TRENDS、EVOLUTION_HINTS；build_experience_evolution(evidence_ledger, hypothesis_layer, recheck_planner, object_temporal_ledger, object_search_interaction, state, object_user_confirmed_location, object_user_denied_location)；候选来源（path/container/occlusion/pocket/recheck）、审计规则、confidence_trend、evolution_reason/block_reason、evolution_hint_for_future。 |
| `decision_monitor/schema.py` | 引入 ExperienceEvolutionResult；DecisionMonitorFrame 新增 experience_evolution。 |
| `decision_monitor/builder.py` | 引入 experience_evolution；在 task_chain_bridge 之后调用 build_experience_evolution，写入 frame.experience_evolution。 |
| `runtime/context.py` | 新增 experience_evolution_type、experience_evolution_status、experience_evolution_reason、experience_evolution_trend、experience_evolution_blocked。 |
| `main.py` | 从 frame.experience_evolution.candidates[0] 写首条摘要到 runtime_ctx。 |
| `tools/decision_monitor_viewer.py` | 新增「经验演化 / Experience Evolution (M0)」卡片；sections 增加 experience_evolution。 |
| `decision_monitor/CONTRACT.md` | 补充 experience_evolution 说明与未实现项。 |
| `docs/MAINLINE_2_EXPERIENCE_EVIDENCE_EVOLUTION_M0_DELIVERY.md` | **新建**。本文档。 |

---

## 2. Experience / Evolution 数据结构说明

### ExperienceCandidate

| 字段 | 类型 | 含义 |
|------|------|------|
| experience_type | str | object_search_path_pattern / container_candidate_pattern / occlusion_resolution_pattern / pocket_check_pattern / recheck_effectiveness_pattern |
| source_module | str | 来源模块 |
| source_path | str | 路径摘要（如 resolution_path 用 → 连接） |
| source_summary | str | 来源摘要 |
| supporting_events_count | int | 支撑次数 |
| contradiction_count | int | 冲突/否认次数 |
| user_confirmed_count | int | 用户确认次数 |
| fallback_count | int | 回退次数 |
| confidence_trend | str | up / flat / down |
| evolution_status | str | candidate / watchlist / promotable / blocked / rejected |
| evolution_reason | str | 可解释原因 |
| promotion_blocked | bool | 是否禁止升格 |
| promotion_block_reason | str | 阻断原因 |
| evolution_hint_for_future | str | preferred / neutral / unreliable |

### ExperienceEvolutionResult

| 字段 | 类型 | 含义 |
|------|------|------|
| candidates | List[ExperienceCandidate] | 1~3 条经验候选 |

---

## 3. 经验候选来源规则说明

- **object_search_path_pattern**：来自 object_search_interaction.search_resolution_path，路径非空即生成一条。  
- **container_candidate_pattern**：path 含 container_check_flow 且 object_temporal_ledger 有容器候选时生成。  
- **occlusion_resolution_pattern**：path 含 occlusion_clear_flow 或 clearing_occlusion 时生成。  
- **pocket_check_pattern**：path 含 pocket_check_flow 时生成。  
- **recheck_effectiveness_pattern**：recheck_planner 有 recheck_action 且 terminal==found 时生成。  
- 若尚无任何候选，则用 evidence_ledger/hypothesis_layer 首条摘要生成一条 object_search_path_pattern 占位。  
- 总候选数截断为最多 3 条。  

---

## 4. 经验审计规则说明

- **单次成功不升格**：supporting_events_count ≤ 1 且 user_confirmed_count == 0 → evolution_status=candidate，promotion_blocked=True，promotion_block_reason=single_success_not_enough，evolution_reason="仅 1 次成功，缺少重复支撑与用户确认，暂不升格"。  
- **多次支撑+低冲突+用户确认才可能 promotable**：supporting_events_count >= 2 且 user_confirmed_count >= 1 且 contradiction_count <= 0 且 fallback_count <= 1 且非高风险 → evolution_status=promotable，promotion_blocked=False，evolution_hint_for_future=preferred。  
- **fallback/否认过多阻止升格**：fallback_count >= 2 或 contradiction_count >= 1 → evolution_status=blocked 或 rejected，promotion_blocked=True，promotion_block_reason=fallback_or_contradiction_high，evolution_hint_for_future=unreliable。  
- **有用户确认但仅单次支撑**：support >= 1 且 confirm >= 1 且 fallback <= 1 → evolution_status=watchlist，promotion_blocked=True，evolution_reason="已有用户确认但仅单次支撑，进入观察列表"。  
- **高风险语境**：minimum_mode_active 或 runtime_domain_state==frozen → 一律 promotion_blocked，evolution_reason="高风险语境（守底/冻结），不升格"，evolution_hint_for_future=unreliable。  

---

## 5. confidence_trend / evolution_status 规则说明

- **confidence_trend**：user_confirmed_count >= 1 且 contradiction_count == 0 且 fallback_count <= 1 → up；contradiction_count >= 1 或 fallback_count >= 2 → down；否则 flat。  
- **evolution_status**：见第 4 节；优先级为 blocked/rejected > watchlist > promotable > candidate。  

---

## 6. evolution_reason / block_reason 生成规则说明

- 单次成功：evolution_reason="仅 1 次成功，缺少重复支撑与用户确认，暂不升格"，promotion_block_reason=single_success_not_enough。  
- 可升格：evolution_reason="来自{source_module}，已有 N 次支撑且 M 次用户确认，可考虑沉淀"，promotion_block_reason=None。  
- 回退/否认过多：evolution_reason="回退或用户否认过多，暂不推荐沉淀" 或 "存在用户否认或取消，不升格"，promotion_block_reason=fallback_or_contradiction_high。  
- 观察列表：evolution_reason="已有用户确认但仅单次支撑，进入观察列表"，promotion_block_reason=single_success_with_confirm。  
- 高风险：evolution_reason="高风险语境（守底/冻结），不升格"，promotion_block_reason=high_risk_context。  

---

## 7. Viewer 展示说明

- 卡片标题：经验演化 / Experience Evolution (M0)。  
- 展示首条候选：experience_type、evolution_status、confidence_trend、promotion_blocked、source_summary/source_path、supporting_events_count、contradiction_count、user_confirmed_count、fallback_count、evolution_reason、promotion_block_reason；并显示「共 N 条候选」。  
- sections 可展开 experience_evolution 查看 candidates。  

---

## 8. 样本运行结果

- **无寻物路径**：生成 1 条占位候选（object_search_path_pattern，来自 evidence_ledger），support=0，status=candidate，promotion_blocked=True。  
- **有 path、terminal=found、无用户否认**：support=1，confirm=0 → candidate，blocked，reason=单次成功不升格。  
- **有 path、用户确认**：support=1，confirm=1 → watchlist，blocked，reason=已有用户确认但仅单次支撑。  
- **有 path、用户否认或 cancelled**：contradiction=1 → blocked/rejected，evolution_reason=存在用户否认或取消。  
- **fallback_count >= 2**：blocked，reason=回退过多。  
- **minimum_mode_active**：任意候选均为 promotion_blocked，reason=高风险语境。  

---

## 9. 真实化与预留

| 项目 | 状态 |
|------|------|
| ExperienceCandidate/ExperienceEvolutionResult、五类 experience_type、五态 evolution_status、候选来源规则、审计规则、confidence_trend、evolution_reason/block_reason、evolution_hint_for_future、Viewer、runtime_ctx 首条摘要、不反写下游 | **真实化** |
| 长期经验库、自动策略更新、学习型权重、跨会话沉淀、多对象经验图谱、持久化 | **未实现**（本轮不做） |

---

## 10. 验收与本轮是否通过

- **验收**：运行时存在可读的 Experience Evolution 结果；至少能生成 1~3 条经验候选；能显式区分单次成功不升格、多次支撑+低冲突+用户确认才可能 promotable、fallback/否认过多 blocked/rejected；Viewer 能展示；不直接改写 hypothesis/object_ledger/recheck 主逻辑；不破坏既有链路。  
- **本轮是否通过**：实现与文档满足上述要求即通过。
