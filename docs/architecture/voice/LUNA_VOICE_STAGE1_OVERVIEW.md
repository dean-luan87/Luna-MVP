# Luna Voice Stage-1 总纲（正式基线）

> 本文档是 **Luna 一期语音板块（Voice Capability）** 的正式架构基线：先立边界、再谈接入；约束先于实现；文档先于接线。  
> Stage-1 **不接 ASR/TTS/Realtime provider**，不接外部大模型，不实现多轮对话，只固化概念边界、治理规则与工程骨架。

## 1. 文档定位

- 本文档定义：Voice capability 在 Luna 体系中的**位置、职责、交互域、协议对象、治理约束**。
- 本文档是后续语音实现、外部语音大模型接入、情感输出接入、白盒观察扩展的**唯一基线**。

## 2. 语音板块定位

- Voice 是 **可插拔能力板块（Capability Layer）**。
- Voice **不是** Luna 主权系统。
- Voice **不拥有**：
  - 任务裁决权（task arbitration）
  - 记忆写入权（memory write authority）
  - 白盒控制权（whitebox authority）
  - 规则治理权（policy/governance authority）

主权与裁决骨架属于 **Core Framework**。

## 3. 一期实现目标（Stage-1：定义/骨架）

- **稳定输入对象**：所有语音输入先落 `VoiceInputEvent`（禁止裸文本直入主链）。
- **受控轻意图**：用 `VoiceIntentCandidate` 表达“轻意图候选”，不做宽推理。
- **安全接入主链**：Voice 只产出 proposal/query/response，交由 Core 决策。
- **可替换 provider 机制**：provider/adapter/registry/schema 的硬边界先固化。

## 4. 一期不做的内容（明确禁止）

- 开放闲聊主链 / 深情绪陪伴 / 人格推理
- 复杂知识问答主链
- 语音直写记忆、语音直改白盒
- 设备运维治理本体
- 真实 ASR/TTS/Realtime 接线
- 外部大模型接入

## 5. 正式交互域（Interaction Domains）

> Voice 的交互域是“受限输入 + 受控输出”的正式交互边界，不是无限对话域。

### 5.1 设备控制域（Device Control Domain）
- **职责**：设备级动作候选（如音量/静音/开始停止等）的表达与确认。
- **边界**：高风险或不确定动作必须走确认/拒绝；不得越权直执行。

### 5.2 任务控制域（Task Control Domain）
- **职责**：任务生命周期候选（开始/暂停/继续/结束/切换）。
- **边界**：任务状态由 Core/TaskChain 主权判定，Voice 仅提案。

### 5.3 任务上下文增强域（Task Context Enhancement Domain）
- **职责**：补充任务上下文（地点/对象/约束/偏好）作为 query/proposal。
- **边界**：不得把增强当作“事实落地”，必须可追溯来源与置信度。

### 5.4 反馈系统域（Feedback Response Domain）
- **职责**：对系统发出的确认/提示进行反馈（是/否/重复/更正/澄清）。
- **边界**：反馈是证据，不等于命令；与任务/环境冲突时需触发确认机制。

### 5.5 开放交互域（Reserved Open Dialogue Domain）
- **状态**：Reserved（不进入一期主线）。
- **边界**：不得以开放域绕开治理规则进入主链执行。

## 6. 主动沟通机制（Proactive Communication）

- 主动沟通不是普通交互域，是 **受控输出机制**。
- 来源可包括：风险系统、任务链节点、设备状态、中台治理层、未来情感引擎。
- **不得直连 TTS**：只能提交 `SpeechRequest` 到 Voice Output Plane（输出面治理）。

## 7. 语音输入入口策略（3 入口）

> Stage-1 固化概念与状态对象，不实现真实唤醒/ASR。

- **唤醒入口**：首次唤醒建立会话窗口。
- **连续会话入口**：30 秒窗口内允许连续 turn；有效交互可刷新窗口。
- **任务短指令入口**：在任务态允许短指令进入（仍需治理与确认）。

