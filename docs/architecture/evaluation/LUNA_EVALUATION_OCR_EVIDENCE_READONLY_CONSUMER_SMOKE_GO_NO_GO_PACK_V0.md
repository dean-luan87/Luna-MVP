# LUNA Evaluation — OCR Evidence Read-Only Consumer Smoke GO / NO-GO Pack v0

**Phase**: `Phase-OCR-Evidence-Consumer-ReadOnly-Smoke-001`

## GO

- 输入 **`bridge_pack` JSON 存在**且 `schema_version` = **`ocr_evidence_pack_candidate_v0`**（runner 若校验失败会写入 `ocr_evidence_readonly_consumer_validation_errors.json` 并以非零码退出；verifier 将据此 **NO_GO**）。
- `eligible_text_evidence` **条数 ≥ 2**（multi-ROI smoke 为 3）。
- 每条证据：**非空 `text`**；**`roi_id` 或 `unit_id` 至少其一**；**`source_unit_ref` 可回溯**；**具备 original 几何**（`original_bbox` 四元组或 `original_polygon` 非空）。
- `evidence_by_roi` **非空**；`consumer_view.text_joined` **非空**。
- `provider_summary` 与 `source_reference_chain_summary` **存在**（后者允许 `chain_item_count=0`，此时 verdict 可为 **CONDITIONAL_GO**）。
- **Audit** 明确：`midplatform_written=false`、`scene_delta_written=false`、`world_model_written=false`、`ai_interpretation_invoked=false`、`paddleocr_invoked=false`、`ocr_routing_changed=false`。

## CONDITIONAL_GO

- **`source_chain` 为空**（未提供 result JSON 或链缺失），但其余 GO 条件满足；须在 soft_notes 中记录。
- 或未来扩展：**部分几何字段缺失**但缺口在 summary / notes 中完整披露（当前 multi-ROI 基线不触发）。

## NO_GO

- Consumer 或评测脚本 **暗示或执行** MidPlatform / Scene Delta / WorldModel **写路径**。
- **调用 AI 解释**、**改 routing**、**调用 PaddleOCR**。
- **丢失 ROI 归属**、**丢失 `source_unit_ref`**、**丢失 original 几何**。
- Verifier 任一硬门禁失败（见 `verify_ocr_evidence_readonly_consumer_smoke_v0.py`）。

## 一句话

本阶段只验证 **OCR `bridge_pack` 可被只读消费者读取**并保留 **文本、ROI 归属、原图几何与 source chain**；**不写** MidPlatform、**不写** Scene Delta、**不调用** AI 解释。
