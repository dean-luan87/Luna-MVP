# v1.8.5 Phase B 引用审计清单（Reference Audit List）

## 一、审计总原则

### 1. 视觉数据流向规则（写死）

**禁止流向：**
- ❌ `core/world_model/*` 不得出现 raw image / frame / bbox / ocr_text
- ❌ `core/task_chain/*` 不得出现 raw image / frame / bbox / ocr_text
- ❌ `decision_controller` 不得出现 raw image / frame / bbox / ocr_text

**唯一合法流向：**
```
utils/* → vision_pipeline/* →（结构化）→ core/world_model/*
```

### 2. 本轮审计目标

- ✅ **标记**：找出所有违规调用点
- ✅ **迁移路径**：给出明确的迁移目标
- ❌ **不做算法改写**：只改归属与路径

---

## 二、utils/ 视觉工具调用审计（最高优先级）

### 1️⃣ CameraHandler

**允许被谁调用：**
- ✅ `vision_pipeline/pipeline_controller.py`

**违规调用位置：**

| 文件 | 行号 | 调用方式 | 状态 |
|------|------|----------|------|
| `main.py` | 107 | `self.camera = CameraHandler()` | ⚠️ **违规** |
| `luna_badge_v1_2/benchmarks/benchmark_full_realtime.py` | 32 | `cam = CameraHandler()` | ⚠️ 测试代码（可忽略） |
| `luna_badge_v1_2/demo_realtime_navigation.py` | 118 | `self.camera = CameraHandler(...)` | ⚠️ 测试代码（可忽略） |

**迁移动作：**
```python
# main.py:107
# TODO: route through VisionPipelineController
# 迁移目标：vision_pipeline/pipeline_controller.py
# 当前：main.py 直接创建 CameraHandler
# 目标：通过 PipelineController 管理摄像头
```

**迁移路径：**
```
CameraHandler
   ↓
vision_pipeline/pipeline_controller.py (统一管理)
   ↓
LV2 Quality Gate
```

---

### 2️⃣ YOLODetector

**违规原因：**
- YOLO 输出 bbox / label = 原始感知结果
- 不应被 task / risk / decision 直接消费

**违规调用位置：**

| 文件 | 行号 | 调用方式 | 状态 |
|------|------|----------|------|
| `main.py` | 126 | `self.yolo_detector = YOLODetector()` | ⚠️ **违规** |
| `main.py` | 451 | `objects = self.yolo_detector.detect(frame)` | ⚠️ **违规**（已标记 TODO） |

**正确迁移路径：**
```
YOLODetector
   ↓
vision_pipeline/lv4_executors/navigation_executor.py
   ↓
（结构化结果：NavigationResult）
   ↓
TaskPlanner / RiskAdvisoryService
```

**迁移动作：**
```python
# main.py:126, 451
# TODO: move YOLO call to vision_pipeline.lv4_executors.navigation_executor
# 当前：main.py 直接调用 YOLODetector.detect()
# 目标：通过 NavigationExecutor 调用，返回结构化 NavigationResult
```

---

### 3️⃣ OCRProcessor

**违规原因：**
- OCR text ≠ 世界事实
- 必须经过候选池 / 时效判断

**违规调用位置：**

| 文件 | 行号 | 调用方式 | 状态 |
|------|------|----------|------|
| `main.py` | 127 | `self.ocr_processor = OCRProcessor()` | ⚠️ **违规** |
| `main.py` | 455 | `texts = self.ocr_processor.extract_text(frame)` | ⚠️ **违规**（已标记 TODO） |

**高危检查：**
- ✅ 未发现直接写入 `LibraryRegistry`
- ✅ 未发现直接写入 `MapRegistry`
- ✅ 未发现直接写入 `SceneRegistry`

**正确迁移路径：**
```
OCRProcessor
   ↓
vision_pipeline/lv4_executors/modeling_executor.py
   ↓
content_candidate (ContentCandidate)
   ↓
CandidatePool.upsert_observation()
```

**迁移动作：**
```python
# main.py:127, 455
# TODO: move OCR call to vision_pipeline.lv4_executors.modeling_executor
# 当前：main.py 直接调用 OCRProcessor.extract_text()
# 目标：通过 ModelingExecutor 调用，生成 ContentCandidate，进入 CandidatePool
```

---

### 4️⃣ QwenVLProcessor

**⚠️ 这是当前工程最危险的一个**

**违规原因：**
- QwenVL = 强语义模型
- 一旦直连 decision，会绕过所有 Gate

**违规调用位置：**

