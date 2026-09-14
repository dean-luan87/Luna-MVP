# LUNA Voice 白盒搜索字段字典 V1

面向 `RequestTraceSearchEntry` / `RequestTraceSearchResult`；**结构化过滤**，非全文检索。

| 字段名 | 中文解释 | 适合过滤 / 展示 | 典型取值 | 注意事项 |
|--------|----------|-------------------|----------|----------|
| `request_id` | 业务请求 ID | **过滤**、展示 | 非空字符串 | 精确匹配 |
| `trace_id` | 追踪 ID | **过滤**、展示 | UUID 等 | 精确匹配 |
| `chain_type` | 抽链拓扑类型 | **过滤**、展示 | `success_chain`、`provider_fallback_chain`、`legacy_rollback_chain` 等 | 与 `TraceQuery` 一样支持短名别名 |
| `provider_name` | 当前叙事 provider | **过滤**、展示 | `piper`、`piper` | 问题导向常用：`piper` 筛 Fish 相关 |
| `status` | 查询层规范化状态 | **过滤**、展示 | `success`、`degraded_success`、`failed`、`suppressed` | 来自 `build_request_trace_summary` |
| `failure_type` | 与 summary 主错误类型对齐 | **过滤** | 与 `primary_error_type` 同族 | 子串匹配 |
| `failure_signature` | 合成签名（issue+stage+链型+错误类型） | **过滤** | 小写拼接串 | 子串或前缀匹配；**非**稳定协议字段，仅辅助检索 |
| `primary_issue_type` | 归因 issue 类型 | **过滤**、展示 | `provider_unavailable`、`playback_failure` 等 | 子串或等于 |
| `alert_level` | 白盒展示档位 | **过滤**、展示 | `normal`…`critical` | 支持 `high_risk\|critical` 多值 |
| `presentation_semantic` | 展示语义（挂色层） | **过滤**、展示 | `ok`、`info`、`attention`、`warning`、`danger` | 由 `alert_level` 映射；支持多值 |
| `has_fallback` | 是否发生 fallback | **过滤**、展示 | 布尔 | 来自 summary |
| `has_rollback` | 是否发生 rollback | **过滤**、展示 | 布尔 | 来自 summary |
| `archive_tier` | 归档层级 | **过滤**、展示 | `hot`、`pending_backup` | `search_chains_to_results` 需传入 `archive_tier_by_request_id`；无映射则筛不出 |
| `is_action_required` | 是否需人工跟进 | **过滤**、**结果展示** | 布尔 | 来自 problem summary；`RequestTraceSearchResult` 亦带出，便于列表一眼判断 |
| `priority_score` | 规则优先级分 | **过滤**（`priority_min`）、展示 | 整数 | `priority_min` 为下界 |
| `final_execution_mode` | 收口终态 | **过滤**、展示 | `provider_chain`、`legacy_fallback`、`failed_no_output` 等 | 链字段 |
| `start_after` / `start_before` | 时间窗（链开始时间） | **过滤** | Unix 秒 | 与 `TraceQuery` 一致 |
| `problem_focus` | 问题导向快捷键 | **过滤** | 见指南 §4 | 与其它条件 AND |

**只适合展开 / 专业模式**（本入口不默认返回）：  
- 完整 `stages`、`key_fields`、原始 `raw_observation_refs`、长 JSON 链对象 —— 请用 `request_id` 命中后再加载单链。

---

关联：[搜索与检索说明](./LUNA_VOICE_SEARCH_AND_PROBLEM_DISCOVERY_GUIDE_V1.md)、[变更清单](./LUNA_VOICE_SEARCH_AND_PROBLEM_DISCOVERY_CHANGESET_V1.md)。
