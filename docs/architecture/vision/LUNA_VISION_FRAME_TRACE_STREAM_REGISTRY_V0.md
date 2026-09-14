# Luna — Vision Frame Trace + Stream Registry v0

**Phase**：`Phase-Vision-FrameTrace-StreamRegistry-001`  
**前置**：`Vision-VideoFrame-Minimal-Ingest-001` 产物（`video_frame_*`）已存在。

## 本阶段定位（重要）

**不是**视角识别、**不是** YOLO/VLM/OCR 的前置模型。本 phase **仅**把视频流与已采样帧登记为 **标准帧轨迹**（`stream_id`、`frame_id`、`timestamp_ms`、`image_ref`、指纹、sampling policy 引用等），供后续 **输入治理** 与 **ROI stub** 消费。

**不得**在本 phase 之后直接接入视角识别或 Vision Recognition Provider。合法下一跳见：[Vision 主线 phase 顺序与输入门控 v0](./LUNA_VISION_MAINLINE_PHASE_ORDER_AND_INPUT_GATE_V0.md)（必须先 **Vision-Frame-Input-Governance-001**，再 **Vision-Frame-ROI-Proposal-And-Segmentation-Stub-001**）。

## 目标

在 `video_frame_envelope_v0` 之上，**只读**生成：

1. **Stream registry**（`vision_stream_registry_v0`）：流标识、离线视频来源、分辨率、FPS、总帧数、采样帧数、采样策略文件引用。  
2. **Frame trace**（`vision_frame_trace_event_v0` JSONL）：每采样帧一条 `frame_sampled` 事件，含独立 `trace_id`、与 envelope 对齐的 `stcm_anchor` / `sampling_reason_codes`。  
3. **Frame lineage matrix**：按 `frame_index` 排序的 `previous_frame_id` / `next_frame_id` 链。  
4. **Sampling consistency report**：计数对齐、`sampled_indices` 与 envelope 顺序、指纹与 `image_ref` 存在性等。  
5. **Audit**：声明 registry / trace 已生成，且禁止项均为 false。

## 严禁

与 ingest phase 相同：无 YOLO/OCR/VLM/AI/导航/摄像头/MidPlatform fact/Scene Delta/WorldModel。

## 实现与命令

- `capabilities/vision_runtime/vision_stream_registry_v0.py`  
- `capabilities/vision_runtime/vision_frame_trace_v0.py`  
- Runner：`tools/evaluation/vision/run_vision_frame_trace_stream_registry_v0.py`  
- Verifier：`tools/evaluation/vision/verify_vision_frame_trace_stream_registry_v0.py`  

CLI 与产物清单见：`../evaluation/LUNA_EVALUATION_VISION_FRAME_TRACE_STREAM_REGISTRY_V0.md`。

## 非宣称

本 phase **不** 引入任何视觉模型；**不** 等价于「已准备好接视角识别」。  
后续任何 YOLO/OCR/VLM/视角识别 **必须** 只消费经 **Frame Input Governance** 与 **ROI Proposal Stub** 整理后的标准输入（目标形态见 `vision_provider_input_pack_v0`，见 [Vision 主线 phase 顺序与输入门控 v0](./LUNA_VISION_MAINLINE_PHASE_ORDER_AND_INPUT_GATE_V0.md)）。

**禁止**从本 phase 产物直接 wiring 到 Vision Recognition Provider。
