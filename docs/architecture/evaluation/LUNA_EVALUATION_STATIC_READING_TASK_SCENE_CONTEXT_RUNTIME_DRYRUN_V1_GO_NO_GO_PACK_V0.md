# GO / NO_GO — Static Reading Task Scene Context Runtime DryRun v1

## GO

- current case intake；task/scene 缺失评估；clarification 候选；confidence=insufficient；query 不生成；RRD preconditions unmet  
- `final_decision=WAIT_FOR_USER_CLARIFICATION`；不伪造 task/scene/ranked source；verifier=GO  

## NO_GO

- 伪造 task/scene、ranked source、invoke ISRC/RRD、scene detector、OCR、camera、事实层/WM/SceneDelta  

## 一句话

在缺 task/scene 的 case 下 dry-run 澄清路径并阻断下游 runtime；不识别真实场景、不 TTS。
