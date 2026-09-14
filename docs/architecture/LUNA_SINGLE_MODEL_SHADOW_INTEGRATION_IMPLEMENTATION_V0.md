# Phase-Model-002 — Single Model Shadow Integration Implementation v0

**阶段名**：Phase-Model-002  
**性质**：实现（implementation）但仅 shadow/candidate-only；不放权、不接入 real execute/retry/reopen/release  
**约束来源（必须 obey）**：
- `docs/architecture/LUNA_NAVIGATION_GOVERNANCE_CONSTITUTIONAL_CLOSURE_V0.md`
- `docs/architecture/LUNA_MODEL_INTEGRATION_ENTRY_DEFINITION_V0.md`
- `docs/architecture/LUNA_MODEL_INTEGRATION_CONTRACT_V0.md`
- `docs/architecture/LUNA_BOUNDED_MODEL_INTEGRATION_DEFINITION_V0.md`
- `docs/architecture/LUNA_MODEL_INPUT_BOUNDARY_AND_CONTEXT_POLICY_V0.md`
- `docs/architecture/LUNA_MODEL_OUTPUT_CONTRACT_AND_CANDIDATE_SCHEMA_V0.md`
- `docs/architecture/LUNA_MODEL_AUDIT_REPLAY_DISABLE_REQUIREMENTS_V0.md`

---

## 1) 本阶段唯一目标（写死）

接入 **1 个模型** 进入系统，以 **shadow / candidate-only** 模式运行：  
基于受限输入输出统一 candidate schema，并进入白盒/trace/replay，但不拥有任何真实控制权。

---

## 2) 明确非目标（写死）

- 不接第二个模型
- 不做模型调度器 / 模型池 / 多模型 fallback / 投票
- 不做自动执行（不把输出接到 execute/retry/reopen/release）
- 不开启默认路径
- 不扩大真实 side effects 面

---

## 3) 代码交付物（实现路径）

### 3.1 单模型 shadow 接入 runtime（唯一实现）
- `capabilities/model_integration/single_model_shadow_integration_v0.py`

职责：
- 默认关闭 + 显式 enable 才调用模型
- 调用单一模型（可注入 callable）
- 输出进入 candidate adapter（schema/contract enforcement）
- 写入 whitebox trace 与 replay record
- disable 开关 + 失败自动回退无模型基线
- 永不产出可执行命令（candidate-only）

### 3.2 Candidate adapter（输出 contract + schema + forbidden 阻断）
- `capabilities/model_integration/model_candidate_adapter_v0.py`

职责：
- 输入边界：检测/剔除 forbidden input keys（v0 浅过滤 + 记录）
- 输出 contract：严格 JSON 解析；allowlist output_kind；forbidden kinds/语义扫描并阻断
- 映射到统一 candidate schema v0（白盒/回放消费）
- 任一异常/不合规：回退 baseline（不影响主链）

### 3.3 Verifier（A–L 场景覆盖）
- `tools/verify_single_model_shadow_integration_v0.py`

验证：
- disabled by default
- explicit enable 才调用模型
- forbidden input probe 不进入模型（adapter 记录 + 阻断键）
- valid candidate 输出 schema valid
- forbidden outputs（execute/release）被阻断并回退 baseline
- malformed JSON / timeout / exception 回退 baseline
- disable switch runtime 生效
- whitebox/replay 文件存在（可审计/可回放）

---

## 4) Model-002 的真实入口是什么

入口函数：
- `run_single_model_shadow_integration_v0(ShadowIntegrationInputV0(...))`

显式开关：
- `explicit_model_integration_enable_v0=True` 才允许调用模型（默认 false）
- `disable_switch=True` 强制禁用并回退 baseline

---

## 5) 如何体现 shadow / candidate-only（不拿执行权）

硬约束体现：
- 输出仅为结构化状态与 candidate schema（写入 whitebox/replay），不返回任何可执行指令
- 明确字段：`no_execution_side_effects=true`
- `forbidden_output_blocked` 命中则自动 `baseline_fallback_used=true`

---

## 6) 如何体现 forbidden 输入被过滤

- adapter 对 `restricted_context_summary` 做 forbidden key 浅过滤并记录 `forbidden_input_keys_seen`
- 禁止输入不会进入候选 schema；后续实现若出现控制字段泄漏按 Model-001/requirements 触发 no-go

---

## 7) 如何体现 forbidden 输出被真正阻断

- 对 `output_kind` 做 allowlist/denylist
- 对输出内容做最小 forbidden 语义扫描（execute/release/retry/reopen/default-on/override/grant control/long-running）
- 命中即：
  - `forbidden_output_blocked=true`
  - `baseline_fallback_used=true`
  - 产出空 candidates 的 schema 记录（可审计）

---

## 8) 如何体现可审计、可回放

本实现写入：
- whitebox：`var/model_whitebox/model_shadow_whitebox_v0.jsonl`
- replay：`var/model_replay/model_shadow_replay_v0.jsonl`

每次记录包含 `request_id`/hashes/模型信息/解析与阻断结果摘要。

---

## 9) 如何体现 disable / fallback 成立

- 默认禁用：`explicit_model_integration_enable_v0=false` → 不调用模型，直接 baseline
- 运行时禁用：`disable_switch=true` → 强制 baseline
- 模型异常/超时/解析失败 → 自动 baseline，并写入 whitebox/replay 记录

---

## 10) 明确声明（阶段边界）

- 默认路径仍未开启  
- 本阶段未进入 full controlled trial  
- 本阶段未扩大真实 side effects 面  
- 本阶段未让模型拿到执行权  
- 本阶段只完成 single model shadow integration，不做多模型/不做放权  

