# Luna Evaluation — OCR Provider Selection Smoke v0

**Phase**: `Phase-OCR-Real-Provider-Adapter-Selection-001`

## 目的

验证 OCR 主线在 **normalization 之后** 具备 **provider registry + selection + audit + selection report**，且 **默认仅 stub**；在误配置（Paddle runtime 开、real 关）下 **硬拒绝**；在「请求 heavy、real 环境关」下 **仍 success 且 fallback_to_stub**。

## 命令

```bash
python3 tools/evaluation/ocr/run_ocr_provider_selection_smoke_v0.py \
  --output-root /ABS/PATH/_eval_out/ocr_provider_selection_smoke_v0

python3 tools/evaluation/ocr/verify_ocr_provider_selection_smoke_v0.py \
  --smoke-root /ABS/PATH/_eval_out/ocr_provider_selection_smoke_v0
```

## 产物（`--output-root`）

| 文件 | 说明 |
|------|------|
| `ocr_provider_registry_snapshot.json` | 默认 registry 快照。 |
| `ocr_provider_selection_smoke_summary.json` | A/B/C 三用例摘要。 |
| `ocr_provider_selection_case_a_result.json` | 默认 stub 路径完整 bridge 结果。 |
| `ocr_provider_selection_case_b_result.json` | `allow_heavy_ocr=true`、real 仍关。 |
| `ocr_provider_selection_case_c_result.json` | Paddle runtime 开、real 关 → `status=error`。 |
| `ocr_provider_selection_report.json` | Case A 的 `provider_selection_report`。 |
| `ocr_provider_selection_audit_report.json` | Case A audit 中与 selection 相关子集。 |
| `ocr_provider_selection_verifier_report.json` | verifier 输出。 |

## 依赖

- 工作区内 `configs/ocr/ocr_image_input_governance_v0.example.json`
- Python 可导入 `PIL`（生成小图 PNG）
