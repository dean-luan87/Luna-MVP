# LUNA — RapidOCR Raw Text Candidate Evaluation v0

## Phase

- **Phase-ModelOCR-004C**
- **Goal:** 评估 **RapidOCR + ONNXRuntime** 作为**轻量本地** OCR 候选，统一输出 **raw text candidates**；不替代主架构、不接下游。

## Preconditions

- **004A** macOS Vision：已完成；**~460 ms/帧**（100 帧 ~46s），**非实时主力**，仅 fallback/基线。
- **PaddleOCR：** det+rec **pinned_partial**；**004B** 负责依赖就绪。
- 本阶段：**候选验证**，不进入 **004B / 005** 实现。

## Boundaries（硬）

- 仅 **raw text candidates**；无语义、无导航、无 SceneTask/Fusion/Output。
- `semantic_interpretation_enabled=false`，`allows_execute_now=false`，`real_tts_invoked=false`，无下游。
- 不改 `evidence_type`；不关 `pending_real_sidewalk_run`（本工具不涉及）。

## Implementation

| 组件 | 路径 |
|------|------|
| Adapter | `capabilities/model_ocr/rapidocr_adapter_v0.py` |
| Evaluate | `tools/evaluate_rapidocr_raw_text_v0.py` |
| Verify | `tools/verify_rapidocr_raw_text_v0.py` |

**CLI 示例：**

```bash
python3 tools/evaluate_rapidocr_raw_text_v0.py \
  --video-path /Users/luanlei/Desktop/Luna-Core/test_video_complex_6m42s.mp4 \
  --output-root logs/rapidocr_raw_text_004c_<timestamp> \
  --frame-step 30 \
  --max-sampled-frames 100
```

**依赖：** `pip install rapidocr-onnxruntime onnxruntime`（记录版本与模型路径见 summary `dependency_probe`）。

## Per-sample envelope

见仓库 adapter：`provider_id`=`rapidocr_onnxruntime_v0`，`ocr_runtime_mode`=`local_onnxruntime_offline`，含 `latency_ms`、`bbox_status`/`confidence_status`、`raw_text_joined_strategy`。

## Summary metrics

见 `ocr_raw_text_summary.json`：`total_runtime_seconds`、`avg/p50/p95 latency`、`model_asset_status`、`reproducibility_risk`。

## Cross-references

- Test matrix：`LUNA_RAPIDOCR_RAW_TEXT_TEST_MATRIX_V0.md`
- vs Vision：`LUNA_RAPIDOCR_VS_MACOS_VISION_PERFORMANCE_NOTE_V0.md`
- Go/No-Go：`LUNA_RAPIDOCR_RAW_TEXT_GO_NO_GO_PACK_V0.md`
