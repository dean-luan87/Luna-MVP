# LUNA Evaluation — OCR Tile Evidence Merge Stub Smoke v0

**阶段**：`Phase-OCR-Tile-Evidence-Merge-Stub-001`

## 运行

```bash
python3 tools/evaluation/ocr/run_ocr_tile_evidence_merge_stub_smoke_v0.py \
  --output-root "/ABS/PATH/_eval_out/ocr_tile_evidence_merge_stub_smoke_v0"
```

环境变量由脚本设置：`LUNA_ENABLE_OCR_TILE_PLANNER_V0=true` 等。

## 产物

| 文件 | 说明 |
|------|------|
| `ocr_tile_evidence_merge_stub_summary.json` | 摘要 |
| `ocr_tile_evidence_items.json` | `tile_evidence_items` |
| `ocr_tile_evidence_coordinate_matrix.json` | 每 tile 原图 bbox / polygon 摘要 |
| `ocr_tile_evidence_merged_result.json` | merge stub 输出镜像 |
| `ocr_tile_evidence_bridge_pack.json` | bridge_pack |
| `ocr_tile_evidence_source_chain.json` | 结果 `source_chain` |
| `ocr_tile_evidence_audit_report.json` | audit |
| `ocr_tile_evidence_merge_stub_notes.md` | 备注 |
| `ocr_tile_evidence_merge_stub_verifier_report.json` | verifier |

## Verifier

```bash
python3 tools/evaluation/ocr/verify_ocr_tile_evidence_merge_stub_smoke_v0.py \
  --smoke-root "/ABS/PATH/_eval_out/ocr_tile_evidence_merge_stub_smoke_v0"
```
