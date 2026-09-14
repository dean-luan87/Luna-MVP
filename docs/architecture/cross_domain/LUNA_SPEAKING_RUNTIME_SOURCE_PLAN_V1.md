# speaking/runtime 真源方案（V1）

## 1. 目标

### 为什么 submit 闭环成立后，下一步要补 speaking/runtime 真源

在《[LUNA_REAL_OUTPUT_SUBMIT_V1_IMPLEMENTED_NOTE.md](./LUNA_REAL_OUTPUT_SUBMIT_V1_IMPLEMENTED_NOTE.md)》中，系统已经证明“真实输出链”最小闭环成立：

- `SpeechRequest` 能被真实生成
- `VoiceOutputPlane.submit()` 能被真实调用
- `request_id` 能串起最小 trace（`submit_invoked/selection/cutover/playback`）
- 默认关闭、可回退；跨域旁路仍为 whitebox-only 不越权

此时 speaking/runtime 的“真状态”才有可依附的锚点：**真实请求生命周期**。如果在 submit 之前讨论 speaking/runtime，只能得到不绑定真实请求的推断状态，后续还要重做“状态归属边界”的对齐。

### 这份文档解决什么问题

本文件只做方案（不改代码、不扩 submit 候选范围），回答：

- speaking/runtime 的**真状态**到底有哪些（状态机与事件定义）
- 哪些节点可以算“真源”，哪些只能算“推断/派生”
- 真源应挂在哪一层，如何与现有 submit 闭环耦合并保持可观测
- 为什么在缺少真源前，**不得讨论真实抢占与 Level 2**

---

## 2. 当前现状（事实）

### 2.1 已有最小 trace（但 speaking 仍不可信）

当前最小闭环 trace 已具备：

- `submit_invoked`（证明 submit 被调用）
- `selection`（provider 选择）
- `cutover`（provider chain / legacy 的终态）
- `playback`（目前用于闭合终态的占位 observation；**不等同** speaking 真源）

这些节点足以证明“提交链成立”，但**不足以证明“正在播报”**，因为 Stage-2/2.1 明确不接 `speech_gate/audio_worker`。

### 2.2 当前仍没有可信的 speaking/runtime 状态源

- `VoiceFinalTextDispatchResult.metadata` 与三条旁路白盒仅用于**观测/对账**，不能当作 speaking 真状态。
- `PlaybackObservation` 当前仍为 Stage-1 placeholder；其 `started/finished` 在 V1 submit 的 dry-run 模式下是人为闭合，用于证明链路节点存在，而非真实播放。

---

## 3. speaking/runtime 真状态定义（V1 状态机）

### 3.1 两层概念：request 生命周期 vs playback 生命周期

**A. request 生命周期（提交链层）**：可以在不接播放层的情况下成立（但不等于 speaking）。

- `request_created`
- `request_submitted`
- `request_accepted` / `request_rejected`

**B. playback 生命周期（执行层）**：必须绑定真实播放执行层，才配叫“speaking 真源”。

- `playback_started`
- `playback_finished`
- `playback_failed`
- `playback_cancelled`

### 3.2 最小状态集合（必须可被 request_id 串起）

V1 方案要求 speaking/runtime 真源至少覆盖以下状态与含义：

- **`request_created`**：`SpeechRequest` 已被构造（尚未提交）
- **`request_submitted`**：`VoiceOutputPlane.submit()` 已被调用（已尝试提交）
- **`playback_started`**：执行层确认已开始播放（此刻才可称 speaking=true）
- **`playback_finished`**：自然播放结束（完整播完）
- **`playback_failed`**：执行层明确失败（provider 合成失败、播放失败、delivery 失败等需区分）
- **`playback_cancelled`**：被治理层/用户/系统取消（取消原因可枚举）

### 3.3 真状态 vs 推断状态（写死口径）

- **真状态（source-of-truth）**：必须来自“拥有该事实的最靠近执行层的一点”，且能绑定 `request_id`。
- **推断状态（derived/inferred）**：由上游观测拼接、时间窗推断、或 placeholder 补齐得到；只能用于 UI/调试，不可驱动抢占/裁决。

---

## 4. 真源候选（仓库内可挂载的位置）

本节梳理可作为 speaking/runtime 真源的候选落点，并说明它们分别能覆盖哪些状态。

### 候选 A：`VoiceOutputPlane.submit()` 前后（输出面入口）

