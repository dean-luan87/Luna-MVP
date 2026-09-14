# Luna Evaluation — VisionDetectionEvidence Schema Alignment GO / NO_GO Pack v0

**Verifier**：`tools/evaluation/vision/verify_vision_detection_evidence_schema_alignment_v0.py`  
**Phase**：`Phase-VisionDetectionEvidence-Schema-Alignment-001`

## GO

- **schema_version=vision_detection_evidence_v0**；必填字段齐全。  
- **Supervision mapping** 含 xyxy / confidence / class_id / tracker_id。  
- **stub compat fixture**：`synthetic=true`，`fact_status=not_fact`。  
- **boundary report**：label_not_fact、tracker_id_not_identity、no_navigation_decision。  
- **audit** 无写路径、无 YOLO/主线/导航。

## CONDITIONAL_GO

- mapping **gaps** 非空但仅为可选字段说明；无越界。

## NO_GO

- 接入 Supervision 主线；YOLO/真实 detector；label=confirmed；tracker 当身份；写事实层；导航；audit 缺失。

## 一句话

本 smoke **只**定义 Luna **VisionDetectionEvidence v0** 与 Supervision 映射；**不**调用真实检测。
