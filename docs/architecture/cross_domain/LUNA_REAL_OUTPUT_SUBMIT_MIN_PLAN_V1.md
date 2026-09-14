# 真实输出链最小 submit 方案（V1）

## 1. 目标

### 为什么当前先补 submit / 输出平面，而不是先补 speaking/runtime

当前系统已经具备旁路 whitebox-only 深接入、统一编排入口与观察摘要，但**缺少真实提交链**：

- `SpeechRequest` schema 已存在（`capabilities/voice/schemas/speech_request.py`）
- `VoiceOutputPlane.submit()` 接口已存在（`capabilities/voice/interfaces/voice_output_plane.py`）
- 语音主线分流与 cross-domain orchestrator 已真实接入（见《[LUNA_MAINLINE_MIN_REAL_INTEGRATION_PATH_V1.md](./LUNA_MAINLINE_MIN_REAL_INTEGRATION_PATH_V1.md)》）
- **但主线分流路径并不构造 `SpeechRequest`，也不调用 `VoiceOutputPlane.submit()`**

在“提交动作”不存在的前提下先补 speaking/runtime，会得到不绑定请求的“假状态”，后续补 submit 时还会反复重对齐“状态属于哪个节点”的边界。因此顺序必须先补：

> **让输出请求真的能走起来（生成 + submit + 可验证），再定义它什么时候算开始播、结束播。**

### 这份文档解决什么问题

本文件只做方案定义，不改代码，目标是把“最小真实 submit 闭环”写清楚：

1. `SpeechRequest` 在当前主线里的**最小生成点**应在哪里  
2. `VoiceOutputPlane.submit()` 在当前主线里的**最小调用点**应在哪里  
3. V1 **只允许什么类型**的输出进入真实提交候选  
4. whitebox-only 如何升级到“真实输出候选但仍严格限制”的**演进形态（非实现）**  
5. 在不接 speaking/runtime 真源的情况下，如何**验证** submit 动作成立

---

## 2. 当前现状（事实）

### 2.1 结构体/接口已存在

- `SpeechRequest`：`capabilities/voice/schemas/speech_request.py`
- `VoiceOutputPlane`（Protocol）：`capabilities/voice/interfaces/voice_output_plane.py`

### 2.2 主线不提交真实输出请求

语音输入主线分流入口：

- `capabilities/voice/runtime/voice_final_text_dispatcher.py::dispatch_voice_final_text(...)`

其返回 `VoiceFinalTextDispatchResult`，并在三条分支（short/long/reject）末尾统一进入：

- `_run_cross_domain_orchestrator_v1(...)`

当前 **旁路仍停在 metadata / whitebox-only**：

- `risk_interrupt_v1` / `sidewalk_nav_v1` / `retail_find_item_v1` 仅并入 `VoiceFinalTextDispatchResult.metadata[...]`
- orchestrator 摘要 `metadata["cross_domain_orchestrator_v1"]` 中 `near_real_output_candidate_any=False`

### 2.3 仓库内存在可接 `SpeechRequest` 的 TTS 入口，但未成为“主线事实链”

仓库中已有以 `SpeechRequest` 为输入的 TTS 执行入口（用于骨架与观测）：

- `capabilities/voice/output/tts_request_executor.py::execute_tts_request(request=SpeechRequest, ...)`
- `capabilities/voice/runtime/tts_unified_entry.py::run_tts_unified_entry(request=SpeechRequest, legacy_submit=..., ...)`

但这些入口**尚未**被 `dispatch_voice_final_text` 的主线分流调用，因此“真实 submit 闭环”对主线而言仍未成立。

---

## 3. 最小 submit 闭环定义（V1）

本节定义“最小闭环”应包含的三个动作：**生成请求、调用 submit、形成可验证观测**。它不等同于完整输出系统，不触及 speaking/runtime。

### 3.1 哪一层生成 `SpeechRequest`

**建议生成点（最小且不破坏现有分流职责）**：

- 位置：`VoiceFinalTextDispatchResult` 生成完成、`cross_domain_orchestrator_v1` 运行完成之后  
  （原因：旁路白盒与编排摘要已挂载完成，便于把 metadata 投影到 request.metadata，且不改变分流裁决本身）

**约束（写死）**：

- V1 生成 `SpeechRequest` 的候选必须来自“原主链稳定输出”的文本（见 §4）  
- V1 不允许旁路直接生成可外显文本候选（跨域旁路仍为 whitebox-only）

> 注：当前 `VoiceFinalTextDispatchResult` 本身未定义统一的“最终将播报文本字段”，因此 V1 方案必须同时定义“主链稳定输出文本的最小来源”（见 §4.1）。该来源在实现阶段可落为一个极小的文本映射/生成层，但本文件不实现。

### 3.2 哪一层调用 `VoiceOutputPlane.submit()`

**建议调用点（最小且单出口）**：

- 一个“输出面入口层”（可被主线唯一调用），负责：
  - 接收 `SpeechRequest`
  - 执行 selector/provider chain（或 legacy）
  - 记录 observation（用于验证 submit 动作成立）

V1 方案不要求立刻接入真实播放执行层（speech_gate/audio_worker），但必须保证：

- 存在一个**单一 submit 入口**，主线不允许多点直连 TTS
- `request_id` 能贯穿 observation，满足抽链规则（见 §5）

### 3.3 第一版允许什么类型的输出进入真实提交候选

V1 允许的范围应极窄，只为“把 submit 链跑起来”服务：

