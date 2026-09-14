# LUNA Voice 白盒字段语义字典 V1

## 0. 文档定位

- 给人看的**语义层**：字段含义、来源、典型取值、异常含义。
- 不是代码自动生成的字段列表照抄；与实现不一致时以代码为准并应回修本字典。
- 关联文档：[双模式总图](./LUNA_VOICE_WHITEBOX_VIEW_MODES_V1.md)、[数据契约](./LUNA_VOICE_WHITEBOX_VIEW_CONTRACT_V1.md)、[展开规则](./LUNA_VOICE_WHITEBOX_EXPANSION_RULES_V1.md)。

## 1. 优先说明字段（跨对象）

以下字段在简洁/专业两模式中出现频率高，优先读懂。

| 字段名 | 中文解释 | 所属对象 | 来源 | 典型取值 | 异常时代表什么 |
|--------|----------|----------|------|----------|----------------|
| `chain_type` | 本条链在抽链器眼里的**拓扑归类**（成功主链 / 降级分叉 / 回退 / 失败 / 抑制等） | `RequestTraceChain`、`RequestTraceIssue`、`RequestTraceDiagnosticSummary`、`RequestTraceSummary.chain_type_raw` | 抽链规则根据 observation 序列与终态推断 | `success_chain`、`provider_fallback_chain`、`legacy_rollback_chain`、`failed_chain`、`suppressed_chain`、`unknown` | `unknown`：证据不足或新路径未归类；`failed_chain`/`suppressed_chain`：需结合 issue 看根因 |
| `provider_name` | 本条链上**主叙事对应的 TTS provider**（常与 selection 一致） | `RequestTraceChain`、`RequestTraceSummary`、`RequestTraceIssue` | 来自链上 provider 相关 stage / observation 汇总 | `piper`、`piper`、空 | 空：入口未记录或抽链未命中；与「当前主样本 piper」对比可判断是否为分叉样本 |
| `final_execution_mode` | **最终执行路径模式**（以 cutover/收口观测为准的粗粒度终态） | `RequestTraceChain`、`RequestTraceSummary`、`RequestTraceIssue` | `TTSCutoverObservation.final_execution_mode` 等收口字段 | `provider_chain`、`legacy_fallback`、`failed_no_output` 等（以实现为准） | 与 `status`/issue 组合看：例如长期 `failed_no_output` 升高说明输出侧系统性问题 |
| `status` | **链级健康度**（抽链原始） | `RequestTraceChain.status`（`status_raw` 在 Summary 中） | 抽链器按阶段与错误聚合 | `ok`、`partial`、`failed`、`suppressed` | `partial`：查询层常映射为 `unknown`，需专业模式看 stages；`suppressed`：多为策略/治理抑制 |
| `primary_issue_type` | **主问题类型**（规则化归因码） | `RequestTraceIssue`、`RequestTraceDiagnosticSummary` | `request_trace_issue_analyzer` 规则输出 | `none`、`provider_unavailable`、`provider_chain_failure`、`request_suppressed`、`playback_failure` 等 | `observation_gap`：观测缺失；`unknown_failure`：规则未能归类 |
| `primary_issue_reason` | **主问题一句话原因**（可与 checkpoint 对照） | 同上 | 分析器模板/规则拼接 | 短英文或短语原因 | 空且 `primary_issue_type` 非 `none`：展示层应提示「待补全」并下钻 stages |
| `failed_stage` | **最先失败或最关键的失败阶段名** | `RequestTraceIssue`、`RequestTraceDiagnosticSummary` | 分析器从 `errors` 或 `fail` stage 推断 | 与 `TraceStageRecord.stage_name` 同命名空间 | 空：失败点未落到单 stage 或仅有链级错误 |
| `severity` | **严重度档位**（供后续颜色/排序；本阶段仅为字符串） | `RequestTraceIssue`、`RequestTraceDiagnosticSummary` | 分析器规则 | `info`、`warning`、`degraded`、`error`、`critical` | 简洁模式里 `error`/`critical` 应优先冒泡；与 status 冲突时以 issue 为准做展示 |
| `has_fallback` | **是否发生 provider 降级/旁路**（含链类型或观测双重推断） | `RequestTraceIssue`、`RequestTraceSummary` | Summary：`chain_type` 与 stage 中 `ProviderFallbackObservation` 等 | `true`/`false` | 在 Piper 主样本下 `true` 多表示主 provider 失败后的补救路径 |
| `has_rollback` | **是否发生 TTS 回退链路** | `RequestTraceIssue`、`RequestTraceSummary` | Summary：`legacy_rollback` 或 `TTSRollbackObservation` | `true`/`false` | 短时暴涨需对照 provider/网络/音频管线 |
| `request_id` | **业务请求唯一标识**（白盒主键之一） | 几乎所有对象 | 入口 `SpeechRequest` / 观测携带 | 非空字符串 | 空：非法导出，链不可关联 |
| `trace_id` | **分布式追踪 ID**（可选，与日志/观测对齐） | `RequestTraceChain`、`RequestTraceSummary`、`RequestTraceIssue` | 入口注入或运行时生成 | UUID 或项目约定格式 | 空：仅能靠 `request_id` 关联；跨系统排障变难 |
| `started_at` | **链开始时间**（Unix 秒，浮点） | `RequestTraceChain`、`RequestTraceSummary` | 来自最早相关观测时间戳 | 数值 | 缺失则无法算 `duration_ms` |
| `ended_at` | **链结束时间** | 同上 | 来自收口或最后观测 | 数值 | 早于 `started_at`：数据异常 |
| `duration_ms` | **耗时（毫秒）** | `RequestTraceSummary`（计算字段） | `ended_at - started_at` | ≥0 的浮点 | 异常大：结合阶段与 provider；缺失：起止时间不全 |

