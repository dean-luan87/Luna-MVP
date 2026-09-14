# Luna — VisionDetectionEvidence Schema v0

**Phase**：`Phase-VisionDetectionEvidence-Schema-Alignment-001`

## 目的

在 **`vision_recognition_evidence_pack_v0`** 与 **Supervision Detections** 结构参考之间，定义 Luna 自有 **`vision_detection_evidence_v0`** 字段标准：候选视觉检测证据（**not_fact**），可回溯 **frame_id / roi_id / unit_id**，保留 **source_chain**。

## 核心原则

- **VisionDetectionEvidence** 是候选证据，不是事实。  
- **label** 不是 confirmed object；**confidence** 不是真实性；**tracker_id** 不是身份（`track_id_scope=provider_local | none`）。  
- **bbox / mask / polygon** 仅为几何候选。  
- 不得直接触发导航；不得写 MidPlatform fact / Scene Delta / WorldModel。

## Supervision 映射（摘要）

| Supervision | Luna |
|-------------|------|
| xyxy | bbox_in_frame / bbox_in_unit |
| confidence | confidence |
| class_id | class_id |
| class name | class_name / label |
| mask | mask_ref |
| polygon | polygon_in_frame |
| tracker_id | tracker_id |

## 评测

见 [LUNA_EVALUATION_VISION_DETECTION_EVIDENCE_SCHEMA_ALIGNMENT_V0.md](../evaluation/LUNA_EVALUATION_VISION_DETECTION_EVIDENCE_SCHEMA_ALIGNMENT_V0.md)。

## 建议下一跳

**Phase-Vision-Supervision-Adapter-AB-Test-001**（已完成路径）：见 [LUNA_VISION_SUPERVISION_ADAPTER_AB_TEST_V0.md](./LUNA_VISION_SUPERVISION_ADAPTER_AB_TEST_V0.md)。其后 **Gated YOLO Candidate Adapter**（单独 gated phase）。
