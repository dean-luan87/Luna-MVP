# RealVideo FrameSample Smoke — GO / NO_GO Pack v0

## GO

- `sample_scope=frame_sample_smoke_only`；frame sample index ≥1（smoke 期望 10 帧）
- 全部 `eligible_for_recognition=false`；`fact_status=not_fact`；`write_allowed=false`
- case coverage 全部 `execution_status=sample_mapping_only`
- poster/facility mapping：`poster_track_b_closed=true`；无 detection 调用
- no-write boundary 通过；verifier **GO**

## CONDITIONAL_GO

- `sample_count` 较少但 registry/mapping/boundary/audit 完整且无越界

## NO_GO

- 运行 OCR / Vision / YOLO / 摄像头
- 生成 OCRRequest / fusion / reference
- 写事实层或改 routing

## 下一 phase

`Phase-CrossModal-Vision-OCR-TestBoard-v1-RealVideo-ROI-to-OCR-Reference-001`（reference-only）
