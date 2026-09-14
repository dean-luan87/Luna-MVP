# Luna — User Clarification Prompt Runtime DryRun for Reading v1

**Phase**：`User-Clarification-Prompt-Runtime-DryRun-for-Reading-v1-001`  
**性质**：阅读链澄清提示 runtime dry-run（非真实播报）

## 治理链（dry-run）

```
Clarification Template → selection → priority/safety → cooldown/repeat
  → SpeechRequest candidate → Speech Gate pre-submit (ADMIT_AS_CANDIDATE)
  → VOP adapter candidate (READY_FOR_FUTURE_VOP_SUBMIT)
  → WAIT_FOR_USER_RESPONSE
```

## 当前 case

- `missing_both_task_and_scene`  
- `final_decision=WAIT_FOR_USER_RESPONSE`  
- 无用户回答 → 不填充 task/scene  

## 边界

不 TTS、不 VOP invoke、不 SpeechRequest submit、不写 STM/fact。

## 前置

[LUNA_USER_CLARIFICATION_PROMPT_TEMPLATE_FOR_READING_V1.md](./LUNA_USER_CLARIFICATION_PROMPT_TEMPLATE_FOR_READING_V1.md)

## 实现

- `capabilities/midplatform/user_clarification_prompt_runtime_dryrun_for_reading_v1.py`  
- `tools/evaluation/midplatform/run_user_clarification_prompt_runtime_dryrun_for_reading_v1.py`  
- `tools/evaluation/midplatform/verify_user_clarification_prompt_runtime_dryrun_for_reading_v1.py`

## 评测

[LUNA_EVALUATION_USER_CLARIFICATION_PROMPT_RUNTIME_DRYRUN_FOR_READING_V1.md](../evaluation/LUNA_EVALUATION_USER_CLARIFICATION_PROMPT_RUNTIME_DRYRUN_FOR_READING_V1.md)

## 建议下一 phase

- `Static-Reading-Task-Scene-Context-Reevaluation-DryRun-v1`  
- 已完成：见 [LUNA_USER_CLARIFICATION_RESPONSE_PARSING_DRYRUN_FOR_READING_V1.md](./LUNA_USER_CLARIFICATION_RESPONSE_PARSING_DRYRUN_FOR_READING_V1.md)
