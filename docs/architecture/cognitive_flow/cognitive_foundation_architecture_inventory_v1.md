# Cognitive Foundation Architecture Inventory v1

## Phase

`Phase-Cognitive-Foundation-Architecture-Reconciliation-and-Whitebox-Reintegration-v1-001`  
Execution mode: V0 — read-only architecture reconciliation and whitebox planning.

## A-route architecture inventory

| Layer | Current assets / concepts | Role | Boundary |
|---|---|---|---|
| Cognitive Brain | Goal, Context, Attention Controller, Self State, Workspace, Simulation, Evaluation, Feedback, Intent; root `cognitive/` candidate/snapshot/tick/kernel skeleton. | Defines what requires understanding and evaluates cognitive sufficiency candidates. | No direct Provider/model/hardware call; no final Truth/Decision/Action. |
| Neural Governance | Intent translation, Neural signals, CWO, signal organization, objective alignment, feedback aggregation, protocol/trace governance. | Translates and supervises cognitive work. | No provider execution, resource enforcement, truth, decision, action, or state mutation. |
| Cognitive Middleware | Situation Report, objective decomposition, Capability Execution Candidate, Provider Management, resource/lifecycle constraints, Evidence Gateway, diagnostics. | Organizes how a CWO may be served. | No Goal, Attention, cognitive completion, truth, decision, action. |
| Provider | OCR, VLM, segmentation/SAM, SLAM/spatial, ASR and future external capability families. | Returns bounded local outputs only. | No direct Brain link or Reality assertion. |
| Evidence / Feedback | Evidence Adapter/Gateway, Middleware Report, Neural Feedback Package, Brain Update Candidate. | Preserves provenance, uncertainty, scope, conflict, and coverage. | Evidence ≠ Truth; feedback ≠ direct state update. |
| Whitebox / validation | Model Test Lens, trace/replay, diagnostics, runners/verifiers, synthetic cognitive validation. | Read-only observability and controlled validation. | No cognitive control, State mutation, or implicit provider invocation. |

## Existing code/asset placement

| Asset area | Reconciled layer | Status |
|---|---|---|
| `cognitive/` | Cognitive Foundation controlled skeleton. | KEEP |
| `capabilities/registry/`, manifests, lifecycle, baseline | Middleware Capability Governance. | KEEP as canonical governance input |
| `capabilities/midplatform/model_manager/` | Provider Management support. | MIGRATE semantically, no rewrite yet |
| Task/field perception/vision/OCR/speech managers | Middleware execution/capability organization and Provider adapters. | MIGRATE through CWO boundary |
| Model Test Lens and local runner bridge | Cognitive Whitebox / test-only observability base. | KEEP + MIGRATE presentation |
| legacy `runtime/main_loop.py` and planning/decision routes | Parallel legacy generation. | Isolate / DEPRECATE from A-route |

## Reconciliation conclusion

The A-route has a complete authority chain for controlled capability use. The remaining work is implementation of approved adapters and controlled invocation skeletons—not new cognitive modules or a replacement middleware estate.
