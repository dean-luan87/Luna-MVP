# GO / NO_GO Pack — Voice Guidance Prompt Template v1

**Phase**：`Voice-Guidance-Prompt-Template-v1-001`

## GO

- voice trigger governance integration 已定义（含既有 voice 文档路径或 placeholder）  
- speech priority：P0 > P3 OCR guidance  
- prompt template matrix + safety constraints + STM contract + repeat/cooldown  
- VOP adapter placeholder；不 TTS / 不 VOP / 不 SpeechRequest  
- no-write boundary 通过；verifier=GO  

## CONDITIONAL_GO

- 仅 placeholder 完整、capability 在 midplatform 路径  

## NO_GO

- 触发 TTS / 调用 VOP / 提交 SpeechRequest  
- OCR guidance 优先级高于 safety  
- 缺少 STM / repeat 规则  
- 写事实层 / WorldModel / SceneDelta  
- navigation / routing 变更  
- benchmark 或 provider 比较宣称  

## 一句话

本阶段只定义 OCR/阅读恢复语音提示模板与语音治理接口；优先级低于安全播报；不播报、不执行引导、不写事实层。
