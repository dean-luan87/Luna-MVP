# Local-Global Progress Gradient Tightening M0

**文件**：`docs/LOCAL_GLOBAL_PROGRESS_GRADIENT_TIGHTENING_M0.md`

## 一、文档定位

1. **不是**场景扩包，**不是** benchmark / triage 改造，**不是**主骨架或 recheck 变更。  
2. **仅**针对 **`local_global_progress_tension`（lg）** 在 `decision_monitor/narrative_evidence_tension_review.py` 中的启发式收紧，拉开 **low / medium / high** 梯度，并保留与 **`phase_closure_outcome_tension`（pc）** 的配对阅读价值。  
3. **未**修改 **`narrative_trace_support_tension`（nt）**；**未**修改 **`tools/tension_severity_profile_map.py`** 的 hard 规则（`critical_candidate` 仍要求 **`pc=high` 且 `lg=high` 同帧**）。

---

## 二、收紧前问题复盘（m14 基线）

依据：`logs/real_scenario_pack_m14_pre_lg_gradient.json`（收紧前快照，见 `logs/local_global_gradient_analysis_m14.json`）。

1. **`lg` 几乎恒为 `medium`（80/81）**：`task_chain_progress_summary` 模板中 **固定包含 `resume=` 字段名**，旧启发式用子串 **`"resume"`** 作为「推进语言」命中条件 → **几乎恒真**。  
2. **`lg=high` 极少（1/81）**：仅 **`resume_chain_fragility_summary`** 命中 **`resume_declared_but_main_not_progressed`** 时抬升。  
3. **`pc=high` + `lg=high` 为 0**：与 Signal Gap 结论一致；收紧前 **`pc=high` 时 `lg` 恒为 `medium`**。  
4. **原因语句过宽**：`progress_language_but_main_not_reached` 覆盖过大，**「正常探索中的 mixed 推进」**与**「全局停滞」**未分层。  

---

## 三、收紧规则摘要（实现）

**文件**：`decision_monitor/narrative_evidence_tension_review.py`

1. **去除 `resume=` 字段名假阳性**：不再用裸子串 **`"resume"`** 作为推进语言；改为 **结构化 token**（如 **`recovering=yes` / `inserted_open=yes` / `local_only_risk=yes` / `main_push_hint=mixed`**）、**显式 `forward|推进|progress`**、**非空的 `resume=` 值**、以及 **`process_observation`** 中的停滞子串。  
2. **弱探索 → `low`**：在 **`resume_chain_progress_reached_main is False`** 前提下，若 **`main_push_hint=mixed`** 且 **无** `local_only_risk` / 插入 / 恢复语义、**warn 无实质风险** → **`weak_exploration_main_mixed_not_yet_global_stall`**。  
3. **结构叠加 → `high`**（保守）：在 **`reached_main` 仍为 False 时，若 **`local_only_risk=yes` 且（`recovering=yes` 或 `inserted_open=yes`）**，或 **warn** 命中 **`pseudo_recovery` / `inserted_branch` / `local_success`** 等与局部成功相关的组合，或 **`resume_chain_waiting_clarification` + 风险/混合推进**、或 **`m11x_ctx_observed` 且 `resume_frag` 非 `none`** 等（见代码 `_lg_escalate_high`）。  
4. **保留原高优先级**：`resume_chain_fragility_summary` 仍含 **`resume_declared_but_main_not_progressed`** → **`high`**（不变）。  

**说明**：曾尝试用 **`inputs.recovery_declared_but_resume_chain_fragile_expected`** 与 **`local_only_risk`** 联合抬升，但 **DecisionMonitorBuilder 不把该 flag 写入 `frame.inputs`**，run_summary 的 m11x 前缀依赖同一来源，**在当前主链落帧下不可复现**，故 **未**采用该路径（避免死代码）。

---

## 四、收紧前后分布对比

**产物**：`logs/local_global_gradient_analysis_m14.json`

| 指标 | 收紧前（pre） | 收紧后（当前 `logs/real_scenario_pack_m14.json`） |
|------|----------------|--------------------------------------------------|
| `lg=low` | 0 | **11** |
| `lg=medium` | 80 | **69** |
| `lg=high` | 1 | **1** |
| `pc=high ∧ lg=high` | 0 | **0** |

