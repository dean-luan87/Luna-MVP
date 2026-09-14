# LUNA Voice — ASR Boundary Contract Go/No-Go Pack v0（Phase-VoiceInteraction-Readiness-002）

## GO

- `LUNA_VOICE_ASR_BOUNDARY_CONTRACT_V0.md` 与 `ASRFinalTextEventV0` 合同落地。  
- Final text 事件 schema、状态机、trace/replay/audit 合同、fallback/suppress、runtime flag 计划文档齐备。  
- `run_voice_asr_boundary_contract_review_v0.py` 产出矩阵 + `verify_voice_asr_boundary_contract_review_v0.py` **GO**。  
- 工具 **constraints**：无 ASR provider、无 Qianwen、无 TTS、无 playback、无 runtime 变更。  
- **仅 `final_text_ready`** 为语义/Qianwen 下游入口（在 `voice_asr_state_machine_matrix.json` 中显式为 true）。

## CONDITIONAL_GO

- 具体 ASR vendor **未选定**；audio capture **仍为未来实现**；final_text dispatch **未接线**（预期）。

## NO_GO

- 调用真实 ASR / Whisper。  
- 调用 Qianwen、执行 TTS / playback。  
- 将 **low_confidence** 全文默认送入 Qianwen；或将 **no_speech / timeout / cancelled** 送入模型。  
- 修改 voice runtime 行为（本 phase 禁止）。
