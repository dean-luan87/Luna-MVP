# Vision Frame Trace + Stream Registry — GO / CONDITIONAL_GO / NO_GO v0

**Phase**：`Phase-Vision-FrameTrace-StreamRegistry-001`  
**Verifier**：`tools/evaluation/vision/verify_vision_frame_trace_stream_registry_v0.py`

## GO

- 所有必需产物存在：`vision_stream_registry.json`、`vision_frame_trace.jsonl`、`vision_frame_lineage_matrix.json`、`vision_sampling_consistency_report.json`、`vision_frame_trace_audit_report.json`。  
- Registry 含非空 `stream_id`、`source_video_ref`，且 `sampled_frame_count > 0`。  
- Frame trace 行数等于 registry 的 `sampled_frame_count`；`frame_id` 全局唯一；`frame_fingerprint` 非空；`image_ref` 指向已存在文件。  
- `vision_sampling_consistency_report.json` 中 `passed == true`。  
- Audit：`stream_registry_generated`、`frame_trace_generated` 为 **true**；禁止类字段均为 **false**。  

## CONDITIONAL_GO（预留）

当前 verifier 以 **GO / NO_GO** 为主。若未来允许 lineage 中部分非关键列缺失而 consistency 仍通过，可在此定义 **CONDITIONAL_GO** 并调整 verifier。

## NO_GO

- 任一必需文件缺失或 JSONL 无法解析。  
- trace 行数与 `sampled_frame_count` 不一致、`frame_id` 重复、指纹为空或 PNG 缺失。  
- sampling consistency `passed != true`。  
- audit 缺失或任一禁止项非 false、或 `stream_registry_generated` / `frame_trace_generated` 非 true。  

## 非宣称

通过本 phase **不等于** 已接入 YOLO/VLM/OCR 或视角识别；**仅** 建立统一帧轨迹与流登记。  
**不得**从 Frame Trace / Registry 直接进入 Vision Recognition Provider；合法顺序见 [LUNA_VISION_MAINLINE_PHASE_ORDER_AND_INPUT_GATE_V0.md](../vision/LUNA_VISION_MAINLINE_PHASE_ORDER_AND_INPUT_GATE_V0.md)。
