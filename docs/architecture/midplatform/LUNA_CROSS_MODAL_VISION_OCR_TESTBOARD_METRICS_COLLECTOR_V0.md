# Luna — CrossModal Vision OCR TestBoard Metrics Collector v0

**Phase**：`Phase-CrossModal-Vision-OCR-TestBoard-Metrics-Collector-Smoke-001`

## 目的

基于 Metrics Schema，**只读**聚合现有 evaluation 产物为 value matrix；不重新跑 OCR / TestBoard。

## 原则

- Collector 是只读统计器；不生成 benchmark 结论、不模型选型、不批准、不写事实层
- `no_write_boundary_pass_rate` 须为 1.0
- `ocr_empty_text_count` 按 case_type 解释

## 评测

[LUNA_EVALUATION_CROSS_MODAL_VISION_OCR_TESTBOARD_METRICS_COLLECTOR_V0.md](../evaluation/LUNA_EVALUATION_CROSS_MODAL_VISION_OCR_TESTBOARD_METRICS_COLLECTOR_V0.md)

## 下一跳

**Phase-CrossModal-Vision-OCR-TestBoard-v1-RealVideo-CaseRegistry-001** — 见 [LUNA_CROSS_MODAL_VISION_OCR_REALVIDEO_CASE_REGISTRY_V0.md](./LUNA_CROSS_MODAL_VISION_OCR_REALVIDEO_CASE_REGISTRY_V0.md)

## 建议下一跳（Registry GO 后）

**Phase-OCR-Poster-Region-OCR-Plan-Stub-001**
