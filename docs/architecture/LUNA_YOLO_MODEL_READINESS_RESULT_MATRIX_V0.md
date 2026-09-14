# LUNA — YOLO Model Readiness Result Matrix v0 (Phase-ModelPerception-014)

## Inputs
- manifest: `configs/models/yolo/yolo_model_manifest_v0.json`
- readiness report: `logs/yolo_model_readiness_001_20260427_1622.json`

## Result matrix

### Manifest
- manifest exists: true
- manifest schema (v0 minimal fields): present
- weights_source: torch_hub_dev
- reproducibility_risk: true

### Dependency readiness
- torch import/version: pass (2.8.0)
- torchvision import/version: pass (0.23.0)
- cv2 import/version: pass (4.12.0)
- numpy import/version: pass (2.0.2)
- pandas import/version: pass (2.3.3)
- seaborn import/version: pass (0.13.2)
- PIL import/version: pass (11.3.0)

### Weights integrity
- pinned_local required: false (because weights_source=torch_hub_dev)
- weights sha256 check: not_required

### Model load
- model load dry-run: pass
- one-frame inference smoke: pass (detection_count=0 on black frame; acceptable)
- output schema sanity: pass (no crash; structured result)

### Governance / safety
- forbidden_output_semantic_count: 0
- allows_execute_now: false
- real_tts_invoked: false

### Readiness summary
- pinned_local_ready: false
- torch_hub_dev_ready: true
- fallback_required: false
- fallback_to: torch_hub_dev

## Notes
- torch.hub 加载过程中存在自动依赖更新尝试（pip 不存在），虽不阻断本次 smoke，但作为 reproducibility 风险证据。

