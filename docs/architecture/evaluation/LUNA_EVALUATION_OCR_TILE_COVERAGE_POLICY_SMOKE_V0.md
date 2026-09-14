# LUNA Evaluation — OCR Tile Coverage Policy Smoke v0

**阶段**：`Phase-OCR-Tile-Coverage-And-Truncation-Policy-001`

## 运行

```bash
python3 tools/evaluation/ocr/run_ocr_tile_coverage_policy_smoke_v0.py \
  --output-root "/ABS/PATH/_eval_out/ocr_tile_coverage_policy_smoke_v0"
```

脚本内强制 `LUNA_ENABLE_OCR_TILE_PLANNER_V0=true`，默认输入 **3000×5334**。

## 产物

| 文件 | 说明 |
|------|------|
| `ocr_tile_coverage_summary.json` | `tile_coverage` 摘要 |
| `ocr_tile_coverage_matrix.json` | 坐标矩阵 + 摘要 |
| `ocr_tile_uncovered_regions.json` | 未物化 tile 的 bbox 列表 |
| `ocr_tile_truncation_policy_report.json` | 截断与 `processing_policy` 镜像 |
| `ocr_tile_coverage_audit_report.json` | audit |
| `ocr_tile_coverage_notes.md` | 备注 |
| `ocr_tile_coverage_verifier_report.json` | coverage verifier |
| `ocr_tile_planner_verifier_report.json` | 复用 tile planner verifier |

## Verifier

```bash
python3 tools/evaluation/ocr/verify_ocr_tile_coverage_policy_smoke_v0.py \
  --smoke-root "/ABS/PATH/_eval_out/ocr_tile_coverage_policy_smoke_v0"
```
