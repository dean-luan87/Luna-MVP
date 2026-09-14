# Luna Evaluation — Gated YOLO Candidate Adapter GO / NO_GO Pack v0

## GO

- ROI unit 选择 > 0，无整帧直连。  
- 输出 `vision_detection_evidence_v0`，`fact_status=not_fact`。  
- audit：`vision_mainline_modified=false`，`vision_provider_registry_default_changed=false`。  
- 真实 YOLO 或 fixture 路径完整。

## CONDITIONAL_GO

- Ultralytics / 模型不可用，但 probe + fixture + gap_notes 完整；无越界。

## NO_GO

- 改 registry 默认 / 接主线 / 整帧输入 / label 标 fact / 写事实层 / 导航 / audit 缺失。

## 一句话

gated evaluation-only：YOLO-like → VisionDetectionEvidence v0；不接主线。
