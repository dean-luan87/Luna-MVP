# Observation Attention Layer V1 — Planning Document

**Phase:** `Phase-P1-Midplatform-Model-Test-Lens-Observation-Attention-Layer-Planning-v1-001`  
**Layer ID:** `ObservationAttentionLayerV1`  
**Status:** Planning only（本阶段不实现 UI、不跑模型、不调用 runner）

## 上游

- Luna Observation Lens V1 Closure GO  
- Human Correction Layer UI Execution GO  
- MobileSAM segmentation trial outputs  
- Perception HUD annotations

## 核心定义

**Observation Attention Layer（观察注意力层）** 是区域分割之后的 **观察调度层**。

它回答：

1. 哪些区域值得继续观察？  
2. 哪些区域和当前任务相关？  
3. 哪些区域可能有风险？  
4. 哪些区域不确定，需要复核？  
5. 下一步应该调用哪个模型继续看？

它不回答：事实类别、导航决策、行动指令、语音输出、事实层写入。

## 处理链路（V1.1 静态/动态补丁）

```
区域分割 → 静态/动态候选判断 → 观察优先级 → 后续模型路线
```

| 类型 | 典型区域 | 优先后续模型 |
|------|----------|--------------|
| static_candidate | 路牌、广告屏、门头、建筑 | OCR、Detection、SLAM reference |
| dynamic_candidate | 车辆、行人、骑行者 | Tracking、Detection、Depth |
| scene_structure_candidate | 道路、斑马线、地面 | Depth、SLAM、可通行复核 |
| unknown_motion_state | 单帧不明 | Detection、Human review |
| needs_tracking_review | 单帧疑似动态 | Tracking（需多帧） |

**单帧限制：** MobileSAM 单帧不得输出 `confirmed_dynamic`；车辆/行人仅为 `dynamic_candidate_by_label`。

## 处理链路（基础）

## 输入来源（V1）

| 来源 | 字段 |
|------|------|
| MobileSAM / segmentation | mask, score, prompt_label, area ratio, boundary quality |
| Perception HUD | entity_id, display_name, confidence, task_relevance, uncertainty_tags |
| Human Correction（可选） | 漏识别、边界不准、标签不可信、任务相关性错误 |
| task_context | 7 种任务上下文 |

## MobileSAM 第一版策略

MobileSAM **只能提供区域边界候选**，`prompt_label` 保持 candidate。

| 区域候选 | 优先级 | 原因 | 后续模型 |
|----------|--------|------|----------|
| 前方车辆 | P0/P1 | 可能风险 + 需 Detection | detection |
| 道路/斑马线 | P0/P1（导航任务） | 导航相关 + 可通行性 | depth + slam |
| 路牌/广告屏 | P1 | 文字相关 | ocr |
| 建筑/大型结构 | P2/P3 | 稳定背景参考 | no_followup / slam_reference |
| 街边设施/杆状物 | P1/P2 | 可能障碍 | detection + depth |

## Schema 产物

| 文件 | 用途 |
|------|------|
| `observation_attention_record_schema_v1.json` | 单区域注意力记录 |
| `region_priority_schema_v1.json` | 优先级等级与原因 |
| `followup_model_route_schema_v1.json` | 后续模型路线候选 |
| `observation_attention_policy_v1.json` | 任务上下文策略 + MobileSAM 策略 + Human Correction 联动 |
| `observation_target_motion_state_schema_v1.json` | 运动状态候选分类 |
| `static_dynamic_observation_policy_v1.json` | 静态/动态/场景结构观察路线 |

## Human Correction 联动

纠错记录 → **priority signal candidate**（非 ground truth）：

- 漏识别 → P0/P1 + detection/OCR/depth/human_review  
- 边界不准 → detection/depth  
- 标签错误 → detection/VLM/human_review  
- 风险判断错误 → human_review  
- 建议不合理 → recommendation_policy_review  

## 后续 UI 影响（规划，本阶段不实现）

- 对象胶囊按 P0/P1 排序  
- HUD 颜色语义保持（绿任务/红风险/黄不确定/蓝环境/紫 OCR/灰背景）  
- 右侧面板：优先观察区域 + 原因 + 建议补测模型  
- 底部摘要：优先观察列表 + Detection/OCR/Depth 建议  

## 与 Detection/OCR 的关系

Observation Attention 是 **Detection/OCR runner 的任务路由来源**：

- 路牌候选 → OCR route  
- 车辆候选 → Detection route  
- 道路区域 → Depth/SLAM route  

本阶段 **不调用 runner**，只生成 route candidate。

## 边界

**禁止：** 执行模型、写 fact/semantic、导航/语音、改 envelope/模型输出、prompt_label 升级事实、纠错当 ground truth、route 立即执行  

**允许：** attention/priority/route candidate、TestBoard、UI 展示规划

## 下游执行阶段（建议）

`Phase-P1-Midplatform-Model-Test-Lens-Observation-Attention-Layer-UI-Execution-And-Post-Review-v1-001`
