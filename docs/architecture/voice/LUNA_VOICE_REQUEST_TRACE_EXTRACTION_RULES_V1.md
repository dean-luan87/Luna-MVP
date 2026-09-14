# Luna Voice Request Trace Extraction Rules V1

## 1. 目标

从现有 observation / 日志中抽取**单条语音请求**的完整处理链，输出可复盘的 **Request Trace**，而不是散点日志。

## 2. 串联 ID 规则

| ID | 必须性 | 用途 |
|----|--------|------|
| `request_id` | **必须** | 单条 TTS/语音请求的主键；无则该事件默认不参与自动抽链 |
| `trace_id` | 推荐 | 跨服务/跨模块关联；缺失时可用阶段事件 + 时间窗兜底 |
| `session_id` | 推荐 | 会话级聚合；多请求归属同一会话 |
| `task_context_id` | 条件 | 任务/设备上下文（若业务层产生）；无则可为空 |

**优先级（同一请求归并）**：`request_id` > `trace_id` 辅助 > `(时间窗 + source_module + 文本 hash)` 兜底。

**要求**：所有阶段节点在可能的情况下均应能回填 **`request_id`**。

## 3. 必须节点（MUST）

满足一次「最小闭环」抽链至少包含：

| 节点（阶段） | 最少信息 |
|--------------|----------|
| `request_ingress` | 能确认请求进入（含 `request_id`） |
| `provider_selection` | **`chosen_provider`**（当前 Piper 主链样本为 **`piper`**） |
| `playback_result` | **`final_execution_mode`**（或与 cutover 等价的终态字段） |

缺少任一 MUST 节点且无法在时间窗内补全 → 判定为 **链断** 或 **不完整链**（见第 5 节）。

## 4. 可选节点（OPTIONAL / EMPTY_ALLOWED）

| 类型 | 说明 |
|------|------|
| **可选** | `message_preparation`、`bridge_or_routing_decision`、`core_or_policy_handling` 的独立事件 |
| **条件出现** | `fallback_or_rollback`（仅当发生 fallback/rollback） |
| **允许为空** | 输入链：`VoiceInputObservation`；bridge：`DialogueBridgeObservation`；`ModelMediationObservation`；细粒度 `PlaybackObservation`；未发生的 fallback |

## 5. 链断点 / 抑制 / 回退 / 失败判定

| 概念 | 判定要点 |
|------|----------|
| **链断了** | 有 ingress 但在超时窗口内无 `provider_selection`；或有 selection 但无与请求一致的 cutover/终态；或同一 `request_id` 出现冲突的 `final_execution_mode` |
| **链被抑制** | routing/policy 阶段为 suppressed，且 **无** provider execution 记录 |
| **链被回退** | 存在 `TTSRollbackObservation` 或等价语义，且终态为 **`legacy_fallback`** |
| **链执行失败** | provider execution 失败且 **未**被 fallback 救回；或终态为失败类 `final_execution_mode`；或 playback 明确失败 |

**fallback**：存在 `ProviderFallbackObservation` 且最终有效输出来自 `fallback_provider`（如 piper 重试 → **piper**）。

## 6. 抽链类型分类

每类链需同时满足 **最小识别条件**（自动/半自动判型）与 **典型收口节点**（后台时间轴最后一格优先展示什么）。

