# Scene-Aware Segmentation Prompt Policy Plan V1

**Phase:** `Phase-P1-Midplatform-Scene-Aware-Segmentation-Prompt-Policy-Planning-v1-001`  
**System ID:** `LunaMidplatformSceneAwareSegmentationPromptPolicyPlanningV1`  
**Status:** Planning only（本阶段不接新模型、不改 runner sandbox、不写 fact）

## 背景问题

当前 MobileSAM 使用 **固定户外街景 prompt set**（`road_sign` / `front_vehicle` / `crosswalk_or_road_region` 等）跨场景运行。换到地铁站台图时：

- `road_sign` prompt 框到行人
- `front_vehicle` prompt 框到站台地面
- 「开往 嘉会湖」指示牌未被 prompt 命中
- UI 将 prompt label 显示为「路牌 / 车辆」，造成语义误导

根因不是 UI 或中台治理链故障，而是 **MobileSAM 被当作跨场景语义分类器使用**。MobileSAM 适合做区域分割候选，不适合用固定语义 prompt 充当真实类别判断。

## 上游 GO

| 基线 | 决策 |
|------|------|
| MobileSAM Single Model Execution Integration | GO |
| Observation Attention Layer Planning | GO |
| Visual Expression System Planning | GO |
| MobileSAM → OCR Runner Sandbox Integration Execution | GO（OCR 链已通，但错误区域会拖死 OCR） |

## 本阶段终点

**segmentation_prompt_policy** — 由 `scene_profile_candidate` 驱动的 prompt 选择与 `prompt_label` 降级策略。不是 runner 执行，不是 fact，不是 UI 落地。

## 核心原则

1. **MobileSAM 只输出 `region_candidate`**，不输出真实类别  
2. **`prompt_label` 只能作为 `source_prompt_hint`**，不能升级为 fact label  
3. **不同 `scene_profile` 使用不同 prompt policy**  
4. **Observation Attention** 根据 `region_candidate + scene_profile + task_context` 决定后续路线  
5. **OCR / Detection / VLM** 承担语义复核，输出仍需 fact admission  

## 冻结链路

```
Input Image
  ↓
scene_profile_candidate          ← candidate_only · not_fact
  ↓
segmentation_prompt_policy     ← 本阶段终点
  ↓
MobileSAM prompt set
  ↓
region_candidate
  ↓
Observation Attention
  ↓
Followup Route Candidate
  ↓
Detection / OCR / Depth / SLAM（未来专项复核）
```

## 三层解决方案

### 1. MobileSAM 降级为区域候选生成器

| 现在（错误） | 应改为 |
|-------------|--------|
| `road_sign` → UI「路牌」 | `display_label` = 文字候选区 / 观察候选 |
| `front_vehicle` → UI「前方车辆」 | `semantic_label` = candidate_only |
| prompt 即类别 | `source_hint` = road_sign_prompt（仅详情展示） |

主图禁止默认显示「P0 路牌」「P0 前方车辆」。允许：P0 文字候选区、P1 屏幕/标识候选、P1 动态目标候选、P2 大型结构候选。

### 2. Scene Profile 驱动 Prompt Policy

支持 profile（均为 candidate）：

- `outdoor_street`
- `subway_platform`
- `indoor_station`
- `indoor_mall`
- `corridor`
- `store_front`
- `unknown_scene`

**地铁站** 不得默认使用街景 prompt。应使用 `scene_prompt_set_subway_platform_v1.json`。

### 3. 通用区域候选 + 专项模型复核

MobileSAM 回答「哪里可能值得看」，不回答「这是什么」。

示例（地铁站）：

| 区域候选 | 后续任务 |
|---------|---------|
| 上方长条区域 | OCR candidate |
| 中间屏幕区域 | OCR / Detection candidate |
| 车门区域 | Detection / Safety candidate |
| 地面边界 | Walkable / Depth candidate |
| 人群区域 | Tracking / Detection candidate |

## Scene Profile Candidate

见 `schemas/scene_aware_segmentation/scene_profile_candidate_schema_v1.json`

字段：`scene_profile_id`、`scene_type_candidate`、`confidence`、`evidence_refs`、`candidate_only`、`not_fact`

