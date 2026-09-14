# Cognitive Architecture–Code Mapping v2

## Mapping matrix

| Architecture module | Current code / asset mapping | Alignment | Gap or risk |
|---|---|---|---|
| Brain contracts | `cognitive/contracts/`, `attention/`, `kernel/`, `organization/`, `process/`, synthetic runtime/validation. | Partial / strong skeleton. | Domain modules are synthetic, not full Brain runtime. |
| Goal / Context / Self State | Candidate payloads in controlled skeleton; architecture documents. | Partial. | No dedicated current-state model implementation for latest architecture. |
| Neural Governance | Architecture documents and signal contracts only. | Missing runtime skeleton. | Must not be improvised inside Middleware/Task Manager. |
| Intent → CWO | Architecture contracts only. | Missing runtime skeleton. | Requires immutable CWO adapter/trace contract later. |
| Middleware Situation Report | Existing Model Manager diagnostics/resource/lifecycle and domain manager outputs. | Partial reusable assets. | No unified CWO-scoped report adapter. |
| Objective Decomposition | Legacy Task Manager + field perception/model routing assets. | Partial reusable assets. | Legacy task goal/plan semantics can leak cognitive authority. |
| Provider Management | Model Manager matching/admission/routing/fallback/lifecycle. | Strong reusable base. | Must accept CWO-derived requirements rather than legacy task entry. |
| Provider Session | Candidate concepts / legacy runners. | Missing controlled-session skeleton. | Runners/bridges must remain test-only. |
| Evidence Gateway | Synthetic `cognitive/evidence/`; legacy normalizers/fusion helpers. | Partial. | No unified non-synthetic Gateway implementation. |
| Neural Feedback | Architecture documents; legacy traces/diagnostics. | Missing. | Must preserve unknown/conflict and not update Brain directly. |
| Whitebox | Model Test Lens static site and trace panels. | Strong visual base. | Needs trace schema projection after controlled tests, not before. |

## Duplicate and authority checks

- **Missing:** Neural Governance, CWO, Provider Session, Middleware Report, Objective Alignment, and non-synthetic Evidence Gateway code boundaries.
- **Potential duplicates:** legacy Task Manager decomposition and Neural CWO translation; only Middleware may adapt CWO to execution work.
- **Potential bypass:** legacy Model Manager/runner paths may produce model results outside the Evidence Gateway unless future adapters force the new contract.
- **No approved direct bridge:** current `cognitive/adapters/` are synthetic only, so they cannot be used for real provider/model integration.

## Mapping result

Current code supports a future narrow controlled skeleton, not a live A-route capability loop. Architecture–code alignment is **partial and directionally consistent**, provided legacy paths remain isolated until adapters are approved.
