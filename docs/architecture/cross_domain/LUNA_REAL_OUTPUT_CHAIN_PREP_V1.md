# 真实输出链准备（V1）

## 1. 目标

### 为什么现在要从 whitebox-only 转向「真实输出链准备」

在《[LUNA_MAINLINE_MIN_REAL_INTEGRATION_PATH_V1.md](./LUNA_MAINLINE_MIN_REAL_INTEGRATION_PATH_V1.md)》已经写清：跨域三条旁路已在真实主线完成 **Level 1 / whitebox-only** 深接入，并具备 `cross_domain_orchestrator_v1` 统一观察摘要。此时继续扩能力面或加旁路，边际收益会快速下降——**能力越多，若仍全部停在 metadata 白盒，对用户可感知的「说出来」仍为零**。

因此下一阶段应先把 **从白盒到真实发声** 的缺口与前置条件盘清，再决定实现顺序。

### 这份文档解决什么问题

- 把 **submit 实链、SpeechRequest 生成、输出平面、speaking/runtime 真源、输出候选进入条件、中断/恢复边界** 的现状与缺口写成可检查的清单。
- 明确 **哪条能力未来最有资格先进入真实输出候选**，以及哪些能力在相当长阶段应 **只观测、不外显**。
- 与《[LUNA_RISK_INTERRUPT_V1_LEVEL2_ADMISSION_GATE_V1.md](./LUNA_RISK_INTERRUPT_V1_LEVEL2_ADMISSION_GATE_V1.md)》对齐：**不直接跳入 Level 2 实现**，先把「真实输出链」本身的结构前提补齐。

---

## 2. 当前真实输出边界回顾

以下事实与《[LUNA_MAINLINE_MIN_REAL_INTEGRATION_PATH_V1.md](./LUNA_MAINLINE_MIN_REAL_INTEGRATION_PATH_V1.md)》一致，作为本文件的基线：

- 三条旁路（`risk_interrupt_v1` / `sidewalk_nav_v1` / `retail_find_item_v1`）在主线中 **只写入** `VoiceFinalTextDispatchResult.metadata` 下的并列白盒 key；编排层另写 `metadata["cross_domain_orchestrator_v1"]` 观察摘要（见《[LUNA_CROSS_DOMAIN_ORCHESTRATOR_V1_IMPLEMENTED_NOTE.md](./LUNA_CROSS_DOMAIN_ORCHESTRATOR_V1_IMPLEMENTED_NOTE.md)》）。
- **当前不进入真实输出候选**：旁路白盒中的 `final_spoken_output` 在深接入阶段被写死为空或等价于不外显，且 `near_real_output_candidate_any` 在 orchestrator 摘要中固定为 `False`。
- **当前不提交 `SpeechRequest`**：`capabilities/voice/runtime/voice_final_text_dispatcher.py` 分流路径不构造、不传递 `SpeechRequest`。
- **当前不走 `VoiceOutputPlane.submit()`**：`capabilities/voice/interfaces/voice_output_plane.py` 仅为 **Protocol（Stage-1 placeholder）**，仓库内 **未发现**实现该协议的输出平面实现类；主线分流结果也未接入该接口。

补充事实（仓库内已存在、但**未与语音输入主线分流闭环**）：

- `SpeechRequest` 数据结构与 `VoiceOutputPlane.submit()` 接口已存在（占位）。
- 另有 TTS 相关模块以 `SpeechRequest` 为输入（例如 `capabilities/voice/runtime/tts_unified_entry.py`、`capabilities/voice/output/tts_request_executor.py`），其文档边界写明 **不替代 speech_gate / audio_worker**、不承诺与主分流自动闭环。  
  这意味着：**「能生成 SpeechRequest」的代码片段存在，但「从本轮分流结果到用户可听」的统一点尚未成为主线事实链**。

---

## 3. 真实输出链缺口清单

以下按「是否存在 / 卡在哪」罗列，便于后续拍板实现顺序。

| 缺口项 | 当前状态（事实） | 典型缺口说明 |
|--------|------------------|----------------|
| **submit 实链是否存在** | **未在语音输入主线成立** | 从 `voice_final_text_dispatcher` 的 `VoiceFinalTextDispatchResult` 到「提交一次可发声请求」没有统一、可观测的调用链。 |
| **`SpeechRequest` 真实生成路径是否成立** | **未与主线分流绑定** | 结构体存在；但 **缺少**「由哪一层、在哪些不变量下、把哪类文本候选升格为 `SpeechRequest`」的主线契约。 |
| **`VoiceOutputPlane.submit()` 真实调用链是否成立** | **不成立** | 仅有 Protocol；无实现类接入；无主线调用点。 |
| **speaking/runtime 真状态来源是否存在** | **在 Stage-1 分流语境下基本不可用** | 旁路侧仍以占位/替代观测为主；`VoiceRuntimeContext` 虽有 `output_busy_state` 等字段，但 **不等价于**真实播报/队列/打断状态。 |
| **输出候选的最小进入条件是否存在** | **未形成主线级契约** | 白盒字段不等同于「可提交候选」；缺少：来源、优先级、去重、冷却、与任务/确认态冲突等 **最小准入规则**。 |
| **中断/恢复边界是否存在** | **未形成可执行边界** | 风险抢占、恢复、误抢占观测等仍停留在准入文档与旁路逻辑概念层，**未**与真实输出队列/播放状态对齐。 |

