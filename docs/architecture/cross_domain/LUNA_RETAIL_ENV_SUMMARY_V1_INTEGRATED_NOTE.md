# retail_env_summary_v1 主线接入（V1）说明

## 接了什么

在 `dispatch_voice_final_text(...)` 入口、分流与旁路编排之前，对 `VoiceRuntimeContext.metadata["retail_env_summary_v1"]` 做一次**稳定化**：

- 若值为 `dict` 且**尚未**带 `summary_schema_version` 前缀 `retail_env_summary_v1/`：调用 `build_retail_env_summary_v1(...)`，用 `replace(...)` 写回 **新的** `VoiceRuntimeContext`（frozen dataclass）。
- 若已带上述 schema：视为已稳定化，**不重复 build**。
- 若 key 不存在或非 dict：不改动 context。

`retail_find_item_v1` 深接入仍只读 `retail_env_summary_v1` 中的环境字段映射到 `RetailEnvironmentInput`；额外稳定化字段（`summary_freshness`、`confidence_weight` 等）保留在 metadata 供观测与未来扩展。

## 写入路径在哪

- `capabilities/voice/runtime/voice_final_text_dispatcher.py`
  - `_retail_env_summary_stabilizer_enabled_v1()`
  - `_maybe_stabilize_runtime_context_retail_env_v1(...)`
  - `dispatch_voice_final_text` 开头在 `classify_voice_input_length_mode` 之前调用

## 回退开关

- `LUNA_ENABLE_RETAIL_ENV_SUMMARY_STABILIZER_V1`：默认等价开启；设为 `0` / `false` / `no` 则跳过稳定化，行为与接入前一致（原始 dict 直透）。

## 与 intent / OCR / risk 的关系

- 稳定化**只改写** `retail_env_summary_v1` 键；**不读、不改**：
  - `find_item_intent_summary_v1`
  - `ocr_summary_v1`
  - `risk_summary_v1`
- orchestrator 顺序与 risk 压制逻辑未改。

## 怎么验证

```bash
python3 tools/test_retail_env_summary_v1_integration.py
python3 tools/test_retail_find_item_v1_deep_integration.py
```

## 哪些还没做

- `retail_find_item_v1/evaluate.py` 尚未消费 `summary_freshness` 做更严格的 gating（仅 metadata 携带）。
- 多级 TTL（货架 vs 门店）仍为单 TTL + env 覆盖。

## 一句话收束

稳定化 summary 已在**主线分流前**注入 `runtime_context`，`retail_find_item_v1` 继续消费同一 key；需要秒退时关 `LUNA_ENABLE_RETAIL_ENV_SUMMARY_STABILIZER_V1`。

