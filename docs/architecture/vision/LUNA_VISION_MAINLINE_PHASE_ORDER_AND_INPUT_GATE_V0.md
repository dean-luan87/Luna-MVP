# Luna — Vision 主线 phase 顺序与输入门控 v0

本文固定 **Vision 视频主线** 的合法推进顺序与 **禁止跳步** 规则，避免在仅有「帧 ingest + 帧轨迹登记」时误接 YOLO、VLM、视角识别或整帧进模型。

## 硬性规则（禁止跳步）

- **Frame Trace / Stream Registry 不是视角识别前置**。`Phase-Vision-FrameTrace-StreamRegistry-001` **只**登记视频流、采样帧、`frame_id` / `stream_id`、时间、`image_ref`、指纹、sampling policy 等到标准帧轨迹；**不调用** YOLO、VLM、OCR，也不产出识别语义。  
- **不得**从 Frame Trace / Registry **直接进入**「视角识别 / Vision Recognition Provider」或任何专用视角检测流水线。  
- 在接 **轻量视角识别**（或任意视觉识别 provider）之前，**必须先**完成：  
  1. `Phase-Vision-Frame-Input-Governance-001`  
  2. `Phase-Vision-Frame-ROI-Proposal-And-Segmentation-Stub-001`  

## 推荐主线顺序

| 顺序 | Phase（概念名） | 作用 |
|------|-----------------|------|
| 1 | Vision-VideoFrame-Minimal-Ingest-001 | 视频 → 帧采样 → `video_frame_envelope_v0` → audit（已实现） |
| 2 | Vision-FrameTrace-StreamRegistry-001 | stream registry + frame trace + lineage + 采样一致性（已实现） |
| 3 | **Vision-Frame-Input-Governance-001**（smoke 已实现） | 帧级接受/拒绝、规范化建议、ROI 准入 vs **识别禁止**；STCM/Performance 占位（见 [LUNA_VISION_FRAME_INPUT_GOVERNANCE_V0.md](./LUNA_VISION_FRAME_INPUT_GOVERNANCE_V0.md)） |
| 4 | **Vision-Frame-ROI-Proposal-And-Segmentation-Stub-001**（smoke 已实现） | 规则 / stub 生成 ROI（center / ground / upper_sign / left / right），**`vision_provider_input_pack_v0`** + ROI crop + 坐标变换；**不用**真实分割 / YOLO / Supervision 主线（见 [LUNA_VISION_FRAME_ROI_PROPOSAL_AND_SEGMENTATION_STUB_V0.md](./LUNA_VISION_FRAME_ROI_PROPOSAL_AND_SEGMENTATION_STUB_V0.md)） |
| 5 | **Vision-Lightweight-Recognition-Adapter-Selection-001**（smoke 已实现） | **`vision_provider_input_pack_v0`** 之上的 **registry + selection + stub adapter**；默认 **vision_stub**；YOLO / Supervision 主线 / VLM 仅 disabled candidate（见 [LUNA_VISION_LIGHTWEIGHT_RECOGNITION_ADAPTER_SELECTION_V0.md](./LUNA_VISION_LIGHTWEIGHT_RECOGNITION_ADAPTER_SELECTION_V0.md)） |
| 6 | **Vision-Recognition-Evidence-Pack-Stub-001**（smoke 已实现） | stub 结果 → **`vision_recognition_evidence_pack_v0`**（`not_fact` / synthetic；回读 input pack 几何）（见 [LUNA_VISION_RECOGNITION_EVIDENCE_PACK_V0.md](./LUNA_VISION_RECOGNITION_EVIDENCE_PACK_V0.md)） |
| 7 | **Vision-Recognition-Evidence-ReadOnly-Consumer-001**（smoke 已实现） | 只读消费 evidence pack → **consumer_view** + 按帧 / ROI 聚合矩阵（见 [LUNA_VISION_RECOGNITION_EVIDENCE_READONLY_CONSUMER_V0.md](./LUNA_VISION_RECOGNITION_EVIDENCE_READONLY_CONSUMER_V0.md)） |

## 必须先做「输入治理 + ROI stub」的四个原因

