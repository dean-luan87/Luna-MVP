# Luna — Evaluation: CrossModal Vision OCR TestBoard v1 Planning v0

**Phase**：`Phase-CrossModal-Vision-OCR-TestBoard-v1-Planning-001`

## 运行

```bash
python3 tools/evaluation/midplatform/run_cross_modal_vision_ocr_testboard_v1_planning_v0.py \
  --v0-closure-root /abs/path/_eval_out/cross_modal_vision_ocr_testboard_v0_closure_smoke_v0 \
  --output-root /abs/path/_eval_out/cross_modal_vision_ocr_testboard_v1_planning_smoke_v0

python3 tools/evaluation/midplatform/verify_cross_modal_vision_ocr_testboard_v1_planning_v0.py \
  --smoke-root /abs/path/_eval_out/cross_modal_vision_ocr_testboard_v1_planning_smoke_v0
```

## 产物

| 文件 | 说明 |
|------|------|
| `cross_modal_vision_ocr_testboard_v1_planning_summary.json` | 规划总览 |
| `cross_modal_vision_ocr_testboard_v1_track_matrix.json` | 三轨 entry/exit/non-claims |
| `cross_modal_vision_ocr_testboard_v1_phase_roadmap.json` | 各轨 phase 列表 |
| `cross_modal_vision_ocr_testboard_v1_non_goals_report.json` | 非目标 |
| `cross_modal_vision_ocr_testboard_v1_risk_register.json` | 风险登记 |
| `cross_modal_vision_ocr_testboard_v1_gate_policy.json` | 门控策略 |
| `cross_modal_vision_ocr_testboard_v1_execution_order.json` | 建议执行顺序 |
| `cross_modal_vision_ocr_testboard_v1_planning_audit_report.json` | 审计 |
| `cross_modal_vision_ocr_testboard_v1_planning_verifier_report.json` | Verifier 报告 |

## GO / NO_GO

[LUNA_EVALUATION_CROSS_MODAL_VISION_OCR_TESTBOARD_V1_PLANNING_GO_NO_GO_PACK_V0.md](./LUNA_EVALUATION_CROSS_MODAL_VISION_OCR_TESTBOARD_V1_PLANNING_GO_NO_GO_PACK_V0.md)
