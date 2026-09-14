# LUNA Evaluation — PaddleOCR Adapter Contract v1（设计-only）

**Phase**：PaddleOCR-ManifestV1-Design-001  
**状态**：设计草案；**不**实现 adapter、**不**推理、**不**改 routing。

## 与 v0 的关系

- **v0**（`LUNA_EVALUATION_OCR_PADDLEOCR_ADAPTER_CONTRACT_V0.md`）：面向旧式 **det_model_dir / rec_model_dir / cls_model_dir** + **六文件 pdmodel/pdiparams** 规划。  
- **v1**：面向 **`paddleocr_current_api_model_manifest_v1`****：以 `PaddleOCR.__init__` 当前参数面为准**（如 `det_model_dir`、`use_angle_cls`、`lang` 等），**model_root / *_model_ref** 描述「离线缓存根 + 子引用」，**不**强制六文件命名；若仍使用 legacy 包，则通过 `model_format: paddle_inference_legacy` 与 `legacy_manifest_ref` 显式声明。

## v1 adapter 输出载体（形状冻结草案）

与 v0 保持同一评测对齐面（字段名可不变，语义扩展）：

```json
{
  "provider_id": "paddleocr_current_api_v1",
  "raw_text": "",
  "candidates": [],
  "bbox": [],
  "confidence": 0.0,
  "language": "zh | en | mixed | unknown",
  "latency_ms": 0,
  "network_request_invoked": false,
  "model_invoked": true,
  "runtime_default_enabled": false,
  "manifest_schema": "paddleocr_current_api_model_manifest_v1",
  "model_format": "paddleocr_current_api | paddle_inference_legacy"
}
```

## 约束（与 manifest v1 example 一致）

- `network_request_invoked`：evaluation 默认可复现为 **false**（与 `network_required: false` 对齐）。  
- `runtime_default_enabled`：**false**。  
- `mainline_provider`：**false**；RapidOCR 仍为轻量主线。

## 后续实现闸门

在 **ManifestV1-Design** verifier **GO** 且人工确认官方模型布局后，再开 **adapter 实现 / trial** phase；本文件不进入主线 runtime。
