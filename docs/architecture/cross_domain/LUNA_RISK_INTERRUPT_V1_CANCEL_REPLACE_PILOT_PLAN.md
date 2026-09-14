# risk_interrupt_v1 真实取消 + 替换 试点评审方案（V1）

## 0. 一句话收束（写死）

本文件只做评审方案：在 **cancel 真能力** 已成立后，评估 `risk_interrupt_v1` 是否应从当前 **preempt-before-submit** 升级为更真实的 **cancel + replace** 试点。**当前不做实现**，且任何升级必须严格锁边界并可秒退回当前方案。

---

## 1. 目标

### 1.1 为什么在 cancel 真能力成立后，才可以讨论更真实的 interrupt 试点

在 cancel 真能力落地之前，`risk_interrupt_v1` 的 Level 2 受限试点只能做：

- **提交前替换（preempt-before-submit）**

因为系统没有一个可依附的“真实停止载体”。现在底座发生了关键变化：

- 系统已经能按 `request_id` **取消正在执行/待执行的播放请求**，并产出 `playback_cancelled` 真事件
- request/playback/cancel 事件链可对账

因此现在具备了讨论更真实“interrupt 语义落地路径”的必要条件：interrupt 在底层最终要落到 **cancel（停止当前）** + **replace（提交新输出）**。

### 1.2 这份方案解决什么问题

- 把 **cancel**（底层能力）与 **interrupt**（高层语义）、**replace**（输出替换）、**recover**（恢复）严格拆开，避免混线
- 写死“允许升级到 cancel+replace 的极小范围”与“绝对禁止项”
- 写死回退路径：任何异常必须可秒退回当前 preempt-before-submit 试点

---

## 2. 当前试点回顾（事实）

### 2.1 当前 Level 2 仍是 preempt-before-submit

当前 `risk_interrupt_v1` Level 2 受限试点实现属于：

- **提交前替换**：在生成 `SpeechRequest` 前对低价值 `prompt/confirmation` 候选进行替换，并记录 `output_decision` 观测

这不等同“真实中断播放”，也不依赖执行层停止能力。

### 2.2 当前已具备 playback_cancelled 真事件

系统已具备：

- 最小真实执行层（Playback Plane + Audio Worker）
- cancel 真能力入口（按 `request_id` 取消当前/待执行）
- `playback_cancelled` 真状态事件（执行层产出）

### 2.3 为什么还不能直接升级为全量 cancel+replace

因为 cancel+replace 的风险更高：

- 会触发“主动停止”与“新输出插入”，更接近真实中断语义
- 容易牵连任务链语义、长文本输出、队列治理与恢复策略
- 需要更严格的：误抢占/误取消观测、回退演练、执行层一致性

因此只能先做“受限评审方案”，锁死可试范围。

---

## 3. 试点范围建议（必须极窄）

### 3.1 仅允许哪些风险等级

- **仅允许**：`risk_level in {high, critical}`
- **禁止**：`low/medium/unknown`，以及任何缺失 risk_summary 的场景（缺失视为不触发）

### 3.2 仅允许哪些原输出类型被取消（写死）

- **仅允许取消**：低价值 `prompt/confirmation` 短文本输出
- **绝对禁止取消**：
  - 任务链相关输出（任何可能改变用户对任务状态理解的输出）
  - 长文本解释类输出
  - 未能按 `request_id` 对账闭合的输出链

### 3.3 仅允许哪些场景

- **仅允许**：联调/灰度环境 + 明确开启试点开关 + 观测链在线可抽链
- **绝对禁止**：默认路径/全量主线/无观测链/无回退演练

---

## 4. cancel 边界（分两层评审）

### 4.1 取消“待执行 request”（推荐先试）

定义：request 已提交，尚未出现 `playback_started`，但已进入执行层队列/待执行状态。

理由：

- 风险更可控：尚未真正开始播，取消不涉及“打断已发声内容”
- 对用户体验冲击小：更接近“撤销待播输出”

V1 试点评审建议：

- **允许**先从“取消待执行 request”开始试点

### 4.2 取消“已 started playback”（必须单独评审，不默认放开）

定义：已出现 `playback_started`，此时取消等价于“真实中断”。

风险点：

- 容易触发“中断成功/失败”的边界问题
- 更依赖执行层与设备层一致性
- 更容易引入恢复/重播争议（当前明确不做恢复）

V1 试点评审建议：

- **不默认允许**取消已 started playback  
- 若必须试，需额外前置：更严格的观测、误抢占阈值、以及更硬的回退演练

---

## 5. replace 边界（cancel 后如何替换输出）

### 5.1 cancel 之后新的 risk output 如何进入 submit

建议口径（仍保持最小化）：

- cancel 成功（或确认已落 cancelled 终态）后，才允许提交新的 risk 输出请求
- 新的 risk 输出仍必须走 `SpeechRequest → VoiceOutputPlane.submit` 的统一路径，并绑定新的 request_id（或明确的 parent_request_id 关联字段；是否新增字段由实现阶段决定）

### 5.2 哪些情况下只 cancel 不 replace

以下情况只允许 cancel，不允许 replace：

- 观测链不闭合（无法确认取消状态）
- risk_summary 抖动或来源不可信（需人工复核）
- 输出类别虽然是 prompt，但文本过长/不可控（超出短文本上限）

### 5.3 哪些情况下直接退回 Level 1

任一满足即退回 Level 1（不再尝试 cancel+replace）：

- 出现越界取消（非 prompt/confirmation）
- 出现风险不足取消（非 high/critical）
- cancel 后产生了错误终态（例如 cancelled 与 finished/failed 混淆）
- 出现链路断裂导致无法对账

---

## 6. 回退与观察（必须写死）

### 6.1 如何秒退回当前 preempt-before-submit

写死回退策略：

- 关闭“cancel+replace 试点开关”（实现阶段必须提供独立开关）
- 保持当前 `preempt-before-submit` 试点仍可用（如仍在观察期）

### 6.2 需要新增哪些观察指标

在现有 preempt 指标之外，cancel+replace 试点必须新增至少：

- cancel 调用次数（按 request_id）
- cancel 成功率（是否落到 `playback_cancelled`）
- cancel 后错误终态（cancelled 与 finished/failed 混淆次数）
- cancel→replace 的链路闭合率（cancel 终态后是否提交新输出、是否闭合）
- 误取消/误替换样本数（见下一节）

### 6.3 哪些样本必须人工复核

必须人工复核：

- 任何越界取消/风险不足取消
- 任何 cancel 后终态混淆
- 任何 cancel+replace 发生但用户最终听到文本不符合预期

---

## 7. 当前阶段不做项（再次写死）

- 不实现恢复/重播
- 不做多 request 编排（连续取消链）
- 不扩到其他旁路
- 不扩大到复杂输出类型
- 不把 risk_interrupt_v1 直接接入这条链（本文件仅评审方案，接线需后续实现评审）

---

## 一句话收束

先把 `risk_interrupt_v1` 从“提交前替换”升级到“真实取消 + 替换”的试点边界评审清楚：**先取消待执行 request、严格限制 prompt/confirmation 与 high/critical、并可秒退回 preempt-before-submit**；评审通过后再进入极小实现。

