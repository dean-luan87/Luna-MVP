# Actual Mutation Surface v1

| Surface | Evidence | Result |
|---|---|---|
| Field admission | `field_event_admission_api_v1.py:132-230` returns `FieldEventAdmissionResultV1`; `candidate_only=True`, `fact_admitted=False`, `field_state_modified=False`, `reducer_executed=False`. | No bypass found. |
| Field reducer | `field_state_reducer/` contains the reducer/module boundary and state transition types. | Canonical source mutation candidate; active caller chain was not executed in this audit. |
| Current World | `current_world_representation_envelope_v1.py:20-55` is frozen/read-only; context integration builds current-world candidates. | No authoritative World Truth write found in reviewed paths. |
| Gateway | `real_visual_evidence_gateway_adapter_v1.py:125-187` rejects `truth_declared`/`fact_admitted` inputs and returns candidate observation. | No source mutation. |
| Cognitive controlled outputs | Controlled engines use frozen dataclasses and explicit negative flags. | Candidate-only evidence, not runtime proof. |
| Real Provider | `field_perception_real_vision_provider_adapter_v1.py:265-288` calls `run_yolo_on_unit_v0` and sets `invocation_performed=True` in its real branch. | Execution surface; authority chain gap recorded as F-001. |

No audited path was found that mutates Field, Current World, Intent, Task, Memory, or Experience merely by producing a Provider/Action/Evidence candidate. Static presence of `write_text` in runners is artifact persistence, not canonical source-state mutation.

