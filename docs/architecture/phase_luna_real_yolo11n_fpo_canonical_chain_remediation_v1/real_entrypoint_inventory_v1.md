# Real Entrypoint Inventory v1

| Entrypoint | Classification | Real load/invocation | Result |
|---|---|---|---|
| `yolo11n_single_frame_execution/run_yolo11n_real_single_frame_provider_execution_v1.py:run` | ACTIVE_EXECUTION_SURFACE / controlled real-capable | `run_authorized_vision_provider_v1` → `run_yolo_on_unit_v0` | Now requires canonical binding context for `real=True`. |
| `run_a_route_s3_real_vision_yolo_evidence_controlled_replacement_v1.py:run` | CONTROLLED_REAL_TRIAL / UPSTREAM INJECTION POINT | Builds context from explicitly supplied governed records, then `_real_case` calls FPO Provider | No context producer currently exists; missing input fails closed. |
| `dynamic_cognitive_flow_real_capability_trial_adapter_v1.py:execute_real_trial_once` | CONTROLLED_REAL_TRIAL | Calls shared FPO Provider adapter | Shared Provider guard blocks real invocation without canonical refs. |
| `run_yolo_real_smoke_v0.py` | TOOL / CONTROLLED REAL SURFACE | Existing local YOLO surface | No canonical product caller proven; outside this narrow adapter change. |
| `vision_runtime/yolo_candidate_adapter_v0.py:run_yolo_real_smoke_v0` | LEGACY_RUNNABLE / LOW-LEVEL TOOL | Direct local YOLO smoke surface | Not an FPO caller; not changed in this phase. |
| `field_understanding/recognition_model_real_output_adapter_dryrun_cases_v1.py` | TEST/DRYRUN | Direct YOLO construction in dryrun fixtures | Not an FPO runtime entrypoint; out of scope. |

The physical model path remains a runtime input. It is not treated as model
identity or binding authority.
