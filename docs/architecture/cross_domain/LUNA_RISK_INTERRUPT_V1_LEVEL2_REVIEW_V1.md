# risk_interrupt_v1 Level 2 候选评审（V1）

## 1. 评审目标

### 为什么现在可以开始做 Level 2 候选评审

与此前仅有 whitebox-only 的状态相比，当前“真实输出链”已具备三段系统事实：

- **submit 闭环成立**（`SpeechRequest` 生成 → `VoiceOutputPlane.submit()` 被调用）
- **request 真源成立**（`request_created/request_submitted/.../terminal` 事件可观测，且同一 `request_id` 串起）
- **playback/speaking 真源成立（V1）**（`playback_started/finished/failed/cancelled` 事件可观测，且与 request 同一 `request_id` 串起；dry-run 不伪造）

因此现在适合回到《[LUNA_RISK_INTERRUPT_V1_LEVEL2_ADMISSION_GATE_V1.md](./LUNA_RISK_INTERRUPT_V1_LEVEL2_ADMISSION_GATE_V1.md)》，做一次正式对账：**哪些门槛已满足、哪些仍未满足、哪些是部分满足**，并据此给出单选结论。

### 这份评审解决什么问题

- 让 Level 2 不再依赖“感觉推进”，而是基于可核查的证据面推进
- 把“可进入试点设计”的边界写死（允许试，但只能怎么试）
- 明确秒退到 Level 1 / Level 0 的条件与信号

---

## 2. 对照准入门槛逐项核对（必须对账）

对照基线文档：`LUNA_RISK_INTERRUPT_V1_LEVEL2_ADMISSION_GATE_V1.md`。

### 2.1 必要前置条件（Gate §4）

1) **真实 `SpeechRequest` → `submit` 链存在且可观测**  
- **结论**：**已满足（V1）**  
- **证据面**：  
  - submit 最小闭环已落地并通过回归（见《[LUNA_REAL_OUTPUT_SUBMIT_V1_IMPLEMENTED_NOTE.md](./LUNA_REAL_OUTPUT_SUBMIT_V1_IMPLEMENTED_NOTE.md)》）  
  - trace/抽链节点存在（submit/selection/cutover 等）且 `request_id` 可串起
- **备注**：当前 submit 候选范围仍极窄（提示/确认短文本），但“链存在且可观测”门槛已过。

2) **真实 speaking/runtime 状态来源存在且可信**  
- **结论**：**部分满足（V1，替代执行层锚点）**  
- **证据面**：  
  - 已有 playback/speaking 真状态事件（见《[LUNA_PLAYBACK_RUNTIME_SOURCE_V1_IMPLEMENTED_NOTE.md](./LUNA_PLAYBACK_RUNTIME_SOURCE_V1_IMPLEMENTED_NOTE.md)》）  
  - 并且守住关键边界：dry-run 不伪造 playback_started
- **未满足点（写死）**：  
  - 当前 repo 仍未接入真实 `speech_gate/audio_worker`，V1 以最小 playback 执行器作为执行层锚点；其语义正确（事件属于执行层），但还不是“真实设备/队列播放”。

3) **真实输出中断/恢复边界已定义**  
- **结论**：**未满足**  
- **缺口**：  
  - 尚未定义可执行的中断粒度、恢复策略、与任务链交互边界

4) **误抢占可观测**  
- **结论**：**未满足（需要 Level 2 试点设计阶段补齐）**  
- **缺口**：  
  - 当前没有“抢占尝试”的结构化事件与原因码（因为尚未进入 Level 2 实现）

5) **回退路径明确可执行**  
- **结论**：**部分满足（Level 1/输出链）**  
- **证据面**：  
  - submit 路径默认关闭、可一键回退（`LUNA_ENABLE_REAL_OUTPUT_SUBMIT_V1`）  
  - 编排层仍有回退开关（`LUNA_DISABLE_CROSS_DOMAIN_ORCHESTRATOR_V1`）  
  - risk_interrupt_v1 自身仍处于 Level 1 whitebox-only（可关闭旁路开关）
- **未满足点（写死）**：  
  - Level 2 专属回退开关与“抢占副作用”回退演练尚不存在（因为 Level 2 未实现）

### 2.2 观察与数据门槛（Gate §5）

- **Level 1 白盒稳定性**：仍需在更长窗口样本上证明（当前属于“可开始收集与评估”，非自动通过）。  
- **风险摘要来源稳定性**：依赖 `risk_summary_v1` 上游；当前已在主线形成优先读 `runtime_context` 的通路，但稳定性与缺省策略需专项数据确认。  
- **orchestrator 观察摘要稳定性**：已具备（`metadata["cross_domain_orchestrator_v1"]`），可作为 Level 2 评审的证据面。  
- **误压制/误标记可衡量**：尚未系统化（与 Level 2 试点设计中“误抢占观测”一起补齐更合理）。  
- **白盒字段完整率**：可开始统计，但需真实运行样本积累。

### 2.3 主线工程门槛（Gate §6）

- **输出平面/submit 实链**：**已具备最小实现（V1）**（证据：submit 闭环 + request 真源）。  
- **运行态桥接**：**部分具备（V1）**（playback 事件可串起，但真实执行层接线仍缺）。  
- **编排层承载**：已具备统一入口与观察摘要，且未破坏旁路边界。

### 2.4 回退门槛（Gate §7）