- **可覆盖**：`request_submitted`、（以及 submit 入口层的 `request_accepted/request_rejected`）
- **无法覆盖**：`playback_started/finished/...`（因为 submit ≠ 播放）
- **优点**：与当前 submit 闭环耦合最强、接入成本最低、可复用 request_id
- **缺点**：只能形成 request 层真源，不能作为 speaking 真源

### 候选 B：TTS 执行入口/返回点（`run_tts_unified_entry`）

- **可覆盖**：provider 选择、provider chain 成功/失败、rollback 终态（与 cutover/rollback observation一致）
- **无法覆盖**：真实播放开始/结束（Stage-2.1 文档边界明确“不替代 speech_gate/audio_worker”）
- **优点**：可提供“音频合成链是否成功”的真源（execution truth）
- **缺点**：仍不是 speaking 真源；只能回答“能不能生成音频”，不能回答“是否正在播报”

### 候选 C：playback/result 观测点（执行层/播放层）

> 注：当前仓库的 `PlaybackObservation` 是 placeholder，但“playback/result 观测点”这一层级是 speaking 真源唯一合理归属点。

- **可覆盖**：`playback_started/finished/failed/cancelled`（speaking 真源）
- **优点**：语义正确、可驱动后续抢占/恢复/队列治理；是 speaking 的唯一真锚点
- **缺点**：接入成本最高（需要真实播放执行层接线或模拟执行层），但这是路线 A 必经环节

### 候选 D：已有 Request Trace 抽链（聚合器视角）

- **可覆盖**：将多 observation 归并成“链路视图”
- **优点**：对排障非常强
- **缺点**：天然是“后验聚合”，不能当作真源（只适合作为观测/诊断层）

---

## 5. 候选对比（可信度 / 成本 / 耦合度）

| 候选 | 可信度（speaking 语义） | 接入成本 | 与 submit 闭环耦合度 | 是否适合做 V1 真源 |
|------|--------------------------|----------|-----------------------|--------------------|
| A `VoiceOutputPlane.submit` | 低（只能证明已提交） | 低 | 高 | **适合作为 request_submitted 真源**，不作为 speaking 真源 |
| B `run_tts_unified_entry` | 中（能证明合成/回退终态） | 中 | 中 | 适合作为 execution truth，仍非 speaking |
| C playback/result 执行层 | 高（speaking 真锚点） | 高 | 中（需保证 request_id 贯穿） | **V1 speaking 真源的唯一正确归属点** |
| D 抽链聚合器 | 低（后验推断） | 低 | 低 | 不作为真源，只作为诊断层 |

---

## 6. 推荐方案（V1）

### 6.1 推荐结论（写死）

V1 speaking/runtime 真源采取“双真源分层”：

1. **request 层真源**：以 `VoiceOutputPlane.submit()` 为锚点，定义 `request_submitted/request_accepted/rejected` 的真状态。  
2. **speaking 层真源**：以“playback/result 执行层观测点”为锚点，定义 `playback_started/finished/failed/cancelled` 的真状态。  

其中，**speaking 真状态只允许来自 playback/result 执行层**；在该真源未接入前，不得用 metadata/白盒或抽链推断去冒充 speaking=true。

### 6.2 为什么选它

- 与“submit 先于 speaking/runtime”的既定顺序一致：先建立 request 生命周期锚点，再把 speaking 真源挂到播放执行层。
- 保持概念正交：submit 负责“请求是否提交”，playback 负责“是否开始/结束播放”。两者混在一起会造成假 speaking。
- 与现有观测体系兼容：两类真源都可通过 `request_id` 写入 observation，再由抽链器聚合为完整链视图。

### 6.3 为什么其他候选暂不选为 speaking 真源

- `run_tts_unified_entry`：只能说明“合成链终态”，不等同“播放开始/结束”；不能作为 speaking 真源。
- 抽链聚合器：后验推断层，不可作为真源。
- `VoiceFinalTextDispatchResult.metadata` 与旁路白盒：属于“输入/旁路处理白盒”，与播放执行事实无关，不可充当 speaking 真源。

---

## 7. 当前阶段不做项（写死）

- 不做 speaking 接管（不让任何模块直接驱动播放层）
- 不做中断/恢复
- 不做旁路真实抢占（Level 2）
- 不做复杂播放队列与 arbitration
- 不扩 submit 候选范围

---

## 一句话收束

先把 speaking/runtime 的真状态来源（request 层锚点 + playback 执行层真锚点）定义清楚；**在没有 playback 真源前，不得讨论真实抢占与 Level 2**。

