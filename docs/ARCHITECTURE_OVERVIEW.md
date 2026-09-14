# Luna-2 工程整体架构说明

## 一、顶层模块划分（目录级）

### 1. 核心模块（`core/`）

#### 1.1 世界建模层（`core/world_model/`）
- **Scene Registry** (`scene/scene_registry.py`): 场景注册表，管理场景切换和连续性
- **Map Registry** (`map/map_registry.py`): 地图注册表，提供客观约束（地形、时间、天气）
- **Memory Registry** (`memory/memory_registry.py`): 记忆注册表，记录主观体验/偏好/不适
- **Library Registry** (`library/library_registry.py`): 知识库注册表，记录慢确认事实（可退潮）
- **Candidate Pool** (`memory/candidate_pool.py`): 事实候选池，管理候选事实的升级流程
- **User Report Router** (`memory/user_report_router.py`): 用户报告路由器，分流用户反馈到 Memory/CandidatePool
- **Emotion Port** (`emotion/emotion_port.py`): 情绪信号入口，处理情绪信号（Phase D Lite）
- **Common Gates** (`common/gates.py`): 统一重定位闸门，防止错位污染
- **Common Types** (`common/types.py`): 通用类型定义（PositionState, EnvironmentContext）

#### 1.2 风险系统（`core/risk/`）
- **Risk Advisory Service** (`risk_advisory_service.py`): 风险告知服务，计算风险等级和生成建议
- **Risk Registry** (`risk_registry.py`): 风险对象注册表，管理风险对象的生命周期
- **Risk Engine** (`risk_engine.py`): 风险引擎，计算风险等级和变化趋势
- **Risk Object Factory** (`risk_object_factory.py`): 风险对象工厂，创建风险对象
- **Warning Policy** (`warning_policy.py`): 警告策略，生成警告文本
- **User Position Provider** (`user_position_provider.py`): 用户位置提供器，提供用户位置信息
- **Robustness Test Harness** (`robustness_test_harness.py`): 鲁棒性测试框架，验证系统稳定性

#### 1.3 任务链（`core/task_chain/`）
- **Task Planner** (`task_planner.py`): 任务规划器，在给定上下文中选择"合适的行动"
- **Types** (`types.py`): 任务链类型定义（ContextBundle, RiskBias, Path）

#### 1.4 决策与控制层（`core/`）
- **Decision Controller** (`decision_controller.py`): 决策控制器，统一决策入口
- **Decision Scheduler** (`decision_scheduler.py`): 决策调度器，管理决策执行顺序
- **Speech Gate** (`speech_gate.py`): 语音总闸，系统级"注意力与发言权中枢"
- **Speech Policy Engine** (`speech_policy_engine.py`): 语音策略引擎，控制播报策略
- **Speech Deduplicator** (`speech_deduplicator.py`): 语音去重器，防止重复播报

#### 1.5 场景处理（`core/scene/`）
- **Scene Registry** (`scene_registry.py`): 场景注册表（旧版，待迁移）
- **Scene State Builder** (`scene_state_builder.py`): 场景状态构建器
- **Scene Stability Tracker** (`scene_stability_tracker.py`): 场景稳定性追踪器
- **Environment Context** (`environment_context.py`): 环境上下文

#### 1.6 系统级模块（`core/`）
- **System Memory** (`system_memory.py`): 系统记忆，管理全局状态
- **Vision Output Controller** (`vision_output_controller.py`): 视觉输出控制器
- **Vision Output State** (`vision_output_state.py`): 视觉输出状态
- **Observer Mode Manager** (`observer_mode_manager.py`): 观察者模式管理器
- **Human Assist Fallback** (`human_assist_fallback.py`): 人工辅助降级
- **Audio Worker** (`audio_worker.py`): 音频工作器，异步处理 TTS
- **Audio Playback Guard** (`audio_playback_guard.py`): 音频播放保护，防止音频冲突

### 2. 主程序（`main.py`）
- **LunaBadgeMVP**: 主程序入口，协调所有模块

