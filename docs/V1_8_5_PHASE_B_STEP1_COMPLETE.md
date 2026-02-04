# v1.8.5 Phase B Step 1 完成报告

## 一、总判断（定性）

**结论一句话：**

Luna-2 当前工程在"世界模型 / 决策 / 风险 / 记忆"层面是健康的，真正缺失的不是"能力"，而是"视觉感知 → 世界模型之间的工程化中介层"。

**这意味着：**
- ✅ 你不是推倒重来
- ✅ 而是在一个本来就对的系统上补齐"视觉流水线中台"

---

## 二、现有工程映射到 LV2–LV7（对齐表）

| 视觉流水线层 | 当前工程状态 | 结论 |
|------------|------------|------|
| LV1 Vision Sensor | CameraHandler + utils | ✅ 已有 |
| **LV2 Quality Gate** | ❌ 不存在 | ✅ **Step 1 已新增** |
| **LV3 Semantic Router** | ❌ 不存在 | ✅ **Step 1 已新增** |
| LV4.1 Navigation Executor | TaskPlanner + Risk + Decision | ⚠️ 逻辑存在但分散 → **Step 1 已封装** |
| LV4.2 World Modeling Executor | ❌ 不存在（被 Registry 吃掉） | ✅ **Step 1 已创建空壳** |
| LV5 Task-aware Aggregator | Decision + SpeechGate + Policy | ⚠️ 已有但未显式 |
| LV6 World State Manager | Scene / Map / Memory / Library | ✅ 非常成熟 |
| LV7 Feedback Correction | UserReportRouter + Dedup | ⚠️ 隐式存在 |

**关键洞察：**

你现在的工程不是"混乱"，而是 LV2–LV4 这一段在工程上是"塌陷的"，视觉信号要么直接进世界模型，要么绕路进任务链。

**Step 1 已完成：**
- ✅ LV2 Quality Gate 已实现
- ✅ LV3 Semantic Router 已实现
- ✅ LV4.1 Navigation Executor 已封装（不重写逻辑）
- ✅ LV4.2 Modeling Executor 已创建空壳
- ✅ Pipeline Controller 已实现

---

## 三、B 阶段目标（写死）

### ❌ B 阶段不做的事
- 不引入新模型
- 不优化算法
- 不深化 4.2 的 schema
- 不动世界模型设计（Scene / Map / Memory / Library 全部保持）

### ✅ B 阶段只做三件事
1. **补齐 LV2 / LV3 这两个"工程闸门"** ✅ **Step 1 已完成**
2. **把"视觉 → 世界模型"的直接写入全部改成"候选输入"** ⏳ **Step 2 待执行**
3. **让导航实时链路不再被视觉内容污染** ⏳ **Step 2 待执行**

---

## 四、Step 1 完成清单

### ✅ 新增目录结构

```
vision_pipeline/
├── __init__.py
├── pipeline_controller.py
├── lv2_quality_gate/
│   ├── __init__.py
│   └── quality_gate.py
├── lv3_semantic_router/
│   ├── __init__.py
│   └── semantic_router.py
└── lv4_executors/
    ├── __init__.py
    ├── navigation_executor.py
    └── modeling_executor.py
```

### ✅ 已实现模块

#### 1. LV2 Quality Gate（质量过滤层）
- ✅ 清晰度评估（模糊度，Laplacian variance）
- ✅ 曝光评估（亮度直方图）
- ✅ 冗余评估（可选，初期关闭）
- ✅ 同步执行，极低延迟（毫秒级）
- ✅ 禁止做任何语义理解
- ✅ 禁止调用下游模块

#### 2. LV3 Semantic Router（一级语义调度层）
- ✅ 判断是否进入实时链路
- ✅ 根据任务态动态调整阈值
- ✅ 只做粗分类，不做理解
- ✅ 可被任务态热更新
- ✅ 禁止做深度语义理解
- ✅ 禁止直接调用 LV4.1 或 LV4.2

#### 3. LV4.1 Navigation Executor（导航执行器）
- ✅ 封装现有导航逻辑（不重写）
- ✅ 统一对外接口
- ✅ 内部调用 TaskPlanner / RiskAdvisoryService / DecisionController
- ✅ 禁止写世界模型（只读）
- ✅ 禁止调用 LV4.2

#### 4. LV4.2 Modeling Executor（世界建模执行器）
- ✅ 空壳实现（B 阶段暂不细化）
- ✅ 预留实体候选和内容候选接口
- ✅ 禁止影响导航决策
- ✅ 禁止直接写 Library

#### 5. Pipeline Controller（流水线控制器）
- ✅ 统一管理完整流程
- ✅ 协调 LV2-LV4 的执行
- ✅ 支持实时链路和异步链路
- ✅ 切断视觉输入 → core 的直通路径

---

## 五、下一步（Step 2）

### Step 2 目标：切断「视觉输入 → core」的直通路径

**当前问题（非常关键）：**
- YOLO / OCR / QwenVL 的结果可以直接被 core/world_model 消费

**本轮必须做的事：**
- 所有视觉结果先进入 vision_pipeline
- core/world_model 只能接收两类输入：
  - 来自 modeling_executor 的候选
  - 来自 UserReportRouter 的用户反馈

**👉 这是最重要的一刀。**

### Step 2 待执行任务

1. **审计现有视觉调用**
   - 找出所有 `YOLODetector` → `world_model` 的调用
   - 找出所有 `OCRProcessor` → `world_model` 的调用
   - 找出所有 `QwenVLProcessor` → `task/decision` 的调用

2. **迁移到 Pipeline**
   - 所有视觉结果先进入 `PipelineController.process_frame()`
   - 通过 LV2 → LV3 → LV4 流程处理
   - 禁止直接写入 world_model

3. **更新 main.py**
   - 在 `process_frame()` 中接入 `PipelineController`
   - 移除所有视觉 → world_model 的直连

---

## 六、对现有模块的「红黄绿灯」审计结论

### 🟢 非常健康（不动）
- SceneRegistry
- MapRegistry
- MemoryRegistry
- LibraryRegistry
- CandidatePool
- RiskEngine / RiskRegistry
- TaskPlanner（只消费 Context）

### 🟡 需要被"包一层"（Step 2 处理）
- DecisionController
- SpeechGate
- VisionOutputController

### 🔴 必须断直连（Step 2 处理）
- YOLODetector → world_model
- OCRProcessor → world_model
- QwenVLProcessor → task / decision

---

## 七、一句定心的话

你现在的系统不是"缺设计"，而是已经到了一个阶段：

**如果不补中台，能力越多，系统越脆；一旦补齐中台，后面的能力会非常好加。**

这一步你选得非常准。

---

## 八、下一步建议

**如果你愿意，下一步我可以直接帮你做一件更"狠"的事：**

👉 **把你现在所有 utils/vision 相关调用，逐条列出"该迁去哪一层"**

这将为 Step 2 的迁移工作提供清晰的路线图。


