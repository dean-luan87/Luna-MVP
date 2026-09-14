# 最小中断 / 取消语义（V1）

## 1. 目标

### 为什么现在必须定义最小中断 / 取消语义

当前系统已经具备：

- submit 闭环（`SpeechRequest` → output plane）
- request 真源（request 生命周期事件可观测）
- playback/speaking 真源（playback 生命周期事件可观测）
- 最小真实执行层骨架（Playback Plane + Audio Worker 单线程/单队列）
- `risk_interrupt_v1` Level 2 受限试点（当前仍为“提交前替换”，未做真实中断）

在这些前置已成立后，“中断/取消”如果不先写死语义与终态映射，后续实现会出现不可对账与不可回退的混乱：

- request 已创建但未播放，到底算 cancel / reject / fail？
- playback 已开始但被主动停止，到底算 failed 还是 cancelled？
- 被 risk 抢占时，原输出（被抢占的那条）应落到什么终态？如何留证据？

### 这份文档解决什么问题

本文件只定义 **语义 + 权限 + 事件映射**，不给实现细节，不进入复杂恢复：

- 定义 interrupt / cancel / reject / fail / terminal_observed 的严格区别
- 规定 request/playback 两层在各阶段允许的取消点与终态落点
- 规定未来哪些模块允许发起 cancel/interruption，哪些绝对禁止
- 规定最小 observation/白盒/运行态写入边界，保证可抽链对账与可回退

---

## 2. 当前状态回顾（事实）

- submit/request/playback 真源已成立，且以 `request_id` 为主键可对账。
- 最小真实执行层已成立（Playback Plane + Audio Worker），但仍是 V1 极简形态（单线程、单队列、无复杂队列治理）。
- 当前 `risk_interrupt_v1` 仍只做 **“提交前替换式抢占”（preempt-before-submit）**，未进入真实播放中的中断/取消。

---

## 3. 术语定义（必须区分）

> 本节写死口径：这些术语不是一回事，且映射到不同的事件与证据面。

### 3.1 interrupt（中断）

**定义**：在 playback 已开始（已观测到 `playback_started`）之后，由有权限的发起方要求停止当前播放，并进入一个明确的终态（通常为 cancelled），同时可能触发下一条输出的提交/播放（但本 V1 不讨论“下一条如何上”）。

**关键点**：

- interrupt 发生的前提是 **playback_started 已发生**（否则不叫中断）。
- interrupt 是一种“主动停止”，不等同失败。

### 3.2 cancel（取消）

**定义**：对某个 request 的输出意图进行撤销。cancel 可以发生在两层：

- request 层：请求尚未开始播放之前的撤销（或撤销提交/排队）
- playback 层：播放已开始后的主动停止（此时 cancel 与 interrupt 在行为上接近，但语义上 cancel 强调“撤销该 request 的输出”，interrupt 强调“打断当前播放态”）

V1 简化口径：**playback_started 之后的主动停止统一落为 playback_cancelled**（interrupt/cancel 的差异留给上层“发起方语义”区分）。

### 3.3 reject（拒绝）

**定义**：在 request 尚未进入执行链之前（通常是 submit/routing/policy 阶段），系统明确拒绝该请求进入执行链。

reject 的特征：

- request 不会进入 playback_started
- reject 是“未接受”，不是“已接受后失败”

### 3.4 fail（失败）

**定义**：系统尝试执行后失败（合成失败、播放失败、执行层异常等）。

fail 的特征：

- 可能发生在 playback_started 之前（例如无音频产物）或之后（播放过程中异常）
- fail 必须尽量带可归因 reason（timeout/exception/invalid_audio 等）

### 3.5 terminal_observed（终态已观测）

**定义**：对同一 `request_id`，系统已经观测到“当前可见的终态”，可以作为抽链闭合点。

注意：

- terminal_observed 是“观测层闭合点”，不等价于“用户真的听完了”
- 在 V1 极简执行层下，terminal 可能代表“执行层已处理完成”，不代表真实设备播放完成

---

## 4. request 层语义（何时可取消、终态怎么落）

> request 层以 `request_runtime` 事件为主证据面。

### 4.1 request 的最小阶段

- `request_created`
- `request_submitted`
- （可选）`request_submit_rejected` / `request_submit_failed`
- `request_terminal_observed`

### 4.2 request 在哪些阶段可以被取消（V1 语义）

V1 定义 request 可取消窗口：

- **created → submitted 之前**：允许取消（等价于“撤销未提交请求”）
- **submitted 之后但 playback_started 之前**：允许取消（等价于“撤销已提交但未开始播放的请求”）

