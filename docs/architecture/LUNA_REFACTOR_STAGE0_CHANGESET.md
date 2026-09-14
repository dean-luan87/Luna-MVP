# Luna 架构整顿 Stage-0：变更清单（边界固化 + 接口占位）

> 目标：**不破坏现有主链运行**，先把 Core / Capabilities / Individual Backend Capability 的边界固化，并完成最小接口占位。

## 1. 本轮新增了哪些文档（产物）

- `docs/architecture/LUNA_MODULE_OWNERSHIP_ANALYSIS.md`
  - 模块归属表（含：当前职责/耦合对象/建议归属层/处理方式/风险）
  - 高风险混合耦合点记录（重点：`main.py`）
  - 后续迁移优先级建议（仅记录，不执行）

- `docs/architecture/LUNA_LAYERED_ARCHITECTURE_TARGET.md`
  - Core Framework 定义与明确排除项
  - Capability Layer（Voice/Vision/Emotion）定义与接入方式
  - Individual Backend Capability（whitebox/memory/logs/traces/audit）逻辑归属
  - 多模型接入原则（provider/adapter/registry/schema 的硬边界）

- `docs/architecture/LUNA_REFACTOR_STAGE0_CHANGESET.md`
  - Stage-0 变更清单（本文）

## 2. 本轮新增了哪些目录占位（不做迁移）

> 注意：目录存在是为了后续演进；**Stage-0 不做大规模迁移**。

### 2.1 Core Framework 目标占位

- `core/runtime/`（README 占位）
- `core/task_chain/`（既有实现存在；本轮未迁移）
- `core/scheduler/`（README 占位）
- `core/controller/`（README 占位）
- `core/policy/`（README 占位）
- `core/state/`（README 占位）
- `core/session/`（README 占位）

### 2.2 Capabilities 目标占位

- `capabilities/voice/`（interfaces/providers/schemas/registry + `VoiceEvent`/接口/registry）
- `capabilities/vision/`（interfaces/providers/schemas/registry + `VisionEvent`/接口/registry）
- `capabilities/emotion/`（interfaces/schemas/registry 占位 + `EmotionEvent`）

### 2.3 Individual Backend Capability bridge 占位

- `backend_bridge/`（README + 子目录 README 占位）
  - `backend_bridge/whitebox/`
  - `backend_bridge/memory/`
  - `backend_bridge/logs/`
  - `backend_bridge/traces/`
  - `backend_bridge/audit/`

### 2.4 shared（跨 capability 的基础占位）

- `shared/schemas/base_events.py`（BaseEvent/BaseContextRef）
- `shared/registry/provider_registry.py`（ProviderRegistry/ProviderRecord）
- `shared/schemas/__init__.py`、`shared/types/__init__.py`、`shared/registry/__init__.py`

## 3. 本轮新增了哪些接口占位代码（长期边界）

### 3.1 Voice（语音）

- `capabilities/voice/interfaces/providers.py`
  - `VoiceInputProvider`
  - `ASRProvider`
  - `TTSProvider`
  - `VoiceDialogueBridge`
- `capabilities/voice/schemas/voice_event.py`
  - `VoiceEvent`（按硬指令字段定义）
- `capabilities/voice/registry/voice_registry.py`
  - `VoiceCapabilityRegistry`（provider registry 管理入口）

### 3.2 Vision（视角/视觉）

- `capabilities/vision/interfaces/providers.py`
  - `VisionProvider`
  - `DetectionProvider`
  - `OCRProvider`
  - `TrackingProvider`
- `capabilities/vision/schemas/vision_event.py`
  - `VisionEvent`（按硬指令字段定义）
- `capabilities/vision/registry/vision_registry.py`
  - `VisionCapabilityRegistry`

### 3.3 Emotion（情感 reserved）

- `capabilities/emotion/interfaces/providers.py`
  - `EmotionProvider`（占位）
- `capabilities/emotion/schemas/emotion_event.py`
  - `EmotionEvent`（占位）
- `capabilities/emotion/registry/emotion_registry.py`
  - `EmotionCapabilityRegistry`（占位）

## 4. 哪些旧文件做了轻量调整？

- **本轮默认不动旧文件**（零行为变更优先）。
- 若后续需要“止血式边界声明”，只允许：
  - 轻量注释补充（ownership / future migration）
  - 新增 facade/adapter 文件并在文档中指向（但不切换主链调用）

## 5. 哪些模块明确保持不动（Stage-0 底线）

- `main.py`（不改调用语义/不改行为/不迁移）
- 语音播放链现状：
  - `_handle_speech_decision` / `_execute_speech_decision` / `_speak_safely`（仍在 `main.py`）
  - `core/speech_gate.py`
  - `core/audio_worker.py`
  - `modules/voice.py`
- ASR 原型：
  - `modules/voice_to_text.py`（保持工具形态，不接入主链）
- Individual backend capability 现状：
  - `decision_monitor/*`（不迁移、不拆服务）

## 6. 哪些迁移留到后续阶段（为什么 Stage-0 不做）

- **`main.py` 解耦**（高风险）：涉及主链编排，Stage-0 禁止改运行逻辑；只先做边界与接口占位，后续以 controller/facade 方式逐步收敛。
- **`modules/voice.py` 迁移到 capabilities/provider**：迁移会改变 import 路径与运行链路，Stage-0 禁止断链；后续用 adapter 先兼容，再迁移。
- **`decision_monitor` 物理拆分**：Stage-0 只做逻辑归属与 bridge 声明，避免重构带来评测/日志脱钩风险。
- **vision_pipeline 结构治理**：涉及大范围模块交互，Stage-0 仅做归属声明与未来拆分标记。

## 7. 本轮验收点对照（8 点）

1. 区分 Core / Capabilities / Individual Backend Capability：**已通过文档与占位目录固化**
2. Voice/Vision/Emotion 可插拔定义：**已建立 capability 目录与接口/registry/schema**
3. whitebox/memory/logs/traces/audit 逻辑归属：**已建立 backend_bridge README 与归属声明**
4. provider/adapter/registry/schema 思路：**shared registry + capability registries + schema 定义**
5. 接口占位不绑死具体模型：**Protocol + dataclass schema，无厂商依赖**
6. 保住当前主链运行：**未改现有主链逻辑与调用**
7. 识别混合耦合与污染点：**ownership 文档记录 `main.py` 等高风险点**
8. 产出完整文档便于后续语音架构设计：**本轮产物齐全**

