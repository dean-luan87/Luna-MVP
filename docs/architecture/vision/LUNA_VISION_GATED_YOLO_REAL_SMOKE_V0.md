# Luna — Gated YOLO Real Provider Smoke v0

**Phase**：`Phase-Vision-Gated-YOLO-Real-Smoke-001`

## 目的

在 **显式 gated**、**evaluation-only**、**本地权重**、**禁止触网下载** 前提下，验证 **真实 Ultralytics YOLO** 推理输出能否转换为 `vision_detection_evidence_v0`（`fact_status=not_fact`）。

## 环境（runner 强制）

- `LUNA_YOLO_EVAL_ONLY=true`
- `LUNA_ENABLE_YOLO_EVAL_PROVIDER_V0=true`
- `LUNA_YOLO_FORCE_FIXTURE_V0=false`
- `LUNA_YOLO_MODEL_PATH` 可选（须为本地已存在文件）

## 边界

不接主线、不改 registry 默认、不写事实层、不导航、不触网。

## 评测

[LUNA_EVALUATION_VISION_GATED_YOLO_REAL_SMOKE_V0.md](../evaluation/LUNA_EVALUATION_VISION_GATED_YOLO_REAL_SMOKE_V0.md)

## 建议下一跳

**Phase-Vision-YOLO-Real-Smoke-Positive-Sample-001**：见 [LUNA_VISION_YOLO_REAL_POSITIVE_SAMPLE_SMOKE_V0.md](./LUNA_VISION_YOLO_REAL_POSITIVE_SAMPLE_SMOKE_V0.md)。
