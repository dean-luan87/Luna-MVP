# Luna — Static Reading Task Scene Context Reevaluation DryRun v1

**Phase**：`Static-Reading-Task-Scene-Context-Reevaluation-DryRun-v1-001`  
**性质**：parsing candidates → TSC 复评 → ISRC query candidates（非 fact）

## 复评结果（simulated）

| 样例 | 完整性 | ISRC query later |
|------|--------|------------------|
| 找出口，商场 | complete | ✓ |
| 我要找门牌 | partial_task_only + 需确认 | ✗ |
| 医院里找科室 | complete | ✓ |
| 读这段字 | partial_task_only | ✗ |
| 我不知道在哪 | insufficient | ✗ |
| 问工作人员吧 | human_staff | ✗ |
| 找洗手间，在商场 | complete | ✓ |
| 车站看几号线 | complete | ✓ |

**Final**：`READY_FOR_INFORMATION_SOURCE_LOCALIZATION_RUNTIME_LATER`；RRD **now=false**。

## 前置

[LUNA_USER_CLARIFICATION_RESPONSE_PARSING_DRYRUN_FOR_READING_V1.md](./LUNA_USER_CLARIFICATION_RESPONSE_PARSING_DRYRUN_FOR_READING_V1.md)

## 实现

- `capabilities/midplatform/static_reading_task_scene_context_reevaluation_dryrun_v1.py`  
- `tools/evaluation/midplatform/run_static_reading_task_scene_context_reevaluation_dryrun_v1.py`  
- `tools/evaluation/midplatform/verify_static_reading_task_scene_context_reevaluation_dryrun_v1.py`

## 评测

[LUNA_EVALUATION_STATIC_READING_TASK_SCENE_CONTEXT_REEVALUATION_DRYRUN_V1.md](../evaluation/LUNA_EVALUATION_STATIC_READING_TASK_SCENE_CONTEXT_REEVALUATION_DRYRUN_V1.md)

## 建议下一 phase

- [LUNA_STATIC_READING_INFORMATION_SOURCE_LOCALIZATION_RUNTIME_DRYRUN_V1.md](./LUNA_STATIC_READING_INFORMATION_SOURCE_LOCALIZATION_RUNTIME_DRYRUN_V1.md)（已实现）
