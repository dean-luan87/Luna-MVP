# LUNA Voice 白盒：异常分级与问题提炼说明 V1

## 1. 为什么在 issue / diagnostic 之外还需要 problem summary

- **Issue**：链级归因结论，字段多、面向排障，适合专业模式全量阅读。
- **Diagnostic**：短模板句，偏英文/结构化，仍是一条链一个块。
- **Problem summary（本轮）**：在两者之上再压一层——**统一展示等级（alert_level）**、**中文一句人话**、**是否需行动**、**可排序的 priority_score**，使「多条链并列」时能回答：**先看哪条、为什么它更重要**。

简洁模式若只平铺 issue_type，仍缺少「首页级」的**可比优先级**；problem summary 填补这一层，且与后续颜色、搜索排序、归档摘要**同构**（本轮不实现颜色与搜索）。

## 2. alert level 与 severity 的区别

| 维度 | severity（底层） | alert_level（展示层） |
|------|------------------|------------------------|
| 来源 | `request_trace_issue_analyzer` 规则输出 | `request_trace_alert_level.presentation_alert_level_from_issue` |
| 取值 | `info` / `warning` / `degraded` / `error` / `critical` | `normal` / `notice` / `warning` / `high_risk` / `critical` |
| 作用 | 与分析器分支一致，便于对照代码 | **面向白盒列表/首页**，与 severity 有映射，且可按**终态**（如 rollback_success）覆盖 |
| 关系 | 保留，不删除 | 叠加上去；默认有 `severity_to_alert_level` 表，场景可覆盖 |

## 3. problem summary 当前作用

- 一条链对应 **一条** `RequestTraceProblemSummary`（`problem_id` 区分请求与类型）。
- **中文 `summary_text`**：规则模板，覆盖成功 / fallback / rollback / 抑制 / 无输出等典型句（见 `request_trace_problem_extractor`）。
- **`priority_score` + `priority_reason`**：规则化分数与可解释片段，支持多链排序与「当前最值得关注」= `most_critical_problem(...)`。

## 4. 优先级排序当前规则（规则化、无学习）

实现见 `request_trace_problem_prioritizer.compute_priority_score`，主要考虑：

1. **alert_level**（权重最高档）
2. **final_execution_mode == failed_no_output**（无有效输出路径）
3. **issue 类型**为 `playback_failure` / `output_delivery_failure`
4. **主样本路径**：`provider_name == piper` 且 alert 已偏高时加权（主链健康视角）
5. **chain_type** 含 fallback / rollback 路径时加分
6. **is_action_required**
7. **ended_at 新鲜度**（越新略优先）

排序：**分数降序**，同分稳定按 `request_id`、`problem_id`。

## 5. 本轮明确不做什么

- 不做真实**颜色 UI**、不做页面
- 不做**自动修复**、沙盒、影子系统
- 不做**大模型**生成摘要或排序
- 不做**搜索系统强化**、服务器归档联动
- **不改**主链、抽链器、分析器、归档主逻辑（本层仅消费其输出）

## 6. 关联代码与文档

| 内容 | 位置 |
|------|------|
| Alert 等级常量与映射 | `capabilities/voice/observations/request_trace_alert_level.py` |
| 问题摘要对象 | `request_trace_problem_summary.py` |
| 提炼器 | `request_trace_problem_extractor.py` |
| 排序器 | `request_trace_problem_prioritizer.py` |
| CLI | `tools/summarize_voice_request_problems.py` |
| 变更清单 | [LUNA_VOICE_ALERT_AND_PROBLEM_SUMMARY_CHANGESET_V1.md](./LUNA_VOICE_ALERT_AND_PROBLEM_SUMMARY_CHANGESET_V1.md) |
