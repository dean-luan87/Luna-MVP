# Luna Voice 链查询（最小能力）说明 V1

## 1. 查询对象是什么

本轮查询的**唯一对象**是已抽好的 **`RequestTraceChain`**（通常为 `extract_voice_request_trace.py --format json` 的导出文件）。  
不在此层直接读取原始 observation / JSONL 日志。

数据流：

```
observation / log → 抽链 → RequestTraceChain（JSON）→ query_voice_request_traces.py
```

## 2. 支持的过滤键

| 参数 | 含义 |
|------|------|
| `--request-id` | 精确匹配 `request_id` |
| `--trace-id` | 精确匹配 `trace_id` |
| `--chain-type` | 与 **查询层规范化** 后的链型对齐（如 `success`、`provider_fallback`、`legacy_rollback`，或 `*_chain` 原名） |
| `--provider-name` | 精确匹配链顶层的 `provider_name`（**当前主样本成功链为 `piper`**；fallback 样本可能为 `piper`，因与抽链器取值一致） |
| `--final-execution-mode` | 如 `provider_chain`、`legacy_fallback`、`failed_no_output` |
| `--status` | 规范化 `success` / `degraded_success` / `failed` / `suppressed` / `unknown`，或与原始 `ok` 等兼容匹配 |
| `--failure-type` | 与 `primary_error_type`、各 `errors[].error_type` **子串**匹配（非全文检索） |
| `--has-fallback` | `true` / `false` |
| `--has-rollback` | `true` / `false` |
| `--start-after` / `--start-before` | 基于 `started_at` 的时间窗（Unix 秒） |

组合过滤为 **AND** 关系。

## 3. 输入数据从哪里来

- 目录下多个 JSON 文件：`--input-dir path/to/dir`（默认 `*.json`，可用 `--glob`）
- 或显式文件：`--input-file a.json --input-file b.json`

推荐与抽链产物一致，例如：

`docs/architecture/voice/fixtures/extracted/*.json`

## 4. 摘要模式 vs 完整模式

| `--mode` | 输出 |
|----------|------|
| `summary`（默认） | **`RequestTraceSummary`**：一行/一条摘要字段，便于扫列表 |
| `full` | 完整 **`RequestTraceChain`** JSON |

`--format json` 时输出 JSON 数组；`text` 时摘要为制表列，完整模式每行一条紧凑 JSON。

## 5. 当前不支持什么

- 数据库、Elasticsearch、Whoosh、向量检索  
- 全文自然语言搜索、模糊搜索整条日志  
- 归档 / 备份 / 15 天策略  
- Web UI、颜色分级、错误聚类  
- **绕过抽链**直接查原始 observation 文件（本脚本不负责）

## 6. 后续如何扩展（仅路线，本阶段不实现）

归档层统一落盘链 JSON → 同一查询 API；后台页面消费 `summary` / `full`；再考虑索引服务、全文检索、可视化。

## 7. 示例（主样本 `provider_name=piper`）

```bash
# 所有 fallback 链（摘要）
python3 tools/query_voice_request_traces.py \
  --input-dir docs/architecture/voice/fixtures/extracted \
  --chain-type provider_fallback

# 顶层 provider_name 为 piper 的链（当前成功主样本）
python3 tools/query_voice_request_traces.py \
  --input-dir docs/architecture/voice/fixtures/extracted \
  --provider-name piper \
  --format json

# rollback 链
python3 tools/query_voice_request_traces.py \
  --input-dir docs/architecture/voice/fixtures/extracted \
  --chain-type legacy_rollback
```

## 8. 主线—白盒—日志一致性检查

- **A 主线**：查询层只依赖抽链产物，不绕主链。  
- **B 白盒**：摘要含 `chain_type`、`has_fallback`、`has_rollback`、错误摘要字段。  
- **C 日志**：输入为可版本化的链 JSON。  
- **D 最终判断**：**主线通顺，白盒一致，日志已落地**。
