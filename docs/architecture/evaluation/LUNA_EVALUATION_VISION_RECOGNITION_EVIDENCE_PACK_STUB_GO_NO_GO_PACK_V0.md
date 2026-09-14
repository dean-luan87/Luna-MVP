# Luna 评测 — Vision Recognition Evidence Pack Stub GO / NO_GO Pack v0

**Verifier**：`tools/evaluation/vision/verify_vision_recognition_evidence_pack_stub_v0.py`  
**Phase**：`Phase-Vision-Recognition-Evidence-Pack-Stub-001`

## GO

- `vision_recognition_evidence_pack.json` 存在；`schema_version=vision_recognition_evidence_pack_v0`。  
- `items` 数量 **> 0**；每条有 **`source_frame_id`**，且有 **`roi_id` 或 `unit_id`**。  
- 每条 item：`synthetic=true`，`stub_provider=true`，`fact_status=not_fact`。  
- 包级 `fact_status=not_fact`；`provider_trace.provider=vision_stub`，`real_provider_invoked=false`。  
- audit：`vision_evidence_pack_generated=true`，禁止类字段（YOLO / Supervision 主线 / VLM / OCR / MidPlatform / Scene Delta / WorldModel / AI interpretation / 导航 / real_provider）均为 **false**。

## CONDITIONAL_GO

- 无 **NO_GO** blockers，但存在 **soft_notes**（例如 `bbox_in_frame` 形态不完整或全零占位等）。

## NO_GO

- 将 stub 标为 **fact**（`fact_status` 非 `not_fact` 或 item 级非 `not_fact`）。  
- audit 缺失或暗示调用了 **YOLO / Supervision 主线 / VLM** 等禁止路径。  
- **MidPlatform / Scene Delta / WorldModel / 导航** 被标记为已发生。  
- evidence pack 缺失或 **items** 为空。

## 一句话

本 smoke **只**把 stub recognition 结果 **打包**为 Luna 证据结构；**不**调用真实模型、**不**写入事实层。