### 3. 工具模块（`utils/`）
- **YOLODetector**: YOLO 物体检测器
- **OCRProcessor**: OCR 处理器
- **QwenVLProcessor**: QwenVL 视觉语言模型处理器
- **WhisperProcessor**: Whisper 语音识别处理器
- **TTSProcessor**: TTS 语音合成处理器
- **CameraHandler**: 相机处理器

### 4. 配置模块（`config/`）
- **系统配置**: 模型路径、相机配置、处理配置、输出配置、调试配置

---

## 二、每个模块的核心职责描述（一句话）

### 世界建模层
- **SceneRegistry**: 管理场景切换和连续性，提供当前场景状态
- **MapRegistry**: 提供客观约束（地形、时间、天气、风险），不直接下判断
- **MemoryRegistry**: 记录主观体验/偏好/不适，不参与事实判断
- **LibraryRegistry**: 记录慢确认事实（可退潮），管理知识库
- **CandidatePool**: 管理候选事实的升级流程，防止污染
- **UserReportRouter**: 分流用户反馈到 Memory/CandidatePool，防止污染事实层
- **EmotionPort**: 处理情绪信号，只影响体验权重，不改变世界

### 风险系统
- **RiskAdvisoryService**: 计算风险等级和生成建议，不直接驱动播报
- **RiskRegistry**: 管理风险对象的生命周期，支持过期和合并
- **RiskEngine**: 计算风险等级和变化趋势，提供风险评估
- **RiskObjectFactory**: 创建风险对象，支持 POINT/LINE/AREA 几何类型
- **WarningPolicy**: 生成警告文本，不直接播报
- **UserPositionProvider**: 提供用户位置信息，每帧更新

### 任务链
- **TaskPlanner**: 在给定上下文中选择"合适的行动"，消费 Scene/Map/Memory/Risk
- **ContextBundle**: 统一上下文包，包含 Scene/Map/Memory/Risk/Emotion

### 决策与控制层
- **DecisionController**: 统一决策入口，协调各决策源
- **DecisionScheduler**: 管理决策执行顺序，防止冲突
- **SpeechGate**: 系统级"注意力与发言权中枢"，控制播报时机
- **SpeechPolicyEngine**: 控制播报策略，决定播报内容和方式
- **SpeechDeduplicator**: 防止重复播报，去重处理

### 系统级模块
- **SystemMemory**: 管理全局状态，提供系统级记忆
- **VisionOutputController**: 控制视觉输出，管理视觉状态
- **ObserverModeManager**: 管理观察者模式，监控系统状态
- **AudioWorker**: 异步处理 TTS，防止阻塞主线程
- **AudioPlaybackGuard**: 防止音频冲突，保护音频设备

---

## 三、模块之间的主要调用关系

### 数据流向（单向）

```
[感知层] → [世界建模层] → [任务链] → [决策层] → [输出层]
    ↓           ↓            ↓          ↓         ↓
 Camera    SceneRegistry  TaskPlanner  Decision  TTS
 Vision    MapRegistry    ContextBundle Controller
 IMU       MemoryRegistry
 GPS       RiskAdvisoryService
```

### 主要调用关系

1. **主程序 → 各模块**
   - `main.py` → `DecisionController` → `DecisionScheduler` → `SpeechGate`
   - `main.py` → `RiskAdvisoryService` → `RiskRegistry` → `RiskEngine`
   - `main.py` → `SceneRegistry` → `MapRegistry` → `MemoryRegistry`

2. **世界建模层内部**
   - `SceneRegistry` → `MapRegistry` (读取地图提示)
   - `SceneRegistry` → `MemoryRegistry` (读取记忆偏置)
   - `MemoryRegistry` → `CandidatePool` (发出事实候选)
   - `CandidatePool` → `LibraryRegistry` (升级候选事实)

3. **任务链消费世界建模**
   - `TaskPlanner` ← `ContextBundle` (包含 Scene/Map/Memory/Risk/Emotion)
   - `TaskPlanner` ← `SceneRegistry.get_current_scene()`
   - `TaskPlanner` ← `RiskAdvisoryService.get_current_risk_bias()`
   - `TaskPlanner` ← `MemoryRegistry.get_experience_hints()`

