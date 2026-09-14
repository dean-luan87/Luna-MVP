# LUNA Voice 长语音主线：默认运行基线（V1）

## 目标

回答一个执行面问题：

> **如果今天把 Voice 长语音能力交给别人接手，默认态应该怎么跑？**

本文件只定义“默认运行基线”（Default Baseline），用于后续：

- 模型替换评审（如 qwen3.6-plus）
- 新模型接入（DeepSeek / 豆包）
- 灰度启停、回退、审计启用

**不改变任何逻辑**，只把默认值与边界写清楚。

## 默认运行基线（一句话）

**默认态：不开 prefilter 分档（`LUNA_VOICE_ENABLE_PREFILTER_ROUTING=0`），长语音解析默认走规则链（rule_only）；如需启用模型链的“主线默认运行”，应通过 `LUNA_QWEN_USE_PRIMARY_BACKUP=1` 显式开启主备 bundle。**

> 说明：当前 `voice_long_input_parse_config` 的默认配置为 `rule_only`，且 `enable_model_adapter=false`，因此在未显式提供 provider 的情况下不会尝试模型链。

## 默认配置（推荐）

### 1) 默认不启用的能力（保持关闭）

- `LUNA_VOICE_ENABLE_PREFILTER_ROUTING`：默认 **0**
  - 仅灰度态/跑批/回归对照时显式开启
- `LUNA_VOICE_ENABLE_MODEL_CHAIN_AUDIT_DEBUG`：默认 **0**
  - 仅复发时启用（应急审计）

### 2) 默认主线是否启用主备（建议显式选择其一）

默认态（不开 prefilter）下，建议明确选择：

- **主线默认（推荐启用模型链时）**：`LUNA_QWEN_USE_PRIMARY_BACKUP=1`
  - 作用：启用 qwen 主备 bundle（primary→backup 的 provider 级重试）
- 若不启用：`LUNA_QWEN_USE_PRIMARY_BACKUP=0`
  - 结果：在当前默认 parse_config 下（rule_only），长语音解析将保持规则链口径为主

> 注意：当 `LUNA_VOICE_ENABLE_PREFILTER_ROUTING=1` 时，当前实现走单模型 provider（plus/turbo 二选一），不走主备 bundle；因此不要把主备开关当成“灰度态必然生效”的能力。

### 3) 默认 timeout（运行参数）

- `LUNA_QWEN_MODEL_TIMEOUT_MS`
  - 默认由 `get_default_voice_long_input_parse_config()` 的 `model_timeout_ms` 提供（当前为 **2000ms**，见 `capabilities/voice/config/voice_long_input_parse_config.yaml`）
  - 灰度/跑批口径通常会显式覆盖（例如 120000ms），但这不是默认态必选项

## 默认 parse_mode 与回退路径（代码口径）

### 1) 默认 parse_mode

来自 `capabilities/voice/config/voice_long_input_parse_config.yaml`：

- `parse_mode: rule_only`
- `enable_model_adapter: false`

因此默认基线是：**规则链优先/唯一**。

### 2) 默认回退

当配置为 `model_preferred_with_rule_fallback` 且 provider 可用时：

- provider 超时 / 异常 / validation 不通过 / provider 返回 None → **回退规则链**（由 `fallback_to_rule_on_timeout` / `fallback_to_rule_on_validation_error` 控制，默认均为 true）

## 默认主模型是谁（口径说明）

在 **prefilter 灰度态** 中：

- `route_to_plus` → `qwen-plus`
- `route_to_turbo` → `qwen-turbo`

在 **默认态（不开 prefilter）** 中：

- 是否使用 `qwen-plus` 作为复杂档主选，取决于是否开启 **主备 bundle**（`LUNA_QWEN_USE_PRIMARY_BACKUP=1`），以及 provider 是否配置就绪（API key 等）。

## 默认监控建议（最小集合）

默认态建议至少关注：

- 规则链：拒答/澄清比例的稳定性（结合上层业务指标）
- 模型链（若启用主备）：成功率/超时/回退率（后续接入统一看板时可与 M3.5 指标对齐）

灰度态（prefilter）才建议采用 M3.5 的全套硬指标口径：

- `json_rate_model_routes` / `val_rate_model_routes` / `fallback_rate_model_routes`
- `mixed_preserve_rate`
- `avg_e2e_ms` / `p95_e2e_ms`
- `rule_or_reject_ratio`
- `timeout_hint_count`
- `pause_stop_expand_gray`

## 哪些能力只在灰度/审计时可开

- prefilter 分档：`LUNA_VOICE_ENABLE_PREFILTER_ROUTING=1`（显式灰度能力，默认不启用）
- 最小审计：`LUNA_VOICE_ENABLE_MODEL_CHAIN_AUDIT_DEBUG=1`（应急定位能力，默认不启用）

## 关联文档

- 运行态与开关总表：`docs/architecture/voice/LUNA_VOICE_RUNTIME_MODES_AND_SWITCHES_V1.md`
- 新模型接入 SOP：`docs/architecture/voice/LUNA_VOICE_MODEL_ONBOARDING_FLOW_V1.md`
- M3.5 封板：`docs/architecture/voice/LUNA_VOICE_PREFILTER_ROUTING_M3_5_PHASE_CLOSEOUT.md`
- 默认态配置清单：`docs/architecture/voice/LUNA_VOICE_RUNTIME_DEFAULT_CONFIG_V1.md`
- 默认态回退 SOP：`docs/architecture/voice/LUNA_VOICE_RUNTIME_ROLLBACK_SOP_V1.md`
- 默认态一键回归脚本：`tools/runtime_default_regression_v1.py`

