# Luna — CrossModal Vision OCR TestBoard v1 Planning v0

**Phase**：`Phase-CrossModal-Vision-OCR-TestBoard-v1-Planning-001`

## 目的

在 TestBoard v0 `closed_for_v0` 前提下，冻结 v1 范围、三轨矩阵、phase roadmap、non-goals、risk register、gate policy 与执行顺序。**本阶段仅规划，不实现、不跑 OCR、不跑 Vision provider。**

## 三条独立测试域

| Track ID | 名称 | 优先级 |
|----------|------|--------|
| `TVOCR_V1_B_POSTER_LAYOUT` | Poster Layout Segmentation Governance | 1（建议先实现） |
| `TVOCR_V1_A_REAL_VIDEO` | Real Video Cases | 2 |
| `TVOCR_V1_C_BENCHMARK_PERFORMANCE` | Benchmark & Performance Layer | 2 |

## 建议实现顺序（规划冻结）

1. Poster Layout Segmentation Governance  
2. Metrics Schema  
3. RealVideo CaseRegistry  
4. …（见 execution_order 产物）

**理由**：先补海报治理与指标框架，再扩真实视频，否则真实视频中的海报类 ROI 难以一致评估。

## 评测

[LUNA_EVALUATION_CROSS_MODAL_VISION_OCR_TESTBOARD_V1_PLANNING_V0.md](../evaluation/LUNA_EVALUATION_CROSS_MODAL_VISION_OCR_TESTBOARD_V1_PLANNING_V0.md)

## Track B 首 phase（已完成则进入 Metrics Schema）

**Phase-OCR-Poster-Layout-Segmentation-Governance-001** — 见 [LUNA_OCR_POSTER_LAYOUT_SEGMENTATION_GOVERNANCE_V0.md](../ocr/LUNA_OCR_POSTER_LAYOUT_SEGMENTATION_GOVERNANCE_V0.md)

## Metrics Schema（Track C）

**Phase-CrossModal-Vision-OCR-TestBoard-Metrics-Schema-001** — 见 [LUNA_CROSS_MODAL_VISION_OCR_TESTBOARD_METRICS_SCHEMA_V0.md](./LUNA_CROSS_MODAL_VISION_OCR_TESTBOARD_METRICS_SCHEMA_V0.md)

## Track A — RealVideo

**Phase-CrossModal-Vision-OCR-TestBoard-v1-RealVideo-CaseRegistry-001** — 见 [LUNA_CROSS_MODAL_VISION_OCR_REALVIDEO_CASE_REGISTRY_V0.md](./LUNA_CROSS_MODAL_VISION_OCR_REALVIDEO_CASE_REGISTRY_V0.md)

## 建议下一跳（Registry GO 后）

**Phase-OCR-Poster-Region-OCR-Plan-Stub-001**（先于 FrameSample Smoke）
