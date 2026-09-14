# CrossModal Vision-OCR Benchmark Collector Real Values Planning v0

**Phase**：`Phase-CrossModal-Vision-OCR-TestBoard-Benchmark-Collector-Real-Values-Planning-001`  
**定位**：为后续 Benchmark / Metrics Collector **真实采值**建立 planning、指标分层（T0/T1/T2）、数据源映射、采集门控与 non-claims。**不是 benchmark**，不采集数值、不运行 OCR/Vision、不比较 provider。

**前置**：v1 Track Closures = `closed_for_evaluation`；Metrics Schema / Smoke Collector / Regression Comparison = GO。

**能力**：`capabilities/midplatform/cross_modal_vision_ocr_benchmark_real_values_planning_v0.py`  
**Runner**：`tools/evaluation/midplatform/run_cross_modal_vision_ocr_benchmark_real_values_planning_v0.py`  
**Verifier**：`tools/evaluation/midplatform/verify_cross_modal_vision_ocr_benchmark_real_values_planning_v0.py`

**PublicFacility Runtime DryRun** 已完成。**Real Values Smoke** 已完成（T0/T1 readonly）。建议下一 phase：Simulation Lab crash_recovery + PaddleOCR batch recovery。
