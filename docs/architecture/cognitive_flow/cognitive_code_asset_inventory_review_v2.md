# Cognitive Code Asset Inventory Review v2

## Method

This is a targeted delta review built on the existing Code Baseline Review. It does not repeat a full inventory; it checks assets whose role changed after Neural Governance, CWO, Provider Management, and Evidence Gateway were frozen.

| File / module area | Current role | Architecture layer | Dependency / authority observation | Status |
|---|---|---|---|---|
| `cognitive/contracts/candidate.py` | Immutable Candidate contract. | Brain/Foundation contract. | Explicitly excludes fact, command, decision, permission, action, memory write, and state mutation. | KEEP |
| `cognitive/contracts/signal.py`, `snapshot.py`, `runtime/tick.py` | Signal/snapshot/event-driven cognitive skeleton. | Brain/Foundation contract. | Synthetic candidate-only operation. | KEEP |
| `cognitive/kernel/`, `attention/`, `organization/`, `process/`, `runtime/instance.py` | Controlled organization skeleton. | Brain-side controlled skeleton. | Emits candidates and trace; no Scheduler/executor/provider call. | KEEP |
| `cognitive/evidence/`, `cognitive/adapters/` | Synthetic evidence/visual/language/audio adapter placeholders. | Evidence boundary placeholder. | Source contract currently accepts synthetic sources only. | MIGRATE |
| Neural Governance / CWO / Objective Alignment code | No dedicated runtime module found. | Neural Governance. | Present as architecture contracts/docs only. | REPLACE by future approved skeleton |
| `runtime/main_loop.py` and sibling runtime | Legacy fixed loop with decision/execution chain. | Parallel legacy runtime. | Must not join A-route controlled chain. | DEPRECATE from A-route |
| `capabilities/midplatform/model_manager/` | Matching/admission/resource/routing/lifecycle/fallback/diagnostics/trace assets. | Provider Management support. | Capability-first candidate logic exists; still legacy API/task references. | MIGRATE |
| `capabilities/midplatform/core/task_manager/` | Task lifecycle, decomposition, dependencies, execution candidates. | Middleware execution organization candidate. | Own `task_goal` / `task_plan` terminology must be CWO-adapted. | MIGRATE |
| `field_perception_orchestrator/`, `vision_manager/`, `ocr_manager/`, `speech_manager/` | Domain capability orchestration/facades. | Middleware + Provider adapter estate. | Candidate/diagnostic assets reusable after CWO boundary. | MIGRATE |
| `capabilities/registry/` + manifests/lifecycle/baselines | Capability governance source. | Middleware governance input. | Canonical source; baseline is engineering governance only. | KEEP |
| `models/ocr/*`, `models/yolo/yolov5n.pt` | Local model artifacts/manifests. | Potential Provider artifacts. | Not connected to A-route; presence does not grant Provider readiness. | KEEP isolated |
| `tools/evaluation/`, `cognitive/validation/` | Validators, dry-runs, replay/traces, synthetic controlled tests. | Validation/diagnostics. | Good controlled-test base; not Provider Invocation Runtime. | KEEP |
| `model_test_lens/` + local bridge | Static UI, test lens, runner bridge, diagnostic panels. | Future read-only Whitebox base. | Must not become cognitive control endpoint. | MIGRATE presentation |

## Inventory conclusion

The repository can host a Controlled Provider Invocation Skeleton, but only after a narrow adapter implementation phase. The current code does not yet implement CWO transport, Neural Governance, Provider Session lifecycle, or a non-synthetic Evidence Gateway.
