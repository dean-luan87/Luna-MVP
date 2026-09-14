# sidewalk_env_summary_v1 主线接入（V1）说明

## 接了什么

在 `dispatch_voice_final_text(...)` 入口、分流与旁路编排之前，对 `VoiceRuntimeContext.metadata["sidewalk_env_summary_v1"]` 做一次**稳定化**：

- 若值为 `dict` 且**尚未**带 `summary_schema_version` 前缀 `sidewalk_env_summary_v1/`：调用 `build_sidewalk_env_summary_v1(...)`，用 `replace(...)` 写回 **新的** `VoiceRuntimeContext`（frozen dataclass）。
- 若已带上述 schema：视为已稳定化，**不重复 build**。
- 若 key 不存在或非 dict：不改动 context。

`sidewalk_nav_v1` 深接入仍只读 `sidewalk_env_summary_v1` 中的 `scene_candidate` / `path_confidence` / `is_outdoor` 映射到 `SidewalkEnvironmentInput`；额外字段（`summary_freshness`、`confidence_weight` 等）保留在 metadata 供观测与未来扩展。

## 写入路径在哪

- `capabilities/voice/runtime/voice_final_text_dispatcher.py`
  - `_sidewalk_env_summary_stabilizer_enabled_v1()`
  - `_maybe_stabilize_runtime_context_sidewalk_env_v1(...)`
  - `dispatch_voice_final_text` 开头在 `classify_voice_input_length_mode` 之前调用

## 回退开关

- `LUNA_ENABLE_SIDEWALK_ENV_SUMMARY_STABILIZER_V1`：默认等价开启；设为 `0` / `false` / `no` 则跳过稳定化，行为与接入前一致（原始三字段 dict 直透）。

## 与 risk 的关系

- 稳定化**只改写** `sidewalk_env_summary_v1` 键；**不读、不改** `risk_summary_v1`。
- orchestrator 顺序与 risk 压制逻辑未改。

## 怎么验证

```bash
python3 tools/test_sidewalk_env_summary_v1_integration.py
python3 tools/test_sidewalk_nav_v1_deep_integration.py
```

## 哪些还没做

- 未要求上游生产链必须写 `event_timestamp`（缺失时用 `event.timestamp`）。
- `sidewalk_nav_v1/evaluate.py` 尚未消费 `summary_freshness` 调整分类（仅 metadata 携带）。
- `retail_env_summary_v1` 同类稳定化未做。

## 一句话收束

稳定化 summary 已在**主线分流前**注入 `runtime_context`，`sidewalk_nav_v1` 继续消费同一 key；需要秒退时关 `LUNA_ENABLE_SIDEWALK_ENV_SUMMARY_STABILIZER_V1`。