- **秒退 Level 1**：已具备（关闭 Level 2 未实现，因此当前等价为保持 Level 1；并可关闭 submit 新路径）。  
- **秒退 Level 0**：具备基本手段（旁路全关 + submit 关闭），但尚未演练“Level 2 副作用”场景（因未实现）。

---

## 3. 当前最接近 Level 2 的能力边界（risk_interrupt_v1）

### 3.1 已具备的真实链路能力（事实）

- risk_interrupt_v1 已完成 Level 1 whitebox-only 真实主线接入（`metadata["risk_interrupt_v1"]`）  
- 主线具备 submit/request/playback 三段“系统事实链”，可为未来 Level 2 抢占提供锚点

### 3.2 什么时候才可能进入真实抢占候选

必须满足至少以下前置：

- 在“真实播放执行层”意义上 speaking 真源可用（不依赖 placeholder）
- 中断/恢复边界定义完成（可执行、可回退）
- 抢占尝试与误抢占可观测（结构化事件/原因码可聚合）

### 3.3 什么时候仍然只能停留在 Level 1

任何满足以下之一时，risk_interrupt_v1 仍必须停留 Level 1（只白盒、不抢占）：

- speaking/playback 真源不可用或不可对账
- submit 链观测断裂（无法用 request_id 闭合）
- 回退链不可执行或未验证

---

## 4. Level 2 试点范围建议（若评审允许进入试点设计）

> 注意：本节仅定义“受限试点设计”的边界，不等同允许实现抢占上线。

### 4.1 仅允许哪类风险等级进入试点候选

- **仅允许**：`risk_level in {high, critical}`  
- 其余等级（low/medium/unknown）全部禁止进入 Level 2 试点候选

### 4.2 第一版只允许抢占哪类输出

在不扩 submit 候选范围的约束下，V1 真实 submit 目前只覆盖提示/确认短文本。若进入试点设计，第一版抢占应进一步收紧为：

- **仅允许抢占**：低价值提示类（prompt/confirmation）  
- **禁止抢占**：任何任务规划类、长文本解释类、以及任何来自跨域旁路的外显输出（当前旁路本就禁止进 submit）

### 4.3 仅允许哪些场景 / 哪些场景绝对禁止

在未接入真实设备/队列播放前，建议写死：

- **仅允许场景**：联调/灰度环境、明确开启试点开关、且观测链在线可抽链  
- **绝对禁止**：默认路径/全量主线、无观测链、无回退演练、以及任何可能影响任务链状态的抢占（未定义挂起/恢复边界）

---

## 5. 回退要求复核（秒退能力）

### 5.1 是否已具备秒退到 Level 1

**结论**：**具备（对当前状态）**。  
原因：Level 2 尚未实现真实抢占副作用，因此“秒退到 Level 1”的最小可执行动作等价于：

- 关闭任何 Level 2 试点开关（未来新增时必须支持）
- 保持 `risk_interrupt_v1` 继续停留在 Level 1 whitebox-only（或直接关闭旁路开关）

### 5.2 是否已具备秒退到 Level 0

**结论**：**具备基本手段，但需在试点设计阶段写死演练流程**。  
当前可执行的 Level 0 回退组合（写死口径）：

- 关闭 `risk_interrupt_v1`（`LUNA_ENABLE_RISK_INTERRUPT_V1=0` 或等价总开关）
- 关闭 submit 新路径（`LUNA_ENABLE_REAL_OUTPUT_SUBMIT_V1=0`）以回到“无真实 submit”的旧路径
- 如需紧急回退编排层（非必须）：`LUNA_DISABLE_CROSS_DOMAIN_ORCHESTRATOR_V1=1`

### 5.3 哪些观测信号必须在线监控（试点设计前置）

即使本轮不做 Level 2 实现，评审仍要求在“受限试点设计”前写死在线监控的最小信号：

- **链路闭合性**：同一 `request_id` 是否能在 trace 中闭合到 terminal（request_terminal_observed + playback_result）  
- **submit 侧异常**：submit 调用失败/拒绝的比例（`request_submit_failed/request_submit_rejected`）  
- **playback 侧异常**：`playback_failed/playback_cancelled` 占比与原因聚合  
- **回退触发**：当观测链断裂或错误率超过阈值时是否自动/人工触发回退（阈值由试点设计明确）

---

## 6. 评审结论（单选）

在当前事实与准入门槛对账结果下，本评审给出单选结论：

- [ ] 仍不具备 Level 2 候选资格
- [x] **具备进入“受限 Level 2 试点设计”资格**
- [ ] 已具备进入 Level 2 最小实现准备资格

### 6.1 结论理由（简述）

之所以可以进入“受限试点设计”，而不是直接进入 Level 2 实现，原因是：

- **已满足**：submit 实链 + request 真源 + playback 事件（V1）构成可对账的三段锚点，具备“评审与试点设计”的证据面  
- **仍未满足**：中断/恢复边界、误抢占可观测、真实设备/队列播放意义上的 speaking 真源、以及 Level 2 专属回退演练

因此最合理推进形态是：**进入极小范围、极严格边界的试点设计阶段**，把“抢占的可执行边界、可观测性、可回退性”写死后，再决定是否落最小实现。

---

## 一句话收束

先对照准入门槛把“已满足/未满足/部分满足”对清楚；当前结论为**可进入受限试点设计**，但仍**不得**直接进入全主线真实抢占实现。

