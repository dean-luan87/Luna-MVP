# LUNA Voice 归档与查询基础（最小可用）V1

## 1. 为什么需要链归档

目前语音白盒能力已经能做到：
- 从 logs / observation 中抽出单条 `RequestTraceChain`
- 对链做查询与链级 issue / diagnostic

但如果只停留在 `logs/` 和临时 `fixtures/extracted`：
- 只能“事后查看”，无法稳定回溯
- 无法做长期趋势/对比
- 更难形成一套可持续调试的历史数据基础

因此需要一个“本地最小归档”层：把链沉淀下来，保证后续查询稳定、扩展可控。

本轮目标不是做完整归档系统，而是把“归档基础层”先立住。

## 2. 归档对象是什么

归档以以下核心对象为主：
- `RequestTraceChain`
- `RequestTraceSummary`
- `RequestTraceIssue`（可选：如果你已有 analysis 输出）
- `RequestTraceDiagnosticSummary`（可选：如果你已有分析输出）

本轮写入时：
- summary 默认由 `RequestTraceChain` 直接推导生成并落盘（不回退到重新跑 analyzer）
- issue / diagnostic 仅在提供 sidecar 输入时才写入（避免引入额外复杂输入格式）

## 3. 目录结构约定

推荐目录结构如下（本轮已实现）：

```text
whitebox_archive/
  voice/
    YYYY-MM-DD/
      chains/
      summaries/
      issues/
      diagnostics/
      manifests/
```

其中每天一个 `manifest.json`，记录最小统计与占位备份状态。

## 4. 当前如何查询归档链

查询入口：
- `tools/query_voice_request_traces.py`

支持两类输入：
- 既有：`--input-dir / --input-file`（读取抽链 JSON）
- 新增：`--archive-dir`（读取 `whitebox_archive` 目录下的归档 chains）

过滤语义保持不变：
- `request_id`
- `trace_id`
- `chain_type`
- `provider_name`
- `final_execution_mode`
- `failure_type`
- `has_fallback`
- `has_rollback`
- 时间范围：`start-after / start-before`

> 注意：本轮查询仍然基于“链对象 -> 临时摘要推断”来过滤（不全文检索、不扫原始日志）。

## 5. 15 天 / T+1 规则（占位）

本轮只实现“归档 tier 的标记规则”，不实现真实备份调度。

规则：
- 近 15 天：`archive_tier = hot`（常备、可直接查）
- 超过 15 天：`archive_tier = pending_backup`（占位：等待 T+1 备份）

manifest 中会记录：
- `archive_tier`
- `backup_status`（占位字段）

未来接入服务器备份时，可以复用这些状态字段。

## 6. 当前不支持什么

本轮明确不做：
- 服务器联动备份
- 调度系统（T+1 实际触发）
- UI 展示层
- 数据库/ES/全文搜索
- 大规模重构抽链/分析链逻辑

## 7. 快速用法（示例）

1) 归档（把某目录下的抽链 JSON 写入归档）：

```bash
python3 tools/archive_voice_request_traces.py --input-dir docs/architecture/voice/fixtures/extracted
```

2) 查询（查归档目录）：

```bash
python3 tools/query_voice_request_traces.py --archive-dir whitebox_archive/voice --chain-type provider_fallback
```

