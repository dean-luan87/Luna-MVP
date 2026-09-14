# LUNA YOLO Stage-1 Detector & Frame Source Matrix v0

**Phase**：Phase-Mainline-GuardedTrial-003

---

## 1. Detector 入口（摘要）

- **主路径**：`capabilities/model_perception/yolo_shadow_adapter_v0.py` — `run_yolo_shadow_adapter_on_sample_v0`（shadow adapter；`disable_yolo` 门卫）。  
- **真实推理类**（可选运行时）：`Luna_Badge_MVP.vision.yolov5_detector.YOLOv5Detector` — Luna-Core 检出时可能 **未安装**，属 **CONDITIONAL_GO** 说明项。  
- **RequestTrace 读取**：`capabilities/core_trw/yolo_request_trace_shadow_adapter_v0.py`（离线产物映射，非推理）。

---

## 2. Frame 来源（摘要）

| 优先级 | 类型 | 说明 |
|--------|------|------|
| 推荐 | `video_file` | `PhoneLocalSampleRefV0.source_video_path` + `cv2.VideoCapture(path)` — **离线/本地文件**，避免摄像头 index。 |
| 支持 | `sample_frame` | 由视频抽样得到的 `frame` 送入 `detect`（仍非 live camera API 优先场景）。 |

**不推荐在本阶段讨论**：直接用摄像头设备作为主输入（计划外；风险高）。

Machine-readable：`yolo_stage1_frame_source_candidate_matrix.json`。
