# GO / NO_GO — Voice Output Plane Adapter for Guidance v1

## GO

- mapping + adapter/SpeechRequest payload candidates + admission + VOP submit dry-run
- `final_decision=READY_FOR_FUTURE_VOP_SUBMIT`
- 不 VOP / 不提交 / 不 TTS / 不写 STM；verifier=GO

## NO_GO

- 真实 VOP、SpeechRequest 提交、TTS、STM 写入、事实层写入

## 一句话

Adapter dry-run 把 SpeechRequest candidate 映射为未来 VOP payload；不调用、不提交、不播报。
