# Phase-Voice-OutputGovernance-000
# Voice Output Governance Existing Asset Inventory v0（现有资产盘点）

**阶段定位**：本阶段只做盘点（inventory baseline），为后续在旧链路上补齐「超时 / 优先级 / 取消 / 过期 / 打断 / provider health / 观测指标」提供证据与路径基线。  
**硬边界（本阶段必须遵守）**：

- 不改 runtime 行为
- 不接新 TTS provider
- 不改真实播报行为
- 不删除 legacy voice 代码
- 不改现有 env 开关语义/默认值
- 不接导航/中台/SceneTask/Fusion/Output 新链路

---

## 1. Existing code assets（代码资产）

> 说明：分类仅用于“盘点阶段的复用判断”，不代表立刻改动。

### 1.1 V1 minimal flow 主链路锚点

- **`capabilities/voice/runtime/voice_input_session_manager.py`**
  - **role**：V1 单入口聚合器；`process_final_text_with_dispatch(...)` 负责从 raw text 组装 `VoiceInputEvent`，绑定 `VoiceV1SessionStateAnchor`，再调用 `dispatch_voice_final_text(...)`。
  - **status**：reusable
- **`capabilities/voice/runtime/voice_final_text_dispatcher.py`**
  - **role**：主分流入口 `dispatch_voice_final_text(...)`；在 orchestrator/观测后，按开关走 `_maybe_submit_real_output_v1(...)` 进入输出平面；包含 “operator toggle transition” 等白盒观测补齐。
  - **status**：reusable（但体量大、旁路耦合多；后续增强需要治理层隔离）
- **`capabilities/voice/output/voice_output_plane_v1.py`**
  - **role**：`VoiceOutputPlaneV1.submit(SpeechRequest)` 的最小“真实可调用锚点”；默认 dry-run 写 JSONL envelope；可选走 `run_tts_unified_entry(...)` + playback executor/plane。
  - **status**：reusable（V1 输出锚点）
- **`capabilities/voice/interfaces/voice_output_plane.py`**
  - **role**：Stage-1 `VoiceOutputPlane` 接口边界（统一出口，禁止模块直连 TTS）。
  - **status**：reusable
- **`capabilities/voice/schemas/speech_request.py`**
  - **role**：Stage-1 `SpeechRequest`；已包含 `priority / interruptible / dedup_allowed / cooldown_key / task_context_id / trace_id / metadata` 等占位字段。
  - **status**：reusable（关键治理字段已有占位）

### 1.2 Session anchor（会话锚点）

- **`capabilities/voice/runtime/voice_v1_session_state_anchor.py`**
  - **role**：`VoiceV1SessionStateAnchor`（最小事实锚；记录 last_user_text/last_system_text/request_id 等，不发明缺失信息）；`apply_no_submit_conservative()` 明确“未 submit 不伪造系统已说”。
  - **status**：reusable

### 1.3 Speech Gate（总闸）

- **`core/speech_gate.py`**
  - **role**：`SpeechGate.can_speak/acquire/force_acquire/release`；包含去重（`scene_hash`）、冷却（cooldown）、占用（tts_busy）、用户说话抑制（user_speaking）与强制抢占（force_acquire）的基础语义。
  - **status**：reusable（但需确认其是否已被 VoiceOutput 主链实际接线）

### 1.4 Piper / Fish / provider 侧资产（现存实现）

- **`capabilities/voice/providers/piper_tts_provider.py`**
  - **role**：Piper TTS provider 实现（provider_chain 中的候选之一）。
  - **status**：legacy_or_reusable（取决于当前 runtime mode 与策略文档）
- **`（已移除）`**
  - **role**：Fish TTS provider 实现（更自然长句表达链路的候选之一）。
  - **status**：legacy_or_reusable
- **`capabilities/voice/runtime/tts_unified_entry.py`**
  - **role**：统一 TTS 执行入口（provider 选择、fallback/rollback、cutover 观测）。
  - **status**：reusable
- **`capabilities/voice/providers/tts_provider_selector.py`**, **`capabilities/voice/providers/tts_fallback_manager.py`**, **`capabilities/voice/output/tts_request_executor.py`**
  - **role**：provider 选择/降级/执行相关组件（供 provider health 与 fallback 观测链复用）。
  - **status**：reusable

### 1.5 Timeout / priority / cancellation / queue 相关占位（现存）

- **`capabilities/voice/schemas/speech_request.py`**
  - **evidence**：已有 `priority / interruptible / dedup_allowed / cooldown_key` 字段（可作为后续治理层的承载点）。
