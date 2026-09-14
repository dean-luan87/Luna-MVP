# 前置规则裁剪层（Pre-Filter Layer）最小设计 M3

## 1. 定位

**位置**：`ASR / 文本输入 → Pre-Filter Layer → 模型链（turbo / plus）或规则链`

**不是**：validator、builder、fallback 裁决、thinking、最终任务裁决层。

**是**：轻量 **过滤**、**压缩**、**粗分类**、**路由建议**（仅建议，不替代 orchestrator 决策）。

**本轮状态**：设计草案；**不接入主链**、不替代现有 validator/builder（与执行指令一致）。

---

## 2. 最小输入

| 字段 | 说明 |
|------|------|
| `raw_text` | ASR 或等效长文本 |
| `session_hint` | 可选，与现 `session_hint` 对齐 |
| `locale` / `product_flags` | 可选，预留 |

---

## 3. 最小输出对象（草案）

建议形态：`VoiceLongInputPreFilterResultV0`（名称可改），字段示例：

| 字段 | 类型 | 含义 |
|------|------|------|
| `cleaned_text` | str | 去冗余、口头语压缩后的主文本（供模型或规则消费） |
| `non_task_fragments` | list[str] | 抽离的非任务背景片段（情绪/身体/闲聊），可空 |
| `skeleton` | dict（可选） | 粗槽位：`goal_hint`、`location_hints`、`time_order_hints`、`constraints` |
| `simple_or_complex` | enum | `simple` \| `complex`（粗粒度） |
| `mixed_risk` | float 或 enum | mixed 结构风险（0–1 或 low/med/high） |
| `unsupported_risk` | float 或 enum | 违规/不可执行代理风险 |
| `clarification_risk` | float 或 enum | 需追问风险 |
| `multi_step_risk` | float 或 enum | 多段/多意图风险 |
| `routing_suggestion` | enum | `route_to_turbo` \| `route_to_plus` \| `route_to_rule_or_reject` |
| `notes` | str | 可解释轨迹（白盒） |

**说明**：仅为契约草案；字段可删减合并，**不得**与 `VoiceLongInputStructuredParseResult` 混为同一 schema。

---

## 4. 最小应做的事（四块）

### A. 去冗余

- 重复短语合并、明显口头禅（「那个」「就是说」等）压缩（规则 + 可选轻量模型 **不在本轮范围**）。
- 目标：降低 **输入 token** 与模型「跟废话」概率。

### B. 抽骨架

- 从 `cleaned_text` / 正则 / 词典规则中粗提：目标动作、地点/POI 片段、时间/顺序词、限制条件（不走高速等）。
- 非任务块：情绪/身体状态 **旁路** 进 `non_task_fragments`，避免与任务句硬绑。

### C. 粗分类

输出风险标签（规则为主）：

- `simple`：单句单意图、无 mixed 信号。
- `mixed`：`mixed_risk` 高（出现身体/情绪+指令并存等模式）。
- `unsupported_risk`：自动代办、远程控制、违法绕过等模式（与 C5 矩阵 case 对齐）。
- `clarification_risk`：指代不明、缺省关键槽位。
- `multi_step_risk`：显式多段连接词（先/再/然后/最后…）。

### D. 路由建议（三类）

| 建议 | 典型条件（草案） |
|------|------------------|
| `route_to_turbo` | `simple` + 低 mixed + 低 unsupported + 文本长度低于某阈值 |
| `route_to_plus` | 高 mixed / 高 multi_step / 长文本（L4+）/ clarification 边界 |
| `route_to_rule_or_reject` | 极高 unsupported_risk 或明确可规则拒绝 |

**注意**：建议 **不强制执行**；真正选路仍在 **dispatcher / 策略层** 统一生效（后续接入时）。

---

## 4.1 M3.3：规则版最小分档（可实现、可回归）

> 目的：将 “simple → turbo / complex → plus / 极高风险 → rule_or_reject” 从口号落到**可复现的规则**，用于灰度与回归对照。  
> 原则：先规则版，后续再做打分器；不改 schema/validator/builder/provider；不默认接入主链。

### A) 规则输入与白盒输出

- 输入：`raw_text`（必要）+ `session_hint`（可选）
- 输出：`routing_suggestion` + 四个风险标签（mixed/unsupported/clarification/multi_step）+ `notes`

代码参考（最小纯函数占位）：`capabilities/voice/bridge/voice_long_input_prefilter_v0.py`

### B) 最小判定逻辑（v0 示例）

1. **route_to_rule_or_reject（优先级最高）**
   - 命中 “挂…号/代办/支付/转账/下单” 等明显越权或不可执行代理模式（示例：文本同时出现「挂」与「号」）

2. **route_to_turbo（simple）**
   - `len(cleaned_text) ≤ 60`
   - `mixed_risk = low`
   - `unsupported_risk = low`
   - `clarification_risk = low`
   - `multi_step_risk = low`

3. **route_to_plus（complex）**
   - 任一满足：mixed / multi_step / 长句 / clarification 边界 / 约束多

### C) 建议默认阈值（先写死、便于回归）

- `max_turbo_chars = 60`
- `max_plus_chars = 220`（v0 仅用于白盒，不做硬切）

> 阈值后续应以 M3 矩阵、真实样本分位数回归更新；但 M3.3 第一版宜固定，避免变量打散。

---

## 4.2 M3.4：分档灰度验证（先离线、后开关）

> 目标：证明规则分档（prefilter_v0）的路由建议不会把已验证稳定的主链打坏。

