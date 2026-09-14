# Real Authority Chain Before Remediation v1

The audited path was:

`FPO control → external YOLO11n provisioning/model readiness → local FPO Provider admission → model_path → YOLO load/predict`

The local FPO admission carried `model_candidate_ref` and
`model_admission_ref`, but not canonical Capability↔Model binding,
Runtime Admission, or Model↔Provider binding references.

The exact bypass-risk surface was:

- `run_yolo11n_real_single_frame_provider_execution_v1.py:_prepare/_execute`
- `field_perception_real_vision_provider_adapter_v1.py:run_authorized_vision_provider_v1`
- `yolo_candidate_adapter_v0.py:load_yolo_model_local_v0/run_yolo_on_unit_v0`