**`overall_severity_profile`（`map_severity_profile_m14`）**：仍为 **watch 19 / review 62 / critical_candidate 0**（`pc` 仍为 review 主导时，**整体档位对 `lg` 下沉不敏感**）。

---

## 五、代表 case（对比）

| 角色 | case | 收紧后 `lg` | 说明 |
|------|------|---------------|------|
| 合理保持为 **medium** | `R57_summary_looks_ok_but_requires_backfill_real` | **medium** | `local_only_risk=yes` + 主未到位，属典型摩擦 |
| 下沉为 **low** | `R1_container_real` | **low** | **weak exploration**（mixed + 无局部风险标志） |
| 仍为 **high** | `R4_feedback_effective_real` | **high** | `resume_fragility_declared_main_not_progressed` |
| **pc+lg 配对** | 任意 `pc=high` | 多为 **`lg=medium`**，少数 **`lg=low`** | **仍无** `pc=high∧lg=high`；**critical_candidate** 仍为 **0** |

---

## 六、风险评估

- **误报**：通过 **`weak_exploration`** 将部分场景从 **medium 降为 low**，刻意保留「多跳正常复杂度」空间；**未**把大批场景打成 **high**。  
- **漏报**：**`pc=high` + `lg=high`** 仍依赖 **`resume` 强信号与 closure 同帧对齐**；在 **run_summary** 未把 **ctx 期望 flag** 落入 **`inputs`** 前，**难以**仅靠审计层凭空造出 SF-1 组合——与 **Severity Signal Gap** 一致，**下一动因**更可能在 **summary/inputs 对齐** 或 **继续保守收紧 `lg`**，而非扩包硬撞。

---

## 七、测试与 smoke

- **单测**：`tests/test_local_global_progress_gradient_tightening.py`  
- **既有**：`tests/test_narrative_evidence_tension_review.py`  
- **Smoke**：`tools/smoke_local_global_progress_gradient_tightening.py` → `logs/smoke_local_global_progress_gradient.jsonl`  

---

## 八、最终问题（必须回答）

1. **`lg` 是否比之前更有梯度？** **是**：出现 **`low` 档**，`medium` 收窄，**原因字符串**可区分弱探索 / 结构停滞。  
2. **`pc+lg` 是否更有可能形成 future `critical_candidate`？** **部分**：梯度改善有利于人工与 severity **per_dimension** 阅读；**同帧 `pc=high∧lg=high` 仍为 0**，需 **resume/closure 与 task_chain 更强共显**（或未来 **inputs** 对齐）才可能稳定出现。  
3. **是否还要再动一轮 `lg`？** **可选**：若 **`run_summary`** 能稳定输出 **fragility / ctx 锚点** 到可消费字段，再收紧 **high** 的触发会更准；**当前**已可作为 **M0 收口**。  
4. **下一批扩包是否合适？** **可以**：`lg` 已非「恒 medium」；扩包时更易观察 **low vs medium** 分层。  
5. **`nt` 是否仍为第二优先级？** **是**；本轮 **未**动 `nt`。

---

## 九、本轮是否适合作为 `lg` 梯度专项收口

**适合。** 有 **前后统计**、**规则说明**、**代表 case**、**风险与边界**、**测试与 smoke**。

---

## 十、本轮是否通过

**通过。** 启发式已收紧，**只读审计层**；**未**改 benchmark / hard-fail / 主骨架。

**补记**：已进入 **`docs/RESUME_CLOSURE_SIGNAL_ALIGNMENT_REVIEW_M0.md`**，专门解释 **ctx / TCS / `run_summary_reference` 与 `pc∧lg` 不同步**（**非**本轮再改 `lg`）。

---

## 主线—白盒—日志

- **主线**：未改决策主链。  
- **白盒**：`lg` 仍与 `task_chain_progress_summary` / `run_summary` 同链。  
- **日志**：`logs/real_scenario_pack_m14.json`、`logs/local_global_gradient_analysis_m14.json`。  
- **最终判断**：**主线通顺，白盒一致，日志已落地**。
