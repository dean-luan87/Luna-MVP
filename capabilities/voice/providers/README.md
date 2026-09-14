# capabilities/voice/providers（Stage-2）

本目录提供本地离线 TTS Provider 的 **adapter** 与 **选择/回退**机制。

## 约束
- Stage-2 runtime 默认只允许 **离线 provider**（offline-only）。
- 默认禁止云端/网络型语音模型进入主链（requires_network=true 必须被 gate 阻断）
- 禁止把 provider 参数泄露到 Core
- 禁止绕过 selector/fallback（不允许静默 fallback）

## 云端 provider（归档/禁用）

`qwen`（DashScope）属于在线/API provider：

- 默认 `enabled=false`
- `offline_only=true` 时必须被 gate 过滤（不得进入默认 provider chain）
- 作为代码保留资产，不在本阶段物理删除

## 入口约束
- `tts_provider_selector.py`：**唯一公开入口**（public entry）
- `tts_fallback_manager.py`：**内部机制**（internal），外部业务不得直调

