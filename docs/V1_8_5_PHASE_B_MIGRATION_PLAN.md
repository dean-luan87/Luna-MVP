# v1.8.5 Phase B 迁移执行计划（Migration Execution Plan）

## 一、迁移总原则

### 原则（写死）
- ✅ **只改归属与路径**：不改代码逻辑，不优化算法
- ✅ **逐步迁移**：按文件顺序，逐项完成
- ✅ **保持向后兼容**：迁移过程中系统仍可运行

### 迁移顺序
1. **Step 1**: 迁移 `main.py` 中的视觉工具初始化（行 107, 126-128）
2. **Step 2**: 迁移 `main.py` 中的视觉工具调用（行 451, 455, 459）
3. **Step 3**: 迁移 `core/scene_state_builder.py` 中的原始感知接收（行 94-103）

---

## 二、Step 1: 迁移视觉工具初始化（main.py）

### 1.1 CameraHandler 初始化迁移

**文件**: `main.py`  
**行号**: 107  
**当前代码**:
```python
self.camera = CameraHandler()
```

**原调用做了什么**:
- 直接创建 `CameraHandler` 实例
- 在 `LunaBadgeMVP.__init__()` 中初始化摄像头

**迁移后改成什么形式**:
- 移除 `self.camera = CameraHandler()` 这一行
- 在 `PipelineController` 初始化时创建 `CameraHandler`
- `main.py` 通过 `PipelineController` 访问摄像头

**迁移目标模块**:
- `vision_pipeline/pipeline_controller.py`
- `PipelineController.__init__()` 中创建 `CameraHandler`

**Checklist**:
- [ ] 在 `PipelineController.__init__()` 中添加 `CameraHandler` 初始化
- [ ] 在 `PipelineController` 中添加 `read_frame()` 方法（委托给 `CameraHandler`）
- [ ] 在 `main.py:107` 删除 `self.camera = CameraHandler()`
- [ ] 在 `main.py` 中创建 `PipelineController` 实例（替代 `CameraHandler`）
- [ ] 更新所有 `self.camera.read_frame()` 调用为 `self.pipeline_controller.read_frame()`

---

### 1.2 YOLODetector 初始化迁移

**文件**: `main.py`  
**行号**: 126  
**当前代码**:
```python
self.yolo_detector = YOLODetector()
```

**原调用做了什么**:
- 直接创建 `YOLODetector` 实例
- 在 `LunaBadgeMVP.__init__()` 中初始化 YOLO 模型

**迁移后改成什么形式**:
- 移除 `self.yolo_detector = YOLODetector()` 这一行
- 在 `NavigationExecutor` 初始化时创建 `YOLODetector`
- `main.py` 不再直接持有 `YOLODetector` 实例

**迁移目标模块**:
- `vision_pipeline/lv4_executors/navigation_executor.py`
- `NavigationExecutor.__init__()` 中创建 `YOLODetector`

**Checklist**:
- [ ] 在 `NavigationExecutor.__init__()` 中添加 `YOLODetector` 初始化参数
- [ ] 在 `NavigationExecutor.__init__()` 中创建 `YOLODetector` 实例
- [ ] 在 `main.py:126` 删除 `self.yolo_detector = YOLODetector()`
- [ ] 在创建 `NavigationExecutor` 时传入 `YOLODetector` 实例（或让 `NavigationExecutor` 内部创建）

---

### 1.3 OCRProcessor 初始化迁移

**文件**: `main.py`  
**行号**: 127  
**当前代码**:
```python
self.ocr_processor = OCRProcessor()
```

**原调用做了什么**:
- 直接创建 `OCRProcessor` 实例
- 在 `LunaBadgeMVP.__init__()` 中初始化 OCR 模型

**迁移后改成什么形式**:
- 移除 `self.ocr_processor = OCRProcessor()` 这一行
- 在 `ModelingExecutor` 初始化时创建 `OCRProcessor`
- `main.py` 不再直接持有 `OCRProcessor` 实例

