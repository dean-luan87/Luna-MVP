# 白盒阶段-7：搜索与问题检索 — 变更清单 V1

## 1. 新增对象 / 脚本

| 路径 | 说明 |
|------|------|
| `capabilities/voice/observations/request_trace_search_entry.py` | `RequestTraceSearchEntry`、解析辅助 |
| `capabilities/voice/observations/request_trace_search_result.py` | `RequestTraceSearchResult`（concise 行，含 `summary_text`） |
| `capabilities/voice/observations/request_trace_search_result_builder.py` | 组装搜索结果 |
| `capabilities/voice/observations/request_trace_search_query.py` | `matches_search_entry`、`search_chains_to_results` |
| `tools/search_voice_request_problems.py` | CLI：目录/归档 + 多条件过滤 |
| `tests/test_request_trace_search_query.py` | 检索回归 |
| `docs/.../LUNA_VOICE_SEARCH_AND_PROBLEM_DISCOVERY_GUIDE_V1.md` | 设计说明 |
| `docs/.../LUNA_VOICE_SEARCH_FIELD_DICTIONARY_V1.md` | 字段字典 |
| 本文件 | 变更清单 |

## 2. 搜索入口如何定义

- **单一结构**：`RequestTraceSearchEntry`，未设字段 = 不参与过滤。
- **与 `TraceQuery` 复用**：链级条件通过构造 `TraceQuery` 调用 `matches_query`。
- **问题级条件**：在 `RequestTraceProblemSummary` 上匹配；`problem_focus` 为内置规则快捷。

## 3. 当前支持的搜索场景（示例）

- 所有 rollback：`problem_focus=rollback` 或 `has_rollback=true` 或 `chain_type=legacy_rollback_chain`
- 所有 fallback：`problem_focus=fallback` 或 `has_fallback=true`
- 高风险：`alert_level=high_risk|critical` 或 `presentation_semantic=warning|danger` 或 `problem_focus=high_risk`
- 主 provider 相关：`provider_name=piper` 或 `problem_focus=main_provider`
- Piper 主链异常：`only_main_provider_related=true`（需 `provider_name=piper` 且 alert 偏高）
- 需人工：`is_action_required=true` 或 `problem_focus=action_required`

## 4. 当前不支持的能力

- 全文检索、自然语言、正则扫原始日志
- 数据库 / ES / 向量索引服务
- 服务端常驻索引与增量更新
- 大模型改写查询

## 5. 阶段-7 收口与回主线

- **白盒强化在阶段-7 结束**：先回**主线工程**，不继续规划白盒阶段 8/9/10。
- 后续若增强检索，应**扩展** `RequestTraceSearchEntry` / 查询器，**不**改抽链与主链。

## 6. 后续强化方向（不在本轮）

- 真实 UI 搜索框、服务端索引
- 与归档 manifest 自动关联 `archive_tier_by_request_id`
- 搜索结果与问题区 `RequestTraceConciseProblemBoard` 联动
