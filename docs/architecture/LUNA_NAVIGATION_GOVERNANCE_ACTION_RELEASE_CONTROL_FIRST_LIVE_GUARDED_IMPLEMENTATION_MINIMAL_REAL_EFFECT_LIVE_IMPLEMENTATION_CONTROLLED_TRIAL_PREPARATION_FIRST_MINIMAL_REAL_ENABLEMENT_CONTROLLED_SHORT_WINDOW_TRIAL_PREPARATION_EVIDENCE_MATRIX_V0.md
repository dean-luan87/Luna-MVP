# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Live Implementation Controlled Trial Preparation First Minimal Real Enablement Controlled Short-Window Trial Preparation Evidence Matrix v0（证据矩阵冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_FIRST_MINIMAL_REAL_ENABLEMENT_CONTROLLED_SHORT_WINDOW_TRIAL_PREPARATION_EVIDENCE_MATRIX_V0.md`  
**性质**：Phase-Next-154：把 151/152/153 的关键证据矩阵化，用于形成 go/no-go pack 的证据底座（无代码）

---

## Evidence Matrix（写死字段）

字段说明：

- requirement_id
- source_phase
- source_artifact
- evidence_summary
- boundary_type: started | release | closure | illegal_path_detection | readiness | default_path_control
- status: satisfied | partially_satisfied | not_satisfied
- blocker_level: hard_blocker | soft_followup | informational

---

| requirement_id | source_phase | source_artifact | evidence_summary | boundary_type | status | blocker_level |
|---|---|---|---|---|---|---|
| R151-START-UNIQUE | 151 | `docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_FIRST_MINIMAL_REAL_ENABLEMENT_DEFINITION_V0.md` | start_event_observed 写死为唯一开始判据；dry-run/go/shadow_eval 均不构成 started 证据 | started | satisfied | hard_blocker |
| R151-RELEASE-PRECOND | 151 | 同上 | side_effects_released 放行条件写死：只有 started 后短时窗口语义允许，并必须可回落 | release | satisfied | hard_blocker |
| R151-CLOSURE-MIN | 151 | 同上 | 最小成功/失败/收口点写死：closure 后必须回到 se=false 或等价安全闭合 | closure | satisfied | hard_blocker |
| R152-ENTRY-EXPLICIT | 152 | `capabilities/governance/runtime/...controlled_trial_preparation_first_minimal_real_enablement_v0.py` | 真实入口为显式函数调用；未接默认路径 | default_path_control | satisfied | hard_blocker |
| R152-ARMING-NOT-STARTED | 152 | 同上 | 输出 armed_not_started=true，且 start_event_observed 前不置 started | started | satisfied | hard_blocker |
| R152-START-EVENT-WRITE | 152 | 同上 | trace/order 中写入 start_event_observed 并同步置 started=true | started | satisfied | hard_blocker |
| R152-WINDOW-AFTER-STARTED | 152 | 同上 | side_effects window 仅在 started 后语义开启，并最终 recover | release | satisfied | hard_blocker |
| R152-MIN-WRITES | 152 | 同上 | 真实副作用面仅三类：execution_state/result/exception_or_failure（失败时） | release | satisfied | hard_blocker |
| R152-SUCCESS-CLOSURE | 152 | 同上 | success 路径：state+result 写入后 recover false，closed=true | closure | satisfied | hard_blocker |
| R152-FAILURE-CLOSURE | 152 | 同上 | failure 路径：先 recover false，再 best-effort 失败写入收口，closed=true | closure | satisfied | hard_blocker |
| R153-EVAL-GO | 153 | `tools/validate_...shadowed_live_validation_evaluation_v0.py` + `docs/architecture/...SHADOWED_LIVE_VALIDATION_EVALUATION_V0.md` | overall_evaluation=go；9/9 场景通过 | readiness | satisfied | hard_blocker |
| R153-SCENARIOS-AI | 153 | 同上 + `docs/architecture/...SHADOWED_LIVE_VALIDATION_TEST_MATRIX_V0.md` | 覆盖 A–I：not_ready、go-only、dry-run-only、合法 success/failure、非法 release/started/unclosed 探针 | illegal_path_detection | satisfied | hard_blocker |
| R-NONDEFAULT-STILL-OFF | 152/153 | 152 runtime “explicit only” + 153 工具只显式调用 | 默认路径仍未开启（未引入自动触发通道） | default_path_control | satisfied | hard_blocker |

