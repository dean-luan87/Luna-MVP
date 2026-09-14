# GO / NO_GO — User Clarification Prompt Runtime DryRun for Reading v1

## GO

- 澄清 prompt 走完整语音治理链 dry-run；`ADMIT_AS_CANDIDATE` + `READY_FOR_FUTURE_VOP_SUBMIT`；`WAIT_FOR_USER_RESPONSE`  
- 不 TTS/VOP/submit；不填充 task/scene；verifier=GO  

## NO_GO

- TTS/VOP/submit、自动填 task/scene、WM/SceneDelta、benchmark/provider 宣称  

## 一句话

验证澄清提示如何进入 Speech Gate/VOP 候选链并等待用户回答；不真实播报。
