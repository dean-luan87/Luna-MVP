# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Live Implementation Controlled Trial Preparation First Controlled Short-Window Real Trial Post-Execute Decision Shadowed Validation Evaluation v0（审计层冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_FIRST_CONTROLLED_SHORT_WINDOW_REAL_TRIAL_POST_EXECUTE_DECISION_SHADOWED_VALIDATION_EVALUATION_V0.md`  
**阶段**：Phase-Next-165  
**性质**：对 Phase-Next-164 post-execute decision runtime 做 shadowed/guarded/evaluation-first 的验证与评估闭环（不扩实现、不 default-on、不 full controlled trial）

---

## 1) 阶段目标（写死）

165 只回答：

1. 164 是否只在显式入口下生效
2. 是否只有 execute 已 legal final close 后才能进入 decision
3. 是否只会输出白名单 outcome
4. forbidden outcome probe 是否都会被真正阻断
5. decision 后是否始终保持 closed-safe state
6. `retry_allowed_under_same_guardrails` 是否始终不等于自动 retry
7. 164 是否具备进入下一阶段 decision go/no-go pack 的资格（仅 165 评估建议，不替代正式治理链最终裁决）

---

## 2) 严格边界（写死）

禁止：

- 不修改 163 的 definition
- 不扩大 164 的能力边界
- 不新增 default path
- 不把 post-execute decision 扩成真实继续执行链
- 不改变 allowed outcome 语义
- 不改变 forbidden outcome blocker 语义
- 不改变 closed-safe-state 契约
- 不把 validation 写成 implementation 重构

允许：

- 新增 shadowed validation harness / evaluation 工具
- 新增 validation docs / test matrix
- 如有必要，补充只读 telemetry/trace 汇总（不写外部系统）
- 更新文档索引

---

## 3) 核心产出（本阶段必须存在）

### 3.1 主验证工具（必须）

**注意**：原计划的超长工具文件名在 macOS 上可能超过单文件名长度上限（255）。本仓库采用短文件名承载 165 工具。

- `tools/validate_release_control_post_execute_decision_shadowed_validation_evaluation_v0.py`

要求：

- 复用 Phase-Next-164 runtime
- 复用 Phase-Next-164 verifier（先决条件：verifier 必须先通过）
- 覆盖 A–M 场景
- 输出结构化 JSON 报告（每场景 + 总体摘要）
- 给出 `go / conditional_go / no_go`（仅作为 165 评价，不替代正式治理链）

### 3.2 冻结本阶段验证口径（本文档）

本文档冻结 165 的目标、边界、结论口径，明确 **165 是审计层**。

### 3.3 测试矩阵（可选但推荐）

`docs/architecture/..._POST_EXECUTE_DECISION_SHADOWED_VALIDATION_TEST_MATRIX_V0.md`：把场景与预期矩阵化，便于复盘与审计。

---

## 4) 评估输出口径（写死）

主工具输出必须包含（每个场景）：

- `scenario_name`
- `expected_outcome`
- `actual_outcome`
- `explicit_decision_entry_seen`
- `execute_closed_seen`
- `side_effects_released_false_seen`
- `execute_legality_seen`
- `evidence_complete_seen`
- `boundary_violation_seen`
- `allowed_outcome_selected`
- `forbidden_outcome_blocked`
- `human_confirmation_required`
- `requires_new_governance_definition`
- `allows_retry_now`
- `closed_safe_state_preserved`
- `illegal_state_detected`
- `pass_or_fail`
- `evaluation_reason_codes`

总体摘要必须包含：

- `total_scenarios`
- `passed_scenarios`
- `failed_scenarios`
- `entry_gate_integrity`
- `final_close_prerequisite_integrity`
- `allowed_outcome_integrity`
- `forbidden_block_integrity`
- `closed_safe_state_integrity`
- `no_auto_retry_integrity`
- `overall_evaluation`
- `recommended_next_step`

---

## 5) go / conditional_go / no_go 判定（写死）

### go

- 只有 legal final close 后才能进入 decision
- allowed outcome 语义成立
- forbidden outcome 都被正确阻断
- closed-safe state 始终成立
- retry_allowed 不会变成自动 retry
- 非法路径都被正确拦截

### conditional_go

- 核心边界成立
- 但 telemetry、reason code、trace 可读性、证据组织等仍可补强
- 不影响当前 decision legality 的安全成立

### no_go（任一即 no_go）

- 无 legal final close 却进入 decision
- 输出 forbidden outcome
- decision 后破坏 closed-safe state
- 出现隐式 reopen / retry / widen / full-trial continuation / default-on transition
- `retry_allowed_under_same_guardrails` 被实现成自动重试
- default path 存在误触发风险

---

## 6) 明确声明（写死）

- **默认路径仍未开启**
- **本阶段未进入 full controlled trial**
- **本阶段没有扩大真实 side effects 面**