| 文件 | 行号 | 调用方式 | 状态 |
|------|------|----------|------|
| `main.py` | 128 | `self.qwen_processor = QwenVLProcessor()` | ⚠️ **违规** |
| `main.py` | 459 | `description = self.qwen_processor.generate_description(...)` | ⚠️ **违规**（已标记 TODO） |

**高危检查：**
- ✅ 未发现直接调用 `decision_controller`
- ✅ 未发现直接调用 `speech_policy_engine`
- ✅ 未发现直接调用 `task_chain`

**正确迁移路径：**
```
QwenVLProcessor
   ↓
vision_pipeline/lv4_executors/modeling_executor.py
   ↓
(structured interpretation)
   ↓
LV6 World State Manager / LV5 Task-aware Aggregator
```

**迁移动作：**
```python
# main.py:128, 459
# TODO: prohibit direct VL usage outside vision_pipeline
# 当前：main.py 直接调用 QwenVLProcessor.generate_description()
# 目标：通过 ModelingExecutor 调用，生成结构化解释，进入 LV6 / LV5
```

---

## 三、core/ 内部"视觉越权"审计（关键但隐蔽）

### 5️⃣ core/world_model/*

**必查文件审计结果：**

| 文件 | 检查项 | 结果 |
|------|--------|------|
| `scene_registry.py` | image/frame/bbox/ocr | ✅ **干净**（只有注释提到，无实际使用） |
| `map_registry.py` | image/frame/bbox/ocr | ✅ **干净**（只有注释提到，无实际使用） |
| `memory_registry.py` | image/frame/bbox/ocr | ✅ **干净**（只有注释提到，无实际使用） |
| `candidate_pool.py` | image/frame/bbox/ocr | ✅ **干净**（只有注释提到，无实际使用） |

**结论：**
- ✅ `core/world_model/*` 模块是**干净的**
- ✅ 所有视觉相关关键词只出现在注释中（护栏声明）
- ✅ 无实际违规调用

---

### 6️⃣ core/task_chain/task_planner.py

**审计结果：**
- ✅ **干净**：未发现直接使用 image / frame / bbox / ocr
- ✅ 只消费 `ContextBundle`（来自 Scene / Map / Risk / Memory）
- ✅ 符合设计原则：任务链不直接看视觉

**结论：**
- ✅ `TaskPlanner` 是**干净的**，无需迁移

---

### 7️⃣ core/scene_state_builder.py

**审计结果：**

| 行号 | 内容 | 状态 |
|------|------|------|
| 94 | `objects: YOLO 检测结果` | ⚠️ **违规** |
| 95 | `texts: OCR 识别结果` | ⚠️ **违规** |
| 102 | `object_labels = [obj.get("label", "") for obj in objects]` | ⚠️ **违规** |
| 103 | `sign_texts = [text.get("text", "") for text in texts]` | ⚠️ **违规** |

**违规原因：**
- `SceneStateBuilder` 直接接收 YOLO 和 OCR 的原始结果
- 违反了"world_model 不得消费原始感知"的原则

**迁移动作：**
```python
# core/scene_state_builder.py:94-103
# TODO: world_model must not consume raw perception
# 当前：SceneStateBuilder.build() 直接接收 objects (YOLO) 和 texts (OCR)
# 目标：改为接收 WorldUpdate 或结构化 SceneHint
# 迁移路径：通过 vision_pipeline → ModelingExecutor → WorldUpdate → SceneStateBuilder
```

**迁移路径：**
```
YOLO/OCR 原始结果
   ↓
vision_pipeline/lv4_executors/modeling_executor.py
   ↓
WorldUpdate (structured)
   ↓
SceneStateBuilder.build(world_update)
```

---

### 8️⃣ decision_controller.py

**审计结果：**
- ✅ **干净**：未发现直接调用 YOLO / OCR / QwenVL
- ✅ 只做调度，不"看"世界

**结论：**
- ✅ `DecisionController` 是**干净的**，无需迁移

---

### 9️⃣ speech_policy_engine.py

**审计结果：**
- ✅ **干净**：未发现直接使用 OCR / VL 结果
- ✅ 只处理语音策略，不直接消费感知

**结论：**
- ✅ `SpeechPolicyEngine` 是**干净的**，无需迁移

---

## 四、main.py 综合审计（核心违规点）

### 违规调用汇总

| 行号 | 违规内容 | 迁移目标 | 优先级 |
|------|----------|----------|--------|
| 107 | `CameraHandler()` | `vision_pipeline/pipeline_controller.py` | 🔴 **P0** |
| 126 | `YOLODetector()` | `vision_pipeline/lv4_executors/navigation_executor.py` | 🔴 **P0** |
| 127 | `OCRProcessor()` | `vision_pipeline/lv4_executors/modeling_executor.py` | 🔴 **P0** |
| 128 | `QwenVLProcessor()` | `vision_pipeline/lv4_executors/modeling_executor.py` | 🔴 **P0** |
| 451 | `yolo_detector.detect(frame)` | 通过 `NavigationExecutor` | 🔴 **P0** |
| 455 | `ocr_processor.extract_text(frame)` | 通过 `ModelingExecutor` | 🔴 **P0** |
| 459 | `qwen_processor.generate_description(...)` | 通过 `ModelingExecutor` | 🔴 **P0** |

