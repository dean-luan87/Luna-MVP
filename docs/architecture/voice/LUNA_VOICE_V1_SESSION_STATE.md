# Luna Voice V1 — 最小会话状态层（状态锚点）

**文件**：`docs/architecture/voice/LUNA_VOICE_V1_SESSION_STATE.md`  
**性质**：设计与落位准备（**不是**复杂状态机规格）  
**关联闭环**：`docs/architecture/voice/LUNA_VOICE_V1_MINIMAL_FLOW.md`、`tools/verify_voice_v1_minimal_flow.py`  
**真实性**：No Fabrication Rule 仍由 `guard_v1_speakable_text` / 主线约束承载；**状态层不得绕开**（见 §G）

---

## A. 目标

在已验证的最小主链上，补一层**最薄**的**会话状态锚点**，用于：

- 记录「当前会话处于哪一步」的事实（便于观测、对账、后续挂接语义层）；
- **不**引入复杂状态机、**不**扩回复能力、**不**替代 Core 裁决。

---

## B. 最小字段（V1 先只允许这一组）

| 字段 | 含义（V1 口径） |
|------|-----------------|
| `session_id` | 会话标识（与 `VoiceInputEvent.session_id` 对齐） |
| `turn_id` | 当前轮次标识（与 `VoiceInputEvent.turn_id` / `request_id` _generation 对齐；事实源在输入事件） |
| `conversation_status` | 会话级 UX 状态（见 §C；**区别于**时间治理四态 `voice_runtime_phase`） |
| `current_mode` | 当前模式快照（与 `VoiceInputEvent.is_task_mode` / 业务 mode 对齐的字符串） |
| `last_user_text` | 上一轮**已接受**的用户文本摘要（可截断；**非**「脑补未说出内容」） |
| `last_system_text` | 上一轮**已提交播报**的系统文本（以 `SpeechRequest.text_candidate` 或等价事实为准） |
| `waiting_for_user` | 是否在等待用户下一轮输入（布尔） |
| `interrupted` | 上一轮是否被用户打断（布尔；与采集/播放侧信号对齐后更新） |

### 可选 +1 字段（仅当需要与输出链对账时）

- **`last_output_request_id`**（可选）：最后一次 `SpeechRequest.request_id`。  
  **理由**：输出与输入 `request_id` 常不一致；最小对账需要一条稳定关联。**若**短期只用 JSONL trace 对账，可暂不加入字段，不强制膨胀。

---

## C. 最小状态枚举（`conversation_status`）

建议口径（字符串枚举即可）：

| 值 | 含义 |
|----|------|
| `idle` | 无有效会话或未唤醒 |
| `listening` | 正在采集/等待切段（可与 `capturing_input` 时间窗重叠，但语义偏 UX） |
| `thinking` | 已收到本句文本，主链处理中（`dispatch` 进行中） |
| `speaking` | 已提交输出、播放中或 dry-run 等价阶段 |
| `waiting_user` | 已说完，等待用户下一轮 |

**辅助（可与 status 并存或写入 metadata，二选一即可，先不膨胀）：**

| 值 | 含义 |
|----|------|
| `interrupted` | 打断已发生，等待回收策略（可映射为 `interrupted=True` + status 回到 `listening`/`idle`） |
| `timeout_closed` | 会话窗过期或超时收口（可与 `VoiceWakeWindowManager` 过期、`cutoff_reason` 对齐） |

**与现有代码的关系（事实）：**

- `VoiceInputEvent.voice_runtime_phase` / `VoiceTimeGovernanceRuntime.phase`（`idle` / `session_open` / `capturing_input` / `processing_after_input`）是**时间治理四态**，已在事件上携带。  
- **`conversation_status`** 是 **V1 会话 UX 层**锚点，**不**替代四态；二者应对齐文档，避免混用命名。

---

## D. 最小职责

| 问题 | V1 口径 |
|------|---------|
| **说完以后系统处于什么状态？** | `conversation_status = waiting_user`（或 `idle` 若会话窗已关闭且无延续）；`waiting_for_user = True` |
| **打断以后状态怎么回收？** | `interrupted = True`；随后根据策略进入 `listening`（继续听）或 `idle`（结束）；**回收规则**应先于语义层，以采集/播放观测为准 |
| **下一句进来如何知是否同一会话延续？** | 同一 `session_id` + 会话窗仍有效（`VoiceWakeWindowManager` / `active_window` 事实）→ 视为延续；**不**凭状态层「猜」用户意图 |

