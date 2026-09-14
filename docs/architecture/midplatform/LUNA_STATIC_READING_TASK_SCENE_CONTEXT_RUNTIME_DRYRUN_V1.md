# Luna — Static Reading Task Scene Context Runtime DryRun v1

**Phase**：`Static-Reading-Task-Scene-Context-Runtime-DryRun-v1-001`  
**性质**：task/scene 上下文 runtime dry-run（非真实识别）

## 当前 case 决策

- `final_decision=WAIT_FOR_USER_CLARIFICATION`  
- `missing_context_status=missing_both_task_and_scene`  
- 生成 **user clarification candidate**（不 TTS）  
- **不**生成 task/scene context candidate、information source query、ranked source area  
- **不** invoke ISRC / RRD runtime  

## 与 Luna 世界模型主线

本 dry-run 体现「重构用户生活世界」路径：缺上下文时不硬凑 OCR/场景，而是保留澄清候选与 long-term candidate 链，等待第一视角与任务经验补齐。

## 前置

[LUNA_STATIC_READING_TASK_SCENE_CONTEXT_POLICY_V1.md](./LUNA_STATIC_READING_TASK_SCENE_CONTEXT_POLICY_V1.md)

## 实现

- `capabilities/midplatform/static_reading_task_scene_context_runtime_dryrun_v1.py`  
- `tools/evaluation/midplatform/run_static_reading_task_scene_context_runtime_dryrun_v1.py`  
- `tools/evaluation/midplatform/verify_static_reading_task_scene_context_runtime_dryrun_v1.py`

## 评测

[LUNA_EVALUATION_STATIC_READING_TASK_SCENE_CONTEXT_RUNTIME_DRYRUN_V1.md](../evaluation/LUNA_EVALUATION_STATIC_READING_TASK_SCENE_CONTEXT_RUNTIME_DRYRUN_V1.md)

## 建议下一 phase

- `User-Clarification-Prompt-Runtime-DryRun-for-Reading-v1`（模板已定义：见 [LUNA_USER_CLARIFICATION_PROMPT_TEMPLATE_FOR_READING_V1.md](./LUNA_USER_CLARIFICATION_PROMPT_TEMPLATE_FOR_READING_V1.md)）  
- `Static-Reading-Information-Source-Localization-Runtime-DryRun-v1`（task/scene 可用后）
