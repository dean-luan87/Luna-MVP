# Luna Evaluation — MidPlatform OCR Evidence Read-Only Ingest Candidate Smoke v0

**Phase**: `Phase-MidPlatform-OCR-Evidence-ReadOnly-Ingest-Candidate-001`

## 目的

验证中台侧可基于 **OCR read-only consumer** 产物生成 **`midplatform_ocr_evidence_ingest_candidate_v0`**：保留 **文本拼接、按 ROI 证据、几何矩阵、source chain、provider summary**；**不**写事实层、**不**写 Scene Delta、**不**写 WorldModel、**不**调用 AI 解释、**不**调用 OCR provider、**不**改 OCR routing。

## 前置

- `Phase-OCR-Evidence-Consumer-ReadOnly-Smoke-001` = GO  
- `Phase-OCR-Lightweight-Provider-Multi-ROI-Smoke-001` = GO  
- `Phase-OCR-ROI-Evidence-Coordinate-Lift-001` = GO  

**默认输入 consumer 根目录**：`_eval_out/ocr_evidence_readonly_consumer_smoke_v0/`

## 命令

```bash
python3 tools/evaluation/midplatform/run_midplatform_ocr_evidence_readonly_ingest_candidate_smoke_v0.py \
  --output-root /ABS/PATH/_eval_out/midplatform_ocr_evidence_readonly_ingest_candidate_smoke_v0

python3 tools/evaluation/midplatform/verify_midplatform_ocr_evidence_readonly_ingest_candidate_smoke_v0.py \
  --smoke-root /ABS/PATH/_eval_out/midplatform_ocr_evidence_readonly_ingest_candidate_smoke_v0
```

可选：显式指定 consumer 根目录：

```bash
python3 tools/evaluation/midplatform/run_midplatform_ocr_evidence_readonly_ingest_candidate_smoke_v0.py \
  --output-root /ABS/PATH/_eval_out/midplatform_ocr_evidence_readonly_ingest_candidate_smoke_v0 \
  --consumer-root /ABS/PATH/_eval_out/ocr_evidence_readonly_consumer_smoke_v0
```

## 读取的 Consumer 输入

| 文件 | 作用 |
|------|------|
| `ocr_evidence_readonly_consumer_view.json` | `evidence_count`、`text_joined`、`provider_summary` |
| `ocr_evidence_by_roi_matrix.json` | `evidence_by_roi`、文本矩阵派生 |
| `ocr_evidence_geometry_matrix.json` | `geometry_matrix` |
| `ocr_evidence_source_chain_summary.json` | `source_chain_summary` |

## 产物

| 文件 | 说明 |
|------|------|
| `midplatform_ocr_evidence_ingest_candidate_summary.json` | 输入路径、校验、`candidate_id` 等。 |
| `midplatform_ocr_evidence_ingest_candidate.json` | Ingest candidate 主体。 |
| `midplatform_ocr_evidence_ingest_text_matrix.json` | 按 ROI 展平的文本行表。 |
| `midplatform_ocr_evidence_ingest_geometry_matrix.json` | 几何矩阵副本。 |
| `midplatform_ocr_evidence_ingest_source_chain_summary.json` | source chain 摘要副本。 |
| `midplatform_ocr_evidence_ingest_audit_report.json` | 只读 audit。 |
| `midplatform_ocr_evidence_ingest_notes.md` | 短说明。 |
| `midplatform_ocr_evidence_ingest_verifier_report.json` | Verifier 报告。 |

## Verifier 退出码

- **GO** / **CONDITIONAL_GO**：**0**；**NO_GO**：**2**。
