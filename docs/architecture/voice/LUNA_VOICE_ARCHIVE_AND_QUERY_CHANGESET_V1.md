# LUNA Voice 归档与查询 ChangeSet V1

## 1. 本轮新增/修改的对象与脚本

新增（归档基础层）：
- `capabilities/voice/observations/request_trace_archive.py`
  - 本地写入器：写入 `RequestTraceChain` / `RequestTraceSummary`
  - 可选写入：`RequestTraceIssue` / `RequestTraceDiagnosticSummary`
  - 更新最小 `manifest.json`
  - 归档 tier 占位：`hot | pending_backup`
- `capabilities/voice/observations/request_trace_archive_manifest.py`
  - 最小 manifest / 索引对象
  - tier 计算函数（近 15 天常备 / 超过 15 天待备份占位）
- `tools/archive_voice_request_traces.py`
  - 输入抽链 JSON 目录
  - 可选输入 issue / diagnostic sidecar 目录（同一 `chain_id` 命名规则）
  - 输出：写入归档目录并打印落盘路径

修改（查询支持归档目录）：
- `capabilities/voice/observations/request_trace_query.py`
  - 新增 `load_chains_from_archive_directory()`：从归档目录读取 `chains/*.json`
- `tools/query_voice_request_traces.py`
  - 新增参数 `--archive-dir`：指定归档目录查询

新增文档：
- `docs/architecture/voice/LUNA_VOICE_ARCHIVE_AND_QUERY_BASELINE_V1.md`
- `docs/architecture/voice/LUNA_VOICE_ARCHIVE_AND_QUERY_CHANGESET_V1.md`

## 2. 归档目录怎么组织

归档根目录约定为：
- `whitebox_archive/voice/YYYY-MM-DD/`

每一天包含：
- `chains/`：`{chain_id}.json`（RequestTraceChain）
- `summaries/`：`{chain_id}.json`（RequestTraceSummary）
- `issues/`：`{chain_id}.json`（可选，RequestTraceIssue）
- `diagnostics/`：`{chain_id}.json`（可选，RequestTraceDiagnosticSummary）
- `manifests/manifest.json`：最小清单与占位备份状态

`chain_id` 命名规则：
- `{request_id}__{trace_id or no_trace}`

## 3. manifest 记录什么

manifest 记录最小可用统计：
- `total_chain_count` / `chain_ids`
- `provider_counts`
- `issue_type_counts`
- `rollback_count` / `fallback_count`
- `archive_tier`（hot / pending_backup）与 `backup_status`（占位）

## 4. 当前查询支持到什么程度

现有查询过滤语义保持不变。

新增能力是：
- 既支持 `--input-dir/--input-file`（fixtures/extracted）
- 也支持 `--archive-dir`（whitebox_archive）

查询仍通过：
- `RequestTraceChain` 加载
- 临时构建 `RequestTraceSummary` 做过滤

不做全文搜索、不做数据库、不做复杂索引。

## 5. 当前不支持哪些高级能力

本轮明确不做：
- 搜索增强（全文/模糊匹配/向量）
- 简洁/专业两层展示（UI 展示层能力）
- 颜色分级
- 服务器备份与调度

## 6. 后续强化方向

归档基础层稳定后，后续可逐步加入：
- 专业/简洁模式的白盒展示层
- 使用归档 sidecar 中 issue/diagnostic 做更准确展示
- 趋势比较（同一 provider / 同一 issue_type 的时间序列）
- 最终的 T+1 备份服务化接入

