# Luna — Static Readable Region Discovery Guidance Policy v1

**Phase**：`Static-Readable-Region-Discovery-Guidance-Policy-v1-001`  
**性质**：可阅读区域发现与引导策略（`policy_only`）

## 核心流程

1. **仅在**已推理出的候选信息源区域内发现 readable region（非全局找字）  
2. 定义 readable region candidate schema（非 detected text fact）  
3. 可读性多维过滤 → 分类（readable / unreadable / irrelevant / not worth reading）  
4. 用户视角引导（P3，低于安全播报；本阶段不 TTS）  
5. 区域排序与选择 → **static capture handoff**  
6. **OCRRequest future gate** 链接（须先有 candidate + static capture + STC）  
7. 人工/工作人员协助保留；不可读区域 → unresolved / expired long-term candidate  

## 当前 case（OCR 失败链）

- `task_context_available=false`，`scene_context_available=false`  
- `readable_region_discovery_invoked_now=false`  
- **不伪造** readable region / detector 结果  

## 边界

不 detector、不 OCR、不 camera、不 OCRRequest、不 TTS/VOP、不写事实层。

## 前置

[LUNA_STATIC_READING_INFORMATION_SOURCE_LOCALIZATION_POLICY_V1.md](./LUNA_STATIC_READING_INFORMATION_SOURCE_LOCALIZATION_POLICY_V1.md)

## 实现

- `capabilities/midplatform/static_readable_region_discovery_guidance_policy_v1.py`  
- `tools/evaluation/midplatform/run_static_readable_region_discovery_guidance_policy_v1.py`  
- `tools/evaluation/midplatform/verify_static_readable_region_discovery_guidance_policy_v1.py`

## 评测

[LUNA_EVALUATION_STATIC_READABLE_REGION_DISCOVERY_GUIDANCE_POLICY_V1.md](../evaluation/LUNA_EVALUATION_STATIC_READABLE_REGION_DISCOVERY_GUIDANCE_POLICY_V1.md)

## 建议下一 phase

- `Static-Reading-Task-Scene-Context-Runtime-DryRun-v1`（在 [Task Scene Context Policy](./LUNA_STATIC_READING_TASK_SCENE_CONTEXT_POLICY_V1.md) 已定义 schema 后）  
- `Static-Readable-Region-Discovery-Runtime-DryRun-v1`（task/scene + ranked source 可用后）