**迁移目标模块**:
- `vision_pipeline/lv4_executors/modeling_executor.py`
- `ModelingExecutor.__init__()` 中创建 `OCRProcessor`

**Checklist**:
- [ ] 在 `ModelingExecutor.__init__()` 中添加 `OCRProcessor` 初始化参数
- [ ] 在 `ModelingExecutor.__init__()` 中创建 `OCRProcessor` 实例
- [ ] 在 `main.py:127` 删除 `self.ocr_processor = OCRProcessor()`
- [ ] 在创建 `ModelingExecutor` 时传入 `OCRProcessor` 实例（或让 `ModelingExecutor` 内部创建）

---

### 1.4 QwenVLProcessor 初始化迁移

**文件**: `main.py`  
**行号**: 128  
**当前代码**:
```python
self.qwen_processor = QwenVLProcessor()
```

**原调用做了什么**:
- 直接创建 `QwenVLProcessor` 实例
- 在 `LunaBadgeMVP.__init__()` 中初始化 QwenVL 模型

**迁移后改成什么形式**:
- 移除 `self.qwen_processor = QwenVLProcessor()` 这一行
- 在 `ModelingExecutor` 初始化时创建 `QwenVLProcessor`
- `main.py` 不再直接持有 `QwenVLProcessor` 实例

**迁移目标模块**:
- `vision_pipeline/lv4_executors/modeling_executor.py`
- `ModelingExecutor.__init__()` 中创建 `QwenVLProcessor`

**Checklist**:
- [ ] 在 `ModelingExecutor.__init__()` 中添加 `QwenVLProcessor` 初始化参数
- [ ] 在 `ModelingExecutor.__init__()` 中创建 `QwenVLProcessor` 实例
- [ ] 在 `main.py:128` 删除 `self.qwen_processor = QwenVLProcessor()`
- [ ] 在创建 `ModelingExecutor` 时传入 `QwenVLProcessor` 实例（或让 `ModelingExecutor` 内部创建）

---

## 三、Step 2: 迁移视觉工具调用（main.py）

### 2.1 YOLODetector.detect() 调用迁移

**文件**: `main.py`  
**行号**: 451  
**当前代码**:
```python
objects = self.yolo_detector.detect(frame)
```

**原调用做了什么**:
- 直接调用 `YOLODetector.detect()` 方法
- 传入原始 `frame`，获取检测结果 `objects`
- 在 `process_frame()` 方法中调用

**迁移后改成什么形式**:
- 移除 `objects = self.yolo_detector.detect(frame)` 这一行
- 通过 `PipelineController.process_frame()` 处理帧
- 从 `NavigationResult` 中获取结构化检测结果（不再直接获取 `objects`）

**迁移目标模块**:
- `vision_pipeline/pipeline_controller.py`
- `PipelineController.process_frame()` → `NavigationExecutor.run()`

**Checklist**:
- [ ] 在 `NavigationExecutor.run()` 中调用 `YOLODetector.detect()`
- [ ] 在 `NavigationExecutor.run()` 中将检测结果封装到 `NavigationResult`
- [ ] 在 `main.py:451` 删除 `objects = self.yolo_detector.detect(frame)`
- [ ] 在 `main.py:process_frame()` 中调用 `self.pipeline_controller.process_frame(frame, ...)`
- [ ] 从 `PipelineController.process_frame()` 返回结果中提取导航相关信息（不再直接使用 `objects`）

---

### 2.2 OCRProcessor.extract_text() 调用迁移

**文件**: `main.py`  
**行号**: 455  
**当前代码**:
```python
texts = self.ocr_processor.extract_text(frame)
```

**原调用做了什么**:
- 直接调用 `OCRProcessor.extract_text()` 方法
- 传入原始 `frame`，获取 OCR 识别结果 `texts`
- 在 `process_frame()` 方法中调用

