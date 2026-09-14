# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Live Implementation Controlled Trial Preparation First Controlled Short-Window Trial Shadowed Validation Evaluation v0（审计层冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_FIRST_CONTROLLED_SHORT_WINDOW_TRIAL_SHADOWED_VALIDATION_EVALUATION_V0.md`  
**阶段**：Phase-Next-157  
**性质**：对 Phase-Next-156 的短窗 trial runtime 做 shadowed/guarded/evaluation-first 的验证与评估闭环（不扩实现、不 default-on、不 full controlled trial）

---

## 1) 阶段目标（写死）

157 只回答以下问题（且必须可复盘、可解释、可定位到 entry/start/release/abort/recovery/closure 边界）：

1. 156 是否只在显式入口下生效（非默认路径）
2. 显式 intent + approval gate 是否不可绕过
3. `start_event_observed` 是否仍是唯一 started 判据
4. `side_effects_released` 是否只在合法 started 后短时打开，并在 closure 后回落为 `false`
5. timeout / unauthorized surface / audit trace breakage 是否都能触发 abort
6. success / failure 两条路径是否都能稳定 recovery + closure
7. 156 是否具备进入下一阶段（Phase-Next-158 readiness pack）的资格（**仅是 157 评估结论**，不替代正式治理链的最终 go/no-go）

---

## 2) 严格限制（写死）

禁止事项：

- 不修改 151/155 definition
- 不扩大 156 的真实副作用面（side effects surfaces 不得增加）
- 不新增 default-on / 默认路径触发
- 不把 short-window trial 扩成 full controlled trial
- 不改变 started 判据（仍以 `start_event_observed` 为唯一 started 判据）
- 不改变 abort trigger 语义
- 不改变 recovery / closure 契约
- 不把 validation 写成 implementation 重构

允许事项：

- 新增 shadowed validation harness / evaluation 工具
- 新增 validation docs / test matrix
- 如有必要，补充只读 telemetry/trace 汇总（不影响主链，不写入真实外部系统）
- 更新文档索引

---

## 3) 核心产出（本阶段必须存在）

### 3.1 主验证工具（必须）

`tools/validate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_first_controlled_short_window_trial_shadowed_validation_evaluation_v0.py`

要求：

- 复用 Phase-Next-156 runtime（短窗 trial 执行器）
- 复用 Phase-Next-156 verifier（作为先决条件：156 自测必须先通过）
- 场景化跑 A–K（至少覆盖：entry gate、started、release、abort、recovery、closure、default_path_probe、closure_break_probe）
- 输出结构化 JSON 报告（每场景 + 总体摘要）
- 给出 `go / conditional_go / no_go`（仅作为 157 的评价，不替代正式治理链）

### 3.2 冻结本阶段验证口径（本文档）

本文档冻结 157 的目标、边界、结论口径，明确 **157 是审计层**。

### 3.3 测试矩阵（可选但推荐）

`docs/architecture/..._SHADOWED_VALIDATION_TEST_MATRIX_V0.md` 用于把场景与预期矩阵化，便于复盘与审计。

---

## 4) 评估输出口径（写死）

主工具输出必须包含（每个场景）：

- `scenario_name`
- `expected_outcome`
- `actual_outcome`
- `explicit_entry_seen`
- `explicit_intent_seen`
- `approval_seen`
- `start_event_observed_seen`
- `started_seen`
- `side_effects_released_seen`
- `abort_trigger_seen`
- `recovery_seen`
- `closure_seen`
- `rollback_seen`
- `illegal_state_detected`
- `pass_or_fail`
- `evaluation_reason_codes`

总体摘要必须包含：

- `total_scenarios`
- `passed_scenarios`
- `failed_scenarios`
- `entry_gate_integrity`
- `started_boundary_integrity`
- `release_boundary_integrity`
- `abort_integrity`
- `recovery_integrity`
- `closure_integrity`
- `overall_evaluation`
- `recommended_next_step`

---

## 5) go / conditional_go / no_go 判定（写死）

### go

- 显式入口与 intent/approval gate 全成立
- started / release / abort / recovery / closure 边界全部成立
- 非法路径都被正确拦截
- success / failure 都能稳定收口

### conditional_go

- 核心安全边界成立
- 但证据组织（telemetry/trace/reason codes 可读性）仍可补强
- 不影响短窗 guardrail 的安全成立

### no_go（任一即 no_go）

- 无 `start_event_observed` 却出现 started
- 无 started 却 release
- timeout / unauthorized / audit break 不能 abort
- abort 后不能 recovery
- closure 缺失
- closure 后 `side_effects_released` 不回落为 false
- 存在 default-on 误触发风险

---

## 6) 明确声明（写死）

- **默认路径仍未开启**
- **本阶段未进入 full controlled trial**
- **本阶段没有扩大真实 side effects 面**