- **`capabilities/voice/runtime/voice_time_governance_v1.py`**
  - **role**：输入侧时间/窗口治理（wake window、会话时钟）；与输出超时不是同一问题，但为“语音链总体时效治理”提供既有基线。
  - **status**：reusable
- **`capabilities/voice/runtime/voice_segment_timeout_policy.py`**
  - **role**：切段/输入侧 timeout policy（与“输出过期/超时”不同维度）。
  - **status**：reusable（概念上需与输出超时策略区分）
- **`capabilities/voice/output/playback_plane_v1.py`**, **`capabilities/voice/output/audio_worker_v1.py`**
  - **role**：输出执行队列/worker 的最小实现锚点（可支持 cancel 等试点逻辑）。
  - **status**：reusable（但属于执行层，后续治理增强必须保持边界清晰）
- **`capabilities/voice/output/output_priority_policy.py`**
  - **role**：存在优先级策略文件（需进一步确认其是否与 `SpeechRequest.priority` 对齐与被调用）。
  - **status**：unknown（待后续盘点补充“实际接线点”）

---

## 2. Existing document assets（文档资产）

### 2.1 Voice 宪法 / Stage-1 / V1 minimal flow

- **`docs/architecture/voice/LUNA_VOICE_V1_MINIMAL_FLOW.md`**
  - **defines**：V1 单入口与最短闭环路径（`VoiceInputSessionManager` → `dispatch_voice_final_text` → `_maybe_submit_real_output_v1` → `VoiceOutputPlaneV1.submit(SpeechRequest)`），以及 submit 候选范围与开关条件。
  - **validity**：still_valid（以代码事实为准）
- **`docs/architecture/voice/LUNA_VOICE_MAINLINE_BASELINE.md`**
  - **defines**：Voice V1/V2/V3 总基线图；统一硬约束（No Fabrication、统一时空锚点、语义层不得夺权）与验证入口表。
  - **validity**：still_valid
- **`docs/architecture/voice/LUNA_VOICE_V1_PLAN.md`**, **`docs/architecture/voice/LUNA_VOICE_V1_SESSION_STATE.md`**
  - **defines**：V1 计划与 session/state 约束（强调 No Fabrication Rule 高于状态便利）。
  - **validity**：still_valid

### 2.2 真实输出链与观测

- **`docs/architecture/cross_domain/LUNA_REAL_OUTPUT_SUBMIT_V1_IMPLEMENTED_NOTE.md`**
  - **defines**：`LUNA_ENABLE_REAL_OUTPUT_SUBMIT_V1` 受控开启的最小 submit 闭环；JSONL envelope 与最小观测节点集合。
  - **validity**：still_valid
- **`docs/architecture/voice/LUNA_VOICE_WHITEBOX_FIELD_DICTIONARY_V1.md`**
  - **defines**：voice 输出链白盒字段语义字典（chain_type、provider_name、final_execution_mode、issue 等）。
  - **validity**：still_valid（与实现不一致时以代码为准并回修字典）

### 2.3 输出治理定义（后续增强的参照，但不在本阶段落实现）

- **`docs/architecture/LUNA_VOICE_OUTPUT_GOVERNANCE_DEFINITION_V0.md`** 等 Phase-Voice-OutputGovernance-001 系列文档
  - **defines**：治理目标、状态机/打断、优先级/过期/抑制、provider health、TRW 观测要求、Go/No-Go。
  - **validity**：still_valid（本阶段仅把它作为“增强目标参照”，不触发任何实现）

---

## 3. Existing env flags（环境开关资产）

> 本阶段只盘点，不改语义/默认值。

### 3.1 真实 submit 总开关（V1）

- **`LUNA_ENABLE_REAL_OUTPUT_SUBMIT_V1`**
  - **behavior**：未开启时不触发 `_maybe_submit_real_output_v1(...)`，主线不 submit 且默认不写 trace（见 `voice_final_text_dispatcher.py` 与文档）。
  - **risk**：开启后会触发输出平面闭环（虽可 dry-run），必须配合 trace/观测与候选范围硬限制。

### 3.2 输出 submit trace/诊断相关

- **`LUNA_REAL_OUTPUT_SUBMIT_V1_TRACE_JSONL`**
  - **behavior**：JSONL envelope 输出路径；默认 `logs/real_output_submit_v1.jsonl`（`voice_output_plane_v1.py` 与 `voice_final_text_dispatcher.py` 均读取）。
  - **risk**：路径/权限/文件体积；同时存在多处写入点，需要后续统一封装防止分叉。
