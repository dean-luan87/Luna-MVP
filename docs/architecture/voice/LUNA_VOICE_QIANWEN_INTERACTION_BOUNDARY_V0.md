# LUNA Voice — Qianwen Interaction Boundary v0

## 必须区分的两件事

1. **QwenTTSProvider**  
   - 角色：**语音合成**通道之一，受 **Qianwen-first / TTS-fallback** 策略约束。  
   - **不等于**「完整 Qianwen 对话模型已接入主线」。

2. **Qianwen / DashScope 对话或长输入模型 provider**（如 `qwen_external_long_input_model_provider`）  
   - 角色：**模型中介 / 长输入**路径上的组件。  
   - 与 **TTS provider** 边界须在实现与审计字段上分开（`source_text` / `spoken_text` diff 等）。

## 工程状态（readiness 语义）

- **策略与合同**：`LUNA_VOICE_QWEN_FIRST_TTS_FALLBACK_POLICY_V0.md` 等已锚定。  
- **主线 wiring**：readiness 工具默认 **`qianwen_runtime_wiring_done=false`**，须由后续 **授权 phase** 证明。

## 禁止

- 把 **QwenTTSProvider** 误标为 **完整对话能力**。  
- 在未授权前 **删除** Piper / 其他 **fallback**。