| 类型 | 最小识别条件 | 典型收口节点 |
|------|----------------|--------------|
| **成功链** | 无 `ProviderFallbackObservation` / `TTSRollbackObservation` 的必要分叉；`chosen_provider=piper`（主样本）；`final_execution_mode=provider_chain`（或与配置一致的成功终态） | `playback_result`：`TTSCutoverObservation.final_execution_mode` |
| **fallback 链** | 存在 `ProviderFallbackObservation`；主 provider 曾失败且 `fallback_provider`（如 **piper**）产出有效结果 | `fallback_or_rollback` + `playback_result`（终态仍为 `provider_chain` 时常表示「救回」） |
| **rollback 链** | 存在 `TTSRollbackObservation` 或等价语义；`final_execution_mode=legacy_fallback` | `playback_result`：`final_execution_mode=legacy_fallback` |
| **被抑制链** | routing/policy 为 suppressed，且 **无** provider execution 记录；**不是** `provider_execution` 的 failure | `bridge_or_routing_decision` / `core_or_policy_handling`（抑制原因字段待结构化） |
| **失败链** | 终端未恢复：provider chain 失败且未 fallback 成功；或 **`playback_result` 明确失败**（与「仅被抑制」区分） | `playback_result` 或 `failed_no_output` 类终态 |

**补充**：**被抑制链** ≠ provider failure —— 请求可能在治理层被压住，**未进入** `provider_execution`。**失败链**可与「provider 已成功合成音频但播放失败」共存，此时错误节点在 **playback_result**，不在 execution。

## 7. 抽链算法（V1 摘要）

1. 用 `request_id` 过滤候选事件。  
2. 标准化为 `{ stage, status, ts, reason, payload }`。  
3. 按阶段顺序归并：`request_ingress` → … → `playback_result`。  
4. 缺失节点标记 `status=missing`（若业务允许）。  
5. 根据第 6 节判定链路类型。

## 8. Piper 主链三条示例（与验收对齐）

**约定**：示例中 **主链 provider 名称** 写为 **`piper`**。

### 示例 1：Piper 直接成功链

- **阶段**：ingress →（prep 可空）→ selection **`piper`** → execution success → playback success  
- **Observation**：`ProviderSelectionObservation`、`TTSCutoverObservation`  
- **从日志真实抽出**：**可以**（验证脚本 / JSONL 路径下可复现）

### 示例 2：Fish 失败 → Piper fallback 成功链

- **阶段**：ingress → selection **piper** → piper execution fail → **fallback to piper** → piper success → playback success  
- **Observation**：`ProviderSelectionObservation`、`ProviderFallbackObservation`、`TTSCutoverObservation`  
- **从日志真实抽出**：**可以**（piper 失败触发 fallback 时）

### 示例 3：Provider chain 失败 → legacy rollback 成功链

- **阶段**：ingress → provider chain fail → **rollback to legacy** → legacy playback success  
- **Observation**：`ProviderFallbackObservation`、`TTSRollbackObservation`、`TTSCutoverObservation`  
- **从日志真实抽出**：**可以**（触发 rollback 路径时）

## 9. 后续调试后台实现指引（落地性）

按本文件与 `LUNA_VOICE_WHITEBOX_PIPELINE_V1.md`、`LUNA_VOICE_WHITEBOX_OBSERVATION_MAPPING_V1.md` 可直接指导后台一期：

- **页面主视图**：按 **8 段流程** 横向或纵向时间轴排列（每格对应 `WhiteboxPipelineStageV1`），不是按仓库目录树。  
- **每格默认展示**：该段「最少信息」列（见抽链规则 §3 MUST、流程文档各段「最少观察字段」）；无事件则标 `EMPTY_ALLOWED` 或 `missing`。  
- **分叉高亮**：`fallback_or_rollback` 出现 `ProviderFallbackObservation` / `TTSRollbackObservation` 时展开子链。  
- **判型**：用 §6 的「最小识别条件」决定标签（成功 / fallback / rollback / 被抑制 / 失败）。  
- **主样本**：当前默认展示 **`chosen_provider=piper`**；Fish 仅作为分叉示例，不在主样本链上默认假设。

## 10. 主线—白盒—日志一致性检查

- **A 主线**：`request_id` + selection + 终态可闭链。  
- **B 白盒**：必须/可选节点与 8 段流程、Error Trace 文档一致。  
- **C 日志**：Piper 直接成功与两条恢复链可抽；抑制/播放失败链待结构化补强。  
- **D 最终判断**：**主线通顺，白盒一致，日志已落地**。
