# 长语音任务拆解主链 — 三线路线图与阶段（M1）

本文档把「不再散着优化」收敛为三条并行推进线，并固定阶段顺序。  
与模型选型记录见：`LUNA_VOICE_LONG_INPUT_TASK_PARSE_QWEN_SELECTION_RECORD_M0.md`；Provider 默认档见：`LUNA_VOICE_QWEN_EXTERNAL_PROVIDER_AB_DECISION_M0.md`。

---

## 一、主链可上线优化（优先）

**目标**：从「能跑通 benchmark」到「能稳定进真实使用」。

### 1. 中台默认路由（真值）

- **任务域**：`long_voice_task_parse`
- **主选模型**：`qwen-plus`
- **速度型备选**：`qwen-turbo`
- **淘汰（非主链候选）**：`qwen3.5-flash`（仅 shadow/对照）
- **百炼 Qwen 外部长输入 Provider 默认档位**：`optimized`（与 `DEFAULT_QWEN_AB_PROFILE` 对齐；`legacy` 仅 A/B、回归、排障）

代码入口：`mid_platform/model_governance/routing/policies/voice_long_voice_task_parse_policy_m0.py`、  
`mid_platform/model_governance/registry/cards/voice_long_voice_task_parse_registry_cards_m0.py`。

**接入层主备（运行时）**（M1 已落地）：

- 模块：`capabilities/voice/providers/qwen_long_voice_primary_backup_provider.py`
- 工厂：`create_qwen_long_voice_task_parse_provider_bundle_from_env` — 组合 **qwen-plus + qwen-turbo**（专用 prompt 路径），先主后备。
- **语音主线分流**：`voice_final_text_dispatcher.dispatch_voice_final_text` 在设置环境变量  
  **`LUNA_QWEN_USE_PRIMARY_BACKUP=1`（或 `true`/`yes`）** 且百炼已配置时，自动使用 `model_preferred_with_rule_fallback` + 上述 bundle；未设置则行为与改前一致（仍由 YAML 默认 `parse_mode` 决定）。
- 测试：`tests/test_qwen_long_voice_primary_backup_provider_m1.py`
- **M2.1 分时段 benchmark 结论与附录**（主路稳定性 / mixed 口径）：`LUNA_VOICE_LONG_VOICE_M2_1_BENCHMARK_APPENDIX.md`
- **M2.2 备路注入式验证附录**（timeout / exception / None → turbo 接管）：`LUNA_VOICE_LONG_VOICE_M2_2_BACKUP_INJECTION_APPENDIX.md`
- **M3 分档测试 + Pre-Filter 预研**（不测主备 bundle；不接入主链）：
  - Case 矩阵：`LUNA_VOICE_LONG_VOICE_LENGTH_COMPLEXITY_CASE_MATRIX_M3.md` / `configs/voice/voice_long_voice_length_complexity_cases_m3.json`
  - 脚本：`tools/benchmark_long_voice_length_complexity_matrix_m3.py`
  - 结果附录（跑后填）：`LUNA_VOICE_LONG_VOICE_LENGTH_COMPLEXITY_BENCHMARK_APPENDIX_M3.md`
  - Pre-Filter 最小设计：`LUNA_VOICE_PREFILTER_LAYER_MIN_DESIGN_M3.md`

### 2. Fallback 规则（语义分层）

| 层级 | 条件（摘要） | 行为 |
|------|----------------|------|
| **模型调用** | Provider 超时 / 异常 / 返回无法解析为 JSON | 若配置允许，走**规则链**兜底（`voice_long_input_parse_orchestrator`） |
| **结构化校验** | `validate_model_structured_output` 不通过 | **整表不穿透**，走**规则链**（不静默丢候选） |
| **路由层（治理）** | 主选模型不可用（由接入方实现重试策略时） | 策略上**备选**为 `qwen-turbo`；再失败则依卡片的 `fallback_to_rule_chain` |
| **模型输出语义** | `primary_domain=unsupported_or_reject` / `needs_clarification` 等 | 由 **schema + builder** 表达，**不是**「切 API 备选」的同义词 |

说明：**单次请求内** orchestrator 只绑定一个 `VoiceLongInputModelProvider`；**plus → turbo** 的多模型重试需在**接入层/工厂**按中台策略实现，本文件定义的是**治理真值与语义**，不替代具体重试代码路径。

### 3. 真实场景验证（待执行）

在固定 4 条 smoke 之外，补：**长句混合意图+情绪**、**强切后续接**、**连续多轮承接**。  
关注：**mixed 是否漏**、**unsupported 是否误判为可执行**、**多轮是否漂移**（优于只看 avg）。

### 4. 稳定性抽测（待执行）

建议 **20～50 轮**、**分时段**，记录：`avg` / `p95` / `mixed_preserve_rate` / `fallback_rate`。

---

## 二、提速优化（后置、小步）

1. **复杂度分档**：简单低歧义 → `qwen-turbo`；mixed / 多意图 / 长句 / 高风险 → `qwen-plus`（让 plus 少干不该干的活）。  
2. **输入轻量裁剪**：去重复与无效口头词，**保留 mixed 非任务信息**（谨慎）。  
3. **Prompt**：以治理层小修为主（去重、缩短、控字段），**避免大改**破坏已稳定结构。

---

## 三、体系化优化（立项、不赶一次做完）

1. **Prompt 治理层**：宪法 / 任务 / 运行时 / 记忆分层（与现有分层文件演进）。  
2. **思考模型独立**：执行链不承载深度 thinking；思考能力走图书馆/蜂巢/分析链。  
3. **实验清单**：单变量、记口径、可回退（与 A/B 脚本、决策短文一致）。

---

## 阶段执行顺序（建议）

1. **第一阶段**：中台路由与 Provider 默认档已写入仓库；接入方按策略接线并实现（若尚未）plus→turbo 重试。  
2. **第二阶段**：真实场景验证 + 20～50 轮稳定性抽测。  
3. **第三阶段**：复杂度分档（turbo / plus）。  
4. **第四阶段**：输入裁剪 + Prompt 治理层产品化。

---

## 当前明确不做的

换供应商、大改 schema/validator、thinking 进执行链、复杂多模型协同——避免打散已收敛主链。

---

## 后续云端备选接入候选池（占位，未开工）

后续接入仅做 **统一口径对照测试**，不影响当前生产 Qwen 主链默认行为。

- 后续接入候选（第一批）：`DeepSeek`、`豆包 / 火山方舟`
- 现有基线：`Qwen`（已跑通）
- 暂不纳入第一批对照池：`Kimi`、`百度`
- 目的：与 Qwen 在长语音任务拆解链上跑同一套 benchmark 口径横向比较结构稳定性、通过率与时延分位数。
- 当前状态：仅占位，未接入（等待 turbo 纪律收敛后再开工）。

统一测试口径（接入三家时必须跑同一套）：
1) 结构化 JSON 是否稳定
2) validator 通过率是否能到 100%
3) mixed 保留是否稳定
4) 平均时延 / p95 到什么档位
5) 是否会出现类似 `task_control.*` 的协议漂移

统一指标：`json_rate`、`val_rate`、`fallback_rate`、`mixed_preserve_rate`、`avg_ms`、`p95_ms`。
