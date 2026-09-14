# Luna 评测 — Vision ROI Proposal Stub Smoke GO / NO_GO Pack v0

**Verifier**：`tools/evaluation/vision/verify_vision_roi_proposal_stub_smoke_v0.py`  
**Phase**：`Phase-Vision-Frame-ROI-Proposal-And-Segmentation-Stub-001`

## GO

- governance 根目录存在；stub 输出根下 **ROI candidate**、**vision_provider_input_pack**、**audit**、**source_chain_summary**、**stub_summary** 齐全。  
- `roi_items` 数量 **> 0**；所有 pack 的 `input_units` 合计 **> 0**。  
- 每个 ROI：`bbox_in_frame`、`polygon_in_frame`、`proposal_source=rule_stub`、`segmentation_stub.mask_available=false`。  
- 每个 unit：非空 **`image_ref`**（且文件存在）、完整 **`coordinate_transform`**（含 `mode/offset/scale/source/transformed` 尺寸字段）。  
- 每个 pack：`source_chain` 非空。  
- audit：`roi_proposal_stub_generated`、`vision_provider_input_pack_generated` 为 **true**；`yolo_invoked`、`real_detector_invoked`、`supervision_mainline_invoked`、`vlm_invoked`、`ocr_invoked`、`ai_interpretation_invoked`、`navigation_decision_invoked`、`midplatform_fact_written`、`scene_delta_written`、`world_model_written` 均为 **false**。

## CONDITIONAL_GO

- 无 **NO_GO** 级 blockers，但存在 **部分** `input_unit` 缺少有效 `image_ref`（crop 路径缺失），或 verifier 记录的其它 **软降级** 条件（以 `vision_roi_proposal_stub_verifier_report.json` 的 `soft_notes` 为准）。

## NO_GO

- 调用或 audit 暗示调用了 **YOLO / 真实 detector / Supervision 主线 / VLM / OCR**（本 smoke 设计为 **绝不调用**；audit 对应字段须为 false）。  
- **直接进入** recognition provider、写 **MidPlatform fact**、写 **Scene Delta**、写 **WorldModel**、调用 **导航决策**（audit 须为 false）。  
- **audit 缺失** 或关键产物缺失（candidate / pack / matrix / source_chain / verifier 无法完成静态检查）。  
- `roi_items` 或 `input_units` 为空；ROI 缺 bbox / polygon；`proposal_source` 非 `rule_stub`；`mask_available` 非 false；`source_chain` 为空；crop 路径存在但 **不是有效文件**。

## 一句话

本 smoke **只**验证规则 / stub ROI 与 **`vision_provider_input_pack_v0`** 产物链；**不**跑检测、分割、Supervision 主线、识别与中台写入。
