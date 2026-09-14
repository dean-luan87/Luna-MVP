# LUNA Voice 白盒简洁/专业模式数据契约 V1

## 0. 文档定位

- 约定两种模式**最少要带哪些字段**，避免后台/脚本各写各的。
- 实现形态可以是：REST JSON、`RequestTraceConciseView` / `RequestTraceProfessionalView`（见 `capabilities/voice/observations/`）、或导出文件字段子集。
- 关联：[双模式总图](./LUNA_VOICE_WHITEBOX_VIEW_MODES_V1.md)、[字段字典](./LUNA_VOICE_WHITEBOX_FIELD_DICTIONARY_V1.md)、[展开规则](./LUNA_VOICE_WHITEBOX_EXPANSION_RULES_V1.md)。

## 1. 命名约定

- **单链契约**：以下「必需」指展示一条请求时，该模式 API/视图**不得缺省**的字段（可用 `null` 显式表示未知，禁止静默省略键名除非协议另有规定）。
- **系统/dashboard 契约**：系统状态区可额外要求聚合指标（成功/降级/失败计数等），由 `RequestTraceArchiveManifest` + 查询结果计算，见 §4。

## 2. 简洁模式（Concise）必需字段

面向：列表行、仪表盘卡片、**一眼健康度**。

### 2.1 单链行（每条最近链摘要）

| 字段 | 必选 | 说明 |
|------|------|------|
| `request_id` | 是 | 主键 |
| `trace_id` | 否 | 有则展示，便于跳转日志 |
| `chain_type` | 是 | 建议用规范化后的短名（与 `RequestTraceSummary.chain_type` 一致）；若只存 raw，UI 须能映射 |
| `provider_name` | 是 | 允许 `null` |
| `final_execution_mode` | 是 | 允许 `null` |
| `status` | 是 | **规范化**状态：`success` / `degraded_success` / `failed` / `suppressed` / `unknown`（与 `RequestTraceSummary.status` 对齐） |
| `primary_issue_type` | 是 | 无问题时为 `none` 或约定空串（团队二选一，须全系统统一） |
| `primary_issue_reason` | 是 | 可与上一行同时为空规则的「无问题」 |
| `severity` | 是 | 无问题时可为 `info` |
| `has_fallback` | 是 | 布尔 |
| `has_rollback` | 是 | 布尔 |
| `duration_ms` | 否 | 无法计算时 `null` |
| `diagnostic_summary_text` | 否 | 来自 `RequestTraceDiagnosticSummary.summary_text`；无则空串 |

**derive 说明**：`primary_issue_*` / `severity` 以 `RequestTraceIssue` 为准；若某次导出未跑分析器，允许用 `RequestTraceSummary.primary_error_*` 降级填充并标注 `attribution_source=summary`（可选扩展字段）。

### 2.2 系统状态区（与单链分离的聚合块）

| 字段 | 必选 | 说明 |
|------|------|------|
| `default_provider` | 是 | 当前主样本：`piper` |
| `window_success_count` 等 | 否 | 时间窗内成功/降级/失败计数；无则占位 `-` |
| `top_issue_types` | 否 | `primary_issue_type` TopN；可由 manifest 或内存聚合 |
| `manifest_date` | 否 | 若基于 manifest：`YYYY-MM-DD` |

## 3. 专业模式（Professional）必需字段

面向：单链排障，**全量下钻**。

### 3.1 包含全部简洁模式字段

- 实现上可嵌入 `RequestTraceConciseView` 或扁平展开，但必须等价可序列化出 §2.1 全部字段。

### 3.2 链体全量

| 字段 / 对象 | 必选 | 说明 |
|-------------|------|------|
| `RequestTraceChain` 全量 | 是 | 含 `stages`、`errors`、`notes`、`raw_observation_refs` 及所有标量 |
| `stages[].key_fields` | 是 | 每阶段完整字典（体积大，仅专业模式） |
| `errors` | 是 | `TraceErrorRecord` 全量列表 |

### 3.3 Issue 与 Diagnostic 全量

| 对象 | 必选 |
|------|------|
| `RequestTraceIssue` | 是（含 `secondary_*`、`recommended_checkpoints`、`notes`） |
| `RequestTraceDiagnosticSummary` | 是（含 `summary_text`、checkpoints） |

### 3.4 引用与归档

| 字段 | 必选 | 说明 |
|------|------|------|
| `raw_observation_refs` | 是 | 来自 chain；无则空数组 |
| `source_observation_type` / `source_ref`（每 stage） | 是 | 随 `stages` 携带 |
| `archive_manifest` | 否 | 若该链已关联某日 `RequestTraceArchiveManifest`，则附带或给 `manifest_date` + `archive_tier` |

## 4. 只在专业模式显示的字段

以下**不得**作为简洁模式默认列或默认卡片主体（允许「展开/二次点击」见展开规则文档）：

- `RequestTraceChain.stages[].key_fields` **全量**（可允许简洁模式显示 `stage_count` 与单阶段摘要占位，不展开键值）
- `raw_observation_refs`
- `notes`（chain 与 issue 的长备注）
- `RequestTraceIssue.secondary_issue_*`、`recommended_checkpoints` 全文（简洁模式最多显示 checkpoint **条数**或首条）
- `RequestTraceDiagnosticSummary.recommended_checkpoints` 全量列表
- 原始 `stderr` / `traceback`（若未来挂到 stage 或 error；当前模型以结构化 `error_reason` 为主）
- `RequestTraceArchiveManifest` 的明细：`chain_ids` 全列表、`provider_counts` 逐键（简洁模式只显示 Top1 provider 或 `default_provider` 对齐结果即可）

## 5. 必须有中文/业务解释的字段（展示层义务）

在 UI/后台首屏或列头，下列字段**不得**仅展示英文 snake_case，须附工具提示或列说明（文案可引用 [字段字典](./LUNA_VOICE_WHITEBOX_FIELD_DICTIONARY_V1.md)）：

- `chain_type`、`final_execution_mode`、`status`（规范化后）、`primary_issue_type`、`severity`
- `has_fallback`、`has_rollback`
- `failed_stage`（专业模式）

## 6. 与代码中的 ViewModel 对应关系

- `RequestTraceConciseView`：对应 §2.1（+ 可选 `attribution_source`）。
- `RequestTraceProfessionalView`：对应 §3（组合 chain + issue + diagnostic + 可选 manifest）。

## 7. 验收对照

- [ ] 简洁单链行字段不少于 §2.1  
- [ ] 专业模式包含 chain 全量 + issue + diagnostic + refs  
- [ ] §4 列出的字段不在简洁默认面展示  
- [ ] 主样本 provider 在系统区显式为 `piper`（与总图文档一致）
