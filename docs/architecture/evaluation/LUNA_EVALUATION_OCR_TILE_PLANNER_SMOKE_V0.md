# LUNA Evaluation — OCR Tile Planner Smoke v0

**阶段**：`Phase-OCR-Tile-Planner-And-Coordinate-Reconstruction-001`

## 运行命令

```bash
export LUNA_ENABLE_OCR_TILE_PLANNER_V0=true   # smoke 脚本内已强制为 true
python3 tools/evaluation/ocr/run_ocr_tile_planner_smoke_v0.py \
  --output-root "/ABS/PATH/_eval_out/ocr_tile_planner_smoke_v0"
```

默认生成 **3000×5334** PNG（可用 `--width` / `--height` 覆盖）。`--workspace-root`、`--governance-config` 规则同其它 OCR smoke。

## 产物（`--output-root`）

| 文件 | 说明 |
|------|------|
| `ocr_tile_planner_smoke_summary.json` | 摘要 |
| `ocr_tile_plan.json` | `ocr_tile_plan_v0` |
| `ocr_tile_input_units_matrix.json` | `input_units` 镜像 |
| `ocr_tile_coordinate_transform_matrix.json` | 每 tile 变换列表 |
| `ocr_provider_input_pack.json` | 完整 pack |
| `ocr_tile_planner_audit_report.json` | audit 镜像 |
| `ocr_tile_planner_notes.md` | 人工备注 |
| `ocr_tile_planner_verifier_report.json` | verifier 输出 |

## Verifier

```bash
python3 tools/evaluation/ocr/verify_ocr_tile_planner_smoke_v0.py \
  --smoke-root "/ABS/PATH/_eval_out/ocr_tile_planner_smoke_v0"
```

退出码：`0` = `GO`，非零 = `NO_GO`。
