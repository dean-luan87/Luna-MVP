# Luna — Static Reading Information Source Localization Policy v1

**Phase**：`Static-Reading-Information-Source-Localization-Policy-v1-001`  
**性质**：信息源定位策略（`policy_only`）

## 核心流程

1. WorldModel / memory / spatial anchor **优先**查找目标信息可能位置  
2. 无 WorldModel 时 → **场景识别 fallback**  
3. 任务类型 → **信息需求** 映射  
4. 场景 → **信息源区域** 矩阵（非全局找字）  
5. 候选信息源排序 → 排除规则 → 人工/工作人员 fallback  
6. 交接 **Readable Region Discovery**（下一阶段）

## 当前 case（OCR 失败链）

- `task_context_available=false`，`scene_context_available=false`  
- `information_source_localization_decision=WAIT_FOR_TASK_SCENE_CONTEXT`  
- **不伪造**具体场景类型  

## 边界

不 OCR、不 detector、不 camera、不地图 API、不写事实层。

## 前置

[LUNA_ASSISTED_STATIC_READING_RUNTIME_DRYRUN_V1.md](./LUNA_ASSISTED_STATIC_READING_RUNTIME_DRYRUN_V1.md)

## 实现

- `capabilities/midplatform/static_reading_information_source_localization_policy_v1.py`  
- `tools/evaluation/midplatform/run_static_reading_information_source_localization_policy_v1.py`  
- `tools/evaluation/midplatform/verify_static_reading_information_source_localization_policy_v1.py`

## 评测

[LUNA_EVALUATION_STATIC_READING_INFORMATION_SOURCE_LOCALIZATION_POLICY_V1.md](../evaluation/LUNA_EVALUATION_STATIC_READING_INFORMATION_SOURCE_LOCALIZATION_POLICY_V1.md)

## 建议下一 phase

- `Static-Reading-Task-Scene-Context-Policy-v1`（补 task/scene 后解锁区域发现 runtime）  
- 已完成：`Static-Readable-Region-Discovery-Guidance-Policy-v1` → [LUNA_STATIC_READABLE_REGION_DISCOVERY_GUIDANCE_POLICY_V1.md](./LUNA_STATIC_READABLE_REGION_DISCOVERY_GUIDANCE_POLICY_V1.md)
