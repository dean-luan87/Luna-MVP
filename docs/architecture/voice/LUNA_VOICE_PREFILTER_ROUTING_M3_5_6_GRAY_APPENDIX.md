# LUNA Voice Prefilter Routing M3.5.6 Gray Appendix（显式开关扩灰：再抬一档样本量）

## 本轮相对 M3.5.5 的增量（不重复前置附录）

- **前提**：M3.5.5 已在约 1000 条总样本（`m3_5_3` case 集 × 每时段 20 轮 × day/night）下硬指标全绿；本轮 **只再抬一档轮数**，不扩 case 类型、不改骨架与规则。
- **脚本**：`tools/benchmark_prefilter_routing_m3_5_6.py`
- **JSON schema**：`luna.voice.gray_m3_5_6.v1`
- **默认轮数**：每时段 `--rounds 22`（可在 20～25 内按需指定；与 5.5 的差异仅此一档强度）
- **产物路径**：`logs/benchmark_prefilter_routing_m3_5_6_<UTC>.json`
- **case 集**：仍默认 `configs/voice/voice_prefilter_routing_real_cases_m3_5_3.json`

## 执行命令（与 5.5 一致的环境约束）

```bash
export LUNA_EXTERNAL_LLM_PROVIDER=qwen
export DASHSCOPE_API_KEY=...
export LUNA_VOICE_ENABLE_PREFILTER_ROUTING=1
export LUNA_QWEN_MODEL_TIMEOUT_MS=120000

python3 tools/benchmark_prefilter_routing_m3_5_6.py --rounds 22 --time-slot all
```

未显式设置 `LUNA_QWEN_MODEL_TIMEOUT_MS` 时，脚本进程内仍会兜底为 `120000`。未开 `LUNA_VOICE_ENABLE_PREFILTER_ROUTING` 时，产品主链行为不在此脚本覆盖范围内（本 benchmark 进程内会强制设为 `1`）。

## 本轮验收（从 `aggregate` 读取）

**硬门槛（须同时满足）**

- `json_rate_model_routes` = **1.0**
- `val_rate_model_routes` = **1.0**
- `fallback_rate_model_routes` = **0.0**
- `mixed_preserve_rate` **不得较 M3.5.5 退化**（5.5 为 1.0）

**扩灰闸门**

- `timeout_hint_count` 不得明显上升（5.5 为 0）
- `pause_stop_expand_gray` 须为 **false**
- `rule_or_reject_ratio` 不得相对 5.5 **异常偏高**（5.5 约 **0.24**；阈值逻辑同脚本 `--rule-reject-max-ratio`，默认 0.35）
- 关注 `complex_bucket_routed_turbo_count`、`selected_provider_model_id_counts`、`backup_provider_used_count` 是否与质量问题共现

## 结果填写区（跑批后更新）

| 字段 | aggregate 值 | 备注 |
|------|----------------|------|
| git_head / 产物文件名 | **待填** | |
| json_rate | **待填** | |
| val_rate | **待填** | |
| fallback_rate | **待填** | |
| mixed_preserve_rate | **待填** | |
| avg_e2e_ms / p95_e2e_ms | **待填** | |
| rule_or_reject_ratio | **待填** | |
| timeout_hint_count | **待填** | |
| pause_stop_expand_gray | **待填** | |
| mixed_failure_cases | **待填** | C1/C7 是否复发 |
| complex_bucket_routed_turbo_count | **待填** | |

### Day / Night 摘录

- day：**待填**
- night：**待填**

## 本轮结论（三选一，跑批后只保留一条）

1. **可继续扩大显式开关灰度范围**
2. **当前范围可维持，但不建议继续扩大**
3. **灰度扩展出现风险，应暂停推进**

**当前结论**：**待跑批**（执行上述脚本并填入「结果填写区」后，从以上三选一择一）。

## 一句话收束

继续推进显式开关扩灰，但不改骨架、不改规则、不改默认行为；是否进入「长期可保留灰度能力」须以 M3.5.6 全量 JSON 产物为准。
