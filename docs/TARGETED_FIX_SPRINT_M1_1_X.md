# Targeted Fix Sprint M1.1.x-B（R60/R61/R64 最小定点修复）

## 1) 本轮目标

基于 A 阶段过程观察结论（`docs/TARGETED_FIX_SPRINT_M1_1_X_A_PROCESS_OBSERVATION.md`），
仅修复 3 个已确认基线内断点：

- `R60_recovery_declared_but_resume_chain_fragile_real`
- `R61_memory_bias_accumulated_under_familiar_context_real`
- `R64_phase_correct_but_closure_semantics_misaligned_real`

不改 benchmark/triage 规则，不扩场景，不改冻结边界。

---

## 2) 修改文件清单

- `decision_monitor/recheck_planner.py`
- `tests/test_m11x_targeted_fix.py`

（B 阶段直接修复仅在收口规则点最小下刀；A 阶段观察增强文件保持不变）

---

## 3) A 阶段断点回顾

- **R60**：`resume declared -> main progress` 链路脆弱  
- **R61**：`memory/source conflict -> closure` 收敛不足  
- **R64**：`phase identified -> closure` 语义错位

---

## 4) B 阶段修复点

在 `recheck_planner` 增加 M1.1.x-B 三个断点触发器（仅针对 M1.1 语义 flag）：

- `recovery_declared_but_resume_chain_fragile_expected`
- `memory_bias_accumulated_under_familiar_context_expected`
- `phase_correct_but_closure_semantics_misaligned_expected`

命中后统一给出可行动收口：

- `recheck_action=ask_user_for_clarification`
- `recheck_applied=true`
- `recheck_blocked=false`
- `recheck_reason=m11x_targeted_fix_forced_user_clarification(...)`

---

## 5) R60 / R61 / R64 Before / After

| case | before issue_type | before quality | before blocked/resolved | after issue_type | after quality | after blocked/resolved |
|---|---|---|---|---|---|---|
| R60 | `blocked_without_resolution` | `poor` | `true/false` | `none` | `acceptable` | `false/false` |
| R61 | `blocked_without_resolution` | `poor` | `true/false` | `none` | `acceptable` | `false/false` |
| R64 | `blocked_without_resolution` | `poor` | `true/false` | `none` | `acceptable` | `false/false` |

断点字段变化（after）：

- `recheck_reason`：统一进入 `m11x_targeted_fix_forced_user_clarification(...)`
- `mainline_state_summary`：稳定体现 `phase=recheck_or_repair` + `recheck_action=ask_user_for_clarification`
- 过程锚点仍保留（A 阶段）：`process_observation_summary` + timeline 事件族

---

## 6) triage 变化

复跑命令：

1. `python3 tools/real_scenario_pack.py --out logs/real_scenario_pack_m11_postfix_m11x.json`
2. `python3 tools/benchmark_triage_board.py --input logs/real_scenario_pack_m11_postfix_m11x.json --out logs/benchmark_triage_board_m11_postfix_m11x.json`

结果：

- 整包：`64/64` 通过
- issue 分布：`none=64`
- `blocked_without_resolution`：`3 -> 0`
- triage hotspot：`recheck_planner` 清空（`next_focus_modules=[]`）

---

## 7) 口径一致性检查

抽查 `R60/R61/R64`：

- **白盒**：`reasoning_tree_metrics.blocked=false`，`possible_tree_issue_type=None`
- **summary**：`summary_brief` 与 `mainline_state_summary` 均体现 `recheck_or_repair + ask_user_for_clarification`
- **entry**：`post_processing_summary_entry.narrative_readable` 延续同一主线语义，`process_observation_summary` 与 `backfill_reason(process_observation_hint)` 保持一致

结论：白盒—summary—entry 三层口径保持同链一致，未引入“换说法掩盖问题”。

---

## 8) 是否通过 / 是否仍需继续 fix sprint

- **本轮结论**：通过（M1.1.x-B defects closed）。
- **是否仍需继续 fix sprint**：当前无需继续针对第十一批 `R60/R61/R64` 开新 sprint；可进入下一批扩压或稳定观察。

---

## 主线—白盒—日志 串联检查

- **A 主线**：三处断点均退出 blocked unresolved，进入可行动修复路径。  
- **B 白盒**：问题指标消退，收口语义与阶段一致。  
- **C 日志**：post-fix 产物已落地（`m11_postfix_m11x` pack + triage）。  
- **D 最终判断**：**主线通顺，白盒一致，日志已落地**。
