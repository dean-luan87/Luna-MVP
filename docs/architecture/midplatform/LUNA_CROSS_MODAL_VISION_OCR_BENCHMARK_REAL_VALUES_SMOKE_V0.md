# CrossModal Vision-OCR Benchmark Collector Real Values Smoke v0

**Phase**：`Phase-CrossModal-Vision-OCR-TestBoard-Benchmark-Collector-Real-Values-Smoke-001`  
**定位**：在 Benchmark Real Values Planning 门控下，**只读**采集允许的 **T0/T1** 指标值；T2 质量/性能保持 `not_collected`。**不是 benchmark**。

**能力**：`capabilities/midplatform/cross_modal_vision_ocr_benchmark_real_values_smoke_v0.py`  
**Runner**：`tools/evaluation/midplatform/run_cross_modal_vision_ocr_benchmark_real_values_smoke_v0.py`  
**Verifier**：`tools/evaluation/midplatform/verify_cross_modal_vision_ocr_benchmark_real_values_smoke_v0.py`

**硬边界**：`no_write_boundary_pass_rate=1.0`；不运行 OCR/Vision；不比较 provider；无 `benchmark_score`。

**Simulation Lab crash_recovery × PaddleOCR 合同/merge** 已完成（见 evaluation 文档）；T2 稳定性指标仍 **future**。

**建议下一 phase（优先级）**：

1. PaddleOCR BatchRecovery Manual Execution（实跑 child 后 re-merge）  
2. Poster real OCR gated execution  
3. RealVideo OCRRequest gated submission  