**迁移后改成什么形式**:
- 移除 `texts = self.ocr_processor.extract_text(frame)` 这一行
- 通过 `PipelineController.process_frame()` 处理帧
- 从 `ModelingResult` 中获取结构化 OCR 结果（`ContentCandidate`），不再直接获取 `texts`

**迁移目标模块**:
- `vision_pipeline/pipeline_controller.py`
- `PipelineController.process_frame()` → `ModelingExecutor.run()`

**Checklist**:
- [ ] 在 `ModelingExecutor.run()` 中调用 `OCRProcessor.extract_text()`
- [ ] 在 `ModelingExecutor.run()` 中将 OCR 结果封装到 `ContentCandidate`
- [ ] 在 `ModelingExecutor.run()` 中将 `ContentCandidate` 添加到 `ModelingResult.content_candidates`
- [ ] 在 `main.py:455` 删除 `texts = self.ocr_processor.extract_text(frame)`
- [ ] 在 `main.py:process_frame()` 中从 `PipelineController.process_frame()` 返回结果中提取 OCR 相关信息（不再直接使用 `texts`）

---

### 2.3 QwenVLProcessor.generate_description() 调用迁移

**文件**: `main.py`  
**行号**: 459  
**当前代码**:
```python
description = self.qwen_processor.generate_description(frame, objects, texts)
```

**原调用做了什么**:
- 直接调用 `QwenVLProcessor.generate_description()` 方法
- 传入原始 `frame`、`objects`、`texts`，获取场景描述 `description`
- 在 `process_frame()` 方法中调用

**迁移后改成什么形式**:
- 移除 `description = self.qwen_processor.generate_description(frame, objects, texts)` 这一行
- 通过 `PipelineController.process_frame()` 处理帧
- 从 `ModelingResult` 中获取结构化场景描述（不再直接获取 `description`）

**迁移目标模块**:
- `vision_pipeline/pipeline_controller.py`
- `PipelineController.process_frame()` → `ModelingExecutor.run()`

**Checklist**:
- [ ] 在 `ModelingExecutor.run()` 中调用 `QwenVLProcessor.generate_description()`
- [ ] 在 `ModelingExecutor.run()` 中将场景描述封装到 `ContentCandidate` 或 `EntityCandidate`
- [ ] 在 `ModelingExecutor.run()` 中将结果添加到 `ModelingResult`
- [ ] 在 `main.py:459` 删除 `description = self.qwen_processor.generate_description(frame, objects, texts)`
- [ ] 在 `main.py:process_frame()` 中从 `PipelineController.process_frame()` 返回结果中提取场景描述（不再直接使用 `description`）

---

### 2.4 process_frame() 方法重构

**文件**: `main.py`  
**行号**: 440-497（整个 `process_frame()` 方法）  
**当前代码结构**:
```python
def process_frame(self, frame):
    # 1. YOLO目标检测
    objects = self.yolo_detector.detect(frame)
    # 2. OCR文字识别
    texts = self.ocr_processor.extract_text(frame)
    # 3. Qwen2-VL生成场景描述
    description = self.qwen_processor.generate_description(frame, objects, texts)
    # 4. 构建结果
    result = {...}
    # 5. 决策闭环
    decision = self._handle_speech_decision(result)
    # ...
```

**原调用做了什么**:
- 直接调用三个视觉工具
- 构建包含 `objects`、`texts`、`description` 的结果字典
- 将结果传递给决策系统

**迁移后改成什么形式**:
- 调用 `self.pipeline_controller.process_frame(frame, task_state, context, user_position)`
- 从 `PipelineController` 返回结果中提取结构化信息
- 构建结果字典时使用结构化信息（不再直接使用原始 `objects`、`texts`、`description`）

**迁移目标模块**:
- `vision_pipeline/pipeline_controller.py`
- `PipelineController.process_frame()`

**Checklist**:
- [ ] 在 `main.py:process_frame()` 开头调用 `self.pipeline_controller.process_frame(...)`
- [ ] 从 `PipelineController.process_frame()` 返回结果中提取：
  - [ ] `navigation_result`（来自 `NavigationExecutor`）
  - [ ] `modeling_result`（来自 `ModelingExecutor`）
