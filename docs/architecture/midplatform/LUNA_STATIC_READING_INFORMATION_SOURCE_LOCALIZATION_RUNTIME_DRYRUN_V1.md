# Luna — Static Reading Information Source Localization Runtime DryRun v1

**Phase**：`Static-Reading-Information-Source-Localization-Runtime-DryRun-v1-001`  
**性质**：消费 4 条 information source query candidates → candidate source areas → ranking placeholder → ranked candidates → RRD handoff（非 fact）

## 链路

```
TSC Reevaluation (4 query candidates)
  → ISRC Runtime DryRun
  → ranked_information_source_area_candidate_collection
  → RRD handoff candidate
  → READY_FOR_READABLE_REGION_DISCOVERY_RUNTIME_LATER
```

## 四条 query（smoke）

| task + scene | 候选信息源区域 |
|--------------|----------------|
| find_exit + shopping_mall | exit_sign, directory_board, elevator_area, service_desk |
| find_department + hospital | department_sign, floor_guide, staff_desk, room_doorplate |
| find_restroom + shopping_mall | restroom_sign, directory_board, elevator_area, service_desk |
| find_transit_line + transit_station | platform_sign, line_number_sign, electronic_screen, staff_counter |

**Final**：`READY_FOR_READABLE_REGION_DISCOVERY_RUNTIME_LATER`；RRD **invoked_now=false**。

## 禁止

- map API / camera / detector / OCR / TTS / VOP  
- readable region 生成、RRD runtime invoke  
- task/scene/information source fact、WorldModel、SceneDelta

## 前置

[LUNA_STATIC_READING_TASK_SCENE_CONTEXT_REEVALUATION_DRYRUN_V1.md](./LUNA_STATIC_READING_TASK_SCENE_CONTEXT_REEVALUATION_DRYRUN_V1.md)

## 实现

- `capabilities/midplatform/static_reading_information_source_localization_runtime_dryrun_v1.py`  
- `tools/evaluation/midplatform/run_static_reading_information_source_localization_runtime_dryrun_v1.py`  
- `tools/evaluation/midplatform/verify_static_reading_information_source_localization_runtime_dryrun_v1.py`

## 评测

[LUNA_EVALUATION_STATIC_READING_INFORMATION_SOURCE_LOCALIZATION_RUNTIME_DRYRUN_V1.md](../evaluation/LUNA_EVALUATION_STATIC_READING_INFORMATION_SOURCE_LOCALIZATION_RUNTIME_DRYRUN_V1.md)

## 建议下一 phase

- [LUNA_STATIC_READABLE_REGION_DISCOVERY_RUNTIME_DRYRUN_V1.md](./LUNA_STATIC_READABLE_REGION_DISCOVERY_RUNTIME_DRYRUN_V1.md)（已实现）
