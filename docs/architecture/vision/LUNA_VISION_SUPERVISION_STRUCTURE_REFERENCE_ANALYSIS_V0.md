# Luna — Vision Supervision Structure Reference Analysis v0

**Phase**：`Phase-Vision-Supervision-Structure-Reference-Analysis-001`  
**性质**：**结构参考 / 映射 / 风险边界 / A/B 计划** — **不接** Luna Vision 主线。

## 前置

- `Phase-Vision-External-Supervision-Adapter-Experiment-001-Rerun-After-Install` = GO（`supervision_installed=true`，`supervision_version=0.28.0`）  
- `Vision-Frame-ROI-Proposal-And-Segmentation-Stub-001` = GO  
- `Vision-Recognition-Evidence-Pack-Stub-001` = GO  
- Scene Delta **generic executor prechain closure** = GO  

## 目标

分析 **Roboflow Supervision** 的 Detections / mask / tracker / zone / annotator 等结构，输出：

- **Capability structure report**  
- **Luna mapping matrix**（Supervision → Luna Vision*Evidence）  
- **Reuse classification**（direct_reuse / reference_only / requires_adapter / …）  
- **Architecture risk report**（不得接管 Luna Core、不得写事实层、不得导航）  
- **A/B test plan**（rule_stub vs synthetic adapter vs future YOLO+Supervision vs Luna evidence pack）  

## 严禁

- 接入主线、调用 **YOLO** / 真实 detector、导航决策、MidPlatform fact / Scene Delta / WorldModel、AI interpretation。

## 评测入口

见 [LUNA_EVALUATION_VISION_SUPERVISION_STRUCTURE_REFERENCE_ANALYSIS_V0.md](../evaluation/LUNA_EVALUATION_VISION_SUPERVISION_STRUCTURE_REFERENCE_ANALYSIS_V0.md)。

## 与外部 Supervision 实验的关系

读取 [LUNA_VISION_EXTERNAL_SUPERVISION_ADAPTER_EXPERIMENT_V0.md](./LUNA_VISION_EXTERNAL_SUPERVISION_ADAPTER_EXPERIMENT_V0.md) 产物目录；本 phase **不重复** synthetic ROI 生成，只做结构层分析。

## 建议下一跳

**Phase-VisionDetectionEvidence-Schema-Alignment-001**（已完成 schema 定义路径）：见 [LUNA_VISION_DETECTION_EVIDENCE_SCHEMA_V0.md](./LUNA_VISION_DETECTION_EVIDENCE_SCHEMA_V0.md)。其后 **Supervision Adapter A/B Test**（evaluation-only）。
