# Real Scenario Pack M1.3 Delivery（第十三批真实场景扩包）

**文件**：`docs/REAL_SCENARIO_PACK_M1_3_DELIVERY.md`  
**本轮定位**：在 **M0.6 冻结基线**之上，在已引入 **`narrative_evidence_tension_review`**（见 `docs/NARRATIVE_EVIDENCE_TENSION_REVIEW_M0.md`）后的**首次**扩包压测：除 harness **hard fail** 外，开始系统记录 **「中高张力但仍通过」** 的辅助观察。**不**将 tension 升级为 hard-fail，**不**改 benchmark/triage 判定规则。

**硬约束**：

- 正式问题仍只分三类：`baseline_covered_defect` / `baseline_excluded_requirement` / `reserve_only_finding`。  
- 辅助标签 **`tension_observed_but_not_failed`** 仅用于交付文档与 `logs/real_scenario_pack_m13.json` 中 `summary.tension_audit`，**不**替代上述三类。

---

## §1. 本轮定位

在 **M1.0 + M1.0.x**、**M1.1 + M1.1.x**、**M1.2** 稳定基线及 **tension 审计层** 之后，第十三批新增 `R71–R76`，联合观察：

1. hard fail（仍以既有 harness 为准）  
2. **tension 高/中但仍通过**（`tension_audit`）  
3. 叙事顺滑、证据支撑偏弱等长期风险  
4. 局部推进与全局主任务推进的张力  
5. entry/summary/whitebox 口径一致下的**共识性偏移**风险（审计层提示）

---

## §2. 新增 case 清单

| case_id | 方向 |
|---------|------|
| `R71_locally_consistent_but_globally_slow_main_progress_real` | A 全局推进不足、局部可解释 |
| `R72_narrative_complete_but_event_support_sparse_real` | B 叙事完整感 vs 事件支撑 |
| `R73_familiar_pattern_bias_stable_without_explicit_failure_real` | C 熟悉语境下偏差稳定化 |
| `R74_phase_closure_reasonable_but_outcome_claim_too_full_real` | D phase/closure vs outcome 叙述 |
| `R75_entry_story_complete_but_backfill_signal_suppressed_real` | E 顺滑叙事 vs backfill 契约 |
| `R76_task_resume_ok_locally_but_global_goal_still_drifting_real` | A/E 局部恢复 vs 全局漂移 |

---

## §3. 整包结果摘要

命令：

1. `python3 tools/real_scenario_pack.py --out logs/real_scenario_pack_m13.json`  
2. `python3 tools/benchmark_triage_board.py --input logs/real_scenario_pack_m13.json --out logs/benchmark_triage_board_m13.json`

结果（`logs/real_scenario_pack_m13.json`）：

- 总 case：**76**  
- passed：**76**  
- failed：**0**  
- quality：**acceptable = 76**  
- issue：**none = 76**（无 `blocked_without_resolution`）

**Pack 附加摘要**（不改变 pass/fail）：

- `summary.tension_audit.tension_observed_but_not_failed_count`：**75**  
- 说明：在 **M0 启发式**下，凡任一维度为 **medium/high** 且 **scenario_passed** 的 case 计入；**`R3_general_search_real`** 为全包中**唯一**未落入该列表的 case（五维均为 **none/low**，未达「中高」阈值）。

---

## §4. triage 摘要

来自 `logs/benchmark_triage_board_m13.json`：

- **最差 case（排序占位）**：`R1_container_real`、`R2_occlusion_real`（全 acceptable 时的默认 triage）。  
- **top modules**：**—**  
- **top issues**：**—**

---

## §5. 正式问题分类（三类）

### `baseline_covered_defect`

- **本轮**：**无** harness 级新失败；未出现 `poor` 或 `blocked_without_resolution`。

### `baseline_excluded_requirement`