- [ ] 重构 `result` 字典构建逻辑，使用结构化结果而非原始感知数据
- [ ] 更新 `_handle_speech_decision()` 调用，传入重构后的 `result`
- [ ] 更新 `_output_results()` 调用，传入重构后的 `result`
- [ ] 更新 `json_logger.log_recognition_result()` 调用，传入重构后的数据

---

## 四、Step 3: 迁移 SceneStateBuilder（core/scene_state_builder.py）

### 3.1 SceneStateBuilder.build_state() 方法签名迁移

**文件**: `core/scene_state_builder.py`  
**行号**: 85-100（方法定义）  
**当前代码**:
```python
def build_state(
    self,
    objects: List[Dict[str, Any]],  # YOLO 检测结果
    texts: List[Dict[str, Any]],     # OCR 识别结果
    risk_level: Optional[str] = None
) -> SceneState:
```

**原调用做了什么**:
- 直接接收 YOLO 和 OCR 的原始结果
- 从原始结果中提取 `object_labels` 和 `sign_texts`
- 构建 `SceneState` 对象

**迁移后改成什么形式**:
- 方法签名改为接收 `WorldUpdate` 或结构化 `SceneHint`
- 不再直接接收 `objects` 和 `texts` 原始感知数据
- 从 `WorldUpdate` 中提取结构化信息

**迁移目标模块**:
- `core/world_model/common/types.py`（`WorldUpdate` 类型）
- `vision_pipeline/lv4_executors/modeling_executor.py`（生成 `WorldUpdate`）

**Checklist**:
- [ ] 在 `core/world_model/common/types.py` 中确认 `WorldUpdate` 类型定义完整
- [ ] 在 `ModelingExecutor.run()` 中生成 `WorldUpdate`（包含 YOLO 和 OCR 的结构化结果）
- [ ] 修改 `SceneStateBuilder.build_state()` 方法签名：
  - [ ] 移除 `objects: List[Dict[str, Any]]` 参数
  - [ ] 移除 `texts: List[Dict[str, Any]]` 参数
  - [ ] 添加 `world_update: WorldUpdate` 参数（或 `scene_hint: SceneHint`）
- [ ] 修改 `SceneStateBuilder.build_state()` 方法实现：
  - [ ] 从 `world_update.structured_data` 中提取物体和文字信息
  - [ ] 更新 `object_labels` 和 `sign_texts` 的提取逻辑（行 102-103）

---

### 3.2 SceneStateBuilder.build_state() 调用点迁移

**文件**: `main.py`  
**行号**: 548, 621, 636（共 3 处调用）  
**当前调用形式**:
```python
scene_state = self.scene_state_builder.build_state(
    objects=result.get("objects", []),
    texts=result.get("texts", []),
    risk_level=...
)
```

**原调用做了什么**:
- 直接传入 YOLO 和 OCR 的原始结果（`objects` 和 `texts`）
- 获取 `SceneState` 对象

**迁移后改成什么形式**:
- 先通过 `PipelineController.process_frame()` 获取 `WorldUpdate`
- 将 `WorldUpdate` 传入 `SceneStateBuilder.build()`
- 不再直接传入原始感知数据

**迁移目标模块**:
- `vision_pipeline/pipeline_controller.py`
- `core/scene_state_builder.py`

**Checklist**:
- [ ] 在 `main.py:548` 处：
  - [ ] 移除 `objects=result.get("objects", [])` 参数
  - [ ] 移除 `texts=result.get("texts", [])` 参数
  - [ ] 先获取 `WorldUpdate`（从 `PipelineController.process_frame()` 返回结果中提取）
  - [ ] 将 `WorldUpdate` 传入 `self.scene_state_builder.build_state(world_update, risk_level=...)`
