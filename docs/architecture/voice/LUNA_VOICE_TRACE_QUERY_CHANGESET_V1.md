# Luna Voice 链查询（最小能力）变更清单 V1

## 1. 新增对象与脚本

| 路径 | 说明 |
|------|------|
| `capabilities/voice/observations/request_trace_summary.py` | `RequestTraceSummary`、`build_request_trace_summary`、查询层 `chain_type`/`status` 规范化 |
| `capabilities/voice/observations/request_trace_query.py` | `TraceQuery`、`filter_chains` / `filter_summaries`、从目录/文件加载链 JSON |
| `tools/query_voice_request_traces.py` | CLI：过滤 + `summary`/`full` + `text`/`json` |
| `capabilities/voice/observations/request_trace_chain.py` | **增补** `RequestTraceChain.from_dict`（供查询加载 JSON） |

## 2. 数据源

仅 **已导出的 `RequestTraceChain` JSON**（与 `extract_voice_request_traces.py` 输出同形）。不查询原始 observation 文件。

## 3. 支持的过滤器

`request_id`、`trace_id`、`chain_type`（短名或 `*_chain`）、`provider_name`、`final_execution_mode`、`status`、`failure_type`（子串）、`has_fallback`、`has_rollback`、`start_after`、`start_before`。

## 4. 不支持的能力

数据库、独立搜索引擎、全文 NL 检索、归档、UI、颜色分级、错误聚类、直接扫原始日志。

## 5. 为什么仍是「最小查询」

只做 **内存结构化过滤** + **摘要视图**，保证可脚本化、可测试、可复用到后续后台，而不引入运维组件。

## 6. 后续强化项（仅列名）

全文检索、模糊匹配、持久化索引、跨目录增量扫描、与归档桶联动、权限与多租户、可视化时间轴。

## 7. 主线—白盒—日志一致性检查

- **A 主线**：查询不替代抽链、不改主链。  
- **B 白盒**：摘要字段与链阶段一致。  
- **C 日志**：输入为链 JSON。  
- **D 最终判断**：**主线通顺，白盒一致，日志已落地**。