### 明确不负责

- 高级意图推理、任务编排、世界状态推断  
- 用状态层**补全**用户未说清的事实（**禁止**）

---

## E. 接入落点（单一推荐方案）

**推荐（最小可落）：**

1. **新增**一个极小 `@dataclass`（例如命名 `VoiceV1SessionStateAnchor`，放置位置建议 `capabilities/voice/schemas/` 或 `capabilities/voice/runtime/`，与现有 `VoiceRuntimeContext` 区分）。  
2. **由 `VoiceInputSessionManager` 持有单实例状态**（与当前「单例 governance + 每句 `session_id` 由调用方传入」一致；多会话并发若存在，再演进到 `Dict[session_id, Anchor]`，**本轮不实现**）。  
3. **更新时机（下一轮实现时）**：  
   - **输入后**：`process_final_text` / `process_final_text_with_dispatch` 返回前：写入 `last_user_text`、`turn_id`、`conversation_status → thinking` 等；  
   - **输出后**：在 `_maybe_submit_real_output_v1` 成功构造 `SpeechRequest` 之后（或 submit 返回后）：写入 `last_system_text`、`conversation_status → speaking/waiting_user`。  

**不推荐**首轮把锚点塞进 `VoiceRuntimeContext.metadata` 作为主源：`VoiceRuntimeContext` 偏向 Core 注入，易与「Voice 侧会话锚」混淆。

---

## F. 与当前 V1 闭环的关系

- 本层**为稳住**已验证闭环服务，**不是**为扩 reply。  
- **不是**复杂多轮对话产品状态机。  
- 后续语义转换器可读取该锚点，**本轮不接语义转换器**。

---

## G. 真实性原则（高于状态层）

- 会话状态层**不能**成为「脑补上下文」的借口：  
  - 只记录**可观测事实**（输入文本、提交文本、窗是否 active、phase 等）。  
- **不能因为**「上一轮延续」就擅自补全用户未说清的事实。  
- **No Fabrication Rule**（见 `guard_v1_speakable_text` / `LUNA_VOICE_V1_PLAN.md`）**优先于**状态层便利。

---

## H. 仓库现状映射（事实摘要）

| 能力 | 位置 | 可复用性 |
|------|------|----------|
| 会话窗 / 四态 | `voice_time_governance_v1.py`、`voice_wake_window_manager.py` | **直接复用**为时间与窗事实 |
| 每句 `session_id` / `turn_id` | `VoiceInputEvent` | **直接复用**；当前 `turn_id` 与 `event_id` 同值生成 |
| `current_mode` / `interrupt_requested` | `VoiceInputEvent` | 字段已存在；**需**与锚点同步策略 |
| `context_resume_hint` / `_last_accepted_normalized` | `VoiceInputSessionManager` | **部分复用**为「上一轮用户文本」摘要，**不是**系统侧 `last_system_text` |
| Core 注入上下文 | `VoiceRuntimeContext`（含 `conversation_window_state` 占位 dict） | **可**未来挂载只读镜像，**首轮**不强制 |
| 系统上一句播报文本 | **无**一等字段 | **缺口**：需在 submit 路径或回调处记录 |

---

## I. 实现状态（首轮已落地）

- **对象**：`capabilities/voice/runtime/voice_v1_session_state_anchor.py` → `VoiceV1SessionStateAnchor`
- **持有**：`VoiceInputSessionManager.v1_session_anchor`
- **输入**：`begin_from_event` 在 `process_final_text_with_dispatch` 内、`dispatch` 之前
- **输出**：`record_successful_output` 在 `_maybe_submit_real_output_v1` 内、`VoiceOutputPlane.submit` **成功返回**之后
- **未 submit**：`apply_no_submit_conservative` 在 `process_final_text_with_dispatch` 返回前
- **验证**：`tools/verify_voice_v1_minimal_flow.py`
