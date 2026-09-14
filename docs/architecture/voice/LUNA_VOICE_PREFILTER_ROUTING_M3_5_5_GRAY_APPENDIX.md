# LUNA Voice Prefilter Routing M3.5.5 Gray Appendix（显式开关扩灰主线恢复）

## 背景与目标

前提：M3.5.4b 已完成 mixed 单点修复，灰度链恢复全绿。

本轮目标：回到 **显式开关扩灰主线**，在不改骨架/规则/默认行为的约束下，仅通过提升灰度强度（轮数/窗口）验证修复后整体稳定性。

## 本轮不做（冻结项）

- 不改 prefilter_v0
- 不改 mixed 修复逻辑
- 不改 prompt
- 不改 schema / validator / builder
- 不改 fallback 语义
- 不切 qwen3.6-plus
- 不接 DeepSeek / 豆包
- 不默认开启分档
- 不新增功能字段/分支

## 执行范围（Run Scope）

- **开关**：`LUNA_VOICE_ENABLE_PREFILTER_ROUTING=1`（显式开关；非产品默认）
- **超时**：`LUNA_QWEN_MODEL_TIMEOUT_MS=120000`（若外部未设置则脚本兜底）
- **样本集**：沿用当前收敛样本集（不新增新类型 case）
  - `configs/voice/voice_prefilter_routing_real_cases_m3_5_3.json`
- **轮数**：每时段 `--rounds 20`（建议默认）
- **时段**：`--time-slot all`（顺序跑 `day`、`night`）
- **脚本**：`tools/benchmark_prefilter_routing_m3_5_5.py`
- **产物**：`logs/benchmark_prefilter_routing_m3_5_5_<UTC>.json`

## 必须输出指标（从 JSON 产物读取）

### 硬指标（Hard）

- `json_rate_model_routes`
- `val_rate_model_routes`
- `fallback_rate_model_routes`
- `mixed_preserve_rate`

### 运营指标（Ops）

- `avg_e2e_ms`
- `p95_e2e_ms`
- `route_counts`
- `rule_or_reject_ratio`
- `timeout_hint_count`
- `pause_stop_expand_gray`

### 观察项（Observation）

- `complex_bucket_routed_turbo_count`
- `selected_provider_model_id_counts`
- `backup_provider_used_count`
- `routing_observation.mixed_failure_cases`
- `routing_observation.mixed_failure_case_counts`
- `routing_observation.mixed_failure_by_time_slot_case_counts`
- `routing_observation.mixed_failure_by_selected_provider_model_id_counts`

## 重点问题（本轮只盯 5 项）

1. **mixed 是否继续稳定**
   - 重点 case：`C7_mixed_sleep_park_nav`、`C1_mixed_nav`
   - 关注：`mixed_preserve_rate` 与 `mixed_failure_*` 分布是否为 0（或是否出现稳定复现掉档）
2. **rule_or_reject_ratio 是否稳定**
3. **p95 是否明显劣化**
4. **complex→turbo 是否开始引发质量问题**
   - 关注：是否伴随 `val_rate` 下滑 / `fallback` 上升 / mixed 复发
5. **timeout 是否仍为 0**
   - 关注：`timeout_hint_count`

## 结果填写区（执行后补齐）

### Aggregate 汇总

- json_rate: **1.0**
- val_rate: **1.0**
- fallback_rate: **0.0**
- mixed_preserve_rate: **1.0**
- avg_ms / p95_ms: **3645.46ms / 7923.63ms**
- route_counts: `turbo=600` / `plus=160` / `rule_or_reject=240`
- rule_or_reject_ratio: **0.24**
- timeout_hint_count: **0**
- pause_stop_expand_gray: **False**

### Day / Night 对比

- day:
  - mixed_preserve_rate: **1.0**
  - rule_or_reject_ratio: **0.24**
  - p95_ms: **8000.64ms**
  - pause_stop_expand_gray: **False**
- night:
  - mixed_preserve_rate: **1.0**
  - rule_or_reject_ratio: **0.24**
  - p95_ms: **7799.03ms**
  - pause_stop_expand_gray: **False**

### Mixed 复发检查（必须写）

- mixed_failure_cases（aggregate）: **[]（0）**
- mixed_failure_by_time_slot_case_counts（重点看 C1/C7）: **{}（无复发）**
- mixed_failure_by_selected_provider_model_id_counts: **{}**

## 一句话结论（三选一）

1. **可继续扩大显式开关灰度范围**
2. 当前范围可维持，但不建议继续扩大
3. 灰度扩展出现风险，应暂停推进

