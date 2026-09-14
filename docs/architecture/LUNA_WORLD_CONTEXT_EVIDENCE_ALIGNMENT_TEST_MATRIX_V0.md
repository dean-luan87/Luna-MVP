# LUNA — WorldContextEvidence Alignment Test Matrix v0

## Phase

- **Phase-WorldModel-ContextEvidence-003**

## Goal

验证 ContextEvidence-003 的“锚点透传 + source reference 对齐”在三类输入下均成立（仍是 candidate-only）。

## Required inputs

- MidPlatform OCR Bridge root（closed_v0）：`logs/midplatform_ocr_bridge_002_fix_ocr_20260429_174540`
- SceneDelta root（closed_v0）：`logs/scene_delta_control_002_fix_20260430_104403`
- sample_matrix：`datasets/world_context_evidence_samples_v0/sample_matrix.json`

## Verifier gates（新增 W–AF）

- **W**：`observed_where_source` 存在且非空
- **X**：`source_reference_chain` 存在且至少 1 项
- **Y**：当 `source_ref_integrity_status in {partial, broken}` 时，`missing_source_refs` 必须非空
- **Z**：不伪造 GPS（`observed_where.geo_location.lat/lng` 必须为 null）
- **AA**：SceneDelta 输入时必须继承 `spatiotemporal_anchor_ref`
- **AB**：`source_modalities` 只允许真实感知模态（ocr/yolo/map/gps/visual_symbol/user_feedback）
- **AC**：`source_layers` 存在且非空
- **AD**：`source_ref_integrity_status` 存在（complete/partial/broken）
- **AE**：`source_evidence_refs` 为空则 NO_GO（hard gate）
- **AF**：unknown anchor 强制 `requires_revalidation=true`

