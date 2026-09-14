# playback / speaking 真源实现（V1）说明

## 改了什么

在 request 真源已成立的基础上，补齐 playback/speaking 层的真状态事件（V1），使系统能在同一 `request_id` 下观测到：

- `playback_started`
- `playback_finished`
- `playback_failed`
- `playback_cancelled`

并保证：

- dry-run 下**不伪造** playback_started（不把“已提交”冒充“已播报”）
- 不扩 submit 候选范围
- 不让跨域旁路进入真实输出
- 不进入 Level 2、不做中断/恢复

## 真源定义（V1）

- request 真源：`VoiceOutputPlane.submit()`（上一阶段已实现）
- playback/speaking 真源：必须来自 playback/result 执行层观测点

本 repo 当前尚未接入真实 `audio_worker/speech_gate`，因此 V1 以一个最小 **playback 执行器** 作为“执行层锚点”，产出 playback_* 事件（仅用于建立真状态链路与抽链闭环，真实设备/队列接线在后续版本完成）。

## 代码落点

- playback 真状态事件模型：`capabilities/voice/observations/playback_runtime_observation.py`
- 执行层锚点（最小 playback 执行器）：`capabilities/voice/output/playback_executor_v1.py`
- 输出平面调用（仅在 EXECUTE_TTS=1 路径）：`capabilities/voice/output/voice_output_plane_v1.py`
  - dry-run（EXECUTE_TTS=0）下不写入 playback_runtime 事件
- 抽链支持：`capabilities/voice/observations/request_trace_extractor.py`
  - 支持 JSONL envelope `type="playback_runtime"`
  - 新增 `playback_result` stage（source_observation_type=PlaybackRuntimeObservation）

## 开关与验证

- `LUNA_REAL_OUTPUT_SUBMIT_V1_EXECUTE_TTS=0`：dry-run，不产生 playback 真状态
- `LUNA_PLAYBACK_RUNTIME_V1_FORCE_CANCEL=1`：强制产出 `playback_cancelled`（用于回归验证）

验证脚本：

```bash
python3 tools/test_playback_runtime_source_v1.py
```

## 哪些还没做

- 不接真实 audio_worker/speech_gate（真实 speaking 真源仍需后续接线）
- 不做中断/恢复
- 不做旁路真实抢占（Level 2）
- 不做复杂播放队列、跨 request 合并