## 2. RequestTraceChain

| 字段名 | 中文解释 | 来源 | 典型取值 | 异常时代表什么 |
|--------|----------|------|----------|----------------|
| `request_id` | 见 §1 | 抽链聚合 | 非空 | 空则该链无效 |
| `trace_id` | 见 §1 | 观测 | 可选 | — |
| `session_id` | 会话级 ID（若入口有） | `SpeechRequest` 等 | 字符串或空 | 空：仅单请求维度 |
| `task_context_id` | 任务/场景上下文 ID | 入口或编排层 | 字符串或空 | 空：无法按任务分桶 |
| `chain_type` | 见 §1 | 抽链推断 | 枚举字符串 | 见 §1 |
| `final_execution_mode` | 见 §1 | cutover/收口 | 见 §1 | 见 §1 |
| `provider_name` | 见 §1 | selection/执行汇总 | `piper` 等 | 见 §1 |
| `started_at` / `ended_at` | 见 §1 | 观测时间 | 浮点 | 见 §1 |
| `status` | 见 §1 | 抽链聚合 | `ok`/`partial`/… | `partial` 需下钻 |
| `stages` | **有序阶段列表**（每段一条 `TraceStageRecord`） | 多类 observation 映射 | 非空列表为主路径 | 空：无阶段或抽链失败 |
| `errors` | **结构化错误列表** | 失败阶段与链级错误 | 可为空 | 非空：专业模式必展示 |
| `notes` | **抽链器备注**（非用户文案） | 抽链器 | 短句列表 | 可提示推断不确定性 |
| `raw_observation_refs` | **原始观测引用**（文件/行等） | 导出脚本 | 字符串列表 | 空：无可回溯引用 |

### 2.1 TraceStageRecord（阶段行）

