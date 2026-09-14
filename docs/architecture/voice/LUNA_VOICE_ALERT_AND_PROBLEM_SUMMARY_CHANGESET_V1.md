# LUNA Voice 白盒阶段-5：异常分级与问题提炼 — 变更清单 V1

## 1. 新增对象 / 脚本

| 路径 | 说明 |
|------|------|
| `capabilities/voice/observations/request_trace_alert_level.py` | 展示层 `alert_level` 常量、`severity_to_alert_level`、`presentation_alert_level_from_issue`、`ALERT_LEVEL_SORT_WEIGHT` |
| `capabilities/voice/observations/request_trace_problem_summary.py` | `RequestTraceProblemSummary` 最小摘要结构（含 `priority_score`、`priority_reason`、`ended_at`） |
| `capabilities/voice/observations/request_trace_problem_extractor.py` | `extract_problem_summary(chain, issue, diagnostic)`、`extract_problem_summary_from_parts(...)` |
| `capabilities/voice/observations/request_trace_problem_prioritizer.py` | `compute_priority_score`、`prioritize_problems`、`top_k_problems`、`most_critical_problem` |
| `tools/summarize_voice_request_problems.py` | 从目录/文件读 chain JSON → 分析 → 摘要 → 排序 → JSON 或文本 |
| `tests/test_request_trace_problem_summary.py` | 提炼与排序回归 |
| `docs/architecture/voice/LUNA_VOICE_ALERT_AND_PROBLEM_SUMMARY_GUIDE_V1.md` | 设计说明 |
| 本文件 | 变更清单 |

## 2. alert level 如何定义

- **五档**：`normal` / `notice` / `warning` / `high_risk` / `critical`。
- **与 severity 默认映射**：`info→normal`，`warning→notice`，`degraded→warning`，`error→high_risk`，`critical→critical`。
- **场景覆盖**（优先于默认映射）：无输出/播放类 issue → `critical`；抑制 → `notice`；纯成功 → `normal`；fallback 降级成功 → `warning`；rollback 成功 → `high_risk` 等（见 `presentation_alert_level_from_issue`）。

## 3. problem summary 如何提炼

- **输入**：`RequestTraceChain` + `RequestTraceIssue` + `RequestTraceDiagnosticSummary`（与现有 `analyze_request_trace_issue` 输出衔接）。
- **输出**：填充 `RequestTraceProblemSummary`；`status` 使用 `build_request_trace_summary(chain).status`。
- **summary_text**：规则化**中文**短句（成功 / fallback / rollback / 抑制 / 无输出等）；未命中模板时退回 diagnostic 英文摘要截断 + 标记。
- **is_action_required**：rollback 成功、无输出类为 `true`；纯成功、抑制、fallback 成功等为规则表中的 `false/true`。
- **problem_id**：`{request_id}:{primary_issue_type}:{trace_id|notrace}`。

## 4. priority_score 如何计算

- **整数分**，越大越优先；由 `compute_priority_score` 单条计算，`prioritize_problems` 统一重算并排序。
- **因子**：alert 档位权重 × 2000、`failed_no_output` +5000、playback/delivery issue +3500、piper 且已偏高 +1500、fallback/rollback 路径加权、`is_action_required` +600、24h 内新鲜度最多约 +400。
- **priority_reason**：拼接主要加分项短句，便于验收与日志（非自然语言生成）。

## 5. 当前支持的问题摘要类型（规则侧）

| 类型 | alert_level（典型） | summary_text（典型） |
|------|----------------------|----------------------|
| 正常成功 | normal | 链级成功，无归因问题。 |
| fallback 成功 | warning | 主 provider 失败，已由 fallback provider 成功接管。 |
| rollback 成功 | high_risk | provider chain 失败，已回滚到 legacy。 |
| 被抑制 | notice | 请求被治理层抑制，未进入执行链。 |
| 播放失败 / 无输出 | critical | 请求未形成有效播报输出。 |
| 观测缺口 / 未归类 | notice 或模板退化 | 见提炼器分支 |

## 6. 后续强化方向（不在本轮）

- **颜色**：alert_level → 色板（仅映射，本轮无 UI）
- **首页 / 简洁模式**：直接消费 `RequestTraceProblemSummary` 列表或 `most_critical_problem`
- **搜索 / 归档**：按 `priority_score`、`alert_level` 排序与过滤
- **自动修复入口**：依赖 issue checkpoint，不在本轮
- **蜂巢 / 大模型**：不参与排序与摘要

## 7. 边界确认

- **未修改**：`request_trace_issue_analyzer.py` 主逻辑、`request_trace_extractor.py`、主链、归档主流程。
- **未新增**：页面、颜色实现、LLM 调用、搜索索引。
