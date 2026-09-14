# Luna Voice Error Trace Chain V1

## 1. 什么是 Error Trace Chain

### 1.1 为什么错误链不是「报错字符串」

单条报错字符串或堆栈只能回答「哪行代码抛了」，不能稳定回答：**同一 `request_id` 在 8 段流程里走到了哪一段、哪一段做了分叉决策、最终是以什么模式收口**。  
因此 Error Trace Chain 必须以**阶段节点**为单位串联，而不是以异常文本为中心。

### 1.2 定义

`Error Trace Chain` **不是**单条异常字符串或堆栈摘要，而是一条**带阶段节点**的处理链：

- 每个节点对应 Whitebox Pipeline 的一段（或子状态）  
- 节点上携带：`stage`、`status`（ok / fail / suppressed / skipped）、`reason`（可空）、`request_id`、`timestamp`  
- 任意请求出问题时，应能**抽出一条链**，回答：请求从哪来、走到哪一层、为何失败/被抑制/被回退、最终有没有播出去  

标准阶段顺序（与流程文档对齐）：ingress → preparation → routing/policy → selection → execution → fallback/rollback（可选）→ playback result。

## 2. 至少 5 类典型错误链示例

以下 **`provider_name` 样本**：主成功路径为 **`piper`**；Fish 仅出现在 fallback/选型示例中。

---

### 2.1 Piper 直接成功链（非错误，作为基线对照）

| 顺序 | 阶段 | 状态 | 说明 |
|------|------|------|------|
| 1 | request_ingress | ok | 请求进入，`request_id` 分配 |
| 2 | message_preparation | ok / partial | 文本与策略在 `SpeechRequest` 上（独立观测可缺） |
| 3 | bridge_or_routing_decision | ok | 进入统一入口与 selector |
| 4 | provider_selection | ok | **`chosen_provider=piper`** |
| 5 | provider_execution | ok | Piper 执行成功，`TTSProviderResult` 有效 |
| 6 | fallback_or_rollback | skipped | 无失败则无 fallback/rollback |
| 7 | playback_result | ok | **`final_execution_mode=provider_chain`**（或与配置一致） |

**会出现的 observation**：`ProviderSelectionObservation`、`TTSCutoverObservation`（`provider_chain_ok` / `final_execution_mode`）。  
**错误节点**：无（成功链）。  
**收口**：正常播放路径结束。  
**日志可抽性**：**可** — 用 `request_id` 串联 selection + cutover；`PlaybackObservation` 可能仍粗。

---

### 2.2 Fish 不可用 → Piper fallback 成功链

| 顺序 | 阶段 | 状态 | 说明 |
|------|------|------|------|
| 1 | request_ingress | ok | 同 2.1 |
| 2 | provider_selection | ok | **`chosen_provider=piper`**（配置允许时） |
| 3 | provider_execution | **fail** | Fish 执行失败，如 `failure_type=not_available` |
| 4 | fallback_or_rollback | ok | **fallback 到 `piper`**，`output_valid=true` |
| 5 | provider_execution | ok | Piper 执行成功 |
| 6 | playback_result | ok | `final_execution_mode=provider_chain` |

**会出现的 observation**：`ProviderSelectionObservation`、`ProviderFallbackObservation`（primary=piper, fallback=piper）、`TTSCutoverObservation`。  
**错误节点**：**provider_execution（piper）** — 第一次执行失败。  
**收口**：fallback 成功后仍归一到 provider_chain 终态。  
**日志可抽性**：**可** — fallback 与 cutover 字段可拼链。

---

### 2.3 Provider chain 失败 → legacy rollback 成功链

| 顺序 | 阶段 | 状态 | 说明 |
|------|------|------|------|
| 1 | request_ingress | ok | — |
| 2 | provider_selection | ok | 可能先选 piper 等 |
| 3 | provider_execution | **fail** | 整条 provider chain 失败 |
| 4 | fallback_or_rollback | ok | **rollback**，如 `rollback_trigger=provider_chain_failure` |
| 5 | playback_result | ok | **`final_execution_mode=legacy_fallback`** |

**会出现的 observation**：`ProviderFallbackObservation`（`output_valid=false`）、`TTSRollbackObservation`、`TTSCutoverObservation`。  
**错误节点**：**provider_execution（chain）** 或 **fallback 未救回前的失败**。  
**收口**：legacy 路径成功则终态为 `legacy_fallback`。  
**日志可抽性**：**可** — rollback 与 `final_execution_mode` 可拼链。

---

### 2.4 输出治理层抑制请求链

| 顺序 | 阶段 | 状态 | 说明 |
|------|------|------|------|
| 1 | request_ingress | ok | 请求曾进入 |
| 2 | bridge_or_routing_decision / core_or_policy_handling | **suppressed** | 冷却/去重/节律等拦截 |
| 3 | provider_selection | skipped | 未进入 |
| 4 | provider_execution | skipped | — |
| 5 | playback_result | suppressed | 执行前即结束 |

**会出现的 observation（理想）**：`OutputDecisionObservation`（占位）、未来 policy 事件。  
**错误节点**：**routing/policy** — 非 provider 故障，而是**被抑制**。  
**收口**：无 TTS 执行、无播放或仅有「被抑制」终态标记（依实现）。  
**日志可抽性**：**部分** — 依赖结构化抑制事件；当前多靠日志语义，抽链可能不完整。

---

### 2.5 最终播放失败链

| 顺序 | 阶段 | 状态 | 说明 |
|------|------|------|------|
| 1 | request_ingress | ok | — |
| 2 | provider_selection | ok | 如 `piper` |
| 3 | provider_execution | ok | 已有有效音频字节 |
| 4 | playback_result | **fail** | 播放底座失败、或 gate 阻断未播出 |

**会出现的 observation**：`TTSCutoverObservation.final_executor`；未来完整 `PlaybackObservation`。  
**错误节点**：**playback_result**。  
**收口**：`final_execution_mode` 可能为失败类枚举或待定义失败终态。  
**日志可抽性**：**部分** — 执行成功但播放失败需播放层结构化字段补强。

---

## 3. 错误链判断规则（摘要）

- provider 执行失败但 fallback 成功 → **可恢复失败**（整条链可标为 fallback 成功链）  
- provider chain 失败且 rollback 成功 → **链路恢复成功（legacy）**  
- routing/policy 抑制且无 execution → **执行前抑制链**  
- playback 失败 → **终端失败链**  
- 无异常且 `chosen_provider=piper` 直出 → **成功链**（对照 2.1）

## 4. 当前状态声明

- Piper 主链上 **2.1 / 2.2 / 2.3** 类链在统一入口与验证流中 **可较稳定抽取**。  
- **2.4 / 2.5** 已定义阶段语义，**结构化观测仍待补强**。  

## 5. 主线—白盒—日志一致性检查

- **A 主线**：成功与 fallback/rollback 恢复路径已进入错误链定义。  
- **B 白盒**：5 类示例与 8 段流程、observation 映射一致。  
- **C 日志**：2.1–2.3 可抽；2.4–2.5 按「缺失项」跟踪。  
- **D 最终判断**：**主线通顺，白盒一致，日志已落地**（抑制/播放失败细粒度为已知缺口）。
