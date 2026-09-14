# Phase-Next-178 — Meta-Governance Evidence Matrix v0

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_FIRST_CONTROLLED_SHORT_WINDOW_REAL_TRIAL_META_GOVERNANCE_EVIDENCE_MATRIX_V0.md`  
**阶段**：Phase-Next-178  
**用途**：将 151/155/158/159/162/163/166/167/170/171/174/175/176/177 的关键证据矩阵化，用于支撑 178 go/no-go 结论。  

---

## 字段（写死）

- **requirement_id**
- **source_phase**
- **source_artifact**
- **evidence_summary**
- **boundary_type**：`entry_gate | higher_order_prerequisite | allowed_meta_governance_outcome | forbidden_meta_governance_blocking | closed_safe_state | no_next_runtime | default_path_control | non_expansion`
- **status**：`satisfied | partially_satisfied | not_satisfied`
- **blocker_level**：`hard_blocker | soft_followup | informational`

---

## Evidence Matrix（v0）

| requirement_id | source_phase | source_artifact | evidence_summary | boundary_type | status | blocker_level |
|---|---:|---|---|---|---|---|
| MG-151-CLS-01 | 151 | 151 started/release/closure 冻结结论 | 闭合安全态基线（不默认放权、不隐式继续真实运行） | closed_safe_state | satisfied | informational |
| MG-155-GRD-01 | 155 | 155 short-window trial guardrail 冻结 | allow/deny/abort policy 冻结，禁止隐式扩围/长期化 | non_expansion | satisfied | informational |
| MG-158-RDY-01 | 158 | 158 readiness pack = go | readiness=go 仅为准备资格，不等于真实继续运行批准 | entry_gate | satisfied | informational |
| MG-159-EXE-01 | 159 | 159 execute definition | execute 边界冻结（与 readiness 分离） | higher_order_prerequisite | satisfied | informational |
| MG-162-EXE-GNG-01 | 162 | 162 execute go/no-go pack = go | execute 合法性资格包成立，不等于长期运行批准 | higher_order_prerequisite | satisfied | informational |
| MG-163-DEC-01 | 163 | 163 post-execute decision definition | decision allow/deny + closed-safe + no-auto-retry 冻结 | higher_order_prerequisite | satisfied | informational |
| MG-166-DEC-GNG-01 | 166 | 166 post-execute decision go/no-go pack = go | post-execute decision 资格成立（仍非真实继续运行批准） | entry_gate | satisfied | informational |
| MG-167-PDG-01 | 167 | 167 post-decision governance definition | lower-order governance 的 entry/allowlist/denylist/closed-safe/no-next-runtime 冻结 | non_expansion | satisfied | informational |
| MG-170-PDG-GNG-01 | 170 | 170 post-decision governance go/no-go pack = go | 进入 higher-order 治理链资格成立 | entry_gate | satisfied | informational |
| MG-171-HO-01 | 171 | 171 higher-order governance definition v0 | higher-order governance 边界冻结（为 meta-governance 上游输入） | higher_order_prerequisite | satisfied | informational |
| MG-174-HO-GNG-01 | 174 | 174 higher-order governance go/no-go pack = go | 进入 meta-governance 的资格成立 | entry_gate | satisfied | informational |
| MG-175-META-ENTRY-01 | 175 | 175 meta-governance definition v0 | meta-governance 唯一进入条件写死（higher-order legal + closed-safe + default path disabled + evidence/audit） | entry_gate | satisfied | informational |
| MG-175-META-OUT-01 | 175 | 175 meta-governance definition v0 | outcome 白名单与黑名单写死；禁止 implicit reopen/retry/widen/default-on/long-running | allowed_meta_governance_outcome | satisfied | informational |
| MG-176-ENTRY-01 | 176 | `capabilities/governance/runtime/...meta_governance_v0.py` | runtime 要求显式入口；不满足 => illegal + remain_closed_safe | entry_gate | satisfied | informational |
| MG-176-PREREQ-01 | 176 | 同上 | higher-order completed+legality+closed_safe+pack_ok+default_path_disabled 前置；不满足 => 保守/阻断 | higher_order_prerequisite | satisfied | informational |
| MG-176-ALLOW-01 | 176 | 同上 | 仅输出 175 allowlist；兜底非 allowlist 强制回落 safe outcome | allowed_meta_governance_outcome | satisfied | informational |
| MG-176-BLOCK-01 | 176 | 同上 | forbidden probes（implicit reopen/retry/widen/long-running 等）=> blocked=true + block outcome | forbidden_meta_governance_blocking | satisfied | informational |
| MG-176-CLOSE-01 | 176 | 同上 | 写死 `keeps_system_closed=true`、`closed_safe_state_preserved=true` | closed_safe_state | satisfied | informational |
| MG-176-NEXT-01 | 176 | 同上 | 写死 `allows_next_runtime_now=false`（no-next-runtime-now） | no_next_runtime | satisfied | informational |
| MG-177-ALL-01 | 177 | `tools/validate_release_control_meta_governance_shadowed_validation_evaluation_v0.py` 输出 | A–M 场景覆盖；summary：passed=14/14；integrity 全 pass；overall=go | non_expansion | satisfied | informational |
| MG-DEFAULT-OFF-01 | 176/177 | 176 runtime + 177 default_path_probe 场景 | default path 未开启且误触发被拦截（not_explicit_entry => illegal；default_path_enabled => block） | default_path_control | satisfied | informational |