## Segmentation Prompt Policy

见 `schemas/scene_aware_segmentation/segmentation_prompt_policy_v1.json`

根据 `scene_profile_candidate` 选择 prompt set。`subway_platform` **禁止**默认挂载 `road_sign` / `front_vehicle` / `crosswalk_or_road_region` 街景 prompt。

## Prompt Set

- `scene_prompt_set_outdoor_street_v1.json` — 户外街景（prompt 后缀 `_candidate` 或中性命名）
- `scene_prompt_set_subway_platform_v1.json` — 地铁站专用

地铁站关键 OCR 导向 prompt：

- `station_direction_sign` → OCR P0/P1
- `station_name_board` → OCR P0
- `route_map_or_line_info` → OCR P1
- `advertisement_panel` → OCR P1/P2

## Prompt Label 降级

所有 prompt 输出必须携带：

- `segmentation_prompt_id`
- `source_prompt_hint`
- `candidate_only: true`
- `prompt_is_not_fact: true`

禁止：

- `prompt_label` → display fact label
- `road_sign` → 路牌事实
- `station_direction_sign` → 指示牌事实

## UI 展示规则

见 `prompt_label_display_policy_v1.json`

- 主图：中台任务语义，非原始 prompt 语义  
- 详情：可显示 `source_prompt_hint` + `prompt_is_not_fact: true`  
- 禁止：未经 Detection/OCR/VLM 复核即在主图显示「路牌」「车辆」「广告屏」为系统判断  

## 地铁站 Smoke 预期（规划验收）

测试图：`capabilities/test_assets/p1/ocr/ocr_real_image_subway_platform_jiahuihu_v1_001.png`

| 检查项 | 预期 |
|--------|------|
| scene_profile | `subway_platform` candidate |
| prompt set | 使用 station prompt set，非街景 5 prompt |
| station_direction_sign | 应覆盖「开往 嘉会湖」附近或生成 OCR route candidate |
| people_region | 不得显示为「路牌」 |
| road_sign / front_vehicle | 不在 subway profile 默认 prompt 中 |

## 应急短期策略（Execution 阶段实施，本阶段仅规划）

```text
if scene_profile_candidate == subway_platform:
    use subway_platform_prompt_set
else:
    use outdoor_street_prompt_set
```

主图标签改为任务语义，即使 prompt 偏了也不展示错误类别为系统判断。

## 长期路线

1. 通用分割 / 多区域 proposal  
2. scene profile + 中台策略筛选  
3. Detection / OCR / VLM / Depth 专项复核  

**SAM 切区域 → 中台决定看哪里 → OCR/Detection 判断是什么 → Fact Admission 决定是否成为事实**

## 本阶段禁止

- 调用 MobileSAM / OCR / Detection runner  
- 写 fact / 导航决策  
- 改变 runner sandbox 架构  
- 自动 Fusion / 主图 OCR box  
- prompt_label 升级 fact  

## 产出

| 产物 | 路径 |
|------|------|
| Plan | `scene_aware_segmentation/scene_aware_segmentation_prompt_policy_plan_v1.md` |
| Types | `scene_aware_segmentation/scene_aware_segmentation_prompt_policy_types_v1.py` |
| Scene profile schema | `schemas/scene_aware_segmentation/scene_profile_candidate_schema_v1.json` |
| Prompt policy | `schemas/scene_aware_segmentation/segmentation_prompt_policy_v1.json` |
| Subway prompt set | `schemas/scene_aware_segmentation/scene_prompt_set_subway_platform_v1.json` |
| Street prompt set | `schemas/scene_aware_segmentation/scene_prompt_set_outdoor_street_v1.json` |
| Display policy | `schemas/scene_aware_segmentation/prompt_label_display_policy_v1.json` |
| Governance | `governance_standards/model_test_lens_ui/scene_aware_segmentation_prompt_policy_governance_standard_v1.md` |

## 下一阶段

`Phase-P1-Midplatform-Scene-Aware-Segmentation-Prompt-Policy-Execution-v1-001`

- runner prompt config 接线  
- UI `hud_label_layout_policy` 任务语义标签  
- scene profile candidate 启发式（规划期可先 rule-based）  
- 地铁站 smoke execution  
