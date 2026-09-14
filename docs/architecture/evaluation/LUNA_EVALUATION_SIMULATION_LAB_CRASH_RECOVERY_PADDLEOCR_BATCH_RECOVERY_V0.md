# Evaluation — Simulation Lab crash_recovery × PaddleOCR Batch Recovery v0

```bash
python3 tools/evaluation/simulation/run_simulation_lab_crash_recovery_paddleocr_batch_recovery_v0.py \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/simulation_lab_crash_recovery_paddleocr_batch_recovery_v0 \
  --crash-recovery-harness-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/simulation_lab_minimal_harness_v0/crash_recovery \
  --developer-full-harness-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/simulation_lab_minimal_harness_v0/developer_full \
  --benchmark-real-values-smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_benchmark_real_values_smoke_v0 \
  --benchmark-planning-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_benchmark_real_values_planning_v0 \
  --v1-track-closures-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_testboard_v1_track_closures_v0

# Optional after manual child run:
#   --child-summary /path/to/paddleocr_labeled_set_batch_recovery_summary.json

python3 tools/evaluation/simulation/verify_simulation_lab_crash_recovery_paddleocr_batch_recovery_v0.py \
  --phase-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/simulation_lab_crash_recovery_paddleocr_batch_recovery_v0
```

GO/NO_GO：[pack](./LUNA_EVALUATION_SIMULATION_LAB_CRASH_RECOVERY_PADDLEOCR_BATCH_RECOVERY_GO_NO_GO_PACK_V0.md)
