# Luna — Static Reading Task Scene Context Policy v1

**Phase**：`Static-Reading-Task-Scene-Context-Policy-v1-001`  
**性质**：任务/场景上下文策略（`policy_only`）

## 核心流程

1. 定义 **task_context** / **scene_context** schema 与来源  
2. 任务与场景 **归一化**（不执行真实 scene detector）  
3. **task × scene** 矩阵 → `information_source_query` 前置输入  
4. 缺失/低置信/冲突 → **missing context handling** + **user clarification candidate**（不 TTS）  
5. **handoff** 给 Information Source Localization Runtime / RRD Runtime  
6. **RRD runtime preconditions** 明确定义（当前 case 未满足）

## 当前 case

- `task_context_available=false`，`scene_context_available=false`  
- `missing_context_status=missing_both_task_and_scene`  
- **不伪造** task/scene，**不生成** ranked_information_source_area  

## 边界

不 scene detector、不 OCR、不 camera、不地图 API、不写事实层。

## 前置

[LUNA_STATIC_READABLE_REGION_DISCOVERY_GUIDANCE_POLICY_V1.md](./LUNA_STATIC_READABLE_REGION_DISCOVERY_GUIDANCE_POLICY_V1.md)

## 实现

- `capabilities/midplatform/static_reading_task_scene_context_policy_v1.py`  
- `tools/evaluation/midplatform/run_static_reading_task_scene_context_policy_v1.py`  
- `tools/evaluation/midplatform/verify_static_reading_task_scene_context_policy_v1.py`

## 评测

[LUNA_EVALUATION_STATIC_READING_TASK_SCENE_CONTEXT_POLICY_V1.md](../evaluation/LUNA_EVALUATION_STATIC_READING_TASK_SCENE_CONTEXT_POLICY_V1.md)

## 建议下一 phase

- `User-Clarification-Prompt-Template-for-Reading-v1`  
- 已完成 Runtime DryRun：见 [LUNA_STATIC_READING_TASK_SCENE_CONTEXT_RUNTIME_DRYRUN_V1.md](./LUNA_STATIC_READING_TASK_SCENE_CONTEXT_RUNTIME_DRYRUN_V1.md)
