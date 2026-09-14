# Phase-Next-170 — Post-Decision Governance Evidence Matrix v0

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_FIRST_CONTROLLED_SHORT_WINDOW_REAL_TRIAL_POST_DECISION_GOVERNANCE_EVIDENCE_MATRIX_V0.md`  
**阶段**：Phase-Next-170  
**用途**：将 151/155/158/159/162/163/166/167/168/169 的关键证据矩阵化，用于支撑 170 go/no-go 结论。  

---

## 字段（写死）

- **requirement_id**
- **source_phase**
- **source_artifact**
- **evidence_summary**
- **boundary_type**：`entry_gate | decision_prerequisite | allowed_governance_outcome | forbidden_governance_blocking | closed_safe_state | no_next_runtime | default_path_control | non_expansion`
- **status**：`satisfied | partially_satisfied | not_satisfied`
- **blocker_level**：`hard_blocker | soft_followup | informational`

---

## Evidence Matrix（v0）

| requirement_id | source_phase | source_artifact | evidence_summary | boundary_type | status | blocker_level |
|---|---:|---|---|---|---|---|
| EM-151-CLS-01 | 151 | 151 started/release/closure 冻结结论 | close 后保持安全态（不放权默认开启）作为上游不扩张基线 | closed_safe_state | satisfied | informational |
| EM-155-GRD-01 | 155 | 155 short-window trial guardrail 冻结 | allow/deny/abort policy 冻结，禁止隐式扩围/长期化 | non_expansion | satisfied | informational |
| EM-158-RDY-01 | 158 | 158 readiness pack = go | readiness=go 仅代表准备就绪，不等于 execute/继续真实运行 | entry_gate | satisfied | informational |
| EM-159-EXE-01 | 159 | 159 execute definition | execute 语义与边界冻结（与 readiness 分离） | decision_prerequisite | satisfied | informational |
| EM-162-EXE-GNG-01 | 162 | 162 execute go/no-go pack = go | execute 合法性资格包成立，不等于长期运行批准 | decision_prerequisite | satisfied | informational |
| EM-163-DEC-01 | 163 | 163 post-execute decision definition | decision outcome allow/deny + closed-safe + no-auto-retry 冻结 | decision_prerequisite | satisfied | informational |
| EM-166-DEC-GNG-01 | 166 | 166 post-execute decision go/no-go pack = go | 进入 post-decision governance chain 的资格成立（仍不等于真实继续运行批准） | entry_gate | satisfied | informational |
| EM-167-GOV-ENTRY-01 | 167 | 167 governance definition v0 | governance 唯一进入条件：decision legal complete + closed-safe + default path disabled + evidence/audit | entry_gate | satisfied | informational |
| EM-167-GOV-OUT-01 | 167 | 167 governance definition v0 | outcome 白名单与黑名单写死；禁止 implicit reopen/retry/widen/default-on/long-running | allowed_governance_outcome | satisfied | informational |
| EM-168-ENTRY-01 | 168 | `capabilities/governance/runtime/...post_decision_governance_v0.py` | runtime 要求显式入口；不满足 => illegal + remain_closed_safe | entry_gate | satisfied | informational |
| EM-168-PREREQ-01 | 168 | 同上 | decision_completed + decision_legality + closed_safe + default_path_disabled 前置；不满足 => 保守/阻断 | decision_prerequisite | satisfied | informational |
| EM-168-ALLOW-01 | 168 | 同上 | 仅输出 167 allowlist；兜底非 allowlist 强制回落 safe outcome | allowed_governance_outcome | satisfied | informational |
| EM-168-BLOCK-01 | 168 | 同上 | forbidden probes（implicit reopen/retry/widen/long-running 等）=> blocked=true + block outcome | forbidden_governance_blocking | satisfied | informational |
| EM-168-CLOSE-01 | 168 | 同上 | 写死 `keeps_system_closed=true`、`closed_safe_state_preserved=true` | closed_safe_state | satisfied | informational |
| EM-168-NEXT-01 | 168 | 同上 | 写死 `allows_next_runtime_now=false`（no-next-runtime-now） | no_next_runtime | satisfied | informational |
| EM-169-ALL-01 | 169 | `tools/validate_release_control_post_decision_governance_shadowed_validation_evaluation_v0.py` 输出 | A–M 场景覆盖；summary：passed=14/14；integrity 全 pass；overall=go | non_expansion | satisfied | informational |
| EM-169-DEF-01 | 169 | 169 evaluation 文档 | 明确 169 仅验证/评估，不是实现扩张/放权 | non_expansion | satisfied | informational |
| EM-DEFAULT-OFF-01 | 168/169 | 168 runtime + 169 default_path_probe 场景 | default path 未开启且误触发被拦截（not_explicit_entry => illegal） | default_path_control | satisfied | informational |

