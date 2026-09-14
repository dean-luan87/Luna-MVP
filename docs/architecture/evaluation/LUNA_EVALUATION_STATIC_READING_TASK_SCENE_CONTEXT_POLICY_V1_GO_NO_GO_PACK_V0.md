# GO / NO_GO — Static Reading Task Scene Context Policy v1

## GO

- task/scene schema、归一化、task-scene matrix、missing handling、clarification、confidence、ISRC handoff、RRD preconditions 齐全  
- 当前 case 缺 task/scene 为预期；clarification 仅候选；不伪造 ranked source  
- 无 scene detector/OCR/camera；verifier=GO  

## CONDITIONAL_GO

- 仅 policy 定义；`runtime_preconditions_met_now=false`；无 runtime action  

## NO_GO

- 伪造 task/scene、scene detector、OCR、camera、ranked source area、事实层/WM/SceneDelta、benchmark/provider 宣称  

## 一句话

补齐静态阅读进入信息源定位与 RRD runtime 前的 task/scene 上下文策略；本阶段只定义 policy，不执行识别。
