# v1.8.5 Phase B 清理审计清单

## 一、清理 utils/：给每个视觉工具一个"合法身份"

### ✅ 已完成

#### 1. CameraHandler → LV1（Vision Sensor）
- ✅ 文件头已添加使用声明
- ✅ 明确 Role: Vision Sensor
- ✅ 明确 Forbidden: 任何语义判断、过滤或路由

#### 2. YOLODetector / OCRProcessor / QwenVLProcessor
- ✅ 文件头已添加使用声明
- ✅ 明确 Role: Vision Capability Unit
- ✅ 明确 Usage: Must be called ONLY from vision_pipeline.lv4_executors
- ✅ 明确 Forbidden: Direct calls from core/world_model, core/task_chain, decision_controller

### ⏳ 待迁移的调用点

#### main.py（已标记 TODO）
- **位置**: `main.py:445-453`
- **调用**: `YOLODetector.detect()`, `OCRProcessor.extract_text()`, `QwenVLProcessor.generate_description()`
- **状态**: ✅ 已标记 `TODO: migrate to vision_pipeline`
- **迁移目标**: `vision_pipeline.lv4_executors.navigation_executor`

---

## 二、给 core/world_model 加"视觉隔离护栏"

### ✅ 已完成

#### 1. WorldUpdate 类型定义
- ✅ 在 `core/world_model/common/types.py` 中已定义 `WorldUpdate`
- ✅ 明确原则：world_model 只接受"结构化事实"，不接受 frame / image / bbox / ocr_text

#### 2. 各 Registry 的护栏声明
- ✅ `SceneRegistry`: 已添加视觉隔离护栏声明
- ✅ `MapRegistry`: 已添加视觉隔离护栏声明
- ✅ `MemoryRegistry`: 已添加视觉隔离护栏声明
- ✅ `CandidatePool`: 已明确为"视觉事实进入世界模型的唯一合法入口"

### ⏳ 待检查的违规接口

需要逐条检查所有 public 方法，如果参数包含 `image/frame/bbox/raw_text`，标记为 TODO/DEPRECATED。

**检查命令**：
```bash
# 在 Cursor 中全局搜索
grep -r "def.*\(.*frame\|.*image\|.*bbox\|.*ocr_text\|.*raw_text" core/world_model/
```

---

## 三、pipeline_controller：最小可跑闭环

### ✅ 已完成

- ✅ `PipelineController` 已实现最小闭环
- ✅ 支持 Camera → LV2 → LV3 → LV4.1 → Decision 流程
- ✅ 已添加说明：今天的目标不是"功能完整"，而是"所有视觉入口开始走同一条管道"

---

## 四、今天不碰但要"锁死"的地方

### ✅ 已完成

- ✅ `ModelingExecutor` 已添加锁死声明
- ✅ 明确：Schema definition deferred（B 阶段不展开）
- ✅ 明确：Only candidate generation allowed

---

## 五、引用审计清单（待执行）

### 需要全局搜索的关键词

1. **image**
   - 搜索范围：`core/world_model/*`
   - 检查：是否出现在参数或方法中
   - 标记：如果出现，标记为 TODO/DEPRECATED

2. **frame**
   - 搜索范围：`core/world_model/*`
   - 检查：是否出现在参数或方法中
   - 标记：如果出现，标记为 TODO/DEPRECATED

3. **bbox**
   - 搜索范围：`core/world_model/*`
   - 检查：是否出现在参数或方法中
   - 标记：如果出现，标记为 TODO/DEPRECATED

4. **ocr**
   - 搜索范围：`core/world_model/*`
   - 检查：是否出现在参数或方法中
   - 标记：如果出现，标记为 TODO/DEPRECATED

### 检查问题

对于每个匹配项，问一句：
> "它现在所在的模块，有没有资格看到原始视觉？"

如果答案是否定的：
- 不马上改
- 标 TODO + 写迁移目标

---

## 六、今天结束时，工程应该达到的状态

### ✅ 目标状态

- ✅ 视觉能力都"有家可归"（已添加使用声明）
- ✅ core/world_model 不再被视觉污染（已添加护栏声明）
- ✅ 新的视觉流水线有入口、有边界（PipelineController 已实现）
- ✅ 后续任何人加功能，都知道"该加哪"（文档已明确）

### ⏳ 待完成

- ⏳ 完成引用审计（标记所有违规调用）
- ⏳ 迁移 main.py 中的视觉调用到 vision_pipeline
- ⏳ 检查并标记所有违规接口

---

## 七、下一步建议

👉 **下一步直接做一次"引用审计清单"**

我可以按这份工程说明，帮你列出一份"具体到文件名的迁移表"。

你只需要告诉我：
- 是现在继续，还是你先按这轮在 Cursor 里跑一遍？


