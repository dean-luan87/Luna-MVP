# LUNA Evaluation — PaddleOCR Provider Adapter Contract v0（设计-only）

## 未来 `PaddleOCRProviderAdapter` 输出（推理结果载体）

本阶段 **不实现** adapter，仅冻结 JSON 形状，供后续 **授权 trial** 与 harness 对齐。

```json
{
  "provider_id": "paddleocr_ppocrv5_v0",
  "raw_text": "",
  "candidates": [],
  "bbox": [],
  "confidence": 0.0,
  "language": "zh | en | mixed | unknown",
  "latency_ms": 0,
  "network_request_invoked": false,
  "model_invoked": true,
  "runtime_default_enabled": false
}
```

## 约束

- `network_request_invoked`：离线 trial 期望为 **false**（与 `paddleocr_evaluation_readiness_manifest_v0.json` 一致）。  
- `runtime_default_enabled`：**false**（不得暗示主线默认）。  
- 与 RapidOCR harness 使用 **同一套评测输入**（见 A/B 计划文档）。
