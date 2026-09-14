# Provider / Model / Capability Bypass Audit v1

## Confirmed bypass-risk path

`run_yolo11n_real_single_frame_provider_execution_v1.py` constructs a model admission through `resolve_yolo11n_external_provisioning_v1`, then builds FPO provider admission and calls `run_authorized_vision_provider_v1`. The provider adapter calls `run_yolo_on_unit_v0`, which loads/predicts with YOLO in its real branch (`capabilities/vision_runtime/yolo_candidate_adapter_v0.py:292-345`).

The path has useful guards—single-frame scope, provider admission flag, candidate evidence and no direct world mutation—but its input records use local `model_candidate_ref`/`provider_candidate_ref` and `model_admission_ref`, not the frozen binding candidate refs. This is F-001.

## Other paths

- Dynamic real-capability trial imports the compatibility Runtime Admission adapter and checks `runtime_admission.executable` before provider admission (`dynamic_cognitive_flow_real_capability_trial_adapter_v1.py:210-246`). This is closer to the frozen flow, but it still remains a controlled/trial path.
- OCR guarded trials explicitly document a controlled provider invocation and prohibit MidPlatform/World writes. They are not proof of canonical production wiring.
- No A or Task direct Provider selection caller was proven in the reviewed core paths; legacy names are primarily controlled/test/compatibility surfaces.

