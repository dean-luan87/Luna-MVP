# LUNA TTS Provider Offline/Online Inventory v0

## Phase

- Phase-VoiceTTS-Provider-Cleanup-001（Offline-Only TTS Provider Policy & Online Provider Disable v0）

## Purpose

盘点当前仓库中已存在/可能被接入的 TTS provider，并给出：

- offline_local / requires_network / requires_api_key
- currently_in_provider_chain / currently_used_by_main
- keep / disable / remove_candidate（不做物理删除）

## Inventory

### 1) legacy macOS say（Voice）

- **module**: `modules/voice.py`
- **offline_local**: true（本机系统命令 `say`）
- **requires_network**: false
- **requires_api_key**: false
- **currently_in_provider_chain**: false（不在 Stage-2 provider_order）
- **currently_used_by_main**: true（作为 legacy_submit 的实际播放底座）
- **decision**: keep（保留离线 fallback）

### 2) AudioWorker submit_tts（异步播放底座）

- **module**: `core/audio_worker.py::submit_tts`
- **offline_local**: true（本地队列+线程）
- **requires_network**: false
- **requires_api_key**: false
- **currently_in_provider_chain**: N/A（执行底座，不是 provider）
- **currently_used_by_main**: true
- **decision**: keep（必须保留，不得阻塞主循环）

### 3) Piper provider（Stage-2）

- **module**: `capabilities/voice/providers/piper_tts_provider.py`
- **offline_local**: true（本地二进制 `piper` + onnx voice）
- **requires_network**: false
- **requires_api_key**: false
- **currently_in_provider_chain**: true
- **currently_used_by_main**: yes（通过 `tts_unified_entry`，当前 config active_provider=piper）
- **decision**: keep（离线主链 provider）

### 4) Fish provider（Stage-2）

- **module**: `（已移除）`
- **offline_local**: unknown/depends（本实现支持本地 subprocess，但运行时依赖外部可执行入口与模型）
- **requires_network**: unknown（本阶段按“可能在线/不可控”处理）
- **requires_api_key**: false（本地模式）
- **currently_in_provider_chain**: 已移除
- **currently_used_by_main**: no（默认链路不会选中）
- **decision**: disable（先禁用/移出默认链，不物理删除）

### 5) Qwen/Qianwen TTS（DashScope）

- **module**: `modules/qwen_tts.py`（DashScope HTTP TTS）
- **offline_local**: false
- **requires_network**: true
- **requires_api_key**: true（`DASHSCOPE_API_KEY`）
- **currently_in_provider_chain**: registered=true（Stage-2 provider：`capabilities/voice/providers/qwen_tts_provider.py`）
- **currently_used_by_main**: no（默认 config 未启用，provider_order 不包含 qwen）
- **decision**: disable（online provider 不得进入 offline-only 主链；不物理删除）

### 6) pyttsx3（legacy TTSProcessor）

- **module**: `utils/model_interfaces.py::TTSProcessor`（pyttsx3）
- **offline_local**: true（本地库）
- **requires_network**: false
- **requires_api_key**: false
- **currently_in_provider_chain**: false
- **currently_used_by_main**: no（主链不初始化它）
- **decision**: keep_as_legacy_not_initialized（不初始化、不急删）

## Current config snapshot (as-is)

- `capabilities/voice/config/voice_tts_config.yaml`
  - `provider_order`: `["piper"]`
  - `active_provider`: `piper`
  - `local_runtime.piper.enabled`: false
  - `local_runtime.qwen.enabled`: false

