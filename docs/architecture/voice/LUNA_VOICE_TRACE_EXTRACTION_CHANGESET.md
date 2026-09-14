# Luna Voice 最小抽链实现 — 变更清单

## 1. 新增对象与脚本

| 路径 | 说明 |
|------|------|
| `capabilities/voice/observations/request_trace_chain.py` | `RequestTraceChain`、`TraceStageRecord`、`TraceErrorRecord` 及 `to_dict()` |
| `capabilities/voice/observations/request_trace_extractor.py` | 日志加载、按 `request_id`/`trace_id` 聚合、`classify_chain_type`、`build_request_trace_chain`、`extract_trace_from_paths` |
| `tools/extract_voice_request_trace.py` | CLI：`--request-id` / `--trace-id`、`--log`（可重复）、`--format text\|json` |
| `docs/architecture/voice/fixtures/min_trace_samples.jsonl` | 3 条与运行时 observation 同构的扁平行样例（含 `request_id` / `final_execution_mode`） |
| `docs/architecture/voice/fixtures/extracted/fixture_*_trace.json` | 对上述三 `request_id` 脚本 `--format json` 导出快照（便于验收） |
| `tests/test_request_trace_extractor.py` | 针对 fixtures 的最小单测 |

## 2. 用到的 observation / 字段

| 对象 | 用途 |
|------|------|
| `ProviderSelectionObservation` | `provider_selection` 段 |
| `ProviderFallbackObservation` | fallback 段 + `provider_fallback_chain` 判型 |
| `TTSCutoverObservation` | ingress / bridge / execution 推断 / playback 终态 |
| `TTSRollbackObservation` | rollback 段 + `legacy_rollback_chain` 判型 |
| `PlaybackObservation` | 若日志存在则映射 `playback_result`；多数样本 **无** |
| `OutputDecisionObservation` | 若存在且 `accepted=false` 可辅助 **被抑制链**（样本少） |
| `TTSProviderResult` | 非独立日志名；由 cutover + 顶层 `provider_name` 等推断 execution |

## 3. 当前仍难抽或只能占位的阶段

- **`message_preparation`**：默认 `not_connected`（`SpeechRequest` 未随 JSONL 行持久化）。  
- **`core_or_policy_handling`**：`reserved`。  
- **被抑制链**：规则已写，真实日志多数不足以判型 → `suppressed_chain` 常为占位。  
- **播放细粒度失败**：无结构化 `PlaybackObservation` 时无法区分「合成成功但未播」。

## 4. 为什么仍是「最小可用」

- 只做 **单请求**、**本地文件**、**结构化输出**，不接 DB、不做 UI、不改主链。  
- 判型规则与 `LUNA_VOICE_REQUEST_TRACE_EXTRACTION_RULES_V1.md` 对齐，但实现上 **显式允许** `unknown` / `missing`。  
- 默认包含 **fixtures**，保证无本机 `logs/` 也能验收抽链。

## 5. 后续强化项（本变更未实现）

仅列名：全文检索、历史归档、多请求批处理、实时订阅、错误聚类、链缩略/展开 UI、颜色分级、跨机 `trace_id` 注入强约束、独立 `ProviderExecutionObservation` 落盘。

## 6. 主线—白盒—日志一致性检查

- **A 主线**：抽链输入为现有日志形态（validate 脚本 / fixtures）。  
- **B 白盒**：阶段与文档 8 段一致，缺失不伪造。  
- **C 日志**：`request_id` 串联；JSON 可导出。  
- **D 最终判断**：**主线通顺，白盒一致，日志已落地**。
