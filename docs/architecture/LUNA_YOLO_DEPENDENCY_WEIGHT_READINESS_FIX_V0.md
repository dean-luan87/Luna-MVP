# LUNA — YOLO Dependency & Weight Readiness Fix v0 (Phase-ModelPerceptionFix-002)

## Phase
- Phase: **Phase-ModelPerceptionFix-002**
- Type: **Dependency/weight readiness fix (no capability expansion)**

## Trigger (observed failure)
Phase-ModelPerception-004 enabled smoke attempted:
- `disable_yolo=false`
- `invoked_count=0`
- `fallback_count=3`
- per-sample `fallback_reason=model_load_failed`

Console error:
- `No module named 'seaborn'`

## Interpretation
- This is **not** an adapter contract failure.
- This is a **YOLOv5 torch.hub environment dependency** issue.
- Fail-closed fallback, artifact integrity, and safety boundaries remained intact.

## Fix objectives (narrow)
1. Identify missing imports required by the YOLOv5 torch.hub loader path.
2. Fix missing deps (minimal; e.g., install `seaborn`).
3. Evaluate torch.hub “online fetch” risk and propose a pinned/local-weights route.
4. Do not change adapter safety boundaries or downstream integration constraints.
5. Re-run Phase-ModelPerception-004 enabled smoke and target `invoked_count>0`.

## torch.hub risk note (must be explicit)
Current reusable YOLOv5 detector uses:
- `torch.hub.load('ultralytics/yolov5', 'yolov5n', pretrained=True)`

Risks:
- May download/update code/weights implicitly (uncontrolled network and version drift).
- Not ideal for audit/replay determinism.

Preferred route (future, implementation choice):
- pinned local weights (explicit path)
- pinned package versions (requirements lock)
- avoid implicit hub downloads in production-like evaluation

## Readiness tooling
Added readiness check tool:
- `tools/check_yolo_dependency_readiness_v0.py`
It checks import readiness for:
- torch/torchvision/cv2/numpy/pandas/seaborn/PIL
and optionally attempts a **model-load dry-run** (initialize only).

