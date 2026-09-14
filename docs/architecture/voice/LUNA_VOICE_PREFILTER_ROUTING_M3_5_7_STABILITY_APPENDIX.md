# LUNA Voice Prefilter Routing M3.5.7 Stability Appendix（当前灰度范围稳定性观察）

## 目标

在 **不扩大灰度范围、不修改任何业务逻辑** 的前提下，对当前显式开关灰度做一轮 **更长观察窗口** 的稳定性验证，确认 M3.5.6 类 **低频非绿**（model routes 上 `used_model_chain=false` / day 段非绿等）是否再次出现。

## 原则（冻结项）

1. 不扩灰  
2. 不改 prefilter  
3. 不改 prompt  
4. 不改 schema  
5. 不改 validator  
6. 不改 builder  
7. 不改 fallback  
8. 不改 `used_model_chain` / success tagging  
9. 不切 qwen3.6-plus  
10. 不接 DeepSeek / 豆包  

## 固定配置

- `LUNA_VOICE_ENABLE_PREFILTER_ROUTING=1`（显式开关；非产品默认）  
- `LUNA_QWEN_MODEL_TIMEOUT_MS=120000`（若外部未设则脚本进程内兜底）

可选（默认不要求开启；仅在再次出现非绿或定点排障时启用）：

- `LUNA_VOICE_ENABLE_MODEL_CHAIN_AUDIT_DEBUG=1`  
- 或运行脚本时加：`--enable-model-chain-audit-debug`

## 范围

1. 使用当前样本集，**不新增**新类型 case（默认 `configs/voice/voice_prefilter_routing_real_cases_m3_5_3.json`）。  
2. **维持**当前灰度范围，不扩大强度。  
3. 观察窗口建议（可拆多批跑）：  
   - `day` / `night` 双时段  
   - 每时段 **10～15 轮**（脚本默认 **12**）  
4. 重点不是追更大总样本量，而是 **是否再次出现与 M3.5.6 同型非绿**。

## 脚本

- `tools/benchmark_prefilter_routing_m3_5_7.py`

示例：

```bash
export LUNA_EXTERNAL_LLM_PROVIDER=qwen
export DASHSCOPE_API_KEY=...
export LUNA_VOICE_ENABLE_PREFILTER_ROUTING=1
export LUNA_QWEN_MODEL_TIMEOUT_MS=120000

python3 tools/benchmark_prefilter_routing_m3_5_7.py --rounds 12 --time-slot all
```

产物：

- `logs/benchmark_prefilter_routing_m3_5_7_<UTC>.json`  
- `schema`: `luna.voice.gray_m3_5_7.v1`

### 聚合中的 M3.5.7 稳定性字段

在 `aggregate.routing_observation.m3_5_7_stability`（各 `per_time_slot` 块内亦有）：

- `used_model_chain_false_model_route_count`：turbo/plus 上 `used_model_chain=false` 的次数  
- `used_model_chain_false_by_time_slot`：按时段分布  
- `used_model_chain_false_case_ids`：涉及的 case id  
- `model_route_non_green_count`：turbo/plus 上非绿（`used_model_chain=false` 或 `fallback=true`）  
- `day_model_route_non_green_count` / `night_model_route_non_green_count`  
- `c1_mixed_nav_mixed_preserve_failures` / `c7_mixed_sleep_park_nav_mixed_preserve_failures`：mixed 关键词保留失败计数  

## 重点指标（从 JSON 读取）

### 硬指标

- `json_rate_model_routes`  
- `val_rate_model_routes`  
- `fallback_rate_model_routes`  
- `mixed_preserve_rate`  

### 运营指标

- `avg_e2e_ms` / `p95_e2e_ms`  
- `rule_or_reject_ratio`  
- `timeout_hint_count`  
- `pause_stop_expand_gray`  

### 观察项

- `m3_5_7_stability`（见上）  
- `mixed_failure_*`、C1/C7  

## 判断标准

- **若本轮继续全绿**（硬指标满足既有门槛，且未再出现 M3.5.6 同型非绿）：可判定当前灰度范围 **稳定可维持**；后续再决定是否重启扩灰。  
- **若再次出现同型问题**：立即记录产物；启用 `LUNA_VOICE_ENABLE_MODEL_CHAIN_AUDIT_DEBUG` 与 M3.5.6b repro/审计链做 **定点归因**；**不扩大灰度**。  

## 结论（三选一，跑批后填写）

1. **当前灰度范围稳定，可继续维持**  
2. **当前灰度范围可维持，但需继续观察**  
3. **当前灰度范围出现复发风险，需回到专项归因**  

## 结果填写区（执行后更新）

- 产物路径：  
- aggregate 硬指标摘要：  
- `pause_stop_expand_gray`：  
- `m3_5_7_stability` 摘要：  
- 本轮结论（三选一）：  

## 一句话收束

本轮只做「维持范围下的稳定性观察」，不扩灰、不修逻辑；跑完再决定后续是维持、择机扩灰，还是把审计链长期驻场。