- **仅允许**：原主链已经稳定、低风险、可预测的“确认/提示类”短文本（例如 reject 提示、session wake 提示、已知白名单动作的确认提示等）  
- **默认拒绝**：任何开放式长文本、任何需要复杂裁决的多候选输出、任何跨域旁路外显输出

### 3.4 当前哪些旁路仍然不能进 submit（写死）

V1 写死：以下旁路**不得**直接进 submit：

- `risk_interrupt_v1`（即使最接近 Level 2，也必须等 submit 实链与 speaking/runtime 真源成立后再评审）
- `sidewalk_nav_v1`
- `retail_find_item_v1`

旁路当前仅允许：

- 继续 whitebox-only 进入 `VoiceFinalTextDispatchResult.metadata`
- 通过 orchestrator 摘要提供“是否接近真实候选”的编排层观测（但 V1 摘要仍固定为 `False`）

---

## 4. 第一版候选范围（明确口径）

### 4.1 submit 候选应只来自原主链稳定输出

V1 的 submit 候选必须来自“原主链稳定输出”，原因：

- 主线分流已稳定：short/long/reject 的结构化结果可重复验证
- 跨域旁路仍处于 Level 1：只应观测，不应外显
- 先把“提交链”跑通，再谈“由谁提供候选文本”

在实现阶段，需要补一个最小映射/生成层，将 `VoiceFinalTextDispatchResult` 的分流结果映射为**极少数**可播报文本（提示/确认语句）。本文件只要求该映射层满足：

- 文本集合可枚举、可测试（避免隐式 prompt）
- 默认关闭零侵入（开关控制）
- 不影响 `dispatch_type/notes` 与旁路白盒语义

### 4.2 跨域旁路先不直接进 submit

写死口径：V1 submit 闭环不把 `risk_interrupt_v1/sidewalk_nav_v1/retail_find_item_v1` 的任何字段升格为可播报文本候选。

后续若进入“能力候选晋升”评审：

- 优先还是 `risk_interrupt_v1`（安全优先）
- 但必须满足《[LUNA_RISK_INTERRUPT_V1_LEVEL2_ADMISSION_GATE_V1.md](./LUNA_RISK_INTERRUPT_V1_LEVEL2_ADMISSION_GATE_V1.md)》的准入门槛

### 4.3 whitebox-only 如何升级到“真实输出候选但仍严格限制”（不实现，仅定义形态）

建议的最小升级形态（后续里程碑，不在 V1 实现）：

- **L1（当前）**：whitebox-only → 仅写 metadata，不产生可提交候选
- **L1.5（候选受限）**：允许产生“候选标记”，但仍不 submit（仅观测：候选计数、原因码、抑制原因）
- **L2（真实候选）**：在具备 submit 实链 + speaking/runtime 真源 + 回退链后，才允许将候选进入 submit（仍需 gate/优先级/去重/冷却等）

---

## 5. 最小验证方式（不补 speaking/runtime 的前提下）

V1 只验证“提交动作成立”，不验证“正在播报”的真状态。

### 5.1 submit 链打通后如何验证

最小验证应包含两类证据：

1) **结构化返回**：submit 入口返回 (accepted, reason) 或等价结构  
2) **结构化 observation**：可按 `request_id` 抽链，确认请求至少走过 MUST 节点

### 5.2 哪些字段必须可观察（最小集合）

与 `docs/architecture/voice/LUNA_VOICE_REQUEST_TRACE_EXTRACTION_RULES_V1.md` 对齐，最小闭环抽链必须能确认：

- `request_id`（必须）
- `request_ingress`（能确认请求进入）
- `provider_selection`（至少能看到 `chosen_provider`）
- `playback_result` 或等价终态（能看到 `final_execution_mode`）

注意：当前抽链实现中 `message_preparation` 被标记为 `not_connected`，并明确指出：

- “SpeechRequest 未在日志行中持久化；需主链显式落盘”

因此 V1 验证必须优先满足：**request_id 驱动的链级 observation 能闭合**，而不是先追求 speaking/runtime。

### 5.3 在不补 speaking/runtime 的情况下，如何确认提交动作成立

V1 的“提交动作成立”判定建议写死为：

- submit 入口被调用（可由 observation ingress 证明）
- 发生 provider selection（可由 selection observation 证明）
- 产生终态（provider_chain / legacy_fallback / failed_no_output 等），可被抽链脚本归类为 success/fallback/rollback/failed/suppressed

该判定不要求真实播放开始/结束，只要求“输出链的结构骨架已闭环且可观测”。

---

## 6. 与 speaking/runtime 的关系（写死口径）

- speaking/runtime 真源属于“输出链跑起来之后的运行态观察层”，应挂在 request 生命周期节点上：  
  `request_created` → `request_submitted` → `request_accepted` → `playback_started` → `playback_finished/interrupted`
- 在 submit 闭环未成立前，提前定义 speaking/runtime 会缺少锚点，容易形成不可对账的假状态
- 因此 speaking/runtime 是下一阶段；submit 链是 speaking/runtime 的前置

---

## 7. 当前阶段不做项（写死）

- 不补 speaking/runtime 真源
- 不让跨域旁路进入真实输出（旁路不 submit）
- 不进入 Level 2（不做抢占/挂起/恢复）
- 不做复杂中断/恢复编排
- 不做复杂 arbitration（全局多候选裁决器）

---

## 一句话收束

先把真实输出链里“`SpeechRequest` 如何生成、如何 submit、如何验证”这条最小闭环写清楚，再进入下一阶段的 speaking/runtime 真源建设。

