# Luna Voice Stage-1：变更清单（定义/固化/占位）

> 本轮目标：**语音板块架构定义 + 宪法落盘 + 工程骨架与接口对象占位**。  
> 本轮禁止：接 ASR/TTS/Realtime、接外部大模型、实现多轮对话、改写主链、改写 speech_gate/audio_worker 语义。

## 1) 新增了哪些正式文档（产物）

- `docs/architecture/voice/LUNA_VOICE_STAGE1_OVERVIEW.md`
- `docs/architecture/voice/LUNA_VOICE_CONSTITUTION_V1.md`
- `docs/architecture/voice/LUNA_VOICE_MODEL_BOUNDARY_PRECHECK.md`
- `docs/architecture/voice/LUNA_VOICE_STAGE1_CHANGESET.md`

## 2) 新增了哪些目录（工程骨架）

- `docs/architecture/voice/`
- `capabilities/voice/`
  - `docs/`
  - `schemas/`
  - `interfaces/`
  - `runtime/`
  - `bridge/`
  - `output/`
  - `observations/`

## 3) 新增了哪些对象（schema / protocol / observation）

### 3.1 输入侧对象（schemas）
- `VoiceInputEvent`：`capabilities/voice/schemas/voice_input_event.py`
- `VoiceIntentCandidate`：`capabilities/voice/schemas/voice_intent_candidate.py`

### 3.2 Voice → Core 协议对象（schemas，占位）
- `DeviceActionProposal`：`capabilities/voice/schemas/device_action_proposal.py`
- `TaskActionProposal`：`capabilities/voice/schemas/task_action_proposal.py`
- `TaskContextQuery`：`capabilities/voice/schemas/task_context_query.py`
- `ConfirmationResponse`：`capabilities/voice/schemas/confirmation_response.py`

### 3.3 Core → Voice 协议对象（schemas，占位）
- `VoiceRuntimeContext`：`capabilities/voice/schemas/voice_runtime_context.py`
- `TaskFeedbackEvent`：`capabilities/voice/schemas/task_feedback_event.py`
- `TaskQueryResultEvent`：`capabilities/voice/schemas/task_query_result_event.py`
- `ProactiveCommunicationEvent`：`capabilities/voice/schemas/proactive_communication_event.py`
- `DeviceStatusFeedbackEvent`：`capabilities/voice/schemas/device_status_feedback_event.py`
- `PendingConfirmationPrompt`：`capabilities/voice/schemas/pending_confirmation_prompt.py`

### 3.4 输出面对象（schemas / output，占位）
- `SpeechRequest`：`capabilities/voice/schemas/speech_request.py`
- `OutputCategory`：`capabilities/voice/output/output_categories.py`
- `OutputPriorityPolicy`：`capabilities/voice/output/output_priority_policy.py`

### 3.5 Bridge 占位对象（bridge，占位）
- `BridgeRouteType`：`capabilities/voice/bridge/route_types.py`
- `BridgeDecision`：`capabilities/voice/bridge/bridge_decision.py`

### 3.6 运行态占位对象（runtime，占位）
- `ConversationWindowState`：`capabilities/voice/runtime/conversation_window_state.py`
- `TaskShortcutState`：`capabilities/voice/runtime/task_shortcut_state.py`
- `RestrictedDeviceModeState`：`capabilities/voice/runtime/restricted_device_mode_state.py`

### 3.7 白盒观察对象（observations，占位）
- `VoiceInputObservation`：`capabilities/voice/observations/voice_input_observation.py`
- `DialogueBridgeObservation`：`capabilities/voice/observations/dialogue_bridge_observation.py`
- `ModelMediationObservation`：`capabilities/voice/observations/model_mediation_observation.py`
- `OutputDecisionObservation`：`capabilities/voice/observations/output_decision_observation.py`
- `PlaybackObservation`：`capabilities/voice/observations/playback_observation.py`

### 3.8 接口占位（interfaces，占位）
- `ASRProvider`：`capabilities/voice/interfaces/asr_provider.py`
- `TTSProvider`：`capabilities/voice/interfaces/tts_provider.py`
- `VoiceDialogueBridge`：`capabilities/voice/interfaces/voice_dialogue_bridge.py`
- `VoiceOutputPlane`：`capabilities/voice/interfaces/voice_output_plane.py`

## 4) 哪些旧代码明确未动（主链保护）

本轮**不修改**且不得修改的旧链路（本次变更未触碰）：
- `main.py`
- `core/audio_worker.py`
- `core/speech_gate.py`
- 现有 `_handle_speech_decision` / `_execute_speech_decision` / `_speak_safely` 所在链路
- `modules/voice_to_text.py`

## 5) 哪些内容留到下一阶段（为什么本轮不做实现）

留到后续阶段（Stage-2/Stage-3）：
- 真实 ASR/TTS/Realtime provider 接入（本轮禁止接线）
- 外部大模型接入与选型（本轮只做边界 Precheck）
- 多轮对话状态机与复杂对话域（本轮禁止实现）
- Output Plane 与 `core/speech_gate.py` / `core/audio_worker.py` 的真实接线（本轮禁止改语义）
- Whitebox/trace 的真实落地接线（本轮只固化 observation 对象）

原因：Stage-1 只做 **定义/固化/占位**，先立边界防污染；实现会改变运行行为与测试语义，不符合本轮性质。

## 6) 自查结论（越界检查）

- 无外部模型接入
- 无 ASR/TTS/Realtime 接线
- 无多轮对话实现
- 无主链逻辑修改
- 无 speech_gate/audio_worker 语义修改

