# Luna Voice 错误整合与分析 — 变更清单 V1

## 1. 新增对象与脚本

| 路径 | 说明 |
|------|------|
| `capabilities/voice/observations/request_trace_issue.py` | `RequestTraceIssue`、严重度常量 |
| `capabilities/voice/observations/request_trace_diagnostic_summary.py` | `RequestTraceDiagnosticSummary` |
| `capabilities/voice/observations/request_trace_issue_analyzer.py` | `analyze_request_trace_issue`、规则化检查点表 |
| `tools/analyze_voice_request_issues.py` | CLI：加载链 JSON → 输出 issue + diagnostic |

## 2. 分析器输入

仅 **`RequestTraceChain`**（通常为 `extract_voice_request_trace.py --format json` 产物）。**不**直接读原始 observation 日志。

## 3. 支持的 issue 类型

见 `LUNA_VOICE_ERROR_ANALYSIS_GUIDE_V1.md`：`none`、`provider_unavailable`、`provider_chain_failure`、`request_suppressed`、`playback_failure`、`output_delivery_failure`、`observation_gap`、`unknown_failure`。

## 4. 不支持的高级能力

自动修复、沙盒、影子系统、大模型分析、蜂巢联动、UI、全文搜索、归档、颜色、错误聚类。

## 5. 为什么仍是「最小分析」

- 纯规则与查表，可审计、可单测。  
- 输出结构化，供后续自治与 UI 消费，**本轮不实现**那些能力。

## 6. 后续强化方向（仅列名）

自动修复、沙盒回放、影子对比、蜂巢/大模型根因、归档检索、可视化时间轴、颜色策略。

## 7. 主线—白盒—日志一致性检查

- **A 主线**：分析层不修改主链。  
- **B 白盒**：主因与链阶段语义一致。  
- **C 日志**：依赖抽链落地数据。  
- **D 最终判断**：**主线通顺，白盒一致，日志已落地**。
