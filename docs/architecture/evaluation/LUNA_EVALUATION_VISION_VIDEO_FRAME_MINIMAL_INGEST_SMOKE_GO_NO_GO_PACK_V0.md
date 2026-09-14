# Vision 视频帧最小 Ingest Smoke — GO / CONDITIONAL_GO / NO_GO v0

**Phase**：`Phase-Vision-VideoFrame-Minimal-Ingest-001`  
**Verifier**：`tools/evaluation/vision/verify_video_frame_minimal_ingest_smoke_v0.py`

## GO

- `output_root` 目录存在，且 summary、sampling report、envelopes JSONL、matrix、audit 均存在。  
- `sampled_frame_count > 0`，JSONL 行数与 sampling report 一致。  
- 每个 envelope 含 `frame_id`、`stream_id`、`frame_index`、`timestamp_ms`、`width`、`height`、`image_ref`。  
- 每个 `image_ref` 指向的 PNG 文件 **存在**。  
- audit：`video_ingest_executed == true`，且 `real_camera_invoked`、`yolo_invoked`、`ocr_invoked`、`vlm_invoked`、`midplatform_fact_written`、`scene_delta_written`、`world_model_written`、`ai_interpretation_invoked`、`navigation_decision_invoked` 均为 **false**。  

## CONDITIONAL_GO

- 无 NO_GO 级 blockers，但存在 **部分** `image_ref` 文件缺失（verifier 记录 `soft_notes`）。  
- 或未来扩展：外部视频解码成功但元数据（如 FPS）不可靠且已在 soft_notes 声明（当前实现未单独分支）。

## NO_GO

- 缺少任一必需产物或 envelopes 无法解析。  
- `sampled_frame_count == 0` 或与 JSONL 行数不一致。  
- envelope 缺字段或 audit 任一禁止项为 **true** / `video_ingest_executed` 非 true。  

## 非宣称

本 smoke **不** 证明视频质量、实时性、多路流调度或任何视觉理解能力；**仅** 证明离线帧读取 + 采样 + 封装 + 审计链可在评测目录内闭环。  
**不** 表示可以跳过 **Frame Input Governance** 与 **ROI proposal stub** 直接接视角识别；合法主线顺序见 [LUNA_VISION_MAINLINE_PHASE_ORDER_AND_INPUT_GATE_V0.md](../vision/LUNA_VISION_MAINLINE_PHASE_ORDER_AND_INPUT_GATE_V0.md)。
