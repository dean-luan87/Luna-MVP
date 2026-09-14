# capabilities/voice（Stage-1）

Voice 是 **可插拔能力板块**，不拥有主权；Core 才是裁决骨架。

## 本目录负责
- 固化 Voice 的 **概念边界**、协议对象（schema）、接口（Protocol）与观察对象（observations）
- 提供 Dialogue Bridge 与 Output Plane 的 **工程骨架**（Stage-1 仅占位）

## 本目录不负责
- 不接入真实 ASR/TTS/Realtime provider
- 不实现多轮对话系统
- 不改写 Core 主链、TaskChain、whitebox 既有行为
- 不直连 `core/speech_gate.py` / `core/audio_worker.py` 做业务接线（仅在文档中说明未来归位关系）

## 与 Core 的关系
- Voice → Core：proposal / query / response（候选）
- Core → Voice：runtime context / prompt / feedback / proactive（受控）

## 与 Output Plane 的关系
- 任何模块不得直连 TTS；统一提交 `SpeechRequest` 到 Output Plane（Stage-1 仅定义对象与接口）

