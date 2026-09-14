# Poster TestBoard Track B Closure v0

**Phase**：`Phase-Poster-TestBoard-Closure-001`  
**Track**：`TVOCR_V1_B_POSTER_LAYOUT`  
**定位**：对 Poster Track B 四阶段做 **closure-only 聚合**（phase matrix、lineage、track separation、no-write boundary、capability closure、non-claims、open follow-ups）。**不新增能力**。

## 聚合范围（4 phases）

1. `OCR-Poster-Layout-Segmentation-Governance-001`
2. `OCR-Poster-Region-OCR-Plan-Stub-001`
3. `OCR-Poster-VisualSymbolEvidence-Stub-001`
4. `CrossModal-Poster-OCR-ReferenceOnly-001`

## 必须确认（closure 不变量）

- `poster_like`：`full_image_ocr_allowed=false`；`ocr_strategy=segment_first`
- text / visual 分流；text → OCR plan stub；visual → VisualSymbolEvidence stub
- reference-only 并列索引；`overlap_count=0`；无轨道污染
- 全程 `not_fact` / `no_write`；未运行 OCR / QR / brand / visual symbol registry / fusion / semantic join
- `runtime_routing_changed=false`

## 严禁

运行 OCR；QR decode；品牌确认；视觉符号库；fusion；semantic join；写事实层；伪称真实海报 OCR 或 benchmark；改 routing。

## 实现

- Capability：`capabilities/midplatform/poster_testboard_track_b_closure_v0.py`
- Runner：`tools/evaluation/midplatform/run_poster_testboard_track_b_closure_v0.py`
- Verifier：`tools/evaluation/midplatform/verify_poster_testboard_track_b_closure_v0.py`

## 后续

**Phase-Poster-Real-OCR-Gated-Execution-001**（4 text regions gated real OCR）见 [LUNA_POSTER_REAL_OCR_GATED_EXECUTION_V0.md](../ocr/LUNA_POSTER_REAL_OCR_GATED_EXECUTION_V0.md)。

RealVideo 帧采样 smoke 见 [LUNA_CROSS_MODAL_VISION_OCR_REALVIDEO_FRAME_SAMPLE_SMOKE_V0.md](./LUNA_CROSS_MODAL_VISION_OCR_REALVIDEO_FRAME_SAMPLE_SMOKE_V0.md)。
