# risk_interrupt_v1 Level 2 试点观察与退出标准（V1）

## 0. 一句话收束（写死）

本文件只定义 **risk_interrupt_v1 Level 2 受限试点** 的观察与退出标准。当前阶段只允许三种结论：

- **继续维持当前极小试点**
- **退回 Level 1**
- **终止试点并回到 Level 0**

禁止出现“感觉还行，顺手放大一点”的结论口径；扩边界必须进入下一阶段的独立评审与设计。

---

## 1. 观察目标

### 1.1 当前试点要证明什么

在不扩边界、不引入中断/恢复/队列的前提下，验证这版试点能稳定满足：

- **触发边界正确**：只在 `high/critical`、且仅对 `prompt/confirmation` 短文本发生 `preempt_before_submit`
- **可观测可对账**：同一 `request_id` 能闭合到 request+playback 两层轨迹（至少可观测到 terminal 与 playback 终态事件之一）
- **默认安全**：开关关闭时零侵入；开启后异常也可秒退
- **输出符合预期**：用户实际听到的最终文本与“安全抢占提示”一致（不出现乱码/空输出/长文本误入）

### 1.2 当前试点不证明什么（写死）

当前试点 **不**证明：

- 真实播放中的中断/恢复正确性（未实现）
- 多风险事件编排能力（未实现）
- 任务链相关抢占正确性（明确禁止）
- 复杂输出裁决与队列治理能力（未实现）
- 旁路（sidewalk/retail）进入真实输出的合理性（明确禁止）

---

## 2. 观察窗口

### 2.1 最小观察周期（建议）

建议采用 **双窗口**：

- **最小观察周期**：连续 **7 天**
- **稳定性观察周期**：连续 **14 天**

理由：当前试点是“极小范围 + 高风险语义（抢占）”的第一版实现，需要覆盖多种环境波动、开关误配、观测链断裂等工程噪声，而不是追求短期快速扩张。

### 2.2 样本规模口径（建议）

以 `request_id` 为主键统计，建议最低满足：

- **总 submit 样本**：≥ 1,000 条（含未触发抢占的正常提交）
- **触发样本（preempt）**：≥ 50 条（不足则只允许继续收集，不允许扩大）

---

## 3. 必看指标（必须在线盯）

> 指标尽量基于现有可观测证据：`output_decision` + request/playback trace（JSONL envelope）。

### 3.1 触发次数与比例

- **指标**：`risk_interrupt_v1_level2_pilot_preempt_before_submit` 次数  
  - 数据源：`output_decision.reason == "risk_interrupt_v1_level2_pilot_preempt_before_submit"`
- **指标**：触发率 = preempt 次数 / 总 submit 次数  
  - 预期：极低且稳定；突增视为风险

### 3.2 被抢占原输出类型分布

- **指标**：`preempted_output_category` 分布（应仅为 prompt/confirmation）  
  - 数据源：`output_decision.metadata.preempted_output_category`
- **硬约束**：出现非 prompt/confirmation 即为越界（见退出标准）

### 3.3 high/critical 来源稳定性

- **指标**：触发时 `risk_level` 分布（应仅 high/critical）  
  - 数据源：`output_decision.metadata.risk_level` + 上游 `risk_summary_v1` 的一致性抽样核对
- **指标**：`risk_summary_v1` 缺失率/unknown 占比（缺失不应触发抢占）

### 3.4 request/playback 链路闭合率

- **指标**：链路闭合率（按 `request_id`）
  - request 侧：`request_created → request_submitted → request_terminal_observed`
  - playback 侧：出现 `playback_*` 终态事件之一（started/finished/failed/cancelled）
- **解释**：闭合率是“可对账性”的底线；闭合率下降意味着试点进入不可观测状态，应优先回退而不是继续扩展。

### 3.5 误抢占样本数（必须有人审）

- **指标**：误抢占样本数（见 §4 定义）
- **指标**：可疑样本数（需要人工复核）

### 3.6 回退触发次数