4. **用户反馈流**
   - `UserReportRouter` → `MemoryRegistry` (体验/偏好)
   - `UserReportRouter` → `CandidatePool` (事实信号)
   - `UserReportRouter` → `EmotionPort` (情绪信号)

5. **风险系统**
   - `RiskAdvisoryService` → `RiskRegistry` (注册/更新风险对象)
   - `RiskAdvisoryService` → `RiskEngine` (计算风险等级)
   - `RiskAdvisoryService` → `WarningPolicy` (生成警告文本)

6. **决策层**
   - `DecisionController` → `DecisionScheduler` (调度决策)
   - `DecisionScheduler` → `SpeechGate` (控制播报)
   - `SpeechGate` → `AudioWorker` (异步 TTS)

### 禁止的调用关系

- ❌ 任务链 → 世界建模层（只读，不写）
- ❌ 世界建模层 → 决策层（不直接驱动播报）
- ❌ 风险系统 → 决策层（不直接驱动播报）
- ❌ 下游模块 → 上游模块（禁止逆向调用）

---

## 四、模块层级分类

### 感知层 / 视觉相关
- **CameraHandler** (`utils/`): 相机处理器
- **YOLODetector** (`utils/`): YOLO 物体检测器
- **OCRProcessor** (`utils/`): OCR 处理器
- **QwenVLProcessor** (`utils/`): QwenVL 视觉语言模型处理器
- **VisionOutputController** (`core/vision_output_controller.py`): 视觉输出控制器
- **VisionOutputState** (`core/vision_output_state.py`): 视觉输出状态

**注意**: 当前工程中**尚未实现 LV2 Quality Gate 和 LV3 Semantic Router**，这些应该在视觉流水线中实现。

### 导航与实时决策
- **TaskPlanner** (`core/task_chain/task_planner.py`): 任务规划器，选择路径
- **DecisionController** (`core/decision_controller.py`): 决策控制器，统一决策入口
- **DecisionScheduler** (`core/decision_scheduler.py`): 决策调度器，管理决策执行顺序
- **RiskAdvisoryService** (`core/risk/risk_advisory_service.py`): 风险告知服务，计算风险等级
- **RiskEngine** (`core/risk/risk_engine.py`): 风险引擎，计算风险等级和变化趋势

### 信息理解 / 内容处理
- **OCRProcessor** (`utils/`): OCR 处理器
- **QwenVLProcessor** (`utils/`): QwenVL 视觉语言模型处理器
- **WhisperProcessor** (`utils/`): Whisper 语音识别处理器

**注意**: 当前工程中**尚未实现 LV4.2 World Modeling Executor**，内容抽取应该在视觉流水线中实现。

### 世界建模 / 记忆
- **SceneRegistry** (`core/world_model/scene/scene_registry.py`): 场景注册表
- **MapRegistry** (`core/world_model/map/map_registry.py`): 地图注册表
- **MemoryRegistry** (`core/world_model/memory/memory_registry.py`): 记忆注册表
- **LibraryRegistry** (`core/world_model/library/library_registry.py`): 知识库注册表
- **CandidatePool** (`core/world_model/memory/candidate_pool.py`): 事实候选池
- **SystemMemory** (`core/system_memory.py`): 系统记忆

### 用户反馈
- **UserReportRouter** (`core/world_model/memory/user_report_router.py`): 用户报告路由器
- **EmotionPort** (`core/world_model/emotion/emotion_port.py`): 情绪信号入口
- **SpeechGate** (`core/speech_gate.py`): 语音总闸，接收用户反馈
- **HumanAssistFallback** (`core/human_assist_fallback.py`): 人工辅助降级

---

## 五、当前存在的问题分析

### 5.1 多个模块同时做"是否导航"的判断

**问题**: 当前工程中**不存在**明确的"是否导航"判断逻辑。

**建议**: 
- 应该在 `LV3 Semantic Router` 中实现"是否导航"的判断
- `TaskPlanner` 应该只负责"在导航时选择路径"，不负责判断"是否导航"

### 5.2 多处重复的图像质量 / 清晰度判断

**问题**: 当前工程中**不存在**图像质量/清晰度判断逻辑。

