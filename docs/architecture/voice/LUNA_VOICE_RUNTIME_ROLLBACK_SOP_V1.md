# LUNA Voice：默认态回退 SOP（V1）

## 目标

把“默认态出现非绿时怎么处理”写成一份**可直接执行**的回退操作口径（不依赖个人经验）。

本文件不改任何逻辑，只定义**触发条件 / 操作顺序 / 必留日志**。

## 适用范围

- 默认态（Default）：`LUNA_VOICE_ENABLE_PREFILTER_ROUTING=0`
- 可选包含：默认态启用主备（`LUNA_QWEN_USE_PRIMARY_BACKUP=1`）的情况
- 不适用于：正在扩灰的实验阶段（M3.5 扩灰已封板，默认不开 prefilter）

## 0) 统一原则（写死）

- 优先保证：**主线可用**（宁可回退到 rule_only，也不要带故障继续放大）
- 回退操作必须：**可逆、可观测、可复盘**
- 任何“非绿”都要先做：**保留日志与产物**，再做切换

## 1) 触发条件（哪些指标非绿必须暂停/回退）

### 1.1 必须暂停进一步动作的条件（硬闸门）

满足任一即进入回退流程：

- 模型链（若启用）出现**非零** `fallback_rate`
- 出现持续性超时/明显抖动（p95 接近 timeout，或超时提示显著增多）
- `val_rate` 非 1.0（若当前链路可观测 validator）
- 业务侧观测到明显误路由/拒答异常上升（结合上层指标）

> 说明：默认态可能走 rule_only，某些指标在回归脚本中会为 null；此时以“是否出现异常拒答/解析失败/耗时异常”为主。

## 2) 回退路径（从轻到重）

### 2.1 场景 A：仅模型链不稳（默认态已启用主备 bundle）

目标：快速让主线回到稳定基线。

- **动作 1（优先）**：回退到纯默认态 rule_only
  - `LUNA_QWEN_USE_PRIMARY_BACKUP=0`
  - 预期：长语音回到 `rule_only` 路径，停止模型链不稳定带来的影响

- **动作 2（必要时）**：显式调整 timeout（仅作为运行参数，不改变语义）
  - 例如临时提升 `LUNA_QWEN_MODEL_TIMEOUT_MS`
  - 仅用于确认“问题是否由超时边界导致”，不要把它当作长期修复

### 2.2 场景 B：出现 model_chain 识别/打标异常（低频复发）

目标：不修逻辑，先保留证据再回退。

- **动作 1**：开启应急审计（只在排障窗口）
  - `LUNA_VOICE_ENABLE_MODEL_CHAIN_AUDIT_DEBUG=1`
  - 只为收集：raw payload/json + detection reason 字段
- **动作 2**：如仍非绿，回退到 rule_only
  - `LUNA_QWEN_USE_PRIMARY_BACKUP=0`
- **动作 3**：排障结束后关闭审计
  - `LUNA_VOICE_ENABLE_MODEL_CHAIN_AUDIT_DEBUG=0`

### 2.3 场景 C：误开 prefilter（灰度态误入默认态）

目标：恢复默认态边界（prefilter 默认关闭）。

- 立即设置：
  - `LUNA_VOICE_ENABLE_PREFILTER_ROUTING=0`
- 并确认：
  - 不要同时依赖 `LUNA_QWEN_USE_PRIMARY_BACKUP` 作为“灰度态主备”（当前实现口径下不生效）

## 3) 回退后验证（最小回归）

回退动作完成后，至少执行一次默认态回归：

- `python3 tools/runtime_default_regression_v1.py`

并确认：

- KPI（耗时/拒答比例等）回到稳定区间
- 产物已落盘 `logs/runtime_default_regression_v1_<UTC>.{json,md}`

## 4) 必留日志（回退时必须保留哪些信息）

- 回退前后环境变量快照（至少包含）：
  - `LUNA_VOICE_ENABLE_PREFILTER_ROUTING`
  - `LUNA_QWEN_USE_PRIMARY_BACKUP`
  - `LUNA_VOICE_ENABLE_MODEL_CHAIN_AUDIT_DEBUG`
  - `LUNA_QWEN_MODEL_TIMEOUT_MS`
- 默认态回归产物：
  - `logs/runtime_default_regression_v1_<UTC>.json/.md`
- 若开启审计：保留包含审计字段的产物/日志片段（无需长期常开）

## 一句话收束

默认态出现非绿：先保留证据，再按“从轻到重”的顺序回退；必要时回到 `rule_only`，确保主线稳定可用。

