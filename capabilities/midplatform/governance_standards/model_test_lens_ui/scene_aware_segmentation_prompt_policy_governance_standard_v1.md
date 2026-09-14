# Scene-Aware Segmentation Prompt Policy Governance Standard V1

**Standard ID:** `SceneAwareSegmentationPromptPolicyGovernanceStandardV1`  
**Phase:** `Phase-P1-Midplatform-Scene-Aware-Segmentation-Prompt-Policy-Planning-v1-001`

## 目的

解决 MobileSAM 固定街景 prompt 跨场景误分割、误标注问题。将 MobileSAM 从「固定语义 prompt 分割」规划为 **scene_profile 驱动的区域候选生成**，并禁止 `prompt_label` 被 UI 或中台解释为真实类别。

## 上游 GO

- MobileSAM Single Model Execution Integration GO  
- Observation Attention Layer Planning GO  
- Visual Expression System Planning GO  
- MobileSAM → OCR Runner Sandbox Integration Execution GO  

## 冻结链路

见 `scene_aware_segmentation_prompt_policy_plan_v1.md`

## 本阶段允许

- 规划 `scene_profile_candidate` / `segmentation_prompt_policy` / prompt set / display policy  
- 定义地铁站与街景 prompt 分离策略  
- 定义 prompt label 降级与 UI 任务语义展示规则  

## 本阶段禁止

- 调用 MobileSAM / OCR / Detection runner  
- 写 fact / 导航决策  
- 改变 runner sandbox 架构  
- `prompt_label` 升级 fact  
- 主图显示 prompt 中文类别为系统判断  

## 核心原则

1. **SAM 切区域** — MobileSAM 只输出 `region_candidate`  
2. **中台决定看哪里** — Observation Attention + scene profile  
3. **专项模型判断是什么** — OCR / Detection / VLM  
4. **Fact Admission 决定是否成为事实**  

## Prompt Label 降级

- 允许：`source_prompt_hint`、`segmentation_prompt_id`、`candidate_only`  
- 禁止：`road_sign` → 路牌事实、`front_vehicle` → 车辆事实  

## 地铁站专项

`subway_platform` profile 必须使用 station prompt set，禁止默认街景 `road_sign` / `front_vehicle` / `crosswalk` prompt。

## 下一阶段

`Phase-P1-Midplatform-Scene-Aware-Segmentation-Prompt-Policy-Execution-v1-001`