### 方案 A：离线路由评估（不执行模型切换，最稳）

1. 对固定 case 集（M3 的 `voice_long_voice_length_complexity_cases_m3.json`）运行 `prefilter_v0`
2. 将 `prefilter_v0.routing_suggestion` 与你们现有的 M3 benchmark “可通过边界”（turbo/plus 的 val/fallback）对齐
3. 输出：
   - 路由命中率（expected vs suggested）
   - suggested 路由下的稳定性代理指标（json/val/fallback 的组合）

对应脚本：
`tools/eval_prefilter_routing_m3_4.py`

### 方案 B：显式开关下灰度接入（通过 A 后再做）

环境变量（**默认关闭**）：
`LUNA_VOICE_ENABLE_PREFILTER_ROUTING=1`

**接入准备（已实现、默认不启用）**：`voice_final_text_dispatcher` 在长链分支读取该开关。

| 开关 | 行为 |
|------|------|
| 未设置 / 0 / false | **与历史一致**：若 `LUNA_QWEN_USE_PRIMARY_BACKUP=1` 则主备 bundle；否则默认规则链等既有逻辑 |
| `=1` | **忽略** `LUNA_QWEN_USE_PRIMARY_BACKUP` 对长链 Provider 的影响；按 `prefilter_v0.routing_suggestion` 选择：`qwen-turbo` 单模型 / `qwen-plus` 单模型 / `parse_mode=rule_only`（规则链，对应 `route_to_rule_or_reject`）。若百炼未配置而建议走模型，则退化为 `rule_only`，并在 `selected_provider_model_id` 中标记 `rule_chain_only_unconfigured_qwen_external` |

**分流结果 `metadata` 观测字段（长链）**：

| 字段 | 说明 |
|------|------|
| `prefilter_routing_enabled` | bool |
| `prefilter_routing_suggestion` | `route_to_turbo` / `route_to_plus` / `route_to_rule_or_reject`；关开关时为 `disabled` |
| `prefilter_simple_or_complex` | prefilter 粗判 |
| `selected_provider_model_id` | 实际选用的路由标签：`qwen-turbo` / `qwen-plus` / `rule_chain_only` / `qwen_primary_backup_bundle`（关开关且开主备时）等 |
| `route_match_expected` | 预留；离线标签对齐时可写入 |
| `prefilter_notes` | prefilter 白盒 notes |

**灰度验收指标（开 B 前写死口径）**：在建议路由下跑批或线上采样时至少观测：

- `json_rate`、`val_rate`、`fallback_rate`（与 M3 稳定性代理一致）
- `mixed_preserve_rate`（mixed 场景是否被错误压扁/丢档）
- `avg_ms`、`p95_ms`
- `turbo` / `plus` / `rule_or_reject`（规则链）**路由命中率**（按 `prefilter_routing_suggestion` 或 `selected_provider_model_id` 聚合）

**一键回退**：取消 `LUNA_VOICE_ENABLE_PREFILTER_ROUTING` 或置 `0`，即恢复「主备 bundle + 既有默认」，无需改代码。

> M3.4 方案 A 通过后：**已具备 B 的接入准备**；是否在生产打开开关属独立灰度决策。

---

## 5. 设计要回答的核心问题

1. **什么样的输入不该直接进 qwen-plus？**  
   极短、明确单意图、低风险的 **可先 turbo** 或 **规则**；避免 plus 的 token/延迟浪费。

2. **什么样的输入仅用 qwen-turbo 即可？**  
   与矩阵 M3 结论绑定：在 **L1–L2 + C1–C2** 等档若 turbo 与 plus 结构指标等价且更快，则路由建议偏向 turbo（以 benchmark 附录为准）。

3. **什么样的输入甚至不值得进模型？**  
   明确不可执行代理、违规诉求：建议 `route_to_rule_or_reject`，由规则链 / reject 路径处理。

4. **如何降 token 与延迟？**  
   缩短 `cleaned_text`、拆分 non_task、减少「废话进模型」；长语音 L5 先压缩再决定是否上 plus。

---

## 6. 当前不做项（写死）

- 不修改 schema / validator / builder / fallback 定义。
- 不接 thinking；不做增量式理解主链改造。
- **不默认启用**前置分档路由：`LUNA_VOICE_ENABLE_PREFILTER_ROUTING` 默认关闭；关闭时 dispatcher 行为与接入准备前一致。
- 不以 pre-filter 输出替代 validator。

---

## 7. 后续接入主链的建议位置

1. **语音最终文本入口**：`voice_final_text_dispatcher` 在调用 `run_long_input_task_planning_v1` **之前**，对 `final_text` 做一次纯函数式 `pre_filter(raw) → cleaned + suggestion`。  
2. **策略消费**：仅将 `routing_suggestion` 作为 **hint** 传给「选 Provider / 选模型」的工厂（与 M1 主备 bundle 并列决策，而非嵌进 bundle 内部）。  
3. **观测**：见 §4.2 方案 B 表中 `metadata` 字段；可额外打日志 `cleaned_text_len` 等与 M3 矩阵对照。

---

## 相关文档

- Case 矩阵：`LUNA_VOICE_LONG_VOICE_LENGTH_COMPLEXITY_CASE_MATRIX_M3.md`
- Benchmark 附录：`LUNA_VOICE_LONG_VOICE_LENGTH_COMPLEXITY_BENCHMARK_APPENDIX_M3.md`
