# LUNA Voice — Full Interaction Chain Definition v0

## 完整语音交互主链（目标态）

```
用户语音输入
  → ASR
  → voice input session（wake / session_id / timeout / interrupt）
  → semantic normalization / intent context
  → Qianwen interaction 或 model mediation（与「仅 TTS」区分）
  → output candidate
  → voice output governance（gate / shadow / hard audit）
  → governed provider entry
  → Qwen TTS 或 fallback TTS（Piper 等）
  → playback / audio worker
  → RequestTrace / replay / audit
```

## 与两类已存在能力的区别

| 能力 | 说明 |
|------|------|
| **Voice Output Governance 007–009** | 输出侧治理、shadow submit、TRW、统一查询导出；**≠** 已接全链语音交互。 |
| **Qwen TTS + long-input 模型 provider** | 合成与长文本模型路径；**≠** 完整对话产品态。 |

本阶段 **readiness_pending**：主链 **未**声明为 `full_voice_interaction_connected`。
