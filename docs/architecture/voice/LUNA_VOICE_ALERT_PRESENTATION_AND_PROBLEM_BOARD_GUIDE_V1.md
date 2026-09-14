# LUNA Voice 白盒：展示语义与简洁模式问题区规则 V1

## 1. 为什么需要 alert presentation 层

- **alert_level**（`normal` / `notice` / `warning` / `high_risk` / `critical`）已用于排序与 issue 归类，但仍偏「内部档位」。
- **展示语义**（`ok` / `info` / `attention` / `warning` / `danger`）面向**人读与 UI 挂色**：先定语义标签，**不**在本轮绑定十六进制颜色，避免实现与设计耦合。
- 映射见 `request_trace_alert_presentation.alert_level_to_presentation_semantic`。

## 2. 为什么 problem summary 之后还要 problem board

- **RequestTraceProblemSummary**：单链一条，可排序。
- **RequestTraceConciseProblemBoard**：站在**简洁模式问题区**视角，回答：
  - 顶部 **top_problem** 是谁、为什么是它；
  - **active_problems**（有限条）与 **已兜住**、**低优先/抑制**如何**分栏**，避免平铺与重复堆叠。

## 3. 简洁模式问题区如何组织

| 区块 | 含义 | 规则要点 |
|------|------|----------|
| **top_problem** | 当前最值得关注的一条 | 见 `request_trace_top_problem_selector`；无则文案说明「无高优先级」 |
| **active_problems** | 需优先跟进的失败/风险（不含已兜住/抑制/纯成功） | 默认最多 **5** 条（可调） |
| **degraded_but_handled** | 降级或回退但已产出/已救回 | fallback 降级成功、rollback 成功等 |
| **suppressed_or_low_priority** | 治理抑制或纯成功等弱提醒 | 单独收口，不与主失败混排 |
| **counts_*** | 分布概览 | 来自 `request_trace_problem_aggregator` |

构建入口：`build_concise_problem_board(...)`（`request_trace_concise_problem_board.py`）。

**去重**：`top_problem` 若同时属于「已兜住」类，只在顶部展示一次，**不会**再在 `degraded_but_handled` 中重复出现。

## 4. top_problem 如何选

1. 对输入全集调用 `prioritize_problems`（继承既有 `priority_score` 规则）。
2. 在排序结果中选取**第一条非「纯成功噪声」**（`alert_level==normal` 且 `primary_issue_type==none`）。
3. 若全部为纯成功，**top_problem = None**，原因字符串说明当前无高优先级问题。
4. **原因说明**（`top_problem_reason`）拼接：分数档位、alert、是否需行动、是否影响默认主样本 `piper`、是否 `failed_no_output`、在排序中的位次等（见 `request_trace_top_problem_selector`）。

## 5. 问题聚合（最小规则）

- `request_trace_problem_aggregator.aggregate_problems`：按 `alert_level`、`primary_issue_type`、`provider_name`、`final_execution_mode` 计数。
- 附加指标：`most_common_issue_type`、`affects_main_provider_count`（`provider_name==piper` 且 alert 为 warning/high_risk/critical）、已兜住/抑制计数等。

## 6. 展示语义与 alert_level 的映射（固定表）

| alert_level | presentation semantic |
|-------------|------------------------|
| normal | ok |
| notice | info |
| warning | attention |
| high_risk | warning |
| critical | danger |

## 7. 本轮明确不做什么

- 真实 **CSS/十六进制颜色**、页面组件、前端交互
- **搜索增强**、自动修复、蜂巢联动、大模型
- 改主链、改抽链/分析/归档主逻辑

## 8. 关联文件

| 内容 | 路径 |
|------|------|
| 展示语义 | `capabilities/voice/observations/request_trace_alert_presentation.py` |
| 聚合 | `request_trace_problem_aggregator.py` |
| Top 选择 | `request_trace_top_problem_selector.py` |
| 问题区模型 | `request_trace_concise_problem_board.py` |
| CLI | `tools/build_voice_problem_board.py` |