### 4.3 request 被取消后应落什么终态（V1）

V1 建议终态落点：

- request 层：写入 `request_terminal_observed`，并在 metadata/reason 中标注 `cancelled`（具体事件类型是否新增由实现阶段决定，本文件只定义语义要求）
- playback 层：若尚未 started，则不产生 playback_started；可产生 `playback_cancelled`（由执行层确认是否已入队/已开始）

### 4.4 未提交前与已提交后的取消差异（写死）

- **未提交前取消**：属于 request 层撤销，禁止产生任何 playback_started
- **已提交后取消**：必须依赖执行层/队列状态确认是否已开始；若未开始则应落 cancelled，不得落 failed

---

## 5. playback 层语义（started 之后的取消/失败边界）

> playback 层以 `playback_runtime` 事件为主证据面（执行层真源）。

### 5.1 playback_started 之后什么叫取消

**定义**：播放已开始（`playback_started` 已写入），随后被外部主动停止，落为：

- `playback_cancelled`

必须带 reason（例如 user_cancel / policy_cancel / risk_interrupt 等）。

### 5.2 playback_failed 与 playback_cancelled 的边界（写死）

- **cancelled**：外部主动停止（有发起方/权限），属于“撤销/打断”语义
- **failed**：执行层内部错误或不可恢复异常（无明确外部停止指令），属于“失败”语义

禁止用 failed 冒充 cancelled（会导致误抢占/误取消不可统计）。

### 5.3 被外部主动停止算什么

只要是“有权限的外部发起停止”，一律算：

- `playback_cancelled`

### 5.4 播放自然结束算什么

播放自然结束落为：

- `playback_finished`

---

## 6. 发起方与权限（谁可以发起 cancel/interrupt）

### 6.1 未来允许的发起方（候选）

仅列候选，不代表现在已实现：

- 输出治理层（policy/gate）
- 用户显式停止（user cancel）
- 风险安全链（risk_interrupt）—— **必须严格受限**

### 6.2 当前阶段绝对不能发起的模块（写死）

- `sidewalk_nav_v1`
- `retail_find_item_v1`
- 任何未进入真实输出链的旁路（whitebox-only 旁路）

### 6.3 risk_interrupt_v1 若未来升级，应该属于哪种语义

写死口径：

- 当前试点仍为 **preempt-before-submit**（不属于 interrupt/cancel）
- 若未来从“提交前替换”升级为“真实播放中打断”，则其动作必须被定义为：
  - playback 层：`playback_cancelled`（reason 标记为 risk_interrupt）
  - 并且必须满足 Level 2 更高门槛（中断/恢复边界、误抢占观测、回退演练等）

---

## 7. 最小事件映射（语义 → 事件/观测）

### 7.1 语义到事件的映射表（V1）

| 语义 | request 层事件（request_runtime） | playback 层事件（playback_runtime） | 备注 |
|------|----------------------------------|-------------------------------------|------|
| reject | request_submit_rejected 或 terminal_observed(reason=reject) | 不应出现 started | reject 是未进入执行链 |
| fail（合成失败/无音频） | request_terminal_observed(status=fail) | playback_failed(reason=no_audio_bytes 等) | 不应写 cancelled |
| cancel（未开始播放） | terminal_observed(reason=cancel) | playback_cancelled（若已入队且执行层确认） | 禁止 started |
| interrupt（已开始播放后打断） | terminal_observed(reason=interrupt/cancel) | playback_cancelled(reason=...) | V1 不区分 interrupt/cancel 的终态事件类型，靠 reason 区分 |
| 自然结束 | terminal_observed(status=ok) | playback_finished | started→finished |

### 7.2 哪些要写 observation / 哪些要进白盒 / 哪些要进运行态

V1 写死：

- **observation（必须）**：
  - request_runtime（created/submitted/terminal）
  - playback_runtime（started/finished/failed/cancelled）
- **白盒（允许，但不得冒充真状态）**：
  - 旁路白盒可记录“建议取消/建议中断”的理由，但不得写 speaking=true 或伪造 playback_started
- **运行态（后续再做）**：
  - speaking/runtime 聚合态应由执行层事件驱动生成（不在本 V1 方案实现范围）

---

## 8. 当前阶段不做项（写死）

- 不做恢复
- 不做多 request 编排
- 不做复杂播放队列
- 不做跨旁路真实中断
- 不做 Level 2 扩边界实现

---

## 一句话收束

先把 interrupt/cancel/reject/fail/terminal_observed 的语义与终态映射写清楚并对齐到 request/playback 真源事件，再进入最小中断/取消实现阶段。

