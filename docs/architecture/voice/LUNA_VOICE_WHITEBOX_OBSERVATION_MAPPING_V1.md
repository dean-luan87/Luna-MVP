# Luna Voice Whitebox Observation Mapping V1

## 1. 文档定位

将现有 observation / 对象映射到 **Voice Whitebox Pipeline V1** 的 8 段流程，并标明：

- 在 **当前 Piper 主链** 上是否**真实产生/可用**（活）  
- 是否仅为**结构占位**（预留）  
- **Fish / ASR / 情感输出** 等后续应在哪一段补强  

## 2. 总映射表

| 流程阶段 | 现有 observation / 对象 | 是否已存在 | 当前用途 | 缺失项 | 后续建议 |
|----------|-------------------------|------------|----------|--------|----------|
| request_ingress | `VoiceInputObservation` | 是 | 输入侧语义（麦克风/上游） | 输出主链未统一接线 | ASR/全双工接入后挂 ingress |
| request_ingress | `SpeechRequest`, `TTSCutoverObservation` | 是 | 请求入口、cutover 快照 | `trace_id` 强约束 | 入口注入并校验 trace |
| message_preparation | `SpeechRequest` | 是 | 文本、优先级、category、cooldown 等 | 标准化文本独立字段 | 增加 `prepared_text` 或等价观测 |
| bridge_or_routing_decision | `DialogueBridgeObservation` | 是 | 对话桥/route（占位） | 主链未接线 | 对话策略与 bridge 决议落地 |
| bridge_or_routing_decision | `OutputDecisionObservation` | 是 | 输出治理决议（占位） | 结构化抑制原因不足 | 与 policy 事件对齐 |
| bridge_or_routing_decision | `TTSCutoverObservation.selector_hit` | 是 | 是否进入 selector | 路由理由可更丰富 | 保留为 routing 辅助字段 |
| core_or_policy_handling | （legacy gate 语义） | 部分 | 冷却/去重等 | 无结构化 observation | 新增 policy decision 观测 |
| core_or_policy_handling | `ModelMediationObservation` | 是 | 模型侧中介/改写（占位） | 未进 Piper 主链 | 情感/多模输出或 core 协作时接 |
| provider_selection | `ProviderSelectionObservation` | 是 | order、chosen、reason | config 脱敏快照规范 | 增加脱敏 runtime 快照 |
| provider_execution | `TTSProviderResult`（非 observation 名但链上核心） | 是 | ok/latency/failure/audio | 无独立 execution 类名 | 可选新增 `ProviderExecutionObservation` |
| fallback_or_rollback | `ProviderFallbackObservation` | 是 | primary/fallback/失败类型 | 与 rollback 合并视图 | 抽链时合并展示 |
| fallback_or_rollback | `TTSRollbackObservation` | 是 | rollback 触发与终态 | 单节点汇总 | 同上 |
| playback_result | `TTSCutoverObservation`（final 字段） | 是 | `final_execution_mode` 等 | 播放细粒度 | 强化 `PlaybackObservation` |
| playback_result | `PlaybackObservation` | 是 | 播放结果（占位） | 实际失败原因等 | 播放底座回调后补全 |

## 3. 指定对象与流程阶段对应（摘要）

| Observation | 主要流程阶段 | Piper 主链上状态 | 备注 |
|-------------|--------------|------------------|------|
| `VoiceInputObservation` | request_ingress（输入扩展） | **预留** | 输出链复盘可不出现 |
| `DialogueBridgeObservation` | bridge_or_routing_decision | **预留** | Fish/ASR/对话增强时接 |
| `ModelMediationObservation` | core_or_policy_handling / 中间改写 | **预留** | 情感输出、模型协同 |
| `OutputDecisionObservation` | bridge_or_routing_decision | **占位** | 抑制链需后续结构化 |
| `ProviderSelectionObservation` | provider_selection | **活** | 当前必有（成功路径） |
| `ProviderFallbackObservation` | fallback_or_rollback | **活（条件）** | 仅失败/fallback 时出现 |
| `TTSCutoverObservation` | request_ingress + playback_result | **活** | 入口与终态关键 |
| `TTSRollbackObservation` | fallback_or_rollback | **活（条件）** | 链失败 rollback 时出现 |
| `PlaybackObservation` | playback_result | **占位** | 终态粗粒度靠 cutover |

## 4. Piper 当前主链结论

- **已真实覆盖（活）**：`ProviderSelectionObservation`（`chosen_provider=piper`）、`TTSProviderResult`、`TTSCutoverObservation`、`ProviderFallbackObservation` / `TTSRollbackObservation`（仅当发生 fallback/rollback）。  
- **结构占位或弱接线**：`VoiceInputObservation`、`DialogueBridgeObservation`、`ModelMediationObservation`、`OutputDecisionObservation`、`PlaybackObservation`。  
- **后续 provider**：同表 `provider_selection` / `provider_execution` / `fallback_or_rollback` 扩展 `chosen_provider=piper` 与失败语义。  
- **后续 ASR / 情感**：分别强化 `request_ingress` / `message_preparation` 与 `ModelMediationObservation`、相关输出段。

## 5. 主线—白盒—日志一致性检查

- **A 主线**：Piper 主链可对 selection → execution → cutover 终态做闭环复盘。  
- **B 白盒**：映射表与 8 段流程一致，活/预留区分明确。  
- **C 日志**：`request_id` 可串起活节点；占位节点允许为空。  
- **D 最终判断**：**主线通顺，白盒一致，日志已落地**。
