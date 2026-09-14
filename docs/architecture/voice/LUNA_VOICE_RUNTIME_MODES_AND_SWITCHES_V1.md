# LUNA Voice 长语音主线：运行态与开关总表（V1）

## 目标

在 M3.5 阶段封板后，将 Voice 长语音链路中已存在的 **运行态、开关、路由能力、主备能力、审计能力**整理成一份主线工程说明，作为后续接入新模型、灰度、回退的统一入口文档。

本文件只做梳理与收束：**不改逻辑、不扩灰、不引入新变量**。

## 关联入口（建议阅读顺序）

1. 默认运行基线（默认怎么跑）：`docs/architecture/voice/LUNA_VOICE_RUNTIME_DEFAULT_BASELINE_V1.md`
2. 新模型接入 SOP（新模型怎么进）：`docs/architecture/voice/LUNA_VOICE_MODEL_ONBOARDING_FLOW_V1.md`
3. M3.5 封板（阶段边界）：`docs/architecture/voice/LUNA_VOICE_PREFILTER_ROUTING_M3_5_PHASE_CLOSEOUT.md`
4. 未来预留模块占位（不实现）：`docs/architecture/voice/LUNA_VOICE_CONTEXT_REDUCTION_LAYER_PLACEHOLDER_V1.md`

## 适用范围

- 长语音主分流入口：`capabilities/voice/runtime/voice_final_text_dispatcher.py`
- prefilter 纯函数层：`capabilities/voice/bridge/voice_long_input_prefilter_v0.py`
- provider（qwen 外部）：`capabilities/voice/providers/qwen_external_long_input_model_provider.py`
- provider（主备 bundle）：`capabilities/voice/providers/qwen_long_voice_primary_backup_provider.py`

## 主线运行态（推荐用语）

本主线建议将运行态明确为以下 4 类（可组合，但需遵循“允许组合/不建议组合”约束）：

### 1) 默认态（Default）

- **定义**：不开启 prefilter 分档路由；按历史默认逻辑选择 provider/bundle/规则链路径。
- **关键开关**：
  - `LUNA_VOICE_ENABLE_PREFILTER_ROUTING=0`（默认）
  - `LUNA_QWEN_USE_PRIMARY_BACKUP`（可选，决定是否启用主备 bundle）

### 2) 灰度态（Prefilter Gray）

- **定义**：开启 prefilter 分档路由；按 `routing_suggestion` 在 long 链路做三路分流：
  - `route_to_turbo` → 单模型 `qwen-turbo`
  - `route_to_plus` → 单模型 `qwen-plus`
  - `route_to_rule_or_reject` → `rule_only`（不进模型链）
- **关键开关**：
  - `LUNA_VOICE_ENABLE_PREFILTER_ROUTING=1`
- **默认策略**：**显式开关、默认关闭**（M3.5 封板结论）

### 3) 主备态（Primary/Backup Bundle）

- **定义**：在未开启 prefilter 分档时，通过主备 bundle 提供 provider 级重试（primary→backup）。
- **关键开关**：
  - `LUNA_QWEN_USE_PRIMARY_BACKUP=1`
- **注意**：当 `LUNA_VOICE_ENABLE_PREFILTER_ROUTING=1` 时，当前实现走 **单模型 provider**（plus/turbo 二选一），不会走主备 bundle 的 primary→backup 逻辑（除非后续版本明确设计并实现）。

### 4) 审计态（Audit Debug）

- **定义**：开启最小审计字段，用于定位 model_chain 识别/打标链问题；默认关闭，仅复发时启用。
- **关键开关**：
  - `LUNA_VOICE_ENABLE_MODEL_CHAIN_AUDIT_DEBUG=1`
- **输出字段（metadata）**：
  - `raw_model_payload_present`
  - `raw_json_present`
  - `raw_json_top_level_keys`
  - `model_chain_detection_reason`
  - `model_chain_detection_failed_reason`

## 开关总表（V1）

