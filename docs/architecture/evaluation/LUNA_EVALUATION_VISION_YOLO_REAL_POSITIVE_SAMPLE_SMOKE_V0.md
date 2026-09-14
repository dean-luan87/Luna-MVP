# Luna Evaluation — YOLO Real Positive Sample Smoke v0

**Runner**：`tools/evaluation/vision/run_yolo_real_positive_sample_smoke_v0.py`  
**Verifier**：`tools/evaluation/vision/verify_yolo_real_positive_sample_smoke_v0.py`

## 命令

```bash
export LUNA_YOLO_MODEL_PATH=/Users/luanlei/LunaRuntime/archive/misc_20260319_105843/yolo11n.pt

python3 tools/evaluation/vision/run_yolo_real_positive_sample_smoke_v0.py \
  --roi-proposal-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/vision_roi_proposal_stub_smoke_v0 \
  --prior-yolo-real-smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/yolo_real_smoke_v0 \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/yolo_real_positive_sample_smoke_v0

python3 tools/evaluation/vision/verify_yolo_real_positive_sample_smoke_v0.py \
  --smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/yolo_real_positive_sample_smoke_v0
```

GO / NO_GO：[LUNA_EVALUATION_VISION_YOLO_REAL_POSITIVE_SAMPLE_SMOKE_GO_NO_GO_PACK_V0.md](./LUNA_EVALUATION_VISION_YOLO_REAL_POSITIVE_SAMPLE_SMOKE_GO_NO_GO_PACK_V0.md)