- **全局推进可证明性**、**正式任务引擎**、**图书馆真写入**、**污染深治理** 等仍为冻结外；不因本批 tension 观察而自动升格为「当前失败」。

### `reserve_only_finding`

- 将 **tension 升级为 soft-fail / 自动判因** 仍属后续专题；**benchmark 规则未改**，故记入 future gap。

---

## §6. tension 观察摘要（辅助标签）

**定义**：`tension_observed_but_not_failed` — `scenario_passed=true` 且 `narrative_evidence_tension_review` 中至少一维为 **medium** 或 **high**。

### 6.1 全包统计

- 计入数量：**75 / 76**（见 §3）。  
- **R71–R76** 均计入，且与多批旧 case 类似，在 M0 启发式下常出现：  
  - `phase_closure_outcome_tension=high`（与 `closure_semantics_misalignment_summary` 等过程显影强相关）  
  - `summary_backfill_tension=high`（与 `post_processing` 多通道 backfill 契约一致）  
  - `local_global_progress_tension=medium`  
  - `memory_bias_tension=high`  
- **`narrative_trace_support_tension`** 在本批新增 case 上多为 **none**（`nt:none`），因时间轴/事件条数相对叙事长度未必触发「叙事↔事件」失衡阈值——**适合作为未来收紧启发式或 soft-fail 的候选**。

### 6.2 是否建议 future review

- **是**：对 **narrative_trace_support** 的触发条件做专题复核（与 M1.3 目标 B 对齐），避免长期依赖「顺但不硬」仅靠其它四维。  
- **是**：将 **tension_audit** 与 **分诊/版本化基线** 绑定，便于对比批次差异（**不**在本轮改 triage 规则）。

---

## §7. 六项正式验收 + 第七项 tension 观察

1. **主导源是否讲得清**：整包仍为 acceptable；**未**因 tension 改验收口径。  
2. **任务位置是否讲得清**：`R71`/`R76` 等仍通过 harness；全局推进是否「足够快」属 **基线外** 可证明性。  
3. **记忆/个性化偏差是否讲得清**：`R73` 等 tension 上 **memory_bias** 常为 high，**可读作审计提示**，非 harness 失败。  
4. **主链状态/阶段是否讲得清**：`R74` 等 **phase_closure** 张力高，与 **closure 语义显影** 一致，**不**等于 phase 错。  
5. **Summary/Narrative/白盒同口径**：未改契约；**tension** 只标「可能需回溯」方向。  
6. **后处理入口边界是否守住**：`R75` 等 **summary_backfill** 仍为 high，**表示契约仍要求回溯**，与「故事顺」并存。  

7. **高 tension 但仍通过**：**75** 个 case 符合辅助定义；含 **R71–R76** 全部。唯一例外 **R3** 五维未达 medium/high，可作为 **低张力对照**。

---

## §8. 当前是否需要开 fix sprint

**不需要**（针对 M1.3 harness 结果）。  
理由：整包 **76/76**，无新的 `baseline_covered_defect` 指标；tension 为观察层。若后续要 **收紧 narrative↔event 启发式** 或 **引入 soft-fail**，可单独立项，**非**本批强制 fix。

---

## §9. 本轮是否通过

**通过（扩包 + tension 摘要落地 + 冻结口径保持）。**

理由：新增 `R71–R76`、产物路径齐全、`summary.tension_audit` 可复现；**未**将 tension 接入 hard-fail。

---

## 主线—白盒—日志一致性检查

- **A 主线**：新 case 均经 `DecisionMonitorBuilder` 构建并进入整包。  
- **B 白盒**：tension 依据 **同帧** summary/entry/快照/时间轴，**不**替代白盒本体。  
- **C 日志**：`logs/real_scenario_pack_m13.json` 含每 case 的 `narrative_evidence_tension_review` 字段；`logs/benchmark_triage_board_m13.json` 为 triage 产物。  
- **D 最终判断**：**主线通顺，白盒一致，日志已落地**。
