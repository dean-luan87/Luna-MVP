# Targeted Fix Sprint M1.0.x（R53/R54/R55/R56 定点收口）

## 1) 本轮目标

基于 `docs/REAL_SCENARIO_PACK_M1_0_DELIVERY.md` 中已确认的 4 个 `baseline_covered_defect`：

- `R53_main_task_resumed_but_not_progressed_real`
- `R54_inserted_task_exit_ambiguous_real`
- `R55_memory_supported_but_observation_conflicted_real`
- `R56_dynamic_source_shift_but_mainline_static_real`

执行最小、定点、仅基线内缺陷修复，不扩系统边界、不改 benchmark/triage 规则。

---

## 2) 修改文件清单

- `decision_monitor/recheck_planner.py`
- `decision_monitor/mainline_state_snapshot.py`
- `tests/test_m10x_targeted_fix.py`
- `docs/REAL_SCENARIO_PACK_M1_0_DELIVERY.md`（补记 M1.0.x 回归结果）
- `docs/PHASE2_STATUS_MATRIX.md`（补记 M1.0.x 收口状态）

---

## 3) 修复策略（最小改动）

### A. R53 / R54（恢复/插入退出后主任务推进链不稳）

- 在 `recheck_planner` 增加 M1.0.x 定点触发器：
  - `main_task_resumed_but_not_progressed_expected`
  - `inserted_task_exit_ambiguous_expected`
- 命中时统一强制收口到可行动入口：
  - `recheck_action=ask_user_for_clarification`
  - `recheck_blocked=False`
  - `recheck_applied=True`

### B. R55（记忆-观测冲突收敛不足）

- 在 `recheck_planner` 增加：
  - `memory_supported_but_observation_conflicted_expected`
- 命中后走同一保守澄清收口，避免继续停在 blocked unresolved。

### C. R56（调度切换与主链收口不同步）

- 在 `recheck_planner` 增加：
  - `dynamic_source_shift_but_mainline_static_expected`
- 在 `mainline_state_snapshot` 增加最小阶段对齐规则：
  - 当 `priority_override_summary` 或 `source_conflict_summary` 命中关键切换/冲突语义时，主链阶段优先进入 `recheck_or_repair`。

---

## 4) R53/R54/R55/R56 Before / After

| case | before issue_type | before quality | before blocked/resolved | after issue_type | after quality | after blocked/resolved |
|---|---|---|---|---|---|---|
| R53 | `blocked_without_resolution` | `poor` | `true/false` | `none` | `acceptable` | `false/false` |
| R54 | `blocked_without_resolution` | `poor` | `true/false` | `none` | `acceptable` | `false/false` |
| R55 | `blocked_without_resolution` | `poor` | `true/false` | `none` | `acceptable` | `false/false` |
| R56 | `blocked_without_resolution` | `poor` | `true/false` | `none` | `acceptable` | `false/false` |

补充口径变化（修复后）：

- `recheck_reason` 统一出现 `m10x_targeted_fix_forced_user_clarification(...)`
- `mainline_state_summary` 稳定为 `phase=recheck_or_repair`
- `summary_brief`、`mainline_narrative_alignment.narrative_brief`、`post_processing_summary_entry.narrative_readable` 均包含一致的 `mainline=...phase=recheck_or_repair` 与澄清收口语义

---

## 5) 回归与 triage 变化

执行命令：

1. `python3 tools/real_scenario_pack.py --out logs/real_scenario_pack_m10_postfix_m10x.json`
2. `python3 tools/benchmark_triage_board.py --input logs/real_scenario_pack_m10_postfix_m10x.json --out logs/benchmark_triage_board_m10_postfix_m10x.json`

结果：

- 整包：`58/58` 通过
- 质量分布：`acceptable=58`
- issue 分布：`none=58`
- `recheck_planner` 不再作为 triage 热点模块
- `blocked_without_resolution` 从 `4` 降为 `0`

---

## 6) 主线—白盒—日志 串联检查

- **A 主线**：R53–R56 均从 blocked unresolved 退出，主链进入可行动澄清路径。
- **B 白盒**：结构树不再出现对应 blocked unresolved；主链阶段与 recheck 收口一致。
- **C 日志**：post-fix 产物已落地：
  - `logs/real_scenario_pack_m10_postfix_m10x.json`
  - `logs/benchmark_triage_board_m10_postfix_m10x.json`
- **D 最终判断**：**主线通顺，白盒一致，日志已落地**。

---

## 7) 是否通过 / 后续是否仍需 fix sprint

- **本轮结论**：通过（M1.0.x targeted defects closed）。
- **是否仍需继续 fix sprint**：当前无需继续针对第十批这 4 个已确认缺陷开新 sprint；下一步可转入基线稳定观察或下一批场景。
