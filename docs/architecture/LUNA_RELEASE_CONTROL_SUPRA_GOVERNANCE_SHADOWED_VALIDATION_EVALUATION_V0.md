# Phase-Next-181 — Supra-Governance Shadowed Validation / Evaluation v0（短文件名承载）

**状态**：validation/evaluation 文档冻结（v0）  
**性质**：只读审计层；不是新 runtime；不扩大真实 side effects；不进入 full controlled trial；不启用默认路径  

---

## 1. 短文件名等价承载声明（必要）

由于 macOS 文件系统对单文件名长度上限（通常 255 bytes）约束，Phase-Next-181 的“长命名目标文件名”长度接近上限（工具 251，文档 247/248），为避免路径前缀/工具链追加后触发 `OSError: [Errno 63] File name too long`，本阶段采用短文件名承载。

- **长命名目标（等价）**：
  - `tools/validate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_first_controlled_short_window_real_trial_supra_governance_shadowed_validation_evaluation_v0.py`
  - `docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_FIRST_CONTROLLED_SHORT_WINDOW_REAL_TRIAL_SUPRA_GOVERNANCE_SHADOWED_VALIDATION_EVALUATION_V0.md`
  - `docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_FIRST_CONTROLLED_SHORT_WINDOW_REAL_TRIAL_SUPRA_GOVERNANCE_SHADOWED_VALIDATION_TEST_MATRIX_V0.md`
- **短文件名实际承载（本仓库真实路径）**：
  - 工具：`tools/validate_release_control_supra_governance_shadowed_validation_evaluation_v0.py`
  - 评估文档（本文）：`docs/architecture/LUNA_RELEASE_CONTROL_SUPRA_GOVERNANCE_SHADOWED_VALIDATION_EVALUATION_V0.md`
  - 测试矩阵：`docs/architecture/LUNA_RELEASE_CONTROL_SUPRA_GOVERNANCE_SHADOWED_VALIDATION_TEST_MATRIX_V0.md`

以上短文件名与长命名目标在功能与语义上**等价承载** Phase-Next-181 产出。

---

## 2. 阶段目标（仅此一件事）

对 Phase-Next-180 的 `supra-governance runtime` 做一层 **shadowed / guarded / evaluation-first** 的验证与评估闭环，用于回答：

1. 是否只在**显式入口**下生效（非默认路径）
2. 是否只有 `meta-governance` **legal complete** 且 **closed-safe** 后才能进入 supra-governance
3. 是否只会输出白名单 `allowed supra-governance outcome`
4. forbidden probes（隐式 reopen/retry/widen/long-running/default-on 等）是否都会被**真正阻断**
5. supra-governance 后是否始终保持 **closed-safe state**
6. `allow_next_governance_preparation_under_same_guardrails` 是否**不等于**自动进入下一阶段 runtime（仍必须 `allows_next_runtime_now=false`）
7. 180 是否具备进入下一阶段 `supra-governance go/no-go pack` 的资格（注意：181 结论不替代正式治理链）

---

## 3. 严格限制（本阶段必须遵守）

**禁止**：
- 不修改 Phase-Next-179 definition
- 不扩大 Phase-Next-180 runtime 能力边界
- 不新增/启用默认路径（default path）
- 不把 supra-governance 扩成真实执行链（retry/reopen/widen/long-running）
- 不改变 allowed/forbidden/closed-safe/no-next-runtime-now 的语义
- 不把 validation 写成 implementation 重构

**允许**：
- 新增 shadowed validation harness / evaluation tool
- 新增 evaluation 文档 / test matrix
- 只读 telemetry / reason codes 汇总（不引入真实 side effects）
- 更新 `docs/architecture/README.md` 索引

---

## 4. 被验证对象与依赖冻结事实（输入约束）

**被验证对象**（Phase-Next-180 runtime）：
- `capabilities/governance/runtime/navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_first_controlled_short_window_real_trial_supra_governance_v0.py`

**冻结事实（不在 181 修改）**：
- 151：started/release/closure 基础边界冻结
- 155：short-window trial guardrail 冻结
- 158：real trial readiness pack = go
- 159：real trial execute definition 冻结
- 162：execute go/no-go pack = go
- 163：post-execute decision definition 冻结
- 166：post-execute decision go/no-go pack = go
- 167：post-decision governance definition 冻结
- 170：post-decision governance go/no-go pack = go
- 171：higher-order governance definition 冻结
- 174：higher-order governance go/no-go pack = go
- 175：meta-governance definition 冻结
- 178：meta-governance go/no-go pack = go
- 179：supra-governance definition 冻结

**明确声明（仍保持）**：
- 默认路径仍未开启
- full controlled trial 仍未开始
- 本阶段不扩大真实 side effects 面

---

## 5. 验证覆盖（A–M 场景集）

181 工具至少覆盖以下场景（与 179/180 边界直接对应）：
- A `no_legal_meta_completion`
- B `closed_safe_not_preserved`
- C `evidence_incomplete`
- D `clean_supra_case`
- E `governance_boundary_violation_case`
- F `widening_needed_case`
- G `forbidden_reopen_probe`
- H `forbidden_retry_runtime_probe`
- I `forbidden_widen_probe`
- J `forbidden_long_running_probe`
- K `default_path_probe`（not explicit entry / default path enabled）
- L `require_new_evidence_case`
- M `structural_block_case`

细化的“场景 → 预期字段与 outcome”矩阵见测试矩阵文档（Phase-Next-181）。

---

## 6. Evaluation 输出口径冻结（结构化字段）

工具输出为 JSON，至少包含：
- scenario_name / expected_outcome / actual_outcome
- explicit_supra_governance_entry_seen
- meta_governance_completed_seen / meta_governance_legality_seen
- closed_safe_state_seen
- evidence_complete_seen / boundary_violation_seen
- allowed_supra_governance_outcome_selected
- forbidden_supra_governance_outcome_blocked
- requires_new_governance_definition / human_confirmation_required
- allows_next_runtime_now / closed_safe_state_preserved / illegal_state_detected
- pass_or_fail / evaluation_reason_codes

总体摘要至少包含：
- total_scenarios / passed_scenarios / failed_scenarios
- entry_gate_integrity / meta_prerequisite_integrity
- allowed_supra_governance_outcome_integrity / forbidden_supra_governance_block_integrity
- closed_safe_state_integrity / no_next_runtime_integrity
- overall_evaluation / recommended_next_step

---

## 7. go / conditional_go / no_go 判定建议（仅 181 评估层）

**go**：
- 只有 legal meta completion + closed-safe 后才能进入
- outcome 白名单成立
- forbidden probes 全部被阻断
- closed-safe 始终成立
- `allows_next_runtime_now=false` 始终成立（不自动进入下一 runtime）
- 非法路径都被拦截

**conditional_go**：
- 核心边界成立
- 但 trace/telemetry/reason code 可读性或证据组织仍需补强

**no_go**（任一触发即 no-go）：
- 无 legal meta completion 却进入
- 输出 forbidden outcome 或 allowlist 外 outcome
- governance 后破坏 closed-safe
- 出现隐式 reopen/retry/widen/long-running/default-on
- `allow_next_governance_preparation_under_same_guardrails` 被实现成自动进入下一 runtime
- default path 存在误触发风险

