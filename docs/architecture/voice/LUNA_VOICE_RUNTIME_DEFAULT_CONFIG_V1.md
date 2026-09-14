# LUNA Voice：默认态运行配置清单（V1）

## 目标

把“当前默认态怎么跑”收成一份**可执行的配置清单**，用于发布前回归、线上故障回退与交接。

本文件只做清单化收口：**不改任何运行逻辑**。

## 当前默认态（一句话）

**默认态（Default）**：不开 prefilter 分档（`LUNA_VOICE_ENABLE_PREFILTER_ROUTING=0`），长语音解析默认走规则链（`parse_mode=rule_only`）。若要在默认态启用模型链，需要显式开启主备 bundle（`LUNA_QWEN_USE_PRIMARY_BACKUP=1`）。

## 默认配置清单（V1）

### 1) 默认模型是谁

- **默认态（不开 prefilter）**：
  - 默认配置下不强制走模型链；是否走模型链取决于是否显式启用 `LUNA_QWEN_USE_PRIMARY_BACKUP=1` 以及 provider 是否配置就绪。
- **灰度态（prefilter 开启时）**（仅供口径说明，非默认）：
  - `route_to_plus` → `qwen-plus`
  - `route_to_turbo` → `qwen-turbo`

### 2) 默认是否开启 prefilter routing

- `LUNA_VOICE_ENABLE_PREFILTER_ROUTING`: **默认 0（关闭）**

### 3) 默认是否开启 primary/backup

- `LUNA_QWEN_USE_PRIMARY_BACKUP`: **默认 0（关闭）**
- 若要在默认态启用模型链：建议显式设置为 **1**

### 4) 默认 timeout 口径

- 默认 `model_timeout_ms` 来自 `capabilities/voice/config/voice_long_input_parse_config.yaml`
  - 当前为 **2000ms**
- 运行时可通过 `LUNA_QWEN_MODEL_TIMEOUT_MS` 覆盖（灰度/跑批常用，例如 120000ms），但这不是默认态必选项

### 5) 默认运行态推荐值（可运营基线）

在“默认不开 prefilter”的约束下，建议明确选择以下其一（避免认知混乱）：

- **默认态（纯规则链）**：
  - `LUNA_VOICE_ENABLE_PREFILTER_ROUTING=0`
  - `LUNA_QWEN_USE_PRIMARY_BACKUP=0`
  - 结果：长语音走 `rule_only`
- **默认态（启用模型链的主线默认运行）**：
  - `LUNA_VOICE_ENABLE_PREFILTER_ROUTING=0`
  - `LUNA_QWEN_USE_PRIMARY_BACKUP=1`
  - 结果：默认态通过主备 bundle 启用模型链（primary→backup）

## 一键回归入口（默认态）

- 脚本：`tools/runtime_default_regression_v1.py`
- 输出：`logs/runtime_default_regression_v1_<UTC>.{json,md}`

## 关联文档

- 运行态与开关总表：`docs/architecture/voice/LUNA_VOICE_RUNTIME_MODES_AND_SWITCHES_V1.md`
- 默认运行基线：`docs/architecture/voice/LUNA_VOICE_RUNTIME_DEFAULT_BASELINE_V1.md`