- [ ] 在 `main.py:621` 处（同样处理）
- [ ] 在 `main.py:636` 处（同样处理）
- [ ] 注意：这些调用点都在 `_handle_speech_decision()` 方法中，需要与 Step 2.4 一起重构

---

## 五、迁移后验证 Checklist

### 5.1 功能验证

- [ ] 系统可以正常启动（无导入错误）
- [ ] 摄像头可以正常读取帧
- [ ] YOLO 检测功能正常（通过 `NavigationExecutor`）
- [ ] OCR 识别功能正常（通过 `ModelingExecutor`）
- [ ] QwenVL 场景描述功能正常（通过 `ModelingExecutor`）
- [ ] 决策系统可以正常接收处理结果
- [ ] 场景状态构建功能正常（通过 `WorldUpdate`）

### 5.2 代码验证

- [ ] `main.py` 中不再有直接调用 `YOLODetector`、`OCRProcessor`、`QwenVLProcessor` 的代码
- [ ] `main.py` 中不再直接创建 `CameraHandler` 实例
- [ ] `core/scene_state_builder.py` 中不再直接接收 `objects` 和 `texts` 原始感知数据
- [ ] 所有视觉工具调用都通过 `vision_pipeline` 进行
- [ ] 所有视觉结果都经过结构化处理后再进入 `core/world_model`

### 5.3 架构验证

- [ ] 视觉数据流向符合规范：`utils/* → vision_pipeline/* → core/world_model/*`
- [ ] `core/world_model/*` 中不再出现 raw image / frame / bbox / ocr_text
- [ ] `core/task_chain/*` 中不再出现 raw image / frame / bbox / ocr_text
- [ ] `decision_controller` 中不再出现 raw image / frame / bbox / ocr_text

---

## 六、迁移执行顺序总结

### 执行顺序（严格按此顺序）

1. **Step 1.1**: 迁移 `CameraHandler` 初始化（`main.py:107`）
2. **Step 1.2**: 迁移 `YOLODetector` 初始化（`main.py:126`）
3. **Step 1.3**: 迁移 `OCRProcessor` 初始化（`main.py:127`）
4. **Step 1.4**: 迁移 `QwenVLProcessor` 初始化（`main.py:128`）
5. **Step 2.1**: 迁移 `YOLODetector.detect()` 调用（`main.py:451`）
6. **Step 2.2**: 迁移 `OCRProcessor.extract_text()` 调用（`main.py:455`）
7. **Step 2.3**: 迁移 `QwenVLProcessor.generate_description()` 调用（`main.py:459`）
8. **Step 2.4**: 重构 `process_frame()` 方法（`main.py:440-497`）
9. **Step 3.1**: 迁移 `SceneStateBuilder.build_state()` 方法签名（`core/scene_state_builder.py:85-100`）
10. **Step 3.2**: 迁移 `SceneStateBuilder.build_state()` 调用点（`main.py:548, 621, 636`）

### 注意事项

- ⚠️ **不要修改代码逻辑**：只改归属与路径
- ⚠️ **保持向后兼容**：迁移过程中系统仍可运行
- ⚠️ **逐步迁移**：完成一项验证一项，不要一次性修改所有代码
- ⚠️ **测试验证**：每完成一个 Step，运行系统验证功能正常

---

## 七、迁移完成标准

### 完成标准（必须全部满足）

- ✅ `main.py` 中不再直接创建或调用任何视觉工具
- ✅ 所有视觉工具调用都通过 `vision_pipeline` 进行
- ✅ `core/scene_state_builder.py` 不再直接接收原始感知数据
- ✅ 所有视觉结果都经过结构化处理后再进入 `core/world_model`
- ✅ 系统功能正常，无回归问题
- ✅ 代码通过架构验证（符合视觉数据流向规范）

---

## 八、迁移文档版本

**文档版本**: v1.0  
**创建日期**: 2024-12-19  
**基于审计**: `docs/V1_8_5_PHASE_B_REFERENCE_AUDIT.md`  
**状态**: 待执行

