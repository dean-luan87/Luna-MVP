# Cognitive Code Alignment Review v1

## Architecture-to-code matrix

| A-route architecture element | Current code location | Alignment | Readiness note |
|---|---|---|---|
| Evidence Candidate | `cognitive/evidence/evidence.py`, `evidence_contract.py` | Aligned | Immutable/synthetic evidence skeleton exists; no real adapter invocation. |
| External capability adapters | `cognitive/adapters/visual_adapter.py`, `language_adapter.py`, `audio_adapter.py` | Partially aligned | Synthetic-only contracts demonstrate boundary; real capabilities remain unconnected. |
| Information Field | Candidate / planning boundary in root cognitive plus legacy information-processing contracts | Partial | No dedicated live Information Field implementation; do not infer one from legacy assets. |
| Internal Representation | Contracts and architecture documentation | Planned / partial | No dedicated representation runtime package found in root `cognitive/`. |
| Schema | Architecture documentation / legacy cognitive-flow candidates | Planned / partial | No canonical root schema runtime found. |
| Current World Understanding | Legacy candidate assets under `capabilities/cognitive_flow/` | Partial | Requires contract alignment to root Candidate before reuse. |
| Context | Candidate traces in `cognitive/organization/organization.py` | Skeleton aligned | Context candidate exists in controlled flow; no autonomous context runtime. |
| Goal contextualization | Candidate traces in `cognitive/organization/organization.py` | Skeleton aligned | Goal is candidate-only and not decision authority. |
| Attention Candidate | `cognitive/attention/attention_contract.py`; organization synthetic pool | Aligned (skeleton) | Source aggregation is deterministic/synthetic only. |
| Attention Controller | `cognitive/attention/controller.py` | Aligned (skeleton) | Allocation candidate only; no sensor/module call, scheduler, or action. |
| Kernel | `cognitive/kernel/kernel.py`, `kernel_contract.py` | Aligned (skeleton) | Emits constraint/consistency/arbitration candidates only. |
| Capability Composition | synthetic capability bundle in `cognitive/organization/organization.py`; process composer | Partial | No standalone composition module; current bundle is controlled trace data only. |
| Resource Modulation | resource candidate in organization skeleton | Planned / partial | No resource-monitoring or dynamic modulation runtime. |
| Workspace | architecture docs and controlled traces | Planned | No `cognitive/workspace/` package; no workspace runtime should be inferred. |
| Simulation / Operation / Evaluation | architecture docs and controlled execution/trace assets | Planned / boundary-only | No live A-route implementations. |
| Process Composer | `cognitive/process/composer.py`, `process_contract.py` | Aligned (skeleton) | Process description is explicitly non-executable. |
| Runtime Instance | `cognitive/runtime/instance.py` | Aligned (skeleton) | Immutable temporary record, not State/executor. |
| Cognitive Tick | `cognitive/runtime/tick.py` | Aligned (contract) | Event trigger model exists; no live scheduler. |
| Controlled execution / trace / replay | `cognitive/runtime/controlled_execution.py`; `cognitive/validation/` | Aligned (V1 synthetic) | Synthetic trace/replay/stress verification only. |
| Reducer boundary | `cognitive/governance/reducer_boundary.py` | Aligned | Candidate-only guard protects State-mutation boundary. |
| Decision / Action | No root cognitive decision/action runtime | Correctly absent | Must remain outside A-route controlled skeleton. |

## Boundary comparison

| Concern | Root `cognitive/` status | Legacy estate risk | Required treatment |
|---|---|---|---|
| Candidate → State | Explicitly guarded | Older modules may use independent lifecycle/state concepts | Keep Reducer boundary authoritative; adapt only candidate-shaped outputs. |
| Event-driven cognition | Tick contract is trigger-based | `runtime/main_loop.py` is fixed interval and decision/execution oriented | Do not reuse legacy loop as Cognitive Runtime. |
| Attention authority | Allocation is candidate-only | Legacy visual/model/task modules contain local policies and routing | Local priority may propose attention only; Controller remains the future allocation authority. |
| Model authority | Real-input adapters are synthetic/no-invoke | OCR, detection, SLAM, model manager have model/provider surfaces | Route all live capability output through EvidenceCandidate and admission. |
| Process authority | Composer is descriptive only | Task-manager includes workflow/dependency mechanics | Keep workflow external; do not let it replace cognitive organization. |

## Reassessment result

The codebase supports the next controlled implementation step for **governance skeleton extension only**, but does not yet support a real Cognitive Runtime. Missing runtime-level elements include live Evidence Field admission, workspace lifecycle, representation/schema runtime, capability-composition runtime, resource modulation, and any approved external capability adapter.

**A-route code alignment status: `KEEP` for root cognitive skeleton; `MIGRATE` for legacy candidate/capability inputs; `REPLACE` for old direct cognitive control paths.**
