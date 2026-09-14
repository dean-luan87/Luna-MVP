# Luna OCR Trigger Gate & ROI Policy v0

**关联**：`LUNA_OCR_PROVIDER_RUNTIME_GOVERNANCE_STANDARD_V0.md`、`configs/ocr/ocr_provider_runtime_governance_v0.example.json`。Trigger Gate 的输入通常来自 **OCRRequest** 与场景状态，由 **OCR Orchestrator** 在调度前或调度内评估；业务模块不直接驱动「是否跑某 provider」。

## OCR Trigger Gate

- **默认**：`default_frame_wise_ocr_allowed = false`。  
- **允许触发**需同时满足（概念）：存在 **疑似文字区域**；对 **任务完成、环境理解或可审计证据** 有 **可陈述价值**；未与更高优先级资源（安全、导航关键路径）冲突。  
- **输出**：允许/拒绝、优先级、建议 Level、可选 ROI 列表（由上游检测或任务生成）。

## ROI-first

- **默认**：`roi_first = true`；`full_image_realtime_ocr_allowed = false`。  
- **ROI 来源**：视觉文字候选、任务目标区域、用户选区、地图锚点关联裁剪等。  
- **配额**：`max_roi_count_default` / `max_roi_count_high_priority`；低于 `min_roi_confidence` 的候选不进入 OCR 或降级为 Level 0。

## 整图 OCR

仅用于 **evaluation、低频静态、用户显式请求、受控 fallback**；须单独审计与预算，不得与实时默认路径混用。
