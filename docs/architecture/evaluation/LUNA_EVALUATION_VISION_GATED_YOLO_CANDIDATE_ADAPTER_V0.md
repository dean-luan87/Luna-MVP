# Luna Evaluation — Gated YOLO Candidate Adapter v0

**Phase**：`Phase-Vision-Gated-YOLO-Candidate-Adapter-001`  
**Runner**：`tools/evaluation/vision/run_yolo_candidate_adapter_eval_v0.py`  
**Verifier**：`tools/evaluation/vision/verify_yolo_candidate_adapter_eval_v0.py`

## 输入

| 根目录 | 默认 |
|--------|------|
| Schema alignment | `_eval_out/vision_detection_evidence_schema_alignment_smoke_v0/` |
| ROI proposal | `_eval_out/vision_roi_proposal_stub_smoke_v0/` |
| Supervision A/B（参考） | `_eval_out/supervision_adapter_ab_test_smoke_v0/` |

## 命令

```bash
python3 tools/evaluation/vision/run_yolo_candidate_adapter_eval_v0.py \
  --vision-detection-schema-alignment-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/vision_detection_evidence_schema_alignment_smoke_v0 \
  --roi-proposal-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/vision_roi_proposal_stub_smoke_v0 \
  --supervision-ab-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/supervision_adapter_ab_test_smoke_v0 \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/yolo_candidate_adapter_eval_smoke_v0

python3 tools/evaluation/vision/verify_yolo_candidate_adapter_eval_v0.py \
  --smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/yolo_candidate_adapter_eval_smoke_v0
```

真实 YOLO（可选）：

```bash
export LUNA_YOLO_EVAL_ONLY=true
export LUNA_ENABLE_YOLO_EVAL_PROVIDER_V0=true
# export LUNA_YOLO_MODEL_PATH=/path/to/model.pt
```

GO / NO_GO：[LUNA_EVALUATION_VISION_GATED_YOLO_CANDIDATE_ADAPTER_GO_NO_GO_PACK_V0.md](./LUNA_EVALUATION_VISION_GATED_YOLO_CANDIDATE_ADAPTER_GO_NO_GO_PACK_V0.md)
