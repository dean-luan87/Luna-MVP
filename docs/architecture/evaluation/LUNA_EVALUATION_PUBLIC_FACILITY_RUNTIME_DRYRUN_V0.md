# Evaluation — Public Facility Runtime DryRun v0

```bash
python3 tools/evaluation/midplatform/run_public_facility_runtime_dryrun_v0.py \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/public_facility_runtime_dryrun_v0 \
  --public-facility-governance-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/public_facility_semantic_correction_governance_smoke_v0 \
  --v1-track-closures-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_testboard_v1_track_closures_v0 \
  --benchmark-real-values-planning-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_benchmark_real_values_planning_v0 \
  --simulation-lab-harness-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/simulation_lab_minimal_harness_v0/developer_full \
  --poster-track-b-closure-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/poster_testboard_track_b_closure_v0

python3 tools/evaluation/midplatform/verify_public_facility_runtime_dryrun_v0.py \
  --dryrun-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/public_facility_runtime_dryrun_v0
```

GO/NO_GO：[pack](./LUNA_EVALUATION_PUBLIC_FACILITY_RUNTIME_DRYRUN_GO_NO_GO_PACK_V0.md)

架构：[../midplatform/LUNA_PUBLIC_FACILITY_RUNTIME_DRYRUN_V0.md](../midplatform/LUNA_PUBLIC_FACILITY_RUNTIME_DRYRUN_V0.md)
