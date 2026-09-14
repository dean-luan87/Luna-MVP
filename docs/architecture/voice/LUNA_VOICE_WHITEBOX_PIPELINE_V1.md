# Luna Voice Whitebox Pipeline V1

## 1. 文档定位

本文件定义语音白盒的**流程型观测链**（按处理阶段串联），不是按模块目录罗列。

- **未来**：白盒定义会演进为调试/观测后台（统一看一条 request 的处理链、定位错误节点）。
- **当前**：只固定**流程链布局、阶段语义、与 observation 的挂接关系**，**不做后台 UI、不改主链执行逻辑**。
- **现实主链样本**：以 **Piper** 为当前工程化、可稳定出音的主链（`active_provider: piper`，`provider_name` 在示例中统一写为 `piper`）；Fish 等作为后续扩展位。

## 2. 为什么按流程布局，不按模块布局

| 视角 | 能回答的问题 |
|------|----------------|
| 模块树 | 「代码在哪个目录 / 哪个类」 |
| 流程链 | 「这条请求从哪进、经哪几段、在哪失败、是否回退、最终有没有播」 |

复盘与排障应按 **request 链** 查日志与观测，而不是按模块树翻散点日志。因此白盒一期以 **8 段固定流程** 为主视图；模块名仅作为辅助定位。

## 3. Voice Whitebox Pipeline V1（8 段）

每段须能回答：**这一段负责什么、最少要看哪些字段、已有哪些 observation、缺什么、Piper 主链是否覆盖**。

枚举常量见：`capabilities/voice/observations/whitebox_pipeline_stage.py`（仅命名，无逻辑）。

### 3.1 `request_ingress`

| 项 | 说明 |
|----|------|
| 回答问题 | 请求从哪里进入？是否带统一 ID？ |
| 最少观察字段 | `request_id`、`trace_id`（若有）、`session_id`、`task_context_id`（若有）、`source_module`、文本候选、`preset_name`、`cutover_enabled` 快照 |
| 当前可挂接 | `SpeechRequest`；`TTSCutoverObservation`（入口与 cutover 状态） |
| 当前缺失 | `trace_id` 全链强约束与持久化规范（部分路径仍靠兜底） |
| Piper 主链是否覆盖 | **是**（统一入口可生成并贯穿 `request_id`） |

### 3.2 `message_preparation`

| 项 | 说明 |
|----|------|
| 回答问题 | 系统准备让谁说什么？文本与输出策略是否就绪？ |
| 最少观察字段 | 原始/标准化文本（若有）、`output_category`、`priority`、`interruptible`、`cooldown_key`、`dedup_key`、metadata 快照 |
| 当前可挂接 | 主要承载在 `SpeechRequest` 字段上 |
| 当前缺失 | 独立「标准化后文本」观测对象；细粒度 preparation 事件 |
| Piper 主链是否覆盖 | **部分**（字段有，独立观测弱） |

### 3.3 `bridge_or_routing_decision`

| 项 | 说明 |
|----|------|
| 回答问题 | 请求被路由到哪条输出链？是否放行？是否降级？ |
| 最少观察字段 | route/category、allow/suppress/degrade 决议、决议原因 |
| 当前可挂接 | `OutputDecisionObservation`（占位）；`TTSCutoverObservation.selector_hit`；`DialogueBridgeObservation`（占位，未主链接线） |
| 当前缺失 | 输出治理层结构化抑制原因与 bridge 决议事件 |
| Piper 主链是否覆盖 | **部分**（selector/cutover 有；bridge 决策多仍为预留） |

### 3.4 `core_or_policy_handling`

| 项 | 说明 |
|----|------|
| 回答问题 | Core/治理层是否批准继续执行（冷却、去重、节律等）？ |
| 最少观察字段 | 政策检查结果、是否进入 provider 选择 |
| 当前可挂接 | legacy `speech_gate` 等运行语义（多为非结构化日志） |
| 当前缺失 | 结构化 policy decision observation |
| Piper 主链是否覆盖 | **弱**（行为存在，白盒对象未完整） |

### 3.5 `provider_selection`

| 项 | 说明 |
|----|------|
| 回答问题 | 为什么选了这个 provider？顺序与理由是什么？ |
| 最少观察字段 | `provider_order`、`chosen_provider`、`selection_reason`、`preset_name`、fallback/rollback 开关快照 |
| 当前可挂接 | `ProviderSelectionObservation` |
| 当前缺失 | runtime 配置脱敏快照标准字段 |
| Piper 主链是否覆盖 | **是**（当前样本 `chosen_provider=piper`） |

