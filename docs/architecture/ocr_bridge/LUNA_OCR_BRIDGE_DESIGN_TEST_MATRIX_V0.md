# LUNA OCR Bridge — Design Test Matrix v0 (Phase-OCRBridge-Design-001)

## 离线工具链

| 步骤 | 命令 / 产物 |
|------|-------------|
| 输入 | OCR-007 `--eligibility-gate-root`（含 `ocr_evidence_routing_pack.json`） |
| 构建 | `python3 tools/ocr_bridge/build_ocr_evidence_pack_from_eval_v0.py ...` |
| 输出 | `ocr_evidence_pack_example.json`、`ocr_midplatform_forwarding_decision_example.json`、`ocr_evidence_pack_validation_report.json`、trace/replay、notes |
| 验收 | `python3 tools/ocr_bridge/verify_ocr_evidence_pack_contract_v0.py --output-root ...` |

## 用例行

1. **合法 eval 导入**：verifier **GO**，`hard_audit` 全 false。
2. **缺 routing pack**：build 失败（显式退出码）。
3. **篡改 symbol `should_enter_raw_text=true`**：`validate_ocr_evidence_pack_v0` 应报 **G**（手工测试矩阵项）。
