# LUNA Voice — Output Governance → Full Interaction Mapping v0

## 映射关系

| Output Governance 能力 | 在全链中的位置 | 说明 |
|------------------------|----------------|------|
| Shadow submit gate | 输出前 **governance** | 不等于 ASR 或对话状态机已完成 |
| RequestTrace / TRW stage | 全链 **可观测性** | 为接线后审计服务；本身不接全链 |
| Unified query/export | **离线/运营视图** | 与 playback 无直接等价 |
| Governed provider entry skeleton | **TTS/Qwen 入口** | 仍须与 `run_tts_unified_entry` 等 **硬门闩** 对齐（见 gap register） |

## 结论

**Output Governance 就绪** 只说明 **输出侧治理与 TRW 基线** 达标一部分；**不能**据此宣称 **Full Voice Interaction = connected**。
