# LUNA Voice — Full Interaction Readiness Review v0 (Phase-VoiceInteraction-Readiness-001)

## 目的

对 **完整语音交互主链**（ASR → session → 语义/意图 → 模型中介 → 输出治理 → TTS → 回放 → TRW）做 **readiness 盘点**，与 **Voice Output Governance**、**Qwen TTS provider** 明确区分。

## 边界（硬）

- **只读**扫描仓库与文档锚点；**不**调用 Qwen、**不**真实 TTS、**不**播报、**不**调 ASR provider。  
- **不**改 voice/OCR runtime、**不**接 MidPlatform / SceneDelta / WorldContext、**不**接 OCRBridge。  
- **不**删除 legacy voice / TTS fallback；**不**改变 **Qianwen-first / TTS-fallback** 口径。

## 工具

- `tools/voice/run_voice_interaction_readiness_review_v0.py`  
- `tools/voice/verify_voice_interaction_readiness_review_v0.py`

## 产物

见 `LunaRuntime/logs/voice_interaction_readiness_001_*` 下的 `voice_*_matrix.json` 与 `voice_interaction_gap_register.json`。
