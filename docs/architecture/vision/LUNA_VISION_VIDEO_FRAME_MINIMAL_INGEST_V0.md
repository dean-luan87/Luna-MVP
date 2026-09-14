# Luna — Vision 视频帧最小 Ingest 骨架 v0

**Phase**：`Phase-Vision-VideoFrame-Minimal-Ingest-001`  
**目标**：建立 **最小** 视频帧离线 ingest：从文件（或评测生成的短视频）解码，按 stride / max_frames 采样，写出 **frame envelope**（JSONL）、**帧 PNG**（`image_ref`）、**采样报告** 与 **固定 audit**。用于 Vision / 视频流主线的 **只读评测产物**，不进入检测、OCR、中台事实层或 Scene Delta。

## 严禁（本 phase）

- 真实摄像头 / 实时硬件采集  
- YOLO / OCR / VLM / AI 解释 / 导航决策  
- MidPlatform fact、Scene Delta、WorldModel 写入  
- 修改 OCR routing  

## 允许

- 离线读取 MP4（OpenCV `VideoCapture`）或生成测试 MP4（`VideoWriter`）  
- 固定数量帧 + stride 采样 + 可选按 `max_width` / `max_height` 缩放  
- 评测目录下写入 summary、sampling report、envelopes JSONL、matrix、audit、notes  

## Frame envelope

见 `capabilities/vision_runtime/video_frame_envelope_v0.py` 中 `video_frame_envelope_v0` 字段约定（含 `stcm_anchor`、`sampling_decision`）。

## 实现与命令

- 能力包：`capabilities/vision_runtime/`  
- Runner：`tools/evaluation/vision/run_video_frame_minimal_ingest_smoke_v0.py`  
- Verifier：`tools/evaluation/vision/verify_video_frame_minimal_ingest_smoke_v0.py`  

评测步骤与 CLI 示例见：`../evaluation/LUNA_EVALUATION_VISION_VIDEO_FRAME_MINIMAL_INGEST_SMOKE_V0.md`。

## Vision 主线顺序（不要跳步）

仅证明「视频 → 采样 → envelope」仍 **不足以** 接视角识别或整帧进模型。合法后续顺序与 **vision_provider_input_pack_v0** 占位见：[Vision 主线 phase 顺序与输入门控 v0](./LUNA_VISION_MAINLINE_PHASE_ORDER_AND_INPUT_GATE_V0.md)。

## 依赖

运行态需要 **OpenCV（cv2）** 与 **NumPy**（用于生成测试帧矩阵）；未安装时 runner 会报错退出，**不** 回退到 YOLO 或云端 API。
