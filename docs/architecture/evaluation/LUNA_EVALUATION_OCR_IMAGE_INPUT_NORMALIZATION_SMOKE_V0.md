# LUNA Evaluation — OCR Image Input Normalization Smoke v0

**阶段**：`Phase-OCR-ImageInput-Normalization-Pipeline-001`

## 运行命令

```bash
python3 tools/evaluation/ocr/run_ocr_image_input_normalization_smoke_v0.py \
  --output-root "/ABS/PATH/_eval_out/ocr_image_input_normalization_smoke_v0"
```

可选：`--workspace-root`、`--governance-config`（须为绝对路径或相对 workspace 的可解析路径）。

## 用例

| Case | 图像尺寸 | 期望行为（摘要） |
|------|-----------|------------------|
| `small` | 512×512 | 闸门 `ALLOW`；策略 `full_image_allowed` 或 `roi_only_stub`；可直通或经恒等变换记录坐标。 |
| `large` | 3000×5334 | `oversized=true`；在示例治理下走 **CONDITIONAL_ALLOW + downscale**；**不得** `original_image_used_directly=true`；存在坐标变换与 provider input pack。 |

## 产物目录（`--output-root`）

- `ocr_image_input_normalization_summary.json`  
- `ocr_image_metadata_probe.json`（cases 聚合）  
- `ocr_image_input_decision.json`  
- `ocr_provider_input_pack.json`  
- `ocr_coordinate_transform_matrix.json`  
- `ocr_image_input_normalization_audit_report.json`  
- `ocr_image_input_normalization_notes.md`  
- `ocr_image_input_normalization_verifier_report.json`（由 verifier 写入）  
- 子目录 `small/`、`large/`：单次桥接完整 JSON 镜像（便于 diff）。

## 校验脚本

```bash
python3 tools/evaluation/ocr/verify_ocr_image_input_normalization_smoke_v0.py \
  --smoke-root "/ABS/PATH/_eval_out/ocr_image_input_normalization_smoke_v0"
```

退出码：`0` = `GO`，非零 = `NO_GO`。