窗口规则（定义性约束）：
- 首次唤醒 → 建立 30s 窗口
- 有效交互 → 刷新窗口
- 长待机/关机 → 会话与任务上下文默认失效

## 8. 输入事件对象（必须）

- `VoiceInputEvent`：标准输入事件对象（不是裸文本）。
- `VoiceIntentCandidate`：轻意图候选对象（只做轻意图，不做宽推理）。

## 9. 一期意图候选类别（必须列出）

- `DeviceControlIntent`
- `TaskControlIntent`
- `TaskContextEnhancementIntent`
- `ConfirmationIntent`
- `FeedbackResponseIntent`
- `ReservedOpenDialogueIntent`

## 10. Dialogue Bridge 定义（受限路由层）

- Bridge 不是大脑；是 **受限路由层**。
- 位置：Voice capability 内部（`capabilities/voice/bridge/`）。
- 职责：把 `VoiceIntentCandidate` 路由为 Voice→Core 的协议对象（proposal/query/response）。
- 不负责：
  - 不负责主链裁决
  - 不负责直接执行
  - 不负责写入白盒/记忆

## 11. Dialogue Bridge 七路由（必须）

1. Device Control Route
2. Task Lifecycle Route
3. Task Context Enhancement Route
4. Confirmation Route
5. Feedback Response Route
6. Restricted Device Mode Route
7. Reserved Open Dialogue Route

优先级原则（硬约束）：
- Restricted Device Mode 最高优先
- Confirmation/Feedback 高于新指令
- 高风险不确定指令必须降级为确认或拒绝

## 12. 执行权限原则（3 类结果）

Voice/Bridge 只能产出三类执行权限结果：
- **直接执行**（仅限低风险高确定性）
- **确认后执行**
- **拒绝执行 / 降级处理**

依据：
- 时效性（time critical）
- 风险（risk）
- 确定性（certainty / ambiguity）

## 13. 冲突确认机制

必须覆盖冲突类型：
- 指令—行为—环境—任务冲突
- 行为不是命令，行为是证据（需要进入确认/澄清）

## 14. 任务上下文失效规则

- 关机 / 长待机 / 上下文断裂：默认进入新任务（由 Core/TaskChain 判定）
- Voice 不得“凭口头延续”跨越失效边界

## 15. Voice Output Plane（统一发声出口）

硬约束：
- **统一发声出口**：各模块只能提交 `SpeechRequest`，不得直连 TTS。
- 主动沟通也只能提交 `SpeechRequest`，不得直控 TTS。

与现有仓库的关系（只做归位说明，不改旧逻辑）：
- `core/speech_gate.py`：发言权治理（gate）
- `core/audio_worker.py`：播放工作线程（playback worker）
- Stage-1 只定义它们未来将被 Output Plane 使用的方式，不改语义。

输出类别（最小枚举）：
- safety / task_progress / interaction_result / device_status / proactive_communication / reserved_dialogue

输出优先级（原则）：
1) safety
2) restricted device mode prompts
3) task_progress / interaction_result
4) device_status
5) proactive_communication
6) reserved_dialogue

## 16. Voice 与 Core / TaskChain 的协议关系

- Voice → Core：`proposal / query / response`
- Core → Voice：`feedback / proactive / status / prompt`
- Core → Voice：`VoiceRuntimeContext` 注入（当前会话/任务/模式/待确认等）
- Whitebox：必须能观察 Voice 输入→Bridge→Core→输出治理→播放 的全链路对象

## 17. 白盒观察要求（Stage-1：对象占位）

必须能表达并被后续接线：
- 输入观察（VoiceInputObservation）
- Bridge 观察（DialogueBridgeObservation）
- Core 处理观察（以 core decision/whitebox 为准）
- 模型转述观察（ModelMediationObservation）
- 输出治理观察（OutputDecisionObservation）
- 播放观察（PlaybackObservation）

## 18. 大模型转述监管要求（Stage-1：规则先行）

必须可追踪三份内容：
- Luna 原始内容（原始输入/上下文）
- 模型候选内容（candidate）
- 最终放行内容（final）

并可记录：
- accept / reject / rewrite 的原因与规则命中