**建议**: 
- 应该在 `LV2 Quality Gate` 中实现统一的图像质量判断
- 避免在多个模块中重复实现质量判断逻辑

### 5.3 模块既做实时决策又写长期记忆的情况

**问题分析**:

1. **RiskAdvisoryService** ✅ **正确**
   - 只计算风险等级，不写记忆
   - 通过 `get_current_risk_bias()` 提供只读接口

2. **TaskPlanner** ✅ **正确**
   - 只选择路径，不写记忆
   - 只读 `ContextBundle`，不修改世界模型

3. **MemoryRegistry** ✅ **正确**
   - 只写记忆，不参与实时决策
   - 通过 `get_experience_hints()` 提供只读接口

4. **UserReportRouter** ✅ **正确**
   - 只路由用户反馈，不参与实时决策
   - 分流到 Memory/CandidatePool，不直接写 Library

5. **DecisionController** ⚠️ **需要检查**
   - 需要确认是否在决策过程中写记忆
   - 建议：决策结果只写 Memory（体验），不写事实

**结论**: 当前架构**基本正确**，模块职责分离清晰。但需要：
- 实现 `LV2 Quality Gate` 和 `LV3 Semantic Router` 来统一视觉处理流程
- 实现 `LV4.2 World Modeling Executor` 来处理内容抽取
- 确保 `DecisionController` 不直接写长期记忆

---

## 六、架构改进建议

### 6.1 视觉流水线集成

按照 `docs/VISION_PIPELINE.md` 的规范，需要实现：

1. **LV2 Quality Gate**: 统一图像质量判断
2. **LV3 Semantic Router**: 统一"是否导航"判断
3. **LV4.1 Navigation Executor**: 导航执行器（部分已实现）
4. **LV4.2 World Modeling Executor**: 世界建模执行器（待实现）
5. **LV5 Task-aware Aggregator**: 任务感知聚合器（部分已实现）
6. **LV6 World State Manager**: 世界状态管理器（部分已实现）
7. **LV7 Feedback Correction**: 反馈纠错层（部分已实现）

### 6.2 模块职责进一步明确

1. **SceneRegistry**: 唯一负责场景切换
2. **MemoryRegistry**: 只写体验记忆，不写事实
3. **CandidatePool**: 只管理候选事实，不直接写 Library
4. **LibraryRegistry**: 只消费 CandidatePool，不直接写事实
5. **TaskPlanner**: 只选择路径，不修改世界模型
6. **DecisionController**: 只协调决策，不写长期记忆

### 6.3 数据流规范化

1. **实时链路**: Camera → LV2 → LV3 → LV4.1 → LV5 → Decision → TTS
2. **异步链路**: Camera → LV2 → LV3 → LV4.2 → LV6 → World Model
3. **反馈链路**: User → LV7 → LV5 → (Update Feedback) → LV6 (Mark Confidence)

---

## 七、总结

### 当前架构优势

1. ✅ **职责分离清晰**: 世界建模、任务链、决策层分离明确
2. ✅ **数据流单向**: 感知 → 世界 → 任务 → 决策 → 输出
3. ✅ **护栏到位**: 统一 Gate、限频、衰减机制完善
4. ✅ **可扩展**: 为二期、三期预留了接口

### 当前架构待完善

1. ⚠️ **视觉流水线**: 需要实现 LV2-LV7 完整流程
2. ⚠️ **内容抽取**: 需要实现 LV4.2 World Modeling Executor
3. ⚠️ **质量判断**: 需要实现 LV2 Quality Gate 统一质量判断

### 架构健康度

- **模块职责**: ⭐⭐⭐⭐⭐ (5/5) - 职责分离清晰
- **数据流**: ⭐⭐⭐⭐⭐ (5/5) - 单向流动，无循环依赖
- **护栏机制**: ⭐⭐⭐⭐⭐ (5/5) - Gate、限频、衰减完善
- **可扩展性**: ⭐⭐⭐⭐⭐ (5/5) - 为未来扩展预留接口
- **视觉流水线**: ⭐⭐⭐ (3/5) - 部分实现，需要完善

**总体评分**: ⭐⭐⭐⭐ (4.5/5) - 架构健康，待完善视觉流水线


