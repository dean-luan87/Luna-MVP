# Luna Evaluation — Supervision Adapter A/B Test v0

**Phase**：`Phase-Vision-Supervision-Adapter-AB-Test-001`  
**Runner**：`tools/evaluation/vision/run_supervision_adapter_ab_test_v0.py`  
**Verifier**：`tools/evaluation/vision/verify_supervision_adapter_ab_test_v0.py`

## 输入

| 根目录 | 默认路径 |
|--------|----------|
| Supervision structure reference | `_eval_out/supervision_structure_reference_analysis_smoke_v0/` |
| VisionDetectionEvidence schema alignment | `_eval_out/vision_detection_evidence_schema_alignment_smoke_v0/` |
| Rule stub ROI | `_eval_out/vision_roi_proposal_stub_smoke_v0/` |
| External supervision experiment | `_eval_out/external_supervision_adapter_experiment_smoke_v0_after_install/` |

## 命令

```bash
python3 tools/evaluation/vision/run_supervision_adapter_ab_test_v0.py \
  --supervision-structure-reference-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/supervision_structure_reference_analysis_smoke_v0 \
  --vision-detection-schema-alignment-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/vision_detection_evidence_schema_alignment_smoke_v0 \
  --rule-stub-roi-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/vision_roi_proposal_stub_smoke_v0 \
  --external-supervision-experiment-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/external_supervision_adapter_experiment_smoke_v0_after_install \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/supervision_adapter_ab_test_smoke_v0

python3 tools/evaluation/vision/verify_supervision_adapter_ab_test_v0.py \
  --smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/supervision_adapter_ab_test_smoke_v0
```

GO / NO_GO：见 [LUNA_EVALUATION_VISION_SUPERVISION_ADAPTER_AB_TEST_GO_NO_GO_PACK_V0.md](./LUNA_EVALUATION_VISION_SUPERVISION_ADAPTER_AB_TEST_GO_NO_GO_PACK_V0.md)。