| 字段名 | 中文解释 | 来源 | 典型取值 | 异常时代表什么 |
|--------|----------|------|----------|----------------|
| `stage_name` | 逻辑阶段名（与 pipeline 阶段对齐） | 映射表/抽链 | 如 `provider_selection` | 未知名：映射未更新 |
| `status` | 该阶段是否完整、跳过、失败等 | 观测覆盖度 | `ok`、`fail`、`missing`、`partial`、`skipped` 等 | `fail`/`missing`：专业模式优先看 `key_fields` |
| `timestamp` | 阶段时间 | 观测 | 浮点或空 | 空：无法做阶段级耗时 |
| `key_fields` | **阶段关键结构化字段**（体积可能大） | 各 observation 拆出 | 字典 | 异常键值对往往直接指向根因 |
| `source_observation_type` | 该阶段主要来源观测类型名 | 类名 | 如 `ProviderSelectionObservation` | 空：来源不明 |
| `source_ref` | 代码或文件引用 | 开发者标注 | `file:line` 等 | 空：不便跳转源码 |

### 2.2 TraceErrorRecord（错误行）

| 字段名 | 中文解释 | 来源 | 典型取值 | 异常时代表什么 |
|--------|----------|------|----------|----------------|
| `stage_name` | 错误归属阶段 | 抽链 | 与 stage 对齐 | 空：链级错误 |
| `error_type` | 错误类型码 | 规则/观测 | 短字符串 | 新类型未入字典时需人工读 `error_reason` |
| `error_reason` | 可读原因 | 同上 | 短语 | 空：信息不足 |
| `severity` | 该条错误级别 | 规则 | `info`/`warning`/`error` | `error`：应进入 issue 候选 |

## 3. RequestTraceSummary

查询层摘要：**不替代** `RequestTraceIssue`，便于列表过滤与排序。

| 字段名 | 中文解释 | 来源 | 典型取值 | 异常时代表什么 |
|--------|----------|------|----------|----------------|
| `chain_type_raw` | 原始 `chain_type` 字符串 | `RequestTraceChain` | 同 `chain_type` | — |
| `chain_type` | **规范化短名**（供查询） | `normalize_chain_type_for_query` | `success`、`provider_fallback` 等 | 未映射值：直接透传需关注 |
| `status_raw` | 原始 `status` | Chain | `ok`/`partial`/… | — |
| `status` | **规范化状态** | `normalize_status_for_query` | `success`、`degraded_success`、`failed` 等 | `unknown`：多来自 `partial` |
| `primary_error_type` / `primary_error_reason` | 从 `errors` 或失败 stage 推断的**主错误** | `_primary_failure` | 字符串或空 | 与 issue 不一致时以 issue 为展示主口径 |
| `stage_count` | 阶段数量 | `len(stages)` | ≥0 | 0：空链 |
| `has_fallback` / `has_rollback` | 见 §1 | 推断函数 | 布尔 | 见 §1 |
| `failure_type` | 与 `primary_error_type` 对齐，便于过滤 | 同上 | 同 error_type 或空 | — |
| `notes` | 来自 chain 的备注 | Chain | 列表 | 简洁模式可折叠 |

## 4. RequestTraceIssue

链级**归因结论**，供「问题摘要区」与专业模式全文使用。

| 字段名 | 中文解释 | 来源 | 典型取值 | 异常时代表什么 |
|--------|----------|------|----------|----------------|
| `final_status` | **归因后的终态语义**（比 raw `status` 更贴近业务） | 分析器 | `success`、`degraded_success`、`rollback_success`、`suppressed`、`failed`、`unknown` | 与 `RequestTraceSummary.status` 并用时优先展示本字段 |
| `secondary_issue_type` / `secondary_issue_reason` | 次要问题 | 分析器 | 可选 | 非空：存在并发或次要故障 |
| `recommended_checkpoints` | **建议排查检查点**（短句列表） | 规则模板 | 字符串列表 | 空：仍可依 `primary_issue` 排障 |
| `notes` | 分析器备注 | 规则 | 列表 | — |

（`request_id`、`trace_id`、`chain_type`、`provider_name`、`final_execution_mode`、`primary_issue_type`、`primary_issue_reason`、`failed_stage`、`severity`、`has_fallback`、`has_rollback` 见 §1。）

## 5. RequestTraceDiagnosticSummary

比 `RequestTraceIssue` **更短**的展示块，偏「一眼跟进」。

