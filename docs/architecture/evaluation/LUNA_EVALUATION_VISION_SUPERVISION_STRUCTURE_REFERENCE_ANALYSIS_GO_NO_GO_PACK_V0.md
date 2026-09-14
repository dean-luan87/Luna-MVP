# Luna Evaluation — Supervision Structure Reference GO / NO_GO Pack v0

**Verifier**：`tools/evaluation/vision/verify_supervision_structure_reference_analysis_v0.py`  
**Phase**：`Phase-Vision-Supervision-Structure-Reference-Analysis-001`

## GO

- **experiment root** 存在；**`supervision_installed=true`**；**`supervision_version`** 非空。  
- capability / mapping / reuse / risk / ab_test / audit 齐全。  
- 映射含 **VisionDetectionEvidence**、**VisionTrackingEvidence**、**VisionZoneEvidence**。  
- risk：**不得接管 Luna Core**、**不得写 MidPlatform fact**、**不得导航**。  
- audit：分析已执行；**yolo/real_detector/mainline/navigation/fact writes** 均为 false。

## CONDITIONAL_GO

- 部分 Supervision API 未在 extended probe 中确认，但报告与 gap 说明完整；无越界行为。

## NO_GO

- 接入主线；调用 YOLO/真实 detector；写事实层；导航；声称 Supervision 替代 Luna Core；**audit** 缺失。

## 一句话

本 smoke **只**做 Supervision 结构参考分析；**不**接主线、**不**调用真实检测。
