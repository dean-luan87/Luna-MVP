# Luna Voice 链级错误整合与原因分析说明 V1

## 1. 为什么需要链级问题分析

单条异常字符串无法回答：**同一 `request_id` 在输出链上经历了 fallback、rollback 还是抑制**。  
链级分析把 `RequestTraceChain` 上的 **provider 失败、fallback、rollback、抑制、播放/交付失败、观测缺口** 收束为 **一个主因类型 + 可执行检查点**，便于后续白盒、查询脚本、UI 复用。

## 2. `RequestTraceIssue` 与 `RequestTraceDiagnosticSummary` 的区别

| 对象 | 侧重 |
|------|------|
| **RequestTraceIssue** | **归因**：主因/次因、`failed_stage`、`severity`、完整 `recommended_checkpoints`、备注 |
| **RequestTraceDiagnosticSummary** | **排查入口**：短摘要 `summary_text`、关键字段并列，便于列表与快速定位 |

二者由同一分析器一次生成；`summary_text` 为规则模板填充，**非大模型生成**。

## 3. 当前支持的 `primary_issue_type`

| 类型 | 含义（链级） |
|------|----------------|
| `none` | 成功链，无结构级问题 |
| `provider_unavailable` | 主 provider 失败，fallback 已产出有效路径（降级成功） |
| `provider_chain_failure` | 配置链上 provider 均失败，已走 legacy rollback 且链路收口为成功 |
| `request_suppressed` | 请求在进 provider 前被抑制 |
| `playback_failure` | 合成或链路已指向播放，但播放/终态表明未完成 |
| `output_delivery_failure` | `failed_no_output` 等且无有效交付 |
| `observation_gap` | 多阶段缺失/未连接，日志覆盖不足 |
| `unknown_failure` | 未命中规则 |

## 4. `recommended_checkpoints` 如何生成

完全 **规则表**：按 `primary_issue_type` 映射到固定中文检查项列表（见 `request_trace_issue_analyzer.checkpoints`）。  
不调用模型、不根据用户自然语言改写。

## 5. 严重度 `severity`

规则化枚举：`info` | `warning` | `degraded` | `error` | `critical`（**不做颜色**；后续 UI 可挂接）。

## 6. 当前不支持什么

- 自动修复、自动改配置、自动重试  
- 沙盒回放、影子系统  
- 大模型 / 蜂巢分析  
- UI、搜索增强、归档、颜色分级  

## 7. 入口脚本

```bash
python3 tools/analyze_voice_request_issues.py --input-dir docs/architecture/voice/fixtures/extracted
python3 tools/analyze_voice_request_issues.py --input-file path/to/chain.json --format json
python3 tools/analyze_voice_request_issues.py --input-dir docs/architecture/voice/fixtures/extracted --request-id fixture_piper_ok_001
```

## 8. 主线—白盒—日志一致性检查

- **A 主线**：输入为已抽链的 `RequestTraceChain`，不绕主链。  
- **B 白盒**：主因与阶段、链型一致。  
- **C 日志**：依赖抽链 JSON 与 `errors`/`stages`。  
- **D 最终判断**：**主线通顺，白盒一致，日志已落地**。
