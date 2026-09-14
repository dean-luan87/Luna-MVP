# Luna — Minimal Runtime Integration Controlled Output Definition v1

**Phase**：`Minimal-Runtime-Integration-Controlled-Output-Definition-v1-001`  
**性质**：definition only；定义最小可控输出合同与边界；不启用 controlled output

## 目标

定义 Luna 在 minimal runtime integration 后续阶段的最小可控输出合同：

- Speech Gate controlled-output contract
- VOP controlled-output contract
- TTS placeholder / dry output policy
- user-visible output boundary
- output abort / recovery
- output observability
- GO / NO-GO criteria

## 核心结论

- 当前允许定义的未来输出只包括 `text_console_output_controlled`、`structured_log_output_controlled`、`speech_request_candidate_to_shadow`、`speech_gate_controlled_decision_candidate`、`vop_controlled_event_candidate`、`tts_placeholder_or_dry_output_candidate`
- 当前仍然禁止真实音频播放、真实 TTS、真实 Speech Gate runtime、真实 VOP runtime
- P0/P1 safety protection、stale safety speech historical-only、non-owner output block、source_chain requirement、abort/recovery 路径都已被合同化
- 下一阶段最多只能进入 `Text-Only-Controlled-Output-Trial`，不能直接进入 live audio

## 主线位置

```text
Minimal-Runtime-Integration-Trial-Definition-v1
  → Minimal-Runtime-Integration-Controlled-Shadow-Trial-v1
  → Minimal-Runtime-Integration-Post-Shadow-Review-v1
  → Minimal-Runtime-Integration-Controlled-Output-Definition-v1
  → Minimal-Runtime-Integration-Text-Only-Controlled-Output-Trial-v1
  → Minimal-Runtime-Integration-Text-Only-Output-Post-Trial-Review-v1
  → Minimal-Runtime-Integration-Closure-v1
```

## 边界

- `definition_only=true`
- `controlled_output_enabled=false`
- `controlled_output_executed=false`
- 不接真实 TTS / VOP / Speech Gate runtime
- 不播放声音
- 不接真实 camera / microphone / ASR / OCR provider / map API / GPS
- 不提交 Task Manager，不触发 navigation action，不修改 route
- 不写 Memory / WorldModel / Fact / Scene Delta

## 下一推荐 Phase

**Minimal-Runtime-Integration-Text-Only-Controlled-Output-Trial-v1** — 已完成  
**Minimal-Runtime-Integration-Text-Only-Output-Post-Trial-Review-v1** — 已完成  
**Minimal-Runtime-Integration-Closure-v1**

注意：text-only trial 与 post-trial review 都已完成。  
下一阶段进入 closure，但仍然不能启用真实语音输出、真实 TTS、真实音频播放或 live runtime。

## 实现

- `capabilities/midplatform/minimal_runtime_integration_controlled_output_definition_v1.py`
- `tools/evaluation/midplatform/run_minimal_runtime_integration_controlled_output_definition_v1.py`
- `tools/evaluation/midplatform/verify_minimal_runtime_integration_controlled_output_definition_v1.py`