| 开关名 | 默认值 | 作用 | 影响范围 | 主线正式能力 | 仅灰度/审计 | 当前建议状态 |
|-------|--------|------|----------|--------------|-------------|--------------|
| `LUNA_VOICE_ENABLE_PREFILTER_ROUTING` | 0 | 开启 prefilter 分档路由（turbo/plus/rule_only 三路） | `voice_final_text_dispatcher` 长链入口 | 是（显式开关能力） | 灰度 | **保留，但默认关闭；当前不建议继续扩大** |
| `LUNA_QWEN_MODEL_TIMEOUT_MS` |（无）| 覆盖长链模型超时（ms） | `voice_final_text_dispatcher` 解析配置 | 是 | 灰度/运行参数 | 保留；灰度/跑批统一口径建议 120000 |
| `LUNA_QWEN_USE_PRIMARY_BACKUP` | 0 | 未启用 prefilter 时启用 qwen 主备 bundle（primary→backup） | `voice_final_text_dispatcher` 默认态 provider 选择 | 是 | 否 | 可用；与 prefilter 灰度态互斥（见组合约束） |
| `LUNA_VOICE_ENABLE_MODEL_CHAIN_AUDIT_DEBUG` | 0 | 输出最小审计字段（raw payload/json + detection reason） | `voice_final_text_dispatcher` metadata + qwen provider | 否（应急） | 审计 | **默认关闭；仅复发时启用** |

## 路由能力（当前实现口径）

### prefilter 分档（v0）

- 入口：`prefilter_long_voice_text_v0(raw_text, session_hint=...)`
- 产物关键字段：
  - `cleaned_text`
  - 风险标签（mixed/unsupported/clarification/multi_step）
  - `routing_suggestion`
- 清洗策略：**极保守**（只剔除口头禅/停顿词前缀与逗号夹心，不做语义改写）

### 三路分流（rule_only / turbo / plus）

在 `voice_final_text_dispatcher.dispatch_voice_final_text()` 中：

- `route_to_rule_or_reject` → `parse_mode=rule_only`（不进模型链）
- `route_to_plus` → 单模型 provider：`qwen-plus`
- `route_to_turbo` → 单模型 provider：`qwen-turbo`

## 允许组合 / 不建议组合

### 允许组合（常见）

- **默认态 + 主备态**：
  - `LUNA_VOICE_ENABLE_PREFILTER_ROUTING=0` + `LUNA_QWEN_USE_PRIMARY_BACKUP=1`
- **灰度态（prefilter）**：
  - `LUNA_VOICE_ENABLE_PREFILTER_ROUTING=1`（其余保持默认；必要时仅调 `LUNA_QWEN_MODEL_TIMEOUT_MS`）
- **灰度态 + 审计态（复发排障时）**：
  - `LUNA_VOICE_ENABLE_PREFILTER_ROUTING=1` + `LUNA_VOICE_ENABLE_MODEL_CHAIN_AUDIT_DEBUG=1`

### 不建议同时开（避免认知混乱）

- `LUNA_VOICE_ENABLE_PREFILTER_ROUTING=1` 与 `LUNA_QWEN_USE_PRIMARY_BACKUP=1`
  - 原因：当前 prefilter 路由分支使用单模型 provider；bundle 开关在此口径下不生效，容易造成“以为开了主备但实际上没走”的误解。

## 工具链（用于回归/观测/审计）

### Benchmark / Smoke（灰度口径）

- `tools/benchmark_prefilter_routing_m3_5_*.py`
- `tools/smoke_prefilter_routing_m3_5.py`

### Audit / Repro（应急）

- `tools/audit_model_chain_failures_m3_5_6a.py`
- `tools/repro_model_chain_failures_m3_5_6b.py`
- `tools/observe_c7_mixed_night_m3_5_7a.py`

## 主线当前结论（写死口径）

- **复杂档主选**：当前 `qwen-plus` 仍为在役复杂档主选（prefilter 开启时 `route_to_plus` 指向 `qwen-plus`）。
- **prefilter 分档能力**：已形成可维持的显式开关灰度能力；**当前默认不开启**，且封板口径为“可维持但不继续扩大”。
- **后续模型替换/新模型接入**：应在本文件定义的运行态框架下进行（开关、观测字段、暂停/回退条件由准入流程统一收口）。

