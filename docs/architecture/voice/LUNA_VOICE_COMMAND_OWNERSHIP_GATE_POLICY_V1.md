# Luna — Voice Command Ownership Gate Policy v1

**Phase**：`Voice-Command-Ownership-Gate-Policy-v1-001`  
**Capability 层**：`capabilities/voice/`（评测 runner：`tools/evaluation/voice/`）

## 职责

判断语音输入是否有资格进入 Luna 后续链路（打断 / 任务控制 / 安全观察 / 澄清等），**不是**完整语义理解。

## 核心枚举

- `ownership_state`：OWNER_CONFIRMED / PROBABLE / UNCERTAIN / NON_OWNER_*
- `speaker_type`、`addressing_status`、`conversation_context`
- `allowed_entrypoints` / `blocked_entrypoints`

## 预留（candidate only）

- **VoiceprintEvidenceCandidate**：高隐私；不得写 speaker identity fact / WorldModel
- **VoiceEmotionEvidenceCandidate**：情感上下文候选；不得写 emotion fact

开源选型参考（文档级）：SpeechBrain、pyannote.audio、3D-Speaker、Resemblyzer。

## 主线顺序

```
Safety-Task-Arbitration-Policy-v1
  → Voice-Command-Ownership-Gate-Policy-v1
  → Voice-Interruption-Governance-DryRun-v1
  → Basic-Navigation-Guidance-Loop-Stabilization-Test-v1
  → Minimal-Runtime-Integration-Trial-Definition-v1
  → Minimal-Runtime-Integration-Controlled-Shadow-Trial-v1
```

## 下一推荐 Phase

**Voice-Interruption-Governance-DryRun-v1** — 已完成  
**Basic-Navigation-Guidance-Loop-Stabilization-Test-v1** — 已完成  
**Minimal-Runtime-Integration-Trial-Definition-v1** — 已完成  
**Minimal-Runtime-Integration-Controlled-Shadow-Trial-v1**

Ownership Gate 的 `allowed_entrypoints` / `safety_only_allowed` / `requires_confirmation` 直接作为 Interruption Governance 的前置输入。
在 Stabilization Test 中，这些字段继续作为 interruption 前置门控，成功拦截旁人 / 电话 / 聊天 / 外放 / 广播的普通打断。
在 Trial Definition 中，这些约束被明确纳入未来 controlled shadow trial 的 abort 条件与 observability trace。

## 边界

policy only；无 ASR / 声纹 / 录音 / TTS stop / Speech Gate / VOP / task commit / WM / Memory

## 实现

- `capabilities/voice/voice_command_ownership_gate_policy_v1.py`
- `tools/evaluation/voice/run_voice_command_ownership_gate_policy_v1.py`
- `tools/evaluation/voice/verify_voice_command_ownership_gate_policy_v1.py`
