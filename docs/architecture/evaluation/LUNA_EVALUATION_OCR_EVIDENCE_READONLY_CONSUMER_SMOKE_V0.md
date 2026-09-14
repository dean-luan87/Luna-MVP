# Luna Evaluation — OCR Bridge Evidence Pack Read-Only Consumer Smoke v0

**Phase**: `Phase-OCR-Evidence-Consumer-ReadOnly-Smoke-001`  
**OCR Bridge Evidence Pack Read-Only Consumer Smoke v0**

## 目的

验证 **`ocr_evidence_pack_candidate_v0` 形态的 `bridge_pack`**（本阶段默认使用 **multi-ROI RapidOCR smoke** 产物）可被 **只读 consumer** 正确读取：校验 `schema_version`、遍历 `eligible_text_evidence`、保留 **文本、ROI 归属、`source_unit_ref`、local / original 几何、`provider_trace`（经 `provider_summary`）**；可选合并同目录 **`ocr_lightweight_provider_multi_roi_result.json`** 顶层的 **`source_chain`** 形成 **`source_reference_chain_summary`**。

**明确不做**：MidPlatform 写路径、Scene Delta 写候选、WorldModel 写候选、AI 解释、partial completion、routing 变更、PaddleOCR。

## 前置

- `Phase-OCR-Lightweight-Provider-Multi-ROI-Smoke-001` = GO  
- `Phase-OCR-ROI-Evidence-Coordinate-Lift-001` = GO  
- `Phase-OCR-Lightweight-Provider-ROI-Input-Smoke-001` = GO  
- `Phase-OCR-Lightweight-Provider-Normalized-Input-Smoke-001` = GO  
- `Phase-OCR-Bridge-Evidence-Pack-Consumer-Static-Test-001` = GO  

**默认输入 `bridge_pack` 根目录**：`_eval_out/ocr_lightweight_provider_multi_roi_smoke_v0/`

## 命令

```bash
python3 tools/evaluation/ocr/run_ocr_evidence_readonly_consumer_smoke_v0.py \
  --output-root /ABS/PATH/_eval_out/ocr_evidence_readonly_consumer_smoke_v0

python3 tools/evaluation/ocr/verify_ocr_evidence_readonly_consumer_smoke_v0.py \
  --smoke-root /ABS/PATH/_eval_out/ocr_evidence_readonly_consumer_smoke_v0
```

可选：显式指定 `bridge_pack` 与 `result.json`（用于 `source_chain`）：

```bash
python3 tools/evaluation/ocr/run_ocr_evidence_readonly_consumer_smoke_v0.py \
  --output-root /ABS/PATH/_eval_out/ocr_evidence_readonly_consumer_smoke_v0 \
  --bridge-pack /ABS/PATH/_eval_out/ocr_lightweight_provider_multi_roi_smoke_v0/ocr_lightweight_provider_multi_roi_bridge_pack.json \
  --result-json /ABS/PATH/_eval_out/ocr_lightweight_provider_multi_roi_smoke_v0/ocr_lightweight_provider_multi_roi_result.json
```

## 产物

| 文件 | 说明 |
|------|------|
| `ocr_evidence_readonly_consumer_summary.json` | 输入路径、校验摘要、`evidence_count` 等。 |
| `ocr_evidence_readonly_consumer_view.json` | `read_only_consumer_view`：`text_joined`、`evidence_by_roi`、`evidence_geometry_matrix`、`provider_summary`、`source_reference_chain_summary`。 |
| `ocr_evidence_by_roi_matrix.json` | 与 view 中 `evidence_by_roi` 一致的 ROI 分组矩阵。 |
| `ocr_evidence_geometry_matrix.json` | 逐条证据的几何矩阵导出。 |
| `ocr_evidence_source_chain_summary.json` | `source_chain` 摘要（若可选 result 可读）。 |
| `ocr_evidence_readonly_consumer_audit_report.json` | 只读 audit：`midplatform_written` / `scene_delta_written` / `world_model_written` / `ai_interpretation_invoked` 等均为 **false**。 |
| `ocr_evidence_readonly_consumer_notes.md` | 短说明。 |
| `ocr_evidence_readonly_consumer_verifier_report.json` | Verifier 报告。 |

## Verifier 退出码

- **GO** / **CONDITIONAL_GO**：**0**；**NO_GO**：**2**。
