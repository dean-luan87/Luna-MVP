# LUNA Qwen Voice Guarded Trial Hook-In v0

**Phase**：Phase-Mainline-RuntimeReadiness-004  \n
**Hook wrapper**：`capabilities/runtime_readiness/qwen_voice_guarded_trial_hook_v0.py`  \n
**候选挂接点**：`capabilities/voice/output/voice_output_plane_v1.py::VoiceOutputPlaneV1.submit`

---

## 目标

在 voice submit 入口处挂接 Qwen Voice governed entry trial gate 评估，但 **默认 no-op**，且不得触发 `run_tts_unified_entry`、真实 provider 或 playback。

---

## 默认行为（必须）

- gate decision 默认 `disabled`
- hook result `enabled=false`、`no_op=true`
- 仅作为 debug metadata 附着在 `RequestRuntimeObservation.metadata.guard​ed_trial_hook`，不改变返回值与控制流

---

## 禁止项

- 不真实调用 Qwen
- 不真实执行 TTS
- 不真实播放
- 不改默认 provider 策略、不删 Piper fallback

