# M3.5：长语音 prefilter 分档路由（显式开关骨架）

## 目标

在**不改变当前默认主链行为**的前提下，把已通过离线评估的 `prefilter_v0` 接入运行时入口，形成：

- 前置裁剪层（最小版）
- 分档路由（simple → turbo / complex → plus / rule_or_reject）
- 显式开关灰度、可观测、可回退

## 总原则（写死）

- 默认主链不改（不开开关时行为与历史一致）
- 所有新能力必须显式开关控制
- 不改 schema / validator / builder / fallback 定义
- 不引入复杂打分器；prefilter 仍保持「薄规则层」

## 开关

- **环境变量**：`LUNA_VOICE_ENABLE_PREFILTER_ROUTING=1`

### 关闭（默认）

- `voice_final_text_dispatcher` 不消费 prefilter 输出
- Provider 选择仍按既有逻辑（例如 `LUNA_QWEN_USE_PRIMARY_BACKUP=1` 时使用主备 bundle，否则走默认规则链配置）

### 开启

1. 运行 `prefilter_long_voice_text_v0(raw_text)` 得到：
   - `cleaned_text`
   - 风险标签（mixed/unsupported/clarification/multi_step）
   - `routing_suggestion`
2. 仅根据 `routing_suggestion` 选择：
   - `route_to_turbo` → 单模型 `qwen-turbo`
   - `route_to_plus` → 单模型 `qwen-plus`
   - `route_to_rule_or_reject` → `parse_mode=rule_only`
3. 进入原有模型链/规则链；validator/builder/fallback 语义不变

## Pre-Filter Layer（最小前置裁剪）

### 本轮只做

- **去冗余（极保守）**：仅剔除明显无意义的口头禅/停顿词（前缀 + 逗号夹心），不做语义重写
- **输出 cleaned_text**：供长链解析消费
- **输出风险标签**：mixed/unsupported/clarification/multi_step

### 本轮明确不做

- 不做摘要/重排/语义改写
- 不做上下文/记忆注入
- 不做权重打分器
- 不做 turbo/plus 并行跑

## 观测字段（长链 metadata）

灰度必须留痕：

- `prefilter_routing_enabled`
- `prefilter_routing_suggestion`
- `prefilter_cleaned_text_len`
- `selected_provider_model_id`
- `backup_provider_used`
- `provider_switch_reason`
- `prefilter_notes`

## 抽测脚本

- `tools/smoke_prefilter_routing_m3_5.py`
  - 支持在进程内设置开关（`--enable-prefilter-routing`）
  - 输出：`json_rate / val_rate / fallback_rate / mixed_preserve_rate / avg_ms / p95_ms / route_counts`

## M3.5.1 小范围灰度（固定口径）

- **运行脚本**：`tools/run_prefilter_routing_gray_m3_5_1.py`  
  - 固定开启 `LUNA_VOICE_ENABLE_PREFILTER_ROUTING=1`（仅本进程）  
  - **结果落盘** JSON（含硬指标、运营指标、`pause_checks`、可选 review 项）  
- **附录模板**：`docs/architecture/voice/LUNA_VOICE_PREFILTER_ROUTING_M3_5_1_GRAY_APPENDIX.md`

## 验收标准（灰度口径）

- 结构稳定性不得退化：`json_rate=1.0`、`val_rate=1.0`、`fallback_rate=0.0`
- mixed 不得明显掉档：`mixed_preserve_rate` 下降需记录并暂停推进
- 性能：simple 进 turbo 后 `avg/p95` 有可见改善；若无改善或稳定性退化，仅保留骨架不推进灰度

