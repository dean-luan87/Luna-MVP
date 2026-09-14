# Legacy Middleware Asset Inventory v1

## Phase and method

- Phase: `Phase-Cognitive-Middleware-Reintegration-Architecture-v1-001`
- Execution mode: V0 — read-only architecture review, mapping, and boundary design.
- Sources: existing Code Baseline Review, Capability Governance baseline, and read-only inspection of current repository assets.

## Inventory

| Asset | Current role / authority | Data flow observed | Future role | Migration status |
|---|---|---|---|---|
| `cognitive/` controlled skeleton | Candidate, Signal, Snapshot, Tick, Kernel, Attention, organization, synthetic evidence/adapters, validation. Candidate-only; no external invocation. | Synthetic signal → candidates → trace. | Cognitive Brain/Foundation boundary; remains separate from legacy runtime. | KEEP |
| `runtime/main_loop.py` | Legacy fixed-loop decision/execution chain. | Fixed tick → `decide` → execution intent. | Isolate from A-route; future review only behind Decision–Execution boundary. | DEPRECATE from A-route |
| `capabilities/midplatform/model_manager/` | Capability matching, admission, provider identity/selection candidates, ownership/resource evaluation, lifecycle, fallback, diagnostics, trace/replay. | Requested capability → candidates → selection/routing candidate → diagnostics/trace. | Provider Management / Resolver input within Cognitive Middleware. | MIGRATE |
| `capabilities/registry/luna_capability_registry_v1.json` + manifests/lifecycle/baselines | Capability module registry, manifests, lifecycle, calibration/baseline governance. | Governance metadata → module eligibility/lifecycle evidence. | Canonical Capability Governance source. | KEEP |
| `model_admission_governance/` and `permission_and_admission_manager/` | Model/skill admission and candidate-only permission checks. | Provider admission/lifecycle gating. | Shared Provider Admission dependency. | KEEP |
| `protocol_manager/` and `protocols/` | Protocol registry, compatibility, change control, trace/replay governance. | Protocol validation across modules. | Shared Protocol Governance dependency. | KEEP |
| `core/task_manager/` | Legacy task lifecycle, task decomposition, dependencies, recovery, execution-request candidates. Input includes `task_goal`; output includes `task_plan`. | Task request → plan/subtasks → execution candidates/status. | Middleware execution-organization adapter after CWO translation; no Goal/Intent ownership. | MIGRATE |
| `field_perception_orchestrator/` | Candidate-only field-perception planning and controlled visual handoff. | Field/task context → perception plan → visual handoff candidate. | Sense capability organization input, CWO-scoped. | MIGRATE |
| `vision_manager/`, `ocr_manager/`, `speech_manager/`, `observation_manager/` | Domain capability manager/facade assets. | Capability-local request → domain output/diagnostics. | Sense Capability Providers / adapters under Middleware. | MIGRATE |
| `model_adapters/`, Provider adapters, local runtime adapters | Provider-specific adaptation/parsing/normalization. | Provider request/response conversion. | Provider Adapter layer. | KEEP with boundary adaptation |
| `model_manager/collaboration/*` and evidence fusion helpers | Multi-provider candidate/fusion/conflict/dry-run assets. | Provider candidates → fused/diagnostic candidates. | Evidence Gateway supporting assets; semantic authority removed. | MIGRATE |
| `model_test_lens/` static site, runner bridge, trace/replay panels | Model/runner diagnostics and local visual test lens. | UI → controlled runner/trace views. | Cognitive Whitebox projection base; read-only/control-plane view. | MIGRATE |
| `tools/evaluation/` and module runners/verifiers | Controlled evaluation, diagnostics, trace/replay verification. | Fixture → module runner → verifier/report. | Validation and diagnostics infrastructure. | KEEP |
| `agent_planning/`, `decision_validation/`, navigation/teacher planning assets | Legacy planning/decision-oriented modules. | Planning/decision candidate paths. | Outside A-route middleware reintegration; preserve as legacy/future separately governed routes. | DEPRECATE from A-route |

## Inventory conclusion

The legacy estate contains reusable execution-governance primitives. The main migration need is authority relocation: legacy task/model-first entry points must become Middleware consumers of Neural-issued CWO, while Registry, Admission, Lifecycle, Protocol, Diagnostics, and Trace assets remain reusable foundations.
