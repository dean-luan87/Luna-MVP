# Luna — YOLO Real Positive Sample Smoke v0

**Phase**：`Phase-Vision-YOLO-Real-Smoke-Positive-Sample-001`

## 目的

在 **可检测正样本**（默认 ultralytics 本地 `bus.jpg`）上运行 **真实 YOLO**，验证 `detection_count > 0` 且可转换为 `vision_detection_evidence_v0`（`fact_status=not_fact`，`synthetic=false`）。

## 前置

- Phase-Vision-Gated-YOLO-Real-Smoke-001 = CONDITIONAL_GO  
- 本地权重（如 `yolo11n.pt`）可加载  

## 边界

evaluation-only；不触网；不接主线；不写事实层。

## 评测

[LUNA_EVALUATION_VISION_YOLO_REAL_POSITIVE_SAMPLE_SMOKE_V0.md](../evaluation/LUNA_EVALUATION_VISION_YOLO_REAL_POSITIVE_SAMPLE_SMOKE_V0.md)

## 建议下一跳

**Phase-Vision-YOLO-Evidence-Pack-Integration-Stub-001**：见 [LUNA_VISION_YOLO_EVIDENCE_PACK_INTEGRATION_STUB_V0.md](./LUNA_VISION_YOLO_EVIDENCE_PACK_INTEGRATION_STUB_V0.md)。
