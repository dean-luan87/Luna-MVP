# Phase-Next-169 — First Controlled Short-Window Real Trial Post-Decision Governance Shadowed Validation Evaluation v0

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_FIRST_CONTROLLED_SHORT_WINDOW_REAL_TRIAL_POST_DECISION_GOVERNANCE_SHADOWED_VALIDATION_EVALUATION_V0.md`  
**阶段**：Phase-Next-169  
**性质**：shadowed / guarded / evaluation-first（验证与评估层）  
**对象**：Phase-Next-168 post-decision governance runtime  
**约束继承**：151 / 155 / 158 / 159 / 162 / 163 / 166 / 167（不得改写）

---

## 0) 本阶段只做一件事（写死）

对 Phase-Next-168 的 post-decision governance 执行器做 shadowed validation / evaluation 闭环，回答：

1. 是否只在显式入口下生效（non-default）
2. 是否只有 decision 已 legal complete 且 closed-safe 后才能进入
3. 是否只会输出白名单 governance outcome
4. forbidden probe 是否都会被真正阻断
5. governance 后是否始终保持 closed-safe state
6. `allow_next_governance_preparation_under_same_guardrails` 是否始终不等于自动进入下一阶段 runtime
7. 是否具备进入下一阶段（post-decision governance go/no-go pack）资格

---

## 1) 严格边界（写死）

禁止：

- 不新增更大真实能力
- 不进入 full controlled trial
- 不开启默认路径
- 不扩大真实 side effects 面
- 不修改 167 definition
- 不扩张 168 能力边界（169 不是重构）

允许：

- 新增 shadowed validation harness / evaluation 工具
- 新增 validation docs / test matrix
- 只读 trace/telemetry 汇总（不改变运行行为）

---

## 2) 主验证工具（短文件名等价声明）

由于 macOS 文件名长度限制，169 主工具采用短文件名承载，功能等价于长命名要求：

- **主工具（短文件名）**：`tools/validate_release_control_post_decision_governance_shadowed_validation_evaluation_v0.py`
- **等价长命名（不落盘，仅声明）**：  
  `tools/validate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_first_controlled_short_window_real_trial_post_decision_governance_shadowed_validation_evaluation_v0.py`

主工具必须复用：

- 168 runtime：`capabilities/governance/runtime/...post_decision_governance_v0.py`
- 168 的场景与断言口径（并输出结构化 evaluation）

## 2.1 Test Matrix 文件名限制声明

由于 macOS 文件名长度限制，169 的 test matrix 采用短文件名承载，功能等价于长命名要求：

- **Test Matrix（短文件名）**：`docs/architecture/LUNA_RELEASE_CONTROL_POST_DECISION_GOVERNANCE_SHADOWED_VALIDATION_TEST_MATRIX_V0.md`
- **等价长命名（不落盘，仅声明）**：  
  `docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_FIRST_CONTROLLED_SHORT_WINDOW_REAL_TRIAL_POST_DECISION_GOVERNANCE_SHADOWED_VALIDATION_TEST_MATRIX_V0.md`

---

## 3) Validation 目标边界（按 167 维度冻结口径）

必须验证并给出结构化结果：

- **entry_gate_integrity**：显式入口；默认路径不触发
- **decision_prerequisite_integrity**：decision legal complete 前不得进入
- **allowed_governance_outcome_integrity**：只能输出 allowlist
- **forbidden_governance_block_integrity**：forbidden probes 必须阻断
- **closed_safe_state_integrity**：治理前后 closed-safe 始终成立
- **no_next_runtime_integrity**：`allows_next_runtime_now=false` 写死

---

## 4) go / conditional_go / no_go（仅 169 评估结论，不替代正式治理链）

### go

- entry / prerequisite / allowlist / blocking / closed-safe / no-next-runtime 全部成立
- 非法路径均被正确拦截

### conditional_go

- 核心边界成立
- 但 trace/readability/reason codes 仍需补强（不影响安全成立）

### no_go

任一出现即 no_go：

- 无 legal decision completion 却进入 governance
- 输出 forbidden governance outcome
- governance 后破坏 closed-safe state
- 出现隐式 reopen / retry runtime / widen / long-running / default-on
- `allow_next_governance_preparation_under_same_guardrails` 变成自动进入下一阶段 runtime
- default path 存在误触发风险

---

## 5) 本阶段验收标准

输出：

- 新增/修改文件清单
- 覆盖场景列表（A–M）
- 结构化 evaluation 报告（含 overall_evaluation 与 recommended_next_step）

并明确声明：

- 默认路径仍未开启
- 本阶段未进入 full controlled trial
- 本阶段没有扩大真实 side effects 面

