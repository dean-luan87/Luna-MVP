# Luna 架构整顿 Stage-0：目标分层架构（边界固化 + 接口占位）

> 本文档是 **Stage-0 硬边界定义**：先立边界，再接能力；先做抽象，不做重写；保证当前主链可运行且行为不被改变。

## A. Luna Core Framework 定义（通用框架层）

### A1. Core Framework 的职责边界（必须包含）

Core Framework 是独立于任何单一能力模块的通用骨架，负责：

- **runtime**：运行时循环、时钟、观测采样节拍、运行态记录
- **task chain**：任务链状态、位置、恢复/插入、主线阶段推进
- **scheduler**：调度决策与执行排程（不绑定具体能力）
- **controller**：把“观测/策略/能力输出”编排为一条可执行主链（不内嵌 capability 逻辑）
- **policy / governance**：规则治理、权限边界、风险优先级、门控（如 speech gate）
- **session / state / context**：会话上下文、状态快照、运行时状态管理

> 典型示例（现有仓库）：`runtime/*`、`core/decision_controller.py`、`core/speech_gate.py`、`decision_scheduler` 等属于 Core 的“骨架/治理/调度”范畴。

### A2. Core Framework 明确不包含（必须排除）

Core Framework **不包含**（且不得内嵌）：

- 语音 ASR/TTS 的具体实现与厂商差异（Voice capability 的 provider/adapter 负责）
- 视觉 OCR/检测/跟踪的具体实现与模型差异（Vision capability 的 provider/adapter 负责）
- 情感系统的具体推断与策略（Emotion capability，Stage-0 仅占位）
- whitebox / memory / logs / traces / audit 的“业务逻辑实现细节”（这些属于个体后端能力层，通过 bridge/facade 暴露给 Core）

## B. Capability Layer 定义（可插拔能力板块）

Capability Layer 是 Luna 的外接器官：**可独立升级、独立替换、支持 provider 切换与多模型接入**。

Stage-0 明确的 capability：
- **Voice（语音）**
- **Vision（视角/视觉）**
- **Emotion（情感，占位）**

### B1. Voice Capability

- **职责**：把“音频输入/识别/合成/播放”能力封装为可替换的 provider，产出统一的 `VoiceEvent`。
- **输入/输出边界**：
  - 输入：音频数据（bytes / stream chunk）、文本（TTS）
  - 输出：`VoiceEvent`（ASR 结果）、音频 bytes（TTS 合成）、或“播放已触发”的副作用（由 provider 自身实现）
- **与 Core 的交互方式**：
  - Core 仅与 `VoiceDialogueBridge`/capability facade 交互
  - Voice 内部通过 `VoiceCapabilityRegistry` 管理 `ASRProvider` / `TTSProvider` / `VoiceInputProvider`
- **为什么不能直接侵入 Core**：
  - 语音厂商差异/运行态差异应被 adapter 吸收
  - Core 只做治理（例如 speech gate）与编排，不承担“如何说/如何识别”的实现负担

### B2. Vision Capability

- **职责**：封装 OCR/检测/跟踪等视觉能力，产出统一的 `VisionEvent`，并允许多个 provider 并存。
- **输入/输出边界**：
  - 输入：frame bytes / frame ref
  - 输出：`VisionEvent` 列表（OCR/检测/跟踪等通过 `event_type` 区分）
- **与 Core 的交互方式**：
  - Vision 内部通过 `VisionCapabilityRegistry` 管理 `DetectionProvider` / `OCRProvider` / `TrackingProvider`
  - Core 只消费“标准事件/标准摘要”，不直接绑定任何 provider API
- **为什么不能直接侵入 Core**：
  - 视觉模型更新频繁，差异巨大，必须压在 adapter/provider 层
  - Core 的稳定性优先于 capability 演进速度

### B3. Emotion Capability（Reserved）

- **职责**：Stage-0 仅定义 schema/registry/interface，占位未来情感推断能力。
- **边界**：不得在 Stage-0 实现真实情感系统，更不得在 Core 内部硬编码。

## C. Individual Luna Backend Capability 定义（个体后端能力层）

这是一组“为整个 Luna 服务”的后端能力，不属于任一单独 capability（Voice/Vision/Emotion）的附属模块。

必须归入该层的能力（至少）：
- **whitebox**
- **memory**
- **logs**
- **traces**
- **audit**

### C1. 本轮（Stage-0）只做逻辑归属定义

- 当前只做 **逻辑归属剥离**（ownership），不做真实拆服务
- 若仓库中存在耦合：只能通过 `bridge / facade / README` **标记边界**，不得粗暴重构或大规模迁移

## D. 多模型接入原则（硬约束）

### D1. provider 统一接入

- 模型/厂商能力必须以 `*Provider` 形式接入 capability 层
- Core 禁止直接 import/绑定任何单一模型实现

### D2. registry 管理能力提供方

- capability 内部必须以 `*CapabilityRegistry` 管理 provider 的注册、默认选择与枚举
- Core 只与 capability 的 facade/bridge 交互（或与 registry 的最小只读视图交互）

### D3. schema 统一输入输出对象

- 语音统一到 `VoiceEvent`
- 视觉统一到 `VisionEvent`
- 情感统一到 `EmotionEvent`（reserved）

### D4. adapter 层吸收差异

- 不同模型/厂商差异（字段、置信度、分段、流式/非流式）必须在 adapter 层吸收
- 上层只看标准 schema，不看 provider 私有结构

### D5. Core 不直接绑定单一模型实现

Core Framework 的目标是“稳定、可治理、可观测、可替换”：
- 可替换：能力随时换 provider
- 可治理：规则与门控不被 capability 反向绑架
- 可观测：whitebox/logs/traces/audit 作为跨能力的后端能力存在