| 字段名 | 中文解释 | 来源 | 典型取值 | 异常时代表什么 |
|--------|----------|------|----------|----------------|
| `summary_text` | **规则模板填充的一小段中文/英文摘要** | 固定模板 + 字段替换 | 单段文本 | 空：未生成摘要（应回退 issue） |
| `recommended_checkpoints` | 同 issue，可裁剪重复 | 规则 | 列表 | 见上 |

（其余字段与 issue 对齐，见 §1。）

## 6. RequestTraceArchiveManifest

按日归档索引：**系统状态区**与「归档查询区（后续）」用。

| 字段名 | 中文解释 | 来源 | 典型取值 | 异常时代表什么 |
|--------|----------|------|----------|----------------|
| `date` | 归档日期 | 归档任务 | `YYYY-MM-DD` | 格式错：无法按日聚合 |
| `version` | manifest 结构版本 | 常量 | `v1` | — |
| `created_at` / `updated_at` | 写入/更新时间 | 归档脚本 | 浮点或空 | — |
| `total_chain_count` | 当日链条数 | 统计 | ≥0 | 与列表长度严重不符：计数逻辑问题 |
| `chain_ids` | 当日 `request_id` 列表（或约定 ID） | 归档 | ID 列表 | 过大：仅应用缩略或分页 |
| `provider_counts` | 各 provider 出现次数 | 统计 | `{"piper":n,...}` | 无 `piper`：与主样本假设冲突时需解释 |
| `issue_type_counts` | 各 `primary_issue_type` 次数 | 统计/退化推断 | 字典 | — |
| `rollback_count` / `fallback_count` | 当日回退/降级次数 | 统计 | ≥0 | 陡增：与简洁模式「关键问题摘要」联动 |
| `archive_tier` | **存储层级**（热/待备份） | `compute_archive_tier` 等 | `hot`、`pending_backup` | `pending_backup`：仅表示龄期，非已备份 |
| `backup_status` | 备份状态占位 | 常量 | `pending` 等 | 本轮不实现真实备份 |

## 7. 关键 observation 字段（节选）

仅列复盘最常用的字段；完整映射见 [LUNA_VOICE_WHITEBOX_OBSERVATION_MAPPING_V1.md](./LUNA_VOICE_WHITEBOX_OBSERVATION_MAPPING_V1.md)。

| 字段名 | 中文解释 | 所属 observation | 来源 | 典型取值 | 异常时代表什么 |
|--------|----------|------------------|------|----------|----------------|
| `chosen_provider` | 被选中的 provider | `ProviderSelectionObservation` | runtime 选择 | `piper` | 非 piper：分叉样本（如 Fish） |
| `provider_order` | 尝试顺序 | 同上 | 配置+运行时 | 列表 | 顺序异常：配置错误 |
| `selection_reason` | 选择原因简述 | 同上 | 策略 | 短字符串 | 空：难解释为何选此 provider |
| `final_execution_mode` | 终态执行模式 | `TTSCutoverObservation` | 收口逻辑 | 见 §1 | 见 §1 |
| `provider_chain_ok` | provider 链是否整体成功 | `TTSCutoverObservation` | 收口 | `true`/`false` | `false`：结合 fallback/rollback |
| `selector_hit` | 是否命中 selector 路径 | `TTSCutoverObservation` | 路由 | 布尔 | 与路由实验相关 |
| `primary_provider` / `fallback_provider` | 主/备 provider（命名以实装为准） | `ProviderFallbackObservation` | 失败触发 | 字符串 | 仅 fallback 链有值 |
| `rollback_reason` 等 | 回退原因 | `TTSRollbackObservation` | 失败触发 | 字符串 | 专业模式看全量 |

## 8. 主线—白盒—日志一致性

- **主线**：字段语义不改变运行时行为。
- **白盒**：展示与字典一致，优先 `piper` 主样本叙事。
- **日志**：`request_id`/`trace_id` 为关联主键；`raw_observation_refs` 用于回到导出文件。
