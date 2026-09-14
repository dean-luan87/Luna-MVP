# GO / NO_GO — Voice Guidance Prompt Runtime DryRun v1

## GO

- 全链 dry-run 产物齐全；`final_decision=GENERATE_SPEECH_REQUEST_CANDIDATE_ONLY`
- 不 TTS / 不 VOP / 不提交 SpeechRequest / 不写 STM
- verifier=GO

## NO_GO

- 真实 TTS、VOP、SpeechRequest 提交、STM 写入
- OCR guidance 优先于 safety
- 事实层 / WorldModel / SceneDelta / routing 变更

## 一句话

Dry-run 验证 prompt 进入语音治理链；SpeechRequest 仅为 candidate，不代表已提交。
