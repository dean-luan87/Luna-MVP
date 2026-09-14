# Luna — Vision Lightweight Recognition Adapter Selection v0

**Phase**：`Phase-Vision-Lightweight-Recognition-Adapter-Selection-001`  
**前置（须均为 GO）**：

- `Vision-VideoFrame-Minimal-Ingest-001`  
- `Vision-FrameTrace-StreamRegistry-001`  
- `Vision-Frame-Input-Governance-001`  
- `Vision-Frame-ROI-Proposal-And-Segmentation-Stub-001`  

**并行 / 非前置硬依赖**：`Vision-External-Supervision-Adapter-Experiment-001-Rerun-After-Install` = GO（仍为 **外部实验线**，不接本 phase）。

## 目标

在 **`vision_provider_input_pack_v0`** 之上建立 **Vision recognition provider adapter selection** 的 **骨架**：

- **VisionProviderAdapterV0** 契约：`supports_input_pack`、`run`、`health_check`、`estimate_cost`；`provider_level` ∈ `stub | lightweight | heavy | vlm`。  
- **Provider registry**：默认仅 **`vision_stub`** `enabled=true`；`yolo_candidate`、`supervision_candidate`、`vlm_candidate` 均为 `enabled=false`。  
- **Selection report**：默认 `selected_provider=vision_stub`、`real_provider_invoked=false`；环境变量若请求真实 provider，本 phase **仍不调用**，并记录 `provider_selection_reason_codes`。  
- **Stub result**：对每个 `input_unit` 生成 **synthetic** 条目（`label=stub_object` 等），**不得**当作事实。  
- **Audit**：禁止 YOLO / Supervision 主线 / VLM / OCR / AI interpretation / 导航 / 中台写入 / Scene Delta / WorldModel；**`full_frame_direct_to_provider` 须为 false**。

## 核心原则

- **不得**让 recognition provider **直接消费整帧**；只能消费 pack 中的 **`input_units`**（本 smoke 校验 `full_frame_direct_to_provider=false`）。  
- **默认**仅启用 **stub**；YOLO / Supervision / VLM 仅作 **disabled candidate**；任何真实模型接入须 **另开 phase**。  
- 环境变量（默认均为关）：`LUNA_ENABLE_VISION_REAL_PROVIDER_V0`、`LUNA_ENABLE_YOLO_RUNTIME_PROVIDER_V0`、`LUNA_ENABLE_SUPERVISION_RUNTIME_PROVIDER_V0`、`LUNA_ENABLE_VLM_RUNTIME_PROVIDER_V0`。本 skeleton 下 **`real_provider_allowed` 恒为 false**；误开 flag 时 **fallback stub**，且 **`real_provider_invoked` 恒为 false**。

## 严禁

无 YOLO、Supervision **主线**、VLM、OCR、AI interpretation、MidPlatform fact、Scene Delta、WorldModel、导航决策；不得将任何 **真实** 视觉模型设为默认 provider。

## Vision 阶段表（评测对齐，v0）

| Phase | Verdict（当前叙述） |
|-------|---------------------|
| Vision-VideoFrame-Minimal-Ingest-001 | GO |
| Vision-FrameTrace-StreamRegistry-001 | GO |
| Vision-Frame-Input-Governance-001 | GO |
| Vision-Frame-ROI-Proposal-And-Segmentation-Stub-001 | GO |
| Vision-External-Supervision-Adapter-Experiment-001-Rerun-After-Install | GO（外部实验线） |
| Vision-Lightweight-Recognition-Adapter-Selection-001 | **GO**（以 `verify_vision_lightweight_recognition_adapter_selection_smoke_v0` 为准） |
| Vision-Recognition-Evidence-Pack-Stub-001 | **GO**（以 `verify_vision_recognition_evidence_pack_stub_v0` 为准；见 [LUNA_VISION_RECOGNITION_EVIDENCE_PACK_V0.md](./LUNA_VISION_RECOGNITION_EVIDENCE_PACK_V0.md)） |
| Vision-Supervision-Structure-Reference-Analysis-001 | **PLANNED / NOT_STARTED** |

## 实现与命令

见 `../evaluation/LUNA_EVALUATION_VISION_RECOGNITION_ADAPTER_SELECTION_SMOKE_V0.md`。

## 与下一工程 phase 的关系

建议下一跳：**Vision-Recognition-Evidence-Pack-Stub-001**（见 [LUNA_VISION_RECOGNITION_EVIDENCE_PACK_V0.md](./LUNA_VISION_RECOGNITION_EVIDENCE_PACK_V0.md)）：将 stub 输出规范为 Luna **`vision_recognition_evidence_pack_v0`**，再考虑只读 consumer 或 gated 真实 provider。

## 与 OCR 主线的类比

与 OCR 的 **provider registry / selection / audit / disabled candidates** 一致：先把 **契约与门禁** 立住，再谈真实模型。
