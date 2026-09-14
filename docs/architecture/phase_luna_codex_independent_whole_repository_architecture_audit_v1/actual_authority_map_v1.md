# Actual Authority Map v1

| Boundary | Actual evidence | Classification | Audit result |
|---|---|---|---|
| A/local cognition | `cognitive_dynamic_loop_engine_v1.py:143-289` forms candidate Need/Sufficiency/Reconsideration and requires candidate-only inputs. | CANONICAL / controlled | No active competing caller proven. |
| Loop | `cognitive_loop_continuity_candidate_engine_v1.py:99-126` derives local dispositions, but the package is candidate-only; `loop_semantic_to_mechanical_cutover` maps supplied A decisions to mechanical commands. | COMPATIBILITY_ONLY | No active runtime caller proven; semantics are a P2 audit surface, not P0. |
| Decision/Action/Runtime | `cognitive_execution_chain_engine_v1.py:55-61,572-784` composes Intent, Decision, Action, and Runtime Executor in a controlled integration. | COMPATIBILITY_ONLY | Candidate-only summary and no external runtime call found. |
| Evidence/Gateway | `real_visual_evidence_gateway_adapter_v1.py:100-260` rejects truth/fact mutation and constructs candidate evidence/observation plus trace. | CANONICAL / controlled | No direct Field/World write found in this adapter. |
| Field | `field_event_admission_api_v1.py:132-230` validates event candidates and returns reducer input; `reducer_adapter_v1.py` explicitly does not invoke the reducer. | CANONICAL | Admission/reducer split is present. |
| Model/Provider | `field_perception_real_vision_provider_adapter_v1.py:225-315` has its own provider admission candidate and invokes YOLO when `execute_real_provider=True`. | ACTIVE_OVERLAP | See F-001. |
| Diagnostics | Health/drift evidence is represented in multiple candidate records; no direct registry repair or Provider invocation was found in reviewed core paths. | CANONICAL / partial | Runtime-wide remediation authority not proven. |