**当前状态：**
- ✅ 已标记 `TODO: migrate to vision_pipeline`（行 443-448）
- ⏳ 待执行实际迁移

---

## 五、最终输出：迁移对照表

### 文件级迁移对照表

| 当前位置 | 违规调用 | 迁移目标 | 迁移方式 |
|----------|----------|----------|----------|
| `main.py:107` | `CameraHandler()` | `vision_pipeline/pipeline_controller.py` | 通过 `PipelineController` 管理 |
| `main.py:126` | `YOLODetector()` | `vision_pipeline/lv4_executors/navigation_executor.py` | 注入到 `NavigationExecutor` |
| `main.py:127` | `OCRProcessor()` | `vision_pipeline/lv4_executors/modeling_executor.py` | 注入到 `ModelingExecutor` |
| `main.py:128` | `QwenVLProcessor()` | `vision_pipeline/lv4_executors/modeling_executor.py` | 注入到 `ModelingExecutor` |
| `main.py:451` | `yolo_detector.detect(frame)` | `NavigationExecutor.run()` | 封装到 `NavigationExecutor` |
| `main.py:455` | `ocr_processor.extract_text(frame)` | `ModelingExecutor.run()` | 封装到 `ModelingExecutor` |
| `main.py:459` | `qwen_processor.generate_description(...)` | `ModelingExecutor.run()` | 封装到 `ModelingExecutor` |
| `core/scene_state_builder.py:94-103` | `build(objects, texts)` | 接收 `WorldUpdate` | 改为接收结构化输入 |

---

## 六、审计结论

### ✅ 干净的模块（不用再碰）

1. **core/world_model/***
   - SceneRegistry ✅
   - MapRegistry ✅
   - MemoryRegistry ✅
   - CandidatePool ✅

2. **core/task_chain/task_planner.py** ✅

3. **core/decision_controller.py** ✅

4. **core/speech_policy_engine.py** ✅

### ⚠️ 技术债源头（必须迁移）

1. **main.py**（核心违规点）
   - 所有视觉工具的直接调用
   - 所有视觉结果的直接消费
   - **迁移优先级：P0**

2. **core/scene_state_builder.py**（隐蔽违规点）
   - 直接接收 YOLO 和 OCR 的原始结果
   - **迁移优先级：P0**

---

## 七、下一步执行顺序

### Step 1: 迁移 utils → vision_pipeline（P0）

1. **CameraHandler** → `PipelineController`
   - 在 `PipelineController` 中管理摄像头
   - `main.py` 不再直接创建 `CameraHandler`

2. **YOLODetector** → `NavigationExecutor`
   - 注入 `YOLODetector` 到 `NavigationExecutor`
   - `main.py` 通过 `PipelineController` 调用

3. **OCRProcessor** → `ModelingExecutor`
   - 注入 `OCRProcessor` 到 `ModelingExecutor`
   - `main.py` 通过 `PipelineController` 调用

4. **QwenVLProcessor** → `ModelingExecutor`
   - 注入 `QwenVLProcessor` 到 `ModelingExecutor`
   - `main.py` 通过 `PipelineController` 调用

### Step 2: 补全 LV2 / LV3（P1）

- 完善 `QualityGate` 的实际评估逻辑
- 完善 `SemanticRouter` 的路由策略

### Step 3: LV4.2 建模细化（P2）

- 细化 `ModelingExecutor` 的 schema
- 实现内容抽取逻辑

---

## 八、审计完成时间

**审计日期：** 2024-12-19  
**审计范围：** 全工程视觉工具调用  
**审计结果：** 8 个违规调用点（7 个在 `main.py`，1 个在 `core/scene_state_builder.py`）  
**迁移优先级：** P0（必须立即执行）

---

## 九、审计验证

**验证方法：**
```bash
# 在 Cursor 中执行以下搜索，确认无遗漏：
grep -r "CameraHandler\|YOLODetector\|OCRProcessor\|QwenVLProcessor" core/
grep -r "\.detect(\|\.extract_text(\|\.generate_description(" core/
```

**预期结果：**
- ✅ `core/` 目录下应该**无任何匹配**
- ✅ 所有调用都应该在 `main.py` 或 `vision_pipeline/` 中

