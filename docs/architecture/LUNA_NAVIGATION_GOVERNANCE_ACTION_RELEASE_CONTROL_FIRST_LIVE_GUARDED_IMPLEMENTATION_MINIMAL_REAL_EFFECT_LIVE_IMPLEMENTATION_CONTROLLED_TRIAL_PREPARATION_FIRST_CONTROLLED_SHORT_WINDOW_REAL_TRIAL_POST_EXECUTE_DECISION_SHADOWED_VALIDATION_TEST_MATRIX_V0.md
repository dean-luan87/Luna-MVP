# Phase-Next-165 — First Controlled Short-Window Real Trial Post-Execute Decision Shadowed Validation Test Matrix v0

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_FIRST_CONTROLLED_SHORT_WINDOW_REAL_TRIAL_POST_EXECUTE_DECISION_SHADOWED_VALIDATION_TEST_MATRIX_V0.md`  
**目标**：把 Phase-Next-164 post-execute decision runtime 的验证场景与预期（entry/final-close prerequisite/outcome-blocking/closed-safe-state）矩阵化，供 165 工具与报告对齐复盘。

---

## 覆盖原则（写死）

- 165 只做验证/评估，不扩 164，不改变 163 语义
- 只有 execute legal final close（closed=true 且 se=false）才允许进入 decision
- outcome 只能是 allowlist；任何 forbidden probe 必须被阻断
- decision 后必须保持 closed-safe state，且 `allows_retry_now=false`（不允许自动重试）

---

## 场景矩阵（A–M）

说明：

- **explicit_entry**：是否通过显式入口调用（165 工具均为 true；除非明确 probe）
- **final_close_prereq**：是否满足 execute legal final close
- **expected_outcome**：应选择的 allowed_outcome_selected（或被 blocked/not_eligible）

| 场景 | 名称 | explicit_entry | final_close_prereq | expected_status | expected_outcome | forbidden_blocked | closed_safe | no_auto_retry |
|---|---|---:|---:|---|---|---:|---:|---:|
| A | no_legal_final_close | true | false | not_eligible | remain_closed_safe | false | true | true |
| B | se_not_false | true | false | not_eligible | remain_closed_safe | false | true | true |
| C | evidence_incomplete | true | true | decided | remain_closed_safe | false | true | true |
| D | clean_success_case | true | true | decided | retry_allowed_under_same_guardrails | false | true | true |
| E | boundary_violation_case | true | true | decided | retry_not_allowed_until_new_definition | false | true | true |
| F | widening_needed_case | true | true | decided | escalate_for_new_governance_definition | false | true | true |
| G | forbidden_reopen_probe | true | true | blocked | remain_closed_safe | true | true | true |
| H | forbidden_retry_probe | true | true | blocked | remain_closed_safe | true | true | true |
| I | forbidden_widen_probe | true | true | blocked | remain_closed_safe | true | true | true |
| J | default_path_probe | false | (n/a) | blocked | remain_closed_safe | false | true | true |
| K | structural_safety_issue | true | true | decided | stop_and_block_further_real_action | false | true | true |
| L | forbidden_full_trial_continuation_probe | true | true | blocked | remain_closed_safe | true | true | true |
| M | forbidden_default_on_transition_probe | true | true | blocked | remain_closed_safe | true | true | true |

---

## 关键断言（用于 165 评价口径）

- **entry gate integrity**：J 必须 blocked（无显式入口不得进入）
- **final close prerequisite integrity**：A/B 必须 not_eligible 且 remain_closed_safe
- **allowed outcome integrity**：C/D/E/F/K outcome 必须落在 allowlist 且符合预期
- **forbidden block integrity**：G/H/I/L/M 必须 blocked 且 forbidden_outcome_blocked=true
- **closed safe state integrity**：所有场景 `closed_safe_state_preserved=true`
- **no auto retry integrity**：所有场景 `allows_retry_now=false`