### 3.6 `provider_execution`

| 项 | 说明 |
|----|------|
| 回答问题 | provider 实际执行了什么？是否产出有效音频？ |
| 最少观察字段 | start/end/latency、可执行体（脱敏）、`output_valid`、`audio_bytes_len` 或路径、`failure_type` / 消息（裁剪） |
| 当前可挂接 | `TTSProviderResult`（ok/latency/failure/audio_bytes） |
| 当前缺失 | 独立 `ProviderExecutionObservation`（可后续新增） |
| Piper 主链是否覆盖 | **是**（Piper 执行成功路径可复盘） |

### 3.7 `fallback_or_rollback`

| 项 | 说明 |
|----|------|
| 回答问题 | 主路径失败后如何兜底？是否 fallback？是否 rollback 到 legacy？ |
| 最少观察字段 | 是否 fallback、是否 rollback、trigger/reason、`primary_provider`、`fallback_provider`、`final_execution_mode` |
| 当前可挂接 | `ProviderFallbackObservation`、`TTSRollbackObservation` |
| 当前缺失 | 单一汇总节点（由抽链规则拼装多 observation） |
| Piper 主链是否覆盖 | **条件覆盖**（无失败则无节点；Fish 失败 / 链失败时可观测） |

### 3.8 `playback_result`

| 项 | 说明 |
|----|------|
| 回答问题 | 最终有没有播出去？以什么模式结束（provider_chain / legacy_fallback / 失败等）？ |
| 最少观察字段 | 是否提交播放、gate 是否阻断、worker 是否执行、最终成功/失败、最终文本与 provider |
| 当前可挂接 | `TTSCutoverObservation.final_execution_mode` / `final_executor`；`PlaybackObservation`（占位） |
| 当前缺失 | 播放成功/失败的细粒度结构化 observation |
| Piper 主链是否覆盖 | **部分**（final mode 有；播放细粒度待补） |

## 4. 当前 Piper 主链典型处理链（示例）

以下阶段序列与 **Piper 直接成功** 一致，可作为「最小闭包」复盘模板：

1. **request_ingress** — 请求进入，`request_id` 生成  
2. **message_preparation** — `SpeechRequest` 携带文本与策略字段（独立观测可空）  
3. **bridge_or_routing_decision** — 进入 TTS 统一入口与 selector（细粒度 bridge 可空）  
4. **core_or_policy_handling** — gate/策略（结构化观测可空）  
5. **provider_selection** — `chosen_provider=piper`  
6. **provider_execution** — Piper 执行成功，`TTSProviderResult` 有效  
7. **fallback_or_rollback** — 无（成功主路径）  
8. **playback_result** — `final_execution_mode=provider_chain`（或与配置一致的终态）

对应观测（真实链上常见）：`ProviderSelectionObservation`、`TTSCutoverObservation`（含 `provider_chain_ok` / `final_execution_mode`）。

**从日志可抽性**：在统一入口与验证脚本产生的 JSONL/结构化输出中，可用 `request_id` 串联上述节点；细粒度 `PlaybackObservation` 仍可能缺失（见映射文档）。

## 5. 当前能力边界

- **以输出链为主**：provider 选择、执行、fallback、rollback、cutover 终态是当前白盒最有数据的区段。  
- **输入链大量为预留**：`VoiceInputObservation`、`DialogueBridgeObservation` 等多为结构占位，待 ASR/对话桥接强化后补全。  
- **流程定义先行，后台实现后置**：本节与 `LUNA_VOICE_WHITEBOX_OBSERVATION_MAPPING_V1.md`、抽链规则共同构成「以后怎么做调试后台」的契约，不绑定具体 UI 技术栈。

## 6. 主线—白盒—日志一致性检查

- **A 主线**：语音 TTS 请求在统一入口下可形成 Piper 为主的成功链。  
- **B 白盒**：8 段流程与现有 observation 映射一致，分叉（fallback/rollback）有明确阶段位。  
- **C 日志**：`request_id` 可串起 selection / fallback / rollback / cutover 等节点（见抽链规则文档）。  
- **D 最终判断**：**主线通顺，白盒一致，日志已落地**（细粒度 playback/输入链仍按「缺失项」跟踪）。