- **`LUNA_REAL_OUTPUT_SUBMIT_V1_EXECUTE_TTS`**
  - **behavior**：`VoiceOutputPlaneV1` 中控制是否走真实 TTS 执行（默认 dry-run）。
  - **risk**：开启后会真正触发 provider chain + playback（依赖本地/在线 provider 可用性）。
- **`LUNA_REAL_OUTPUT_SUBMIT_V1_FORCE_REJECT`**, **`LUNA_REAL_OUTPUT_SUBMIT_V1_FORCE_FAIL`**
  - **behavior**：强制 submit rejected/failed（用于测试/演练）。
  - **risk**：若误开会造成系统性不出声/失败，必须纳入白盒与运行手册。

### 3.3 playback 执行锚点开关（V1）

- **`LUNA_ENABLE_REAL_PLAYBACK_EXECUTION_V1`**
  - **behavior**：控制 playback 走 executor 旧锚点还是 Playback Plane + Audio Worker（见 `voice_output_plane_v1.py`）。
  - **risk**：开启后会进入队列/worker 执行路径，需要更严格的 cancel/interrupt/queue state 观测。

---

## 4. Existing runtime flow（当前运行时流摘要）

### 4.1 V1 minimal flow（从输入到输出平面）

1. **Input 聚合入口**：`VoiceInputSessionManager.process_final_text_with_dispatch(...)`
2. **分流**：`dispatch_voice_final_text(...)`（短链/长链/reject）
3. **受控 submit helper**：`_maybe_submit_real_output_v1(...)`
   - 受 `LUNA_ENABLE_REAL_OUTPUT_SUBMIT_V1` 控制
   - 当前只允许极小候选范围（rejected_input / session_wake）
4. **输出平面**：`get_voice_output_plane_v1().submit(SpeechRequest)`
5. **TTS/Playback（可选）**：
   - 默认 dry-run（写 envelope，不依赖 TTS）
   - `LUNA_REAL_OUTPUT_SUBMIT_V1_EXECUTE_TTS=1` 后走 `run_tts_unified_entry(...)`
   - playback 走 executor 或 plane/worker（受 `LUNA_ENABLE_REAL_PLAYBACK_EXECUTION_V1` 控制）

### 4.2 Speech Gate 在链路中的位置（盘点结论）

- **现有实现**：`core/speech_gate.py` 已存在完整裁决语义。
- **待确认项**：在当前 `VoiceOutputPlaneV1.submit(...)` 与 playback 执行路径中，Speech Gate 是否被作为“输出前最终裁决/占用锁”实际调用（本阶段不改接线，只记录“接线点未知”的缺口）。

---

## 5. Existing observability（现有观测：trace/log/whitebox）

### 5.1 JSONL envelope（real output submit v1）

- **写入点（至少两处）**：
  - `capabilities/voice/runtime/voice_final_text_dispatcher.py::_emit_trace_envelope_v1(...)`
  - `capabilities/voice/output/voice_output_plane_v1.py::_emit_envelope(...)`
- **典型 envelope 类型**（见 `voice_output_plane_v1.py` 与 implemented note）：
  - `request_runtime`（`RequestRuntimeObservation`：request_created/request_submitted/request_terminal_observed 等）
  - `submit_invoked`（`OutputSubmitObservation`）
  - `selection`（`ProviderSelectionObservation`）
  - `fallback`（`ProviderFallbackObservation`）
  - `rollback`（`TTSRollbackObservation`）
  - `cutover`（`TTSCutoverObservation`）
  - `playback_runtime`（playback 运行时观测；用于 cancel/terminal 等确认）
  - `pilot_state_transition` / `output_decision`（试点状态切换与输出决策观测）

### 5.2 白盒字典与抽链体系（TRW）

- **`docs/architecture/voice/LUNA_VOICE_WHITEBOX_FIELD_DICTIONARY_V1.md`** 已给出链级字段语义、issue/summary/stage 的解释与用法。
- **`capabilities/voice/observations/request_trace_extractor.py`** 等抽链组件存在（本阶段不展开读取全链，只记录其存在与与 JSONL 对齐关系）。

### 5.3 缺失/不一致（盘点发现）

- **`guard_v1_speakable_text` 的代码实现定位缺失**：
  - 文档多处引用 `guard_v1_speakable_text`，但在当前仓库中未找到同名函数定义/实现；`_maybe_submit_real_output_v1(...)` 内存在最小 “No Fabrication” token guard（`unknown/todo/placeholder/...`）作为替代。
  - 结论：需要在后续增强阶段做“命名与实现对齐”或明确“旧名废弃/新实现替代”的治理决定（本阶段只记录为缺口）。

