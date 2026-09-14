# CrossModal Vision-OCR TestBoard v1 Track Closures v0

**Phase**：`Phase-CrossModal-Vision-OCR-TestBoard-v1-Track-Closures-001`  
**定位**：对 v1 三条 track（A RealVideo / B Poster / C Metrics）做 **只读 evaluation closure 聚合**；不运行 OCR、不提交 OCRRequest、不写事实层、不生成 benchmark、不改 routing。

**v1 正式状态**：`closed_for_evaluation`（**不是** production ready / benchmark / write-ready）。

| Track | Closure 状态 |
|-------|----------------|
| A RealVideo | `closed_for_reference_evaluation` |
| B Poster | `closed_for_evaluation` |
| C Metrics | `closed_for_smoke_metrics` |

**能力**：`capabilities/midplatform/cross_modal_vision_ocr_testboard_v1_track_closures_v0.py`  
**Runner**：`tools/evaluation/midplatform/run_cross_modal_vision_ocr_testboard_v1_track_closures_v0.py`  
**Verifier**：`tools/evaluation/midplatform/verify_cross_modal_vision_ocr_testboard_v1_track_closures_v0.py`

**输出根目录（示例）**：`_eval_out/cross_modal_vision_ocr_testboard_v1_track_closures_v0/`

**Benchmark real values planning** 已完成（见 [Benchmark Real Values Planning v0](./LUNA_CROSS_MODAL_VISION_OCR_BENCHMARK_REAL_VALUES_PLANNING_V0.md)）。

**建议下一 phase（优先顺序）**：

1. **PublicFacility runtime dry-run**  
2. Benchmark Collector Real Values Smoke（显式 phase）  
3. RealVideo OCRRequest gated submission  
4. Poster real OCR gated execution  
