# Luna Evaluation — Supervision Adapter A/B Test GO / NO_GO Pack v0

**Verifier**：`tools/evaluation/vision/verify_supervision_adapter_ab_test_v0.py`

## GO

- 四路输入 root 存在；`supervision_installed=true`；`vision_detection_evidence_v0` 对齐。  
- rule_stub / supervision `roi_count > 0`。  
- Supervision → VisionDetectionEvidence fixture：`synthetic=true`，`fact_status=not_fact`。  
- A/B matrix、structure score、risk（not_luna_core / no fact write / no navigation）齐全。  
- audit 无越界。

## CONDITIONAL_GO

- 部分 score 子项缺失（soft）；无越界。

## NO_GO

- 主线 / YOLO / 真实 detector；synthetic 标 fact；写事实层；导航；audit 缺失。

## 一句话

evaluation-only 对比 rule_stub 与 supervision synthetic 的结构适配性；**不**接真实检测。
