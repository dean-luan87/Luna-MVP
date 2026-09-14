# Luna — Evaluation: Poster Real OCR Gated Execution v0

**Phase**：`Phase-Poster-Real-OCR-Gated-Execution-001`

## 运行

```bash
python3 tools/evaluation/ocr/run_poster_real_ocr_gated_execution_v0.py \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/poster_real_ocr_gated_execution_smoke_v0 \
  --poster-layout-governance-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/poster_layout_segmentation_governance_smoke_v0 \
  --poster-region-ocr-plan-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/poster_region_ocr_plan_stub_smoke_v0 \
  --poster-visual-symbol-evidence-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/poster_visual_symbol_evidence_stub_smoke_v0 \
  --poster-reference-only-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_poster_ocr_reference_only_v0 \
  --poster-track-b-closure-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/poster_testboard_track_b_closure_v0 \
  --benchmark-real-values-smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_benchmark_real_values_smoke_v0 \
  --system-health-governance-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/system_health_center_governance_v0 \
  --simulation-lab-harness-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/simulation_lab_minimal_harness_v0/developer_full
```

## 验证

```bash
python3 tools/evaluation/ocr/verify_poster_real_ocr_gated_execution_v0.py \
  --smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/poster_real_ocr_gated_execution_smoke_v0
```

## 主要产物

| 文件 | 作用 |
|------|------|
| `poster_real_ocr_gated_execution_summary.json` | 阶段摘要与门控标志 |
| `poster_real_ocr_execution_plan.json` | 4 区 OCR 执行计划 |
| `poster_real_ocr_result_matrix.json` | 分区 OCR 结果矩阵 |
| `poster_layout_text_evidence_candidate.json` | 版面文本证据候选（非事实） |
| `poster_real_ocr_no_write_boundary_report.json` | 无写边界报告 |
| `poster_real_ocr_audit_report.json` | 审计标志 |
| `poster_real_ocr_verifier_report.json` | Verifier 判定 |

## GO / NO_GO

见 [LUNA_EVALUATION_POSTER_REAL_OCR_GATED_EXECUTION_GO_NO_GO_PACK_V0.md](./LUNA_EVALUATION_POSTER_REAL_OCR_GATED_EXECUTION_GO_NO_GO_PACK_V0.md)