---

## 4. 最小前置条件分组

建议把「真实输出链」补齐的前置拆成三组，后续评审与实现顺序可逐组过关。

### 4.1 结构前置（submit / output plane / request path）

- **单一输出面**：明确 `VoiceOutputPlane` 的实现落点与职责边界（谁构造 `SpeechRequest`、谁提交、谁观测）。
- **主线挂钩点**：`VoiceFinalTextDispatchResult` 之后，哪一层是「唯一可提交」的入口（避免多入口直驱 TTS）。
- **可追溯**：从 `request_id/session_id` 到一次 `submit` 尝试可打点（成功/拒绝/原因）。

### 4.2 运行态前置（speaking / 当前输出状态 / 可观测性）

- **真源**：定义「正在播报 / 队列深度 / 是否可打断」的 **单一可信来源**（或受控的多源融合规则），并明确刷新频率与失效策略。
- **桥接到主线**：`VoiceRuntimeContext` 或等价通道如何承载只读运行态（避免旁路再猜）。
- **可观测性**：输出侧与运行态侧至少有一套可对账字段（日志/结构化事件/metadata）。

### 4.3 安全前置（回退 / 误抢占观测 / 降级链）

- **可回退**：任何真实输出候选路径必须可关闭并回到「仅白盒/零旁路」基线（与现有准入门槛一致）。
- **误抢占/误外显可度量**：至少能区分「设计未外显」「被策略拒绝」「异常失败」。
- **降级链**：provider/输出平面失败时的降级策略（静音/提示/回退/仅记录）需先定义，再谈抢占。

---

## 5. 哪些能力未来最有资格先进入真实输出候选（排序建议）

> 说明：本节是 **路线 A（补真实输出链）** 下的候选优先级，不是实现承诺；**不**等同于 Level 2。

### 5.1 第一：`risk_interrupt_v1`

- **原因**：安全优先；与「抢占/中断」语义天然对齐；也是 Level 2 准入讨论的主轴（见《[LUNA_RISK_INTERRUPT_V1_LEVEL2_ADMISSION_GATE_V1.md](./LUNA_RISK_INTERRUPT_V1_LEVEL2_ADMISSION_GATE_V1.md)》）。
- **但仍需**：submit 实链 + speaking/runtime 真源 + 可执行回退 + 误抢占观测，缺一不得进入真实抢占。

### 5.2 第二：`sidewalk_nav_v1`

- **原因**：导航提示属于高频外显，但 **非安全链默认应让位于风险**；在风险压制语义稳定后，可作为「非抢占型外显候选」的第二批试点。
- **前提**：环境摘要来源稳定、控噪策略可接受；仍建议长期保持 **强约束与可回退**。

### 5.3 第三：`retail_find_item_v1`

- **原因**：涉及场景 gating、意图与 OCR 补证接口位，外显误触成本高；更适合在 **真实输出链与观测面稳定** 后再进入候选讨论。
- **阶段建议**：在相当长周期内可 **只允许观测（白盒/结构化字段）**，默认不外显或仅允许极低风险的提示形态（需单独产品/安全评审）。

### 5.4 「先永远不能进」与「先只允许观测」

- **先永远不能进（在真实输出链未成立前）**：任何旁路的 **非白盒外显**、任何绕过输出面的 **直驱 TTS**、任何未定义准入条件的 **自动抢占候选**。
- **先只允许观测（默认）**：`retail_find_item_v1` 与 `sidewalk_nav_v1` 在多数阶段应优先作为 **观测与策略验证**；`risk_interrupt_v1` 在未满足准入门槛前也只允许 **白盒/观测**（与 Level 1 现状一致）。

---

## 6. 当前阶段不做项（写死）

- 不实现 submit 实链（本文件只做缺口梳理）
- 不实现 speaking/runtime 接管
- 不实现 Level 2（真实抢占/挂起/恢复）
- 不实现真实输出候选（不把旁路白盒升格为可提交 `SpeechRequest`）
- 不实现复杂 output arbitration（全局多候选裁决器）

---

## 一句话收束

先把从 whitebox-only 走向真实输出链的 **缺口与前置条件** 梳理清楚，再决定后续是先补 **submit 实链 / 输出平面实现**，还是先补 **speaking/runtime 真状态来源与桥接**（或两者并行但边界清晰）。