---

## 6. Existing gap table（缺口表：与 Phase-001 治理项对齐）

> 表中 “已有字段/占位” ≠ 已完成治理；只表示存在可承载的结构或局部实现。

| 治理项 | 现有资产 / 证据 | 已有字段/占位 | 现状结论 | 主要缺口（本阶段只记录） |
|---|---|---:|---|---|
| **timeout（输出时效/窗口）** | 输入侧有 `VoiceTimeGovernanceRuntime`、`voice_segment_timeout_policy.py` | 部分 | 输出侧尚无统一“过期就不播”的硬门；仅见试点等待窗口 `LUNA_RISK_INTERRUPT_CANCEL_REPLACE_WAIT_MS` | 缺少 `SpeechRequest` 级 expiry/valid_until 与输出前 gate |
| **priority（输出优先级）** | `SpeechRequest.priority`、`output_priority_policy.py`（存在） | 是 | 需要确认实际执行层/队列是否读取并排序 | 缺少端到端优先级语义（安全>导航>任务>闲聊）与观测 |
| **cancellation（取消）** | Level2B 试点在 dispatcher 中调用 playback plane cancel | 部分 | 取消语义存在，但为试点与特定条件下；通用 cancel API/契约未冻结 | 缺少取消边界（已 started 禁止/允许？）与统一观测字段 |
| **expiry（内容过期）** | 未看到 `SpeechRequest` 中的 expiry 字段 | 否 | 当前 submit helper 只做长度限制；没有 expiry 模型 | 缺少过期字段与 stale suppression 统一策略 |
| **interruption（打断）** | `SpeechRequest.interruptible` 字段；`SpeechGate.force_acquire` 语义 | 部分 | 语义存在但接线点未确认；试点有“抢占替换文本” | 缺少可审计的打断决策/状态机与队列行为一致性 |
| **provider health（可用性/延迟/失败率/fallback）** | `tts_unified_entry` + selection/fallback/rollback/cutover 观测存在 | 部分 | 观测面较丰富，但“健康判定/电路熔断/依赖就绪”是否统一由 policy 控制需进一步核对 | 缺少统一 health snapshot + readiness gate 对齐到输出准入 |
| **queue state（队列状态）** | `audio_worker_v1.snapshot_state()` 被试点读取 | 部分 | 队列状态可读，但是否标准化输出给白盒/trace 需确认 | 缺少标准队列状态 schema 与稳定抽取 |
| **stale speech suppression（陈旧播报抑制）** | `SpeechGate` 有 duplicate_scene；submit helper 有极小候选范围 | 部分 | 目前更像“去重/冷却”，不是“内容时效 + 上下文过期” | 缺少 stale 定义、与任务/导航状态对齐的抑制条件 |
| **speech gate result（闸门结果可观测）** | `SpeechGate.can_speak` 返回 (bool, reason) | 是 | 需要确认是否在输出链路里真实调用并落观测 | 缺少统一 gate decision 记录（reason、owner、cooldown 等） |
| **real_tts_invoked audit（真实 TTS 是否被调用）** | `VoiceOutputPlaneV1.execute_tts` 与 trace envelope 可反映 dry_run | 部分 | 能间接判定；但缺少统一字段 `real_tts_invoked` 的强约束落点 | 缺少链级硬字段与 verifier/工具一致性检查 |

---

## 7. Recommended next phase（建议下一阶段）

**Phase-Voice-OutputGovernance-001**（增强阶段）：在**旧链路**上补齐“输出治理合同层”，优先顺序建议：

1. **Output timeout/expiry contract**：在 `SpeechRequest` 上明确 expiry/valid_until（不改变默认行为前提下先落 contract + trace 字段）。
2. **Priority & interruption semantics**：统一优先级枚举/映射与可审计打断理由。
3. **Cancellation contract**：明确 cancel 的状态边界（queued vs started），并把队列状态标准化为观测字段。
4. **Provider health/readiness**：把 `tts_unified_entry` 的观测归一为健康快照，并定义 readiness gate。
5. **Speech Gate wiring audit**：明确 SpeechGate 接线点与 gate-result 的 trace/whitebox 记录。

---

## 8. 本阶段产出声明（必须）

- 本阶段只做盘点：**不改 runtime**、不真实播报、**不接新 provider**、不删除 legacy voice、**不改 env 开关**。

