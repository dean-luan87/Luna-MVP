# Luna Voice Stage-2：Fish + Piper 本地 TTS Provider 链变更清单

> 本轮目标：在 Stage-1 宪法约束下，接入 **Fish（主）+ Piper（兜底）** 的本地离线 TTS Provider 链，建立独立配置与 preset 体系，并实现 selector/fallback/observation/最小测试。  
> 本轮禁止：云端模型、ASR、多轮对话、改写主链、改 speech_gate/audio_worker 语义、把 provider 参数泄露到 Core。

## 1) 新增目录与 README

- `capabilities/voice/providers/README.md`
- `capabilities/voice/config/README.md`

## 2) 新增配置文件

### 2.1 主配置
- `capabilities/voice/config/voice_tts_config.yaml`
  - **关键字段**：
    - `active_provider: piper`
    - `fallback_provider: piper`
    - `provider_order: [piper]`
    - `fallback.enabled` 与 `fallback_on_timeout/exception/invalid_audio`
    - `timeouts.piper_ms` / `timeouts.piper_ms`
    - `presets.default` 与 `presets.available`
    - `backend_override`（reserved）

### 2.2 Fish presets
- `capabilities/voice/config/voice_presets.yaml`
  - 预置 4 套 preset：
    - `calm_female_v1`
    - `navigation_clear_v1`
    - `warning_strong_v1`
    - `gentle_companion_v1`
  - 原则：前端选 preset；系统选 provider；raw 参数不外溢

## 3) Provider adapters（本地离线）

- `（已移除）`
  - 结构化失败：binary 不存在/超时/异常/空音频
  - Fish 特有参数仅留在 provider 内部（Stage-2 不绑定具体 CLI/SDK）

- `capabilities/voice/providers/piper_tts_provider.py`
  - 结构化失败：binary 不存在/超时/异常/空音频
  - 定位为稳定 fallback

## 4) provider 选择与 fallback（系统主权 + 可观察）

- `capabilities/voice/providers/tts_fallback_manager.py`
  - 链路：Fish 失败 → Piper
  - fallback 结果结构化、可观测（不允许静默）

（辅助类型）
- `capabilities/voice/providers/provider_types.py`

## 5) Output 执行包装（不接播放）

- `capabilities/voice/output/tts_provider_runtime.py`
  - `TTSProviderResult` / `TTSFailure`
- `capabilities/voice/output/tts_request_executor.py`
  - 加载 `voice_tts_config.yaml` + `voice_presets.yaml`
  - 调用 provider chain 返回结构化结果
  - **不调用** `core/speech_gate.py` / `core/audio_worker.py`（Stage-2 不接线）

## 6) 白盒观察对象（provider 选择/回退）

- `capabilities/voice/observations/provider_selection_observation.py`
- `capabilities/voice/observations/provider_fallback_observation.py`

## 7) 最小测试/脚本

- `tools/smoke_voice_tts_provider_chain.py`
  - 即便本机无 piper 二进制，也应返回结构化失败，不抛异常
- `tests/test_voice_tts_fallback_manager.py`
  - 验证：Fish 失败时 Piper 兜底；禁用 fallback 时不兜底

## 8) 旧文件未动说明（主链保护）

本轮不改写/不迁移：
- `main.py`
- `core/audio_worker.py`
- `core/speech_gate.py`
- 既有 `_handle_speech_decision` / `_execute_speech_decision` / `_speak_safely` 链路

## 9) 留到下一阶段

- 将 Output Plane 与 `speech_gate/audio_worker` 做真实接线（并保持语义不变）
- 真实 Fish CLI/SDK 参数契约与预置的严谨落地（Stage-2 避免绑定具体实现细节）
- 播放观测（PlaybackObservation）与 trace 落地的工程接入

