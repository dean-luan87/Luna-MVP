# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Live Implementation Controlled Trial Preparation First Controlled Short-Window Real Trial Execute Shadowed Validation Evaluation v0（审计层冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_FIRST_CONTROLLED_SHORT_WINDOW_REAL_TRIAL_EXECUTE_SHADOWED_VALIDATION_EVALUATION_V0.md`  
**阶段**：Phase-Next-161  
**性质**：对 Phase-Next-160 “真实 execute 执行器”做 shadowed/guarded/evaluation-first 的验证与评估闭环（不扩实现、不 default-on、不 full controlled trial）

---

## 1) 阶段目标（写死）

161 只回答：

1. 160 是否只在显式入口下生效（非默认路径）
2. execute intent + approval + readiness_go gate 是否不可绕过
3. `start_event_observed` 是否仍是唯一 started 判据
4. `side_effects_released` 是否只在合法 started 后短时打开并在 final close 后回落
5. timeout / unauthorized surface / audit trace breakage / readiness 缺失 是否都能触发 stop/abort
6. success / failure 两条路径是否都能稳定 recovery + final close
7. 160 是否具备进入下一阶段 execute go/no-go pack 的资格（仅 161 评估建议，不替代正式治理链最终裁决）

---

## 2) 严格边界（写死）

禁止：

- 不修改 151/155/158/159 definition
- 不扩大 160 副作用面
- 不新增 default path
- 不把 real trial execute 扩成 full controlled trial
- 不改变 started 判据
- 不改变 stop/abort trigger 语义
- 不改变 recovery/final close 契约
- 不把 validation 写成 implementation 重构

允许：

- 新增 shadowed validation harness / evaluation 工具
- 新增 validation docs / test matrix
- 如有必要，补充只读 telemetry/trace 汇总（不写外部系统）
- 更新文档索引

---

## 3) 核心产出（本阶段必须存在）

### 3.1 主验证工具（必须）

`tools/validate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_first_controlled_short_window_real_trial_execute_shadowed_validation_evaluation_v0.py`

要求：

- 复用 Phase-Next-160 runtime
- 复用 Phase-Next-160 verifier（先决条件：verifier 必须先通过）
- 场景化跑 A–M
- 输出结构化 JSON 报告（每场景 + 总体摘要）
- 给出 `go / conditional_go / no_go`（仅作为 161 评价，不替代正式治理链）

### 3.2 冻结本阶段验证口径（本文档）

本文档冻结 161 的目标、边界、结论口径，明确 **161 是审计层**。

### 3.3 测试矩阵（可选但推荐）

`docs/architecture/..._EXECUTE_SHADOWED_VALIDATION_TEST_MATRIX_V0.md`：把场景与预期矩阵化，便于复盘与审计。

---

## 4) 评估输出口径（写死）

主工具输出必须包含（每个场景）：

- `scenario_name`
- `expected_outcome`
- `actual_outcome`
- `explicit_entry_seen`
- `execute_intent_seen`
- `approval_seen`
- `readiness_go_seen`
- `start_event_observed_seen`
- `started_seen`
- `side_effects_released_seen`
- `stop_trigger_seen`
- `abort_trigger_seen`
- `recovery_seen`
- `final_close_seen`
- `rollback_seen`
- `illegal_state_detected`
- `pass_or_fail`
- `evaluation_reason_codes`

总体摘要必须包含：

- `total_scenarios`
- `passed_scenarios`
- `failed_scenarios`
- `entry_gate_integrity`
- `readiness_gate_integrity`
- `started_boundary_integrity`
- `release_boundary_integrity`
- `stop_abort_integrity`
- `recovery_integrity`
- `final_close_integrity`
- `overall_evaluation`
- `recommended_next_step`

---

## 5) go / conditional_go / no_go 判定（写死）

### go

- 显式入口与 intent/approval/readiness_go gate 全成立
- started / release / stop/abort / recovery / final close 边界全部成立
- 非法路径都被正确拦截或被识别为 illegal
- success / failure 都能稳定收口

### conditional_go

- 核心安全边界成立
- 但证据组织（telemetry/trace/reason codes 可读性）仍可补强
- 不影响 execute 边界的安全成立

### no_go（任一即 no_go）

- 无 `start_event_observed` 却 started
- 无 started 却 release
- 无 readiness_go 却 execute
- timeout/unauthorized/audit break 无法 stop/abort
- stop/abort 后不能 recovery
- final close 缺失
- final close 后 se 不回落为 false
- 存在 default-on 误触发风险

---

## 6) 明确声明（写死）

- **默认路径仍未开启**
- **本阶段未进入 full controlled trial**
- **本阶段没有扩大真实 side effects 面**

