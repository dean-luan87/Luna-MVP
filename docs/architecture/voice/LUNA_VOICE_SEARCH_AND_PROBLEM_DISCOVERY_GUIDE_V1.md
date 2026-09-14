# LUNA Voice 白盒：搜索与问题检索入口说明 V1

## 1. 为什么在 query 之后还需要统一搜索入口

- **`TraceQuery` + `filter_chains`**：面向**链字段**的结构化过滤（request_id、chain_type、时间窗等），适合脚本与归档扫描。
- **问题导向检索**：排障时更常问「所有 rollback」「所有 Fish 相关」「影响 Piper 主样本的高风险」——这些条件落在 **issue / problem summary / alert_level / presentation** 上，单靠链字段不够。
- **`RequestTraceSearchEntry`**：把链级条件与**问题级条件**收束为**单一输入结构**，CLI / 后续 API 只认这一份，避免参数分裂。

## 2. 搜索入口与 query 的区别

| 维度 | TraceQuery / filter_chains | RequestTraceSearchEntry / search_chains_to_results |
|------|----------------------------|-----------------------------------------------------|
| 数据 | 仅用 `RequestTraceChain` + `RequestTraceSummary` | 每条链再跑 `analyze` + `extract_problem_summary` |
| 能力 | 链字段、时间、has_fallback 等 | 增加 `alert_level`、`presentation_semantic`、`primary_issue_type`、`problem_focus`、`priority_min`、`only_main_provider_related` 等 |
| 输出 | 链或 summary | **`RequestTraceSearchResult`（concise，非全链 JSON）** |

## 3. 当前支持哪些搜索字段

见 [LUNA_VOICE_SEARCH_FIELD_DICTIONARY_V1.md](./LUNA_VOICE_SEARCH_FIELD_DICTIONARY_V1.md)。

## 4. 当前支持哪些问题导向检索

- **显式字段**：`alert_level`（支持 `|` 多值）、`presentation_semantic`、`primary_issue_type`、`is_action_required`、`priority_min`、`only_main_provider_related`、`failure_signature`（子串/前缀）。
- **快捷 `problem_focus`**（单字段触发内置规则）：
  - `rollback`：`legacy_rollback` 链或 `has_rollback`
  - `fallback`：`provider_fallback` 链或 `has_fallback`
  - `high_risk`：`alert_level` 为 high_risk/critical 或展示语义为 warning/danger
  - `main_provider`：影响默认主样本 `piper` 的问题（`problem_focus=main_provider`）
  - `main_provider`：影响当前默认主样本 **piper** 的高关注问题（与 prioritizer 主链叙事一致）
  - `action_required`：`is_action_required=true`

与链级条件为 **AND**；`problem_focus` 与其它已设条件同时满足才命中。

## 5. 默认搜索结果为什么返回 concise

- **目标**：快速发现问题，而不是灌完整链 JSON。
- **`RequestTraceSearchResult`**：含 `summary_text`、`alert_level`、`presentation_semantic`、`priority_score`、`priority_reason` 等一行可读字段；**不含** `stages` 全量。
- **`result_mode`**：预留 `concise` / `detailed`；当前 detailed 仍不返回全链，仅保留扩展位。

## 6. 当前不做什么

- **全文**检索、**自然语言**查询
- **前端**搜索页、**真实**服务端索引（ES/向量库等）
- **大模型**检索与改写
- **改**主链、抽链器、分析器、归档主逻辑（本层仅消费）

## 7. 阶段-7 收口说明

**白盒强化在阶段-7 结束**：先回到**主线工程**，不在此继续扩展白盒阶段 8/9/10。后续若需更强检索，再在**不破坏**本入口的前提下扩展字段或实现。

## 8. 关联代码

| 内容 | 路径 |
|------|------|
| 搜索入口 | `capabilities/voice/observations/request_trace_search_entry.py` |
| 搜索结果行 | `request_trace_search_result.py` |
| 查询器 | `request_trace_search_query.py` |
| 结果组装 | `request_trace_search_result_builder.py` |
| CLI | `tools/search_voice_request_problems.py` |
