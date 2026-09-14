# LUNA — Existing YOLO Integration Inventory v0 (Phase-ModelPerception-002A)

## Phase
- Phase: **Phase-ModelPerception-002A**
- Type: **Inventory + adapter mapping definition only**

## Hard boundaries (confirmed)
- 本阶段只盘点，不实现。
- 不调用真实 YOLO 推理，不生成新的 model perception result。
- 不修改 PerceptionEval-001 / SceneTask / Fusion / Output。
- 不改变 evidence_type，不扩 Option A。
- 不进入 controlled_live_stream / full controlled trial / 真实用户测试。
- 不开启默认路径，不扩大 side effects 面。
- 不执行导航动作，不真实播报。
- 不声明 YOLO 已通过新链路准入。

## Inventory answers (must-answer checklist)

### 1) 当前是否存在 YOLO / object detection 代码？
**存在**，且至少包含两条“YOLO 系列”能力线：
- **A. YOLOv5 目标检测（object detection）**：`Luna_Badge_MVP/vision/yolov5_detector.py`
- **B. Ultralytics YOLO（yolo11）用于 OCR token（并非通用 object detection）**：`vision/ocr/yolo11_ocr_model.py` + runner/adapter

另有测试 mock：
- `luna_badge_tests/tests/qa_1_4_1/mocks/mock_yolo.py`

### 2) 入口文件路径是什么？
- object detection 入口类：
  - `Luna_Badge_MVP/vision/yolov5_detector.py` → `class YOLOv5Detector`
- OCR/文本 token runner：
  - `vision/ocr/yolo11_ocr_runner.py` → `class Yolo11OcrRunner`
  - `vision/ocr/yolo11_ocr_model.py` → `class Yolo11OcrModel`
  - `vision/ocr/yolo11_ocr_adapter.py` → `class Yolo11OcrAdapter`

### 3) 是否使用 ultralytics？
**两种方式都存在：**
- `Luna_Badge_MVP/vision/yolov5_detector.py` 使用 `torch.hub.load('ultralytics/yolov5', ...)`
- `vision/ocr/yolo11_ocr_model.py` 直接 `from ultralytics import YOLO` 并调用 `YOLO(model_path).predict(...)`

### 4) 模型权重路径/加载方式是什么？
- YOLOv5Detector：
  - 代码签名允许传 `model_path: str = "yolov5n.pt"`，但当前实际加载是：
    - `torch.hub.load('ultralytics/yolov5', 'yolov5n', pretrained=True)`
  - **结论**：当前实现依赖 hub 下载/缓存逻辑；`model_path` 主要用于日志，不是真正的加载来源。
- Yolo11OcrModel：
  - `YOLO(model_path)` 由调用方提供 `model_path`；device 通过 predict 参数 `device=self.device`

### 5) 输入是 image/frame/video 还是其他？
- YOLOv5Detector：
  - 输入：`detect(frame: np.ndarray)`（单帧 image）
  - 没有内置视频逐帧循环（但可由上层调用循环喂帧）
- Yolo11OcrRunner：
  - 支持 camera（`cv2.VideoCapture(camera_id)`）逐帧
  - 支持 video（`cv2.VideoCapture(video_path)`）逐帧
  - 输入是 frame，输出是 OCR token 列表（非通用检测）

### 6) 输出字段有哪些？是否包含 bbox/class/conf？
- YOLOv5Detector 输出 detection list，每个 detection 字段：
  - `bbox`: `[x1, y1, x2, y2]`（int，xyxy）
  - `confidence`: float
  - `class_id`: int
  - `class_name`: str（来自 `self.model.names[int(cls)]`）
  - **缺失**：frame_id / timestamp（需要 adapter 在新合同中补齐为 artifact fields）
- Yolo11OcrModel 输出 token list（`YoloOcrToken`）字段：
  - `text`: str（由 `r.names[cls_id]` 取）
  - `bbox_xyxy`: `(x1,y1,x2,y2)` float
  - `confidence`: float
  - runner 侧会带入 `frame_id` 与 `ts`

### 7) 是否已有逐帧视频处理？
**有，但在不同线路：**
- `vision/ocr/yolo11_ocr_runner.py`：支持 camera/video 逐帧循环
- `Luna_Badge_MVP/main.py`：主循环逐帧读取 camera，并定期调用 `YOLOv5Detector.detect`

### 8) 是否已有 trace/replay/whitebox？
结论：**没有按 ModelPerception-001 新合同（adapter + replay/whitebox）形式提供**。
- `Luna_Badge_MVP` 有 debug 导出日志（`logs/debug_export_*.json`），但这属于 MVP 运行时调试日志体系，不等价于 phone_local replay/whitebox contract。
- `Yolo11OcrAdapter` 会生成 `ObservationSignal`（含 provider/ts/payload），但这属于 OCR 管道的信号格式，不是 PerceptionEval-001 五类信号合同。

### 9) 是否已有 fallback/disable？
未发现通用的、按 ModelPerception-001 合同定义的：
- `model_disabled` 开关（fail-closed 不调用模型即可生效）
- `fallback_to_baseline/mock` 机制（可审计、可回放）

### 10) 是否已经接入当前 phone_local PerceptionEval 链？
**未接入**。
- 现有 phone_local 评测链仍为 `baseline_or_mock`，且本次盘点未发现 `YOLOv5Detector` / `ultralytics.YOLO` 被接入 PerceptionEval-001 工具链的路径。

### 11) 哪些部分可复用？
- **可复用（作为“原始检测能力来源”）**
  - `Luna_Badge_MVP/vision/yolov5_detector.py` 的输出字段（bbox/class/conf）形状清晰
- **可复用（作为“帧循环/逐帧输入范式参考”）**
  - `vision/ocr/yolo11_ocr_runner.py` 的 camera/video 逐帧模式（但不是 detection）
- **可复用（作为“tracking id 候选”参考）**
  - `Luna_Badge_MVP/vision/deepsort_tracker.py` 提供 `track_id` 字段，但实现为简化版分配逻辑，不能声称真实稳定跟踪

### 12) 哪些部分不能直接复用？
- `Luna_Badge_MVP/main.py`：包含语音播报与实时执行链路（与本项目 candidate-only 评测链边界不兼容），只能作为历史工程参考，不能直接接入 phone_local 评测链。
- `mock_yolo.py` 引用 `core.yolo_detector.DetectionResult`，但盘点未找到该实现文件；此 mock 需要补齐依赖或替换。

## Explicit “not found” record (do not crash)
- `core/yolo_detector.py`: **not_found**（但被 `mock_yolo.py` 引用）

