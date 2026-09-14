# LUNA — MidPlatform OCR Bridge Upstream Input Evidence Validation v0

## Phase

- **Phase-ModelOCR-MidPlatform-Bridge-002-Fix**

## Purpose

验证 `tools/evaluate_midplatform_ocr_bridge_v0.py`（Bridge-002 skeleton）能读取两类真实上游离线产物：

1) `yolo_ocr_bridge_root`（YOLO × OCR bridge evidence run 输出）
2) `ocr_benchmark_root`（OCR 离线基准/策略回归输出）

并确保 Bridge-002 在不接 runtime / 不接中台 / 不进入下游的前提下，生成：
- evidence inputs
- delta control
- filtering/blocking results
- candidate objects（文本候选/世界候选/ambient 候选）
- trace/replay/whitebox

本阶段只做验证与记录，不实现任何 runtime 写入。

## Validation commands（离线）

### yolo_ocr_bridge_root
```bash
python3 tools/evaluate_midplatform_ocr_bridge_v0.py \
  --input-root logs/yolo_ocr_offline_bridge_003_20260429_154500 \
  --input-type yolo_ocr_bridge_root \
  --output-root logs/midplatform_ocr_bridge_002_fix_yolo_<timestamp>

python3 tools/verify_midplatform_ocr_bridge_v0.py \
  --output-root logs/midplatform_ocr_bridge_002_fix_yolo_<timestamp>
```

### ocr_benchmark_root
```bash
python3 tools/evaluate_midplatform_ocr_bridge_v0.py \
  --input-root logs/ocr_offline_source_policy_009_normal_20260429_124053 \
  --input-type ocr_benchmark_root \
  --output-root logs/midplatform_ocr_bridge_002_fix_ocr_<timestamp>

python3 tools/verify_midplatform_ocr_bridge_v0.py \
  --output-root logs/midplatform_ocr_bridge_002_fix_ocr_<timestamp>
```

## Governance boundary（必须）

- 不接真实 MidPlatform runtime
- 不进入 SceneTask/Fusion/Output
- 不生成 `semantic_summary`
- 不生成 `navigation_action`
- 不执行导航动作
- 不写入真实世界模型

