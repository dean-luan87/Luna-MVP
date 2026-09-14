# Luna — User Clarification Prompt Template for Reading v1

**Phase**：`User-Clarification-Prompt-Template-for-Reading-v1-001`  
**性质**：阅读链缺 task/scene 时的澄清提示模板（`template_only`）

## 与 Luna 世界模型主线

不伪造 task/scene，不用 OCR 填认知空白；澄清提示经 **Speech Gate**（P0/P1 高于 P3/P4 澄清），用户回答由后续 TSC Runtime 解析，再进入 ISRC/RRD。

## 模板类型

- missing_task_context / missing_scene_context / missing_both_task_and_scene  
- low_confidence_task / low_confidence_scene / conflicting_context  
- ask_human_staff_option  

## 边界

不 TTS、不 VOP、不 SpeechRequest、不写 STM/fact/WorldModel。

## 前置

[LUNA_STATIC_READING_TASK_SCENE_CONTEXT_RUNTIME_DRYRUN_V1.md](./LUNA_STATIC_READING_TASK_SCENE_CONTEXT_RUNTIME_DRYRUN_V1.md)

## 实现

- `capabilities/midplatform/user_clarification_prompt_template_for_reading_v1.py`  
- `tools/evaluation/midplatform/run_user_clarification_prompt_template_for_reading_v1.py`  
- `tools/evaluation/midplatform/verify_user_clarification_prompt_template_for_reading_v1.py`

## 评测

[LUNA_EVALUATION_USER_CLARIFICATION_PROMPT_TEMPLATE_FOR_READING_V1.md](../evaluation/LUNA_EVALUATION_USER_CLARIFICATION_PROMPT_TEMPLATE_FOR_READING_V1.md)

## 建议下一 phase

- `User-Clarification-Response-Parsing-DryRun-for-Reading-v1`  
- 已完成 Runtime DryRun：见 [LUNA_USER_CLARIFICATION_PROMPT_RUNTIME_DRYRUN_FOR_READING_V1.md](./LUNA_USER_CLARIFICATION_PROMPT_RUNTIME_DRYRUN_FOR_READING_V1.md)