- **指标**：Level 2 试点开关关闭次数、以及因错误阈值触发回退次数  
  - 目标：回退应可执行、且触发原因可复盘

### 3.7 用户实际听到的最终文本是否符合预期

- **指标**：抢占发生时，最终播报文本是否为“安全抢占提示”（一致性抽样）  
  - 说明：当前为 submit 前替换，理论上应稳定一致；若出现不一致，说明链路存在分叉或文本来源不一致。

---

## 4. 误抢占定义（必须写死）

### 4.1 哪些情况算误抢占（直接判错）

满足任一即判为误抢占：

- **越界抢占**：抢占了非 `prompt/confirmation` 输出
- **风险不足仍抢占**：`risk_level` 非 high/critical 仍触发抢占
- **观测链断裂仍抢占**：无法用 `request_id` 对账到 request_terminal 或 playback 终态（在允许的时间窗内）
- **错误文本**：用户最终听到的不是预期“安全抢占提示”，或出现空/乱码/长文本

### 4.2 哪些情况算可疑但不直接判错

需要人工复核、暂不直接判错：

- 上游 `risk_summary_v1` 在时间上抖动，但触发仍落在 high/critical（需核对时效与来源）
- playback 侧出现 cancelled/failed，但 submit 与 request 侧正常（可能是执行层波动）

### 4.3 哪些情况必须人工复核（写死）

- 每周至少抽样复核固定数量的 preempt 样本（例如 20 条）
- 所有出现 “越界/风险不足/链路断裂/文本不一致” 的样本必须逐条复盘

---

## 5. 退出标准（维持 / 退回 L1 / 回到 L0）

> 阈值可在执行时按真实数据调整，但调整必须走评审，不允许临场拍脑袋放宽。

### 5.1 继续维持当前极小试点（允许条件）

满足全部条件才允许维持：

- 无越界抢占（0 次）
- 风险不足抢占（0 次）
- 链路闭合率稳定在可接受范围（建议 ≥ 99%）
- 误抢占样本数为 0 或极低且可解释（需给出复盘结论）
- 回退链随时可执行且已演练（至少演练一次“秒退到 Level 1/0”）

### 5.2 退回 Level 1（触发条件）

满足任一即退回 Level 1：

- 出现任何越界抢占（非 prompt/confirmation）
- 出现任何风险不足抢占（非 high/critical）
- 链路闭合率持续下降或低于阈值（建议 < 99% 持续 1 天）
- 出现可复现的“文本不一致/空输出”类问题

**退回动作（写死）**：

- 关闭 `LUNA_ENABLE_RISK_INTERRUPT_V1_LEVEL2_PILOT=0`（保持 risk_interrupt_v1 Level 1 whitebox-only）

### 5.3 终止试点并回到 Level 0（触发条件）

满足任一即回到 Level 0：

- 出现不可控循环抢占/安全事件/数据损坏风险
- 退回 Level 1 后问题仍持续（说明试点实现或观测链存在系统性风险）
- 观测链大面积断裂，无法定位原因且影响面扩大

**回到 Level 0 动作（写死）**：

- `LUNA_ENABLE_RISK_INTERRUPT_V1=0`
- `LUNA_ENABLE_REAL_OUTPUT_SUBMIT_V1=0`
- （必要时）`LUNA_DISABLE_CROSS_DOMAIN_ORCHESTRATOR_V1=1` 作为紧急手段

---

## 6. 什么时候才允许讨论扩大边界

扩大边界（例如扩大输出类型、进入任务链相关输出、引入中断/恢复、或引入多风险编排）必须满足：

- 至少完成 **14 天稳定性观察窗口**  
- 误抢占为 0 或极低且可解释，并形成书面复盘结论  
- 链路闭合率长期稳定（建议 ≥ 99%）  
- 回退演练通过（含 Level 1 与 Level 0）  
- 并且必须进入下一阶段的独立评审与设计文档（不得在试点观察期“顺手放大”）

---

## 当前阶段不做项（再次写死）

- 不扩大到其他输出类型
- 不扩大到其他旁路
- 不引入中断恢复
- 不扩大到复杂场景

