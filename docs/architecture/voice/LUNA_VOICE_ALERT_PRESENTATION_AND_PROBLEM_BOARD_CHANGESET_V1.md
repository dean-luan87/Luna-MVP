# 白盒阶段-6：展示语义与简洁模式问题区 — 变更清单 V1

## 1. 新增对象 / 脚本

| 路径 | 说明 |
|------|------|
| `capabilities/voice/observations/request_trace_alert_presentation.py` | `alert_level` → 展示语义 `ok/info/attention/warning/danger` |
| `capabilities/voice/observations/request_trace_problem_aggregator.py` | 最小聚合：`aggregate_problems`、分桶辅助函数 |
| `capabilities/voice/observations/request_trace_top_problem_selector.py` | `select_top_problem` + 中文原因 |
| `capabilities/voice/observations/request_trace_concise_problem_board.py` | `RequestTraceConciseProblemBoard`、`build_concise_problem_board` |
| `tools/build_voice_problem_board.py` | 读 chain JSON → 问题摘要 → 问题区 JSON |
| `tests/test_concise_problem_board.py` | 构建与分桶回归 |
| `docs/.../LUNA_VOICE_ALERT_PRESENTATION_AND_PROBLEM_BOARD_GUIDE_V1.md` | 设计说明 |
| 本文件 | 变更清单 |

## 2. alert presentation 如何定义

- **只做语义标签**，不含颜色值。
- **映射**：`normal→ok`，`notice→info`，`warning→attention`，`high_risk→warning`，`critical→danger`（`alert_level_to_presentation_semantic`）。
- 未知 `alert_level` 默认映射为 `info`，避免误标成 `ok`。

## 3. problem board 如何组织

- **输入**：`List[RequestTraceProblemSummary]`（通常由 `extract_problem_summary` 产出）。
- **输出**：`RequestTraceConciseProblemBoard`，含 `top_problem`、`active_problems`（上限默认 5）、`degraded_but_handled`、`suppressed_or_low_priority`、计数与 `ProblemAggregationSummary`。
- **分桶规则**：见 `request_trace_problem_aggregator` 中 `is_degraded_but_handled` / `is_suppressed_or_low_priority` / `is_pure_success_noise`。
- **与 top 去重**：`top_problem` 的 `problem_id` 会从 `degraded_but_handled` 列表中剔除，避免同一条在顶部与分组重复。

## 4. top_problem 如何提炼

- 全量 `prioritize_problems` 后，**第一条非纯成功**即为 `top_problem`；若无非纯成功则 `None`。
- **原因**：`request_trace_top_problem_selector._explain_top` 生成中文说明。

## 5. 当前不支持的高级能力

- 复杂聚类、相似问题合并（仅 Counter 级聚合）
- 时间窗内「持续发生」检测（未实现；可后续用 manifest/时间序列）
- 真实颜色主题、组件库、交互

## 6. 后续强化方向

- **真实颜色**：`presentation_semantic` → 设计 token / CSS 变量
- **首页 UI**：直接消费 `RequestTraceConciseProblemBoard.to_dict()`
- **搜索增强**：对 `active_problems` / 聚合字段建索引
- **蜂巢分析**：聚合结果上送分析层（本层不调用 LLM）

## 7. 边界

- **未修改**：主链、`request_trace_issue_analyzer` 主逻辑、抽链与归档主流程。
- **未新增**：前端页面、自动修复、大模型调用。
