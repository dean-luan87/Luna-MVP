# LUNA Voice 白盒视图双模式（Concise / Professional）V1

## 0. 文档定位

本文件定义“白盒怎么看”，不是做 UI，也不是改主链。

当前白盒底层能力已经具备：
- 抽链：`RequestTraceChain`
- 摘要：`RequestTraceSummary`
- 问题归因：`RequestTraceIssue`
- 诊断摘要：`RequestTraceDiagnosticSummary`
- 归档与查询：`whitebox_archive/` + `tools/query_voice_request_traces.py`

但现状问题是字段堆叠、语义不清，导致“能看见但难用”。因此需要把展示层固定为**两种信息层级**：
- **简洁模式（Concise Mode）**：先给结论与运行态
- **专业模式（Professional Mode）**：下钻到单链与阶段细节

## 1. 为什么需要两种模式

### 1.1 现状痛点
- **信息层级没分开**：底层字段平铺适合排底层问题，但不适合日常扫健康度。
- **字段缺语义解释**：字段名没有中文解释、来源与异常含义，导致看不懂。

### 1.2 目标收益
- 简洁模式：一眼回答“系统是否健康/当前主链/主要风险/关键问题”。
- 专业模式：一条链一条链看“走到哪一段、为什么失败/抑制/回退、最终有没有播出去”。

## 2. 两种模式的职责边界

### 2.1 简洁模式（Concise Mode）

**回答的问题（必须）**
- 当前系统是否正常（成功/降级/失败概况）
- 当前主链 provider 是谁（当前主样本）
- 当前最重要的问题摘要是什么（按 issue_type 聚合）
- fallback / rollback 是否异常升高（趋势入口占位）
- 最近链摘要列表（最小诊断摘要）

**默认不显示（必须不显示）**
- 原始 observation
- stage `key_fields` 全量
- 原始 `stderr/traceback`
- 大段配置快照

### 2.2 专业模式（Professional Mode）

**回答的问题（必须）**
- 单条链：逐阶段发生了什么（stages + key_fields）
- provider 选择/执行细节（selection/execution）
- 错误链与收口（errors + checkpoints）
- fallback / rollback 的分叉细节
- 归档元数据与来源引用（source refs / archive tier）

## 3. 当前白盒展示结构建议（按“怎么看”组织）

### 3.1 简洁模式布局（建议 4 区）
1) **系统状态区**
- 当前默认 provider（主样本）
- 最近成功/降级/失败计数（按归档/时间窗口聚合，当前可由 manifest/查询结果生成）
- 当前关键异常摘要（按 `primary_issue_type` 聚合）

2) **最近链摘要区**
- `request_id`
- `chain_type`
- `provider_name`
- `final_execution_mode`
- `status`
- `primary_issue_type / primary_issue_reason`
- `severity`
- `has_fallback / has_rollback`
- `duration_ms`

3) **关键问题摘要区**
- issue_type TopN
- fallback/rollback 计数与变化入口（趋势后置，不在本轮实现）

4) **待展开入口**
- 点击某条链 → 进入专业模式（单链详情）

### 3.2 专业模式布局（建议 5 区）
1) **链基本信息**
- request/trace/session/task_context
- chain_type/status/provider/mode/time

2) **Issue / Diagnostic**
- `RequestTraceIssue` 全量字段
- `RequestTraceDiagnosticSummary`（更短的行动入口）

3) **阶段链（Stage Timeline）**
- stages 列表 + 每 stage 的 key_fields
- stage 的 `source_observation_type` / `source_ref`

4) **Fallback / Rollback / Failure 细节**
- provider chain 失败原因（failure_type / reason / detail）
- checkpoints（规则化，不自由文本）

5) **关联引用与归档信息**
- `raw_observation_refs`
- archive tier / manifest 关联（后续可展示）

### 3.3 归档查询区（后续落地）

- **定位**：按日 manifest、provider/issue 分布、fallback/rollback 计数；**不**替代单链专业模式。
- **数据来源**：`RequestTraceArchiveManifest` + `tools/query_voice_request_traces.py` 的查询结果。
- **与简洁模式关系**：系统状态区可引用 manifest 聚合；点选某日/某过滤条件后再进入「最近链摘要」列表（仍为简洁行），单链下钻仍走专业模式。
- **详细字段语义**：见 [LUNA_VOICE_WHITEBOX_FIELD_DICTIONARY_V1.md](./LUNA_VOICE_WHITEBOX_FIELD_DICTIONARY_V1.md) §6。

## 4. 当前 provider 主样本声明（必须）

- **当前主样本 provider = `piper`**（现实可用主链）
- Fish / fallback / rollback 是重要分叉链（可诊断），但**不是默认主样本**
- 因此简洁模式默认以 Piper 主链健康度为主视角展示

## 5. 关联文档（本轮交付）

| 文档 | 内容 |
|------|------|
| [LUNA_VOICE_WHITEBOX_FIELD_DICTIONARY_V1.md](./LUNA_VOICE_WHITEBOX_FIELD_DICTIONARY_V1.md) | 字段语义字典 |
| [LUNA_VOICE_WHITEBOX_VIEW_CONTRACT_V1.md](./LUNA_VOICE_WHITEBOX_VIEW_CONTRACT_V1.md) | 简洁/专业数据契约 |
| [LUNA_VOICE_WHITEBOX_EXPANSION_RULES_V1.md](./LUNA_VOICE_WHITEBOX_EXPANSION_RULES_V1.md) | 模式切换与展开规则 |

轻量视图模型（可选消费）：`capabilities/voice/observations/request_trace_concise_view.py`、`request_trace_professional_view.py`。

## 6. 主线—白盒—日志一致性检查（交付要求）

- A 主线：本文件仅定义视图模式与展示结构，不改主链执行逻辑。
- B 白盒：两种模式都以链对象为中心（`RequestTraceChain/Summary/Issue/Diagnostic`），不回退到模块堆叠。
- C 日志：展示数据来自抽链产物与归档产物（`whitebox_archive`），非直接扫原始 logs。
- D 最终判断：主线通顺，白盒一致，日志已落地。

