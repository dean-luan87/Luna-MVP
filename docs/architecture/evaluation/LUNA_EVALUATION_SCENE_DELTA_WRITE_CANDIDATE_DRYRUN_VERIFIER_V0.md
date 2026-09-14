# Luna Evaluation — Scene Delta Write Candidate Dry-Run Verifier Smoke v0

**Phase**: `Phase-MidPlatform-Scene-Delta-Write-Candidate-DryRun-Verifier-001`

## 目的

对 **OCR 来源 Scene Delta write candidate stub** 产物运行 **dry-run verifier**：生成 summary、字段完备性、映射矩阵、风险报告与 **no-write audit**；并运行 **meta-verifier** 确认无写路径、无执行器调用、**gate_status** 仍为 **not_evaluated**、无 **confirmed_fact**。

## 前置

- `Phase-MidPlatform-Scene-Delta-Write-Candidate-From-OCR-Ingest-Stub-001` = GO  
- `Phase-OCR-Ingest-to-Product-Bus-ReadOnly-Replay-001` = GO  
- `Phase-MidPlatform-OCR-Evidence-ReadOnly-Ingest-Candidate-001` = GO  

**默认输入 write candidate 根目录**：`_eval_out/scene_delta_write_candidate_from_ocr_ingest_stub_smoke_v0/`

## 命令

```bash
python3 tools/evaluation/midplatform/run_scene_delta_write_candidate_dryrun_verifier_v0.py \
  --output-root /ABS/PATH/_eval_out/scene_delta_write_candidate_dryrun_verifier_smoke_v0

python3 tools/evaluation/midplatform/verify_scene_delta_write_candidate_dryrun_verifier_v0.py \
  --smoke-root /ABS/PATH/_eval_out/scene_delta_write_candidate_dryrun_verifier_smoke_v0
```

## 读取的 Stub 输入

| 文件 | 作用 |
|------|------|
| `scene_delta_write_candidate_from_ocr.json` | 主候选载荷 |
| `scene_delta_write_candidate_evidence_matrix.json` | 行数与 `evidence_items` 对齐校验 |
| `scene_delta_write_candidate_gate_stub.json` | gate 字段完备性 |
| `scene_delta_write_candidate_audit_report.json` | stub 侧 audit 存在性 |

## 产物

| 文件 | 说明 |
|------|------|
| `scene_delta_write_candidate_dryrun_summary.json` | `dry_run_id`、源候选 id、证据数、dry-run 状态、写闸门摘要字段。 |
| `scene_delta_write_candidate_field_completeness_report.json` | 字段检查表与 `overall_complete`。 |
| `scene_delta_write_candidate_mapping_matrix.json` | OCR → Scene Delta 概念路径映射（不落库）。 |
| `scene_delta_write_candidate_risk_report.json` | 风险代码列表。 |
| `scene_delta_write_candidate_no_write_audit_report.json` | dry-run no-write audit。 |
| `scene_delta_write_candidate_dryrun_notes.md` | 短说明。 |
| `scene_delta_write_candidate_dryrun_verifier_report.json` | Meta-verifier 报告。 |

## Verifier 退出码

- **GO** / **CONDITIONAL_GO**：**0**；**NO_GO**：**2**。
