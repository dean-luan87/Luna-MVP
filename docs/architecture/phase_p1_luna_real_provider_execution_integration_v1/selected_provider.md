# Selected Provider

Selected implementation: the existing local YOLO11n vision provider:

- `capabilities/midplatform/field_perception_orchestrator/integration/field_perception_real_vision_provider_adapter_v1.py`
- `capabilities/vision_runtime/yolo_candidate_adapter_v0.py`
- model declaration: `vision/detection/yolo/yolo11n.pt`

It is selected because it is local-only, bounded to one frame, already has a
canonical Capability/Model/Provider binding seam, and already maps native
detections to candidate visual evidence. The terminal environment must supply
the declared model asset and `ultralytics`/`torch`; this document does not
claim those dependencies are verified.
