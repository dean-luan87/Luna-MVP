# Luna — Mixed Video Poster Batch Smoke v2 (Gated Path Only)

**Phase**：`Phase-Mixed-Video-Poster-Batch-Smoke-v2-Gated-Path-Only-001`

## 目的

将 v1 mixed batch 的 **直连 RapidOCR** 替换为 **中台前置门控路径**；所有 provider 调用必须经 `OCRRequest` + `ocr_mainline_bridge`，Evidence Pack 绑定 `ocr_request_ref`。

## 禁止

- capability 内 `import RapidOCR` / `RapidOCR()`
- OpenCV/读图 → 直接 provider → pack
- 全帧 scan 作为主 Evidence Pack

## 路径

```
InputCandidate → SQ Gate → Readability Gate → ROI/scan/visual/public_facility routing
→ OCRRequest → ocr_mainline_bridge → OCRTextEvidencePack → OCRSemanticCandidate
```

## 实现

- `capabilities/midplatform/mixed_video_poster_batch_smoke_v2_gated_path_only_v0.py`
- `tools/evaluation/midplatform/run_mixed_video_poster_batch_smoke_v2_gated_path_only_v0.py`
- `tools/evaluation/midplatform/verify_mixed_video_poster_batch_smoke_v2_gated_path_only_v0.py`

## 前置

- v1 mixed batch smoke（scan/plan/图片 bbox 参考）
- linebox + SQ gate smoke
- OCR MidPlatform gated runtime path alignment（路径证明）

## 后续

**Evidence Pack Adapter v1**（见 [LUNA_OCR_EVIDENCE_PACK_ADAPTER_V1_SCAN_OBSERVATION_ALIGNMENT_V0.md](./LUNA_OCR_EVIDENCE_PACK_ADAPTER_V1_SCAN_OBSERVATION_ALIGNMENT_V0.md)）将 v2 产物升级为 `ocr_text_evidence_pack_v1`。

## 评测

[LUNA_EVALUATION_MIXED_VIDEO_POSTER_BATCH_SMOKE_V2_GATED_PATH_ONLY_V0.md](../evaluation/LUNA_EVALUATION_MIXED_VIDEO_POSTER_BATCH_SMOKE_V2_GATED_PATH_ONLY_V0.md)
