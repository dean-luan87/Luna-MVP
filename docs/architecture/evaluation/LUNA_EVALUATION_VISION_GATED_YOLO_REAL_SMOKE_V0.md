# Luna Evaluation — Gated YOLO Real Smoke v0

**Runner**：`tools/evaluation/vision/run_yolo_real_smoke_v0.py`  
**Verifier**：`tools/evaluation/vision/verify_yolo_real_smoke_v0.py`

## 命令

```bash
export LUNA_YOLO_MODEL_PATH=/path/to/local/yolov8n.pt   # 可选；须本地存在

python3 tools/evaluation/vision/run_yolo_real_smoke_v0.py \
  --roi-proposal-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/vision_roi_proposal_stub_smoke_v0 \
  --yolo-candidate-adapter-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/yolo_candidate_adapter_eval_smoke_v0 \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/yolo_real_smoke_v0

python3 tools/evaluation/vision/verify_yolo_real_smoke_v0.py \
  --smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/yolo_real_smoke_v0
```

GO / NO_GO：[LUNA_EVALUATION_VISION_GATED_YOLO_REAL_SMOKE_GO_NO_GO_PACK_V0.md](./LUNA_EVALUATION_VISION_GATED_YOLO_REAL_SMOKE_GO_NO_GO_PACK_V0.md)
