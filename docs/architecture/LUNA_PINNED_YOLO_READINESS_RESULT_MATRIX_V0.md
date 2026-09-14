# LUNA — Pinned YOLO Readiness Result Matrix v0 (Phase-ModelPerception-015)

## Inputs
- manifest: `configs/models/yolo/yolo_model_manifest_v0.json`
- readiness report: `logs/yolo_model_readiness_pinned_001_20260427_1646.json`

## Result matrix

### Manifest
- weights_source: pinned_local
- weights_path: models/yolo/yolov5n.pt
- weights_sha256: present
- weights_file_size_bytes: present
- reproducibility_risk: false

### Dependency readiness
- torch import/version: pass (2.8.0)
- torchvision import/version: pass (0.23.0)
- cv2 import/version: pass (4.12.0)
- numpy import/version: pass (2.0.2)
- pandas import/version: pass (2.3.3)
- seaborn import/version: pass (0.13.2)
- PIL import/version: pass (11.3.0)

### Weights integrity
- weights_path exists: pass
- sha256 matches manifest: pass
- file size recorded: pass

### Model load
- dry-run model load: pass
- one-frame inference smoke: pass (black frame; detection_count=0)
- pinned_local load mechanism: torch.hub `custom` with `source=local` repo cache

### Governance / safety
- forbidden_output_semantic_count: 0
- allows_execute_now: false
- real_tts_invoked: false

### Readiness summary
- pinned_local_ready: true
- fallback_required: false

