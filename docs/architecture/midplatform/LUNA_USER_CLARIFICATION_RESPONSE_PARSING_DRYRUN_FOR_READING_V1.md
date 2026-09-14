# Luna — User Clarification Response Parsing DryRun for Reading v1

**Phase**：`User-Clarification-Response-Parsing-DryRun-for-Reading-v1-001`  
**性质**：模拟用户回答 → task/scene context candidate（非 fact）

## 流程

```
WAIT_FOR_USER_RESPONSE (prior phase)
  → simulated raw_user_response set
  → response parsing matrix (fill policy)
  → task_context_candidate / scene_context_candidate
  → confidence / confirmation
  → TSC handoff candidate
  → READY_FOR_TSC_REEVALUATION_LATER
```

## 边界

不 ASR、不 LLM、不写 task/scene fact、不 invoke ISRC/RRD/TSC runtime。

## 前置

[LUNA_USER_CLARIFICATION_PROMPT_RUNTIME_DRYRUN_FOR_READING_V1.md](./LUNA_USER_CLARIFICATION_PROMPT_RUNTIME_DRYRUN_FOR_READING_V1.md)

## 实现

- `capabilities/midplatform/user_clarification_response_parsing_dryrun_for_reading_v1.py`  
- `tools/evaluation/midplatform/run_user_clarification_response_parsing_dryrun_for_reading_v1.py`  
- `tools/evaluation/midplatform/verify_user_clarification_response_parsing_dryrun_for_reading_v1.py`

## 评测

[LUNA_EVALUATION_USER_CLARIFICATION_RESPONSE_PARSING_DRYRUN_FOR_READING_V1.md](../evaluation/LUNA_EVALUATION_USER_CLARIFICATION_RESPONSE_PARSING_DRYRUN_FOR_READING_V1.md)

## 建议下一 phase

- `Static-Reading-Information-Source-Localization-Runtime-DryRun-v1`  
- 已完成复评：见 [LUNA_STATIC_READING_TASK_SCENE_CONTEXT_REEVALUATION_DRYRUN_V1.md](./LUNA_STATIC_READING_TASK_SCENE_CONTEXT_REEVALUATION_DRYRUN_V1.md)
