# Vision Frame Input Governance — GO / CONDITIONAL_GO / NO_GO v0

**Phase**：`Phase-Vision-Frame-Input-Governance-001`  
**Verifier**：`tools/evaluation/vision/verify_vision_frame_input_governance_v0.py`

## GO

- `frame_trace_root` 存在；summary、matrix、candidate、audit 均存在。  
- `total_frames > 0`，`accepted_frames > 0`，`eligible_for_roi_proposal_count > 0`。  
- `eligible_for_recognition_count == 0`；matrix 每行 `eligible_for_recognition` 为 **false**。  
- `vision_provider_input_candidate.json`：`schema_version == vision_frame_input_candidate_v0`，`candidate_scope == input_governance_only`，`forbidden_next_stages` 含 **`vision_recognition_provider`**。  
- audit：`frame_input_governance_executed == true`；禁止类字段（相机、YOLO、OCR、VLM、Supervision 主线、recognition provider、导航、写入、AI）均为 **false**。

## CONDITIONAL_GO

- trace 可读且产物齐全，但 **`accepted_frames == 0`** 或 **`eligible_for_roi_proposal_count == 0`**（例如全部帧被拒），且 **无** audit 越界。

## NO_GO

- 缺输入目录、缺任一产物、或 `eligible_for_recognition_count != 0` / 矩阵行出现 `eligible_for_recognition != false`。  
- candidate scope / forbidden 列表不符合要求。  
- audit 缺失或任一禁止项非 false。

## 非宣称

本 phase **不** 实现 Performance Controller 或真实 STCM 策略；**不** 调用任何识别模型。
