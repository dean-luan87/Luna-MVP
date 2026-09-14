# LUNA — RapidOCR Raw Text Test Matrix v0

## Phase

- **Phase-ModelOCR-004C**
- **Verifier:** `tools/verify_rapidocr_raw_text_v0.py`

| ID | 检查 | 期望 |
|----|------|------|
| **A** | `rapidocr_onnxruntime` 可 import | `A_rapidocr_import.ok=true` |
| **B** | 产物 + 输入 | summary/per_sample 存在；`input.missing_input_samples` 不得为真 |
| **C** | schema | 全样本合法；部分失败 → soft + CONDITIONAL_GO |
| **D** | bbox 声明 | 同 004A 规则 |
| **E** | confidence 声明 | 同 004A 规则 |
| **F** | `raw_text_joined` | 字段存在 |
| **G** | `allows_execute_now` | 恒 false |
| **H** | `semantic_interpretation_enabled` | 恒 false |
| **I** | `real_tts_invoked` | 恒 false |
| **J** | 下游 | `downstream_invoked=false`，`downstream_invocation_count` 为 0 |
| **K** | trace/replay/whitebox | 存在且非空 |
| **L** | 性能指标 | summary.metrics 含 total_runtime、avg/p50/p95 latency |
| **M** | 模型资产 | `model_asset_status` / `reproducibility_risk` 已记录；`auto_downloaded` → soft |
| **N** | vs macOS Vision | **avg_latency_ms_per_frame < 460**（004A 基线）；否则 NO_GO（性能维度） |
