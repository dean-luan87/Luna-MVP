# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Live Implementation Controlled Trial Preparation First Controlled Short-Window Trial Guardrail Matrix v0（护栏矩阵冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_FIRST_CONTROLLED_SHORT_WINDOW_TRIAL_GUARDRAIL_MATRIX_V0.md`  
**性质**：Phase-Next-155：把 entry/window/runtime/abort/recovery 护栏矩阵化，防止后续 implementation 漏 guardrail（无代码）

---

## Guardrail Matrix（写死口径）

| guardrail_layer | guardrail_id | description | boundary_type | enforcement_point | required | abort_trigger_id_if_violated |
|---|---|---|---|---|---:|---|
| Entry | GR-ENTRY-NONDEFAULT | 必须非默认入口、显式调用、显式 intent + 人工确认/等价批准 | default_path_control | before_arm | 是 | audit_trace_missing_or_broken |
| Entry | GR-ENTRY-PACK-GO | 154 pack 结论必须为 go/conditional_go 且无 hard blocker | readiness | before_arm | 是 | trial_scope_expanded_without_definition |
| Window | GR-WIN-MAX-DURATION | 必须存在最大持续时间上限；禁止无限持续 | window_timeout | during_window | 是 | trial_window_timeout |
| Window | GR-WIN-MAX-ATTEMPTS | 必须存在最大尝试次数/并发限制 | unauthorized_scope | before_start/during_window | 是 | trial_scope_expanded_without_definition |
| Window | GR-WIN-MAX-SCOPE | 必须存在最大范围上限（环境/版本/链路/流量面） | unauthorized_scope | before_start/during_window | 是 | trial_scope_expanded_without_definition |
| Runtime | GR-RUN-START-UNIQUE | started 判据唯一：只能由 start_event_observed 触发 | started | start_gate | 是 | no_start_event_but_started |
| Runtime | GR-RUN-RELEASE-AFTER-STARTED | 未 started 不得 release；release 仅 started 后短时窗口允许且必须回落 | release | side_effects_window | 是 | no_started_but_release / se_not_recovered |
| Runtime | GR-RUN-SURFACE-ALLOWLIST | 只允许三类副作用面（state/result/exception_failure） | unauthorized_scope | during_window | 是 | unauthorized_side_effect_surface |
| Abort | GR-ABORT-IMMEDIATE | 任一越界条件出现必须立即 abort | abort_policy | during_window | 是 | closure_missing |
| Recovery | GR-RECOVER-SE-FALSE | abort/结束后必须 recover 到 se=false 或等价安全闭合态 | closure | after_abort/after_success | 是 | se_not_recovered |
| Recovery | GR-CLOSE-NO-HALFOPEN | 必须 closed=true；不得残留 started-but-unclosed | closure | end | 是 | closure_missing |

