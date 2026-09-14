# GO / NO_GO — User Clarification Response Parsing DryRun for Reading v1

## GO

- 8 条 simulated response；parsing matrix；task/scene candidates；TSC handoff；`READY_FOR_TSC_REEVALUATION_LATER`  
- 无 ASR/LLM/fact/ISRC/RRD；verifier=GO  

## NO_GO

- ASR/LLM、模拟回答当事实、自动写 task/scene、invoke ISRC/RRD/WM  

## 一句话

模拟澄清回答解析为 context candidate，供 TSC 复评；不写 fact。
