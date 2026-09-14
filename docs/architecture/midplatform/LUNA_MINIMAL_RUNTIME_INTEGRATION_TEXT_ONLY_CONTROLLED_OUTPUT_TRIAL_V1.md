# Luna — Minimal Runtime Integration Text-Only Controlled Output Trial v1

**Phase**：`Minimal-Runtime-Integration-Text-Only-Controlled-Output-Trial-v1-001`  
**性质**：controlled output trial only；但严格限制为 text-only family output

## 目标

在 `Controlled-Output-Definition-v1` 约束下执行最小 text-only controlled output trial：

- 生成 `TEXT_ONLY` 文本输出
- 生成 `STRUCTURED_LOG_ONLY` 结构化输出
- 生成 `DRY_SPEECH_PREVIEW`
- 生成 `SHADOW_COMPATIBLE_TEXT_OUTPUT`
- 保持 Speech Gate / VOP 仅 candidate 层
- 保持 no-runtime / no-write 边界锁定

## 覆盖

- 8 个 controlled output cases
- 8 个 `SpeechGateControlledDecision`
- 8 个 `ControlledTextOutputEvent`
- 8 个 `VOPControlledEventCandidate`
- 8 个 `TextOnlyOutputAbortCheck`
- observability trace + no-runtime / no-write 双 boundary report

## 核心结论

- 受控输出 trial 已经可以穿通最小文本级输出链路
- 输出模式被限制在 `TEXT_ONLY`、`STRUCTURED_LOG_ONLY`、`DRY_SPEECH_PREVIEW`、`SHADOW_COMPATIBLE_TEXT_OUTPUT`
- `P0/P1 safety`、`stale historical-only`、`non-owner suppress`、`pending confirmation` 均在对象层被保持
- 没有真实 TTS、真实音频、真实 Speech Gate runtime、真实 VOP runtime、真实外部副作用

## 主线位置

```text
Minimal-Runtime-Integration-Controlled-Shadow-Trial-v1
  → Minimal-Runtime-Integration-Post-Shadow-Review-v1
  → Minimal-Runtime-Integration-Controlled-Output-Definition-v1
  → Minimal-Runtime-Integration-Text-Only-Controlled-Output-Trial-v1
  → Minimal-Runtime-Integration-Text-Only-Output-Post-Trial-Review-v1
  → Minimal-Runtime-Integration-Closure
```

## 边界

- `real_audio_output_invoked=false`
- `runtime_tts_invoked=false`
- `runtime_audio_output_invoked=false`
- `speech_gate_runtime_invoked=false`
- `vop_runtime_invoked=false`
- 不调用音频设备，不调用 TTS engine，不调用外部 TTS API
- 不接真实 camera / microphone / ASR / map API / OCR provider / GPS
- 不提交 Task Manager，不触发 navigation action，不修改 route
- 不写 Memory / WorldModel / Fact / Scene Delta
- 不得将文本输出视为“用户已听见”

## 下一推荐 Phase

**Minimal-Runtime-Integration-Text-Only-Output-Post-Trial-Review-v1** — 已完成  
**Minimal-Runtime-Integration-Closure-v1** — 已完成  
**Phase-Return-To-Vision-Mainline-Planning-v1-001**

注意：post-trial review 与 closure 都已完成。  
本块不再扩展输出链，下一主线切回视角强化，依然不能进入真实 TTS、真实音频播放、真实 camera/map/ASR/OCR provider。

## 实现

- `capabilities/midplatform/minimal_runtime_integration_text_only_controlled_output_trial_v1.py`
- `tools/evaluation/midplatform/run_minimal_runtime_integration_text_only_controlled_output_trial_v1.py`
- `tools/evaluation/midplatform/verify_minimal_runtime_integration_text_only_controlled_output_trial_v1.py`
