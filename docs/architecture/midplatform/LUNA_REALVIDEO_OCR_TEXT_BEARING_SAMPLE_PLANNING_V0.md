# Luna — RealVideo OCR Text-Bearing Sample Planning v0

**Phase**：`Phase-RealVideo-OCR-Text-Bearing-Sample-Planning-001`

## 目的

规划 RealVideo **含字（text-bearing）** 样本标准、采样策略、ROI 选择、ground truth 要求与未来复跑链路。解决 Reference Closure **CONDITIONAL_GO**（10 条 evidence 全 `empty_text`）的样本局限。

## 原则

- **planning_only**：不读视频、不抽帧、不跑 OCR、不生成 evidence
- 不把 `empty_text` 当失败或 `no_text_fact`
- 无 ground truth 不计算 accuracy / benchmark T2
- 全部 `fact_status=not_fact`；`write_allowed=false`

## 实现

- Capability：`capabilities/midplatform/realvideo_ocr_text_bearing_sample_planning_v0.py`
- Runner：`tools/evaluation/midplatform/run_realvideo_ocr_text_bearing_sample_planning_v0.py`
- Verifier：`tools/evaluation/midplatform/verify_realvideo_ocr_text_bearing_sample_planning_v0.py`

## 评测

[LUNA_EVALUATION_REALVIDEO_OCR_TEXT_BEARING_SAMPLE_PLANNING_V0.md](../evaluation/LUNA_EVALUATION_REALVIDEO_OCR_TEXT_BEARING_SAMPLE_PLANNING_V0.md)

## 建议下一跳

**Phase-RealVideo-OCR-Readability-Governance-001** — 见 [LUNA_REALVIDEO_OCR_READABILITY_GOVERNANCE_V0.md](./LUNA_REALVIDEO_OCR_READABILITY_GOVERNANCE_V0.md)。

在已具备含字真实视频或可控 fixture 时：**Phase-RealVideo-Text-Bearing-FrameSample-Smoke-001**。