1. **不能默认吃整帧**：背景、广告、路人、阴影、海报等会大量进入候选，后续中台易被无效证据淹没。  
2. **坐标变换必须可追溯**：例如「出口」「门牌」「台阶」等语义必须能映回 **原始帧** 空间，而非仅「裁剪图里有什么」。  
3. **性能在模型前控制**：Vision 比 OCR 更易被帧率与分辨率拖死；须在 provider 前完成帧级 ROI、crop、resize、采样与预算。  
4. **任务驱动 ROI**：导航（前方通行、地面、障碍）、OCR（标牌/屏幕）、安全（近场动态、边缘）、找物（用户指定区域）等需要 **不同 ROI 提案**，须在识别前进入切割/提案逻辑。

## vision_provider_input_pack_v0（设计占位，ROI stub phase 实现）

与 OCR **input pack** 对齐思路；由 **ROI Proposal / Segmentation Stub** phase 生成，供后续 provider **只消费整理后的单元**：

```json
{
  "schema_version": "vision_provider_input_pack_v0",
  "source_frame_id": "...",
  "source_image_ref": "...",
  "input_units": [
    {
      "unit_id": "roi_001",
      "unit_type": "frame_roi",
      "bbox_in_frame": [0, 300, 640, 480],
      "image_ref": "...",
      "coordinate_transform": {
        "offset_x": 0,
        "offset_y": 300,
        "scale_x": 1.0,
        "scale_y": 1.0
      },
      "task_hint": "ground_navigation"
    }
  ],
  "source_chain": [
    "frame_envelope_ref:...",
    "roi_proposal_stub_created",
    "coordinate_transform_recorded"
  ]
}
```

Stub 阶段可覆盖的典型 ROI 名（示例，非最终实现清单）：`center_roi`、`ground_roi`、`upper_sign_roi`、`left_roi` / `right_roi`、`nearfield_roi`、`full_frame_low_priority_roi` 等。

## 与 OCR 大图问题的类比

若跳过 **输入治理** 与 **ROI / 画面切割**，让模型直接吃整帧，会出现与 **OCR 大图** 类似的问题：**性能、误检、坐标与任务归属** 同时失控。画面切割与规范化分属 **治理** 与 **ROI proposal** 两层，**不可跳过**。

## 外部实验线：Supervision（非主线、非默认 Vision）

与主线 **并行** 的独立评测 phase：**Phase-Vision-External-Supervision-Adapter-Experiment-001**（见 [LUNA_VISION_EXTERNAL_SUPERVISION_ADAPTER_EXPERIMENT_V0.md](./LUNA_VISION_EXTERNAL_SUPERVISION_ADAPTER_EXPERIMENT_V0.md)）。用于验证 Roboflow Supervision 作为 **外部工程库候选**（标准化检测、跟踪、zone 等），**不**接入 Luna Core，**不**替代上述 governance / ROI stub 顺序。吸收路径应为：**实验 → A/B → 只取模块能力 → 不接管主线**。

## 相关文档

- [LUNA_VISION_VIDEO_FRAME_MINIMAL_INGEST_V0.md](./LUNA_VISION_VIDEO_FRAME_MINIMAL_INGEST_V0.md)  
- [LUNA_VISION_FRAME_TRACE_STREAM_REGISTRY_V0.md](./LUNA_VISION_FRAME_TRACE_STREAM_REGISTRY_V0.md)  
- [LUNA_VISION_FRAME_INPUT_GOVERNANCE_V0.md](./LUNA_VISION_FRAME_INPUT_GOVERNANCE_V0.md)  
- [LUNA_VISION_FRAME_ROI_PROPOSAL_AND_SEGMENTATION_STUB_V0.md](./LUNA_VISION_FRAME_ROI_PROPOSAL_AND_SEGMENTATION_STUB_V0.md)  
- [LUNA_VISION_LIGHTWEIGHT_RECOGNITION_ADAPTER_SELECTION_V0.md](./LUNA_VISION_LIGHTWEIGHT_RECOGNITION_ADAPTER_SELECTION_V0.md)  
- [LUNA_VISION_RECOGNITION_EVIDENCE_PACK_V0.md](./LUNA_VISION_RECOGNITION_EVIDENCE_PACK_V0.md)  
- [LUNA_VISION_RECOGNITION_EVIDENCE_READONLY_CONSUMER_V0.md](./LUNA_VISION_RECOGNITION_EVIDENCE_READONLY_CONSUMER_V0.md)  
- [LUNA_VISION_EXTERNAL_SUPERVISION_ADAPTER_EXPERIMENT_V0.md](./LUNA_VISION_EXTERNAL_SUPERVISION_ADAPTER_EXPERIMENT_V0.md)  
