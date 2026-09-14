# risk_interrupt_v1 cancel+replace 候选评审（V1）

## 1. 评审目标

### 1.1 为什么现在需要对 cancel+replace 做正式候选评审

当前系统同时具备：

- `preempt-before-submit` 的 Level 2 受限试点（已实现、默认关闭、可回退）
- 底层 **cancel 真能力**（按 `request_id` 取消待执行/正在执行，并产出 `playback_cancelled` 真事件）
- cancel+replace 的试点边界方案（已写死极窄范围）

但如果没有“是否允许进入实现”的正式结论，会出现从方案直接跳实现的风险。因此本评审的目标是：**明确能不能进入实现、允许进入实现的边界到底是哪一小块**。

### 1.2 这份评审解决什么问题

- 对照试点方案逐项核对：前置是否已满足、哪些仍缺口、哪些仅部分满足
- 把 cancel 边界（待执行 vs 已 started）写成“允许/禁止”的明确结论
- 把 replace 链路闭合性与回退条件写死
- 给出单选结论，避免边界漂移

---

## 2. 对照评审方案逐项核对（必须对账）

对照文档：`LUNA_RISK_INTERRUPT_V1_CANCEL_REPLACE_PILOT_PLAN.md`。

### 2.1 前置能力与证据面

| 前置项 | 结论 | 证据面（当前仓库事实） | 备注/缺口 |
|--------|------|------------------------|-----------|
| **cancel 真能力**（按 request_id） | **已满足（V1）** | `PlaybackPlaneV1.cancel(request_id)` + `playback_cancelled` 真事件；默认关闭 | V1 仅单线程/单队列语义；足够支撑“取消待执行 request”试点 |
| **request/playback 可对账** | **已满足（V1）** | request_runtime + playback_runtime 事件以同一 request_id 聚合 | 仍需在试点实现阶段补充更细的 cancel 观测指标（次数/成功率/混淆） |
| **观测链可抽链** | **部分满足** | `request_trace_extractor` 可消费 output_decision/request_runtime/playback_runtime | cancel+replace 专属指标需补（cancel→replace 闭合率、误取消样本） |
| **秒退到当前方案** | **部分满足** | 现有 preempt-before-submit 试点可独立开关；cancel 能力也默认关闭 | cancel+replace 必须新增独立开关矩阵；未实现前仅能原则保证 |

### 2.2 范围约束（高风险语义必须锁死）

| 约束项 | 结论 | 说明 |
|-------|------|------|
| 仅 high/critical | **必须** | 与现有风险门槛一致，缺失 risk_summary 不触发 |
| 仅 prompt/confirmation | **必须** | 任务链/长文本一律禁止 |
| 不做恢复/重播 | **必须** | cancel+replace 试点只验证“停止 + 替换提交”，不引入恢复语义 |
| 不扩旁路范围 | **必须** | 仅 risk_interrupt_v1；sidewalk/retail 禁止进入 |

---

## 3. cancel 边界评审（写死）

### 3.1 取消待执行 request 是否已具备实现资格

**结论：具备进入受限实现资格。**

理由（当前事实 + 风险控制）：

- 底层 cancel 已支持“取消队列中待执行 request”（单队列语义）并能产出 `playback_cancelled`
- 尚未开始播放时取消，用户体验冲击更可控
- 依赖链路闭合（request/playback/cancel）已可按 request_id 对账

### 3.2 取消已 started playback 是否仍不具备资格

**结论：仍不具备资格（写死禁止）。**

理由：

- 已 started 的取消等价于“真实中断”，会引入中断成功判定、与设备播放一致性、以及更强的恢复/重播争议
- 当前 V1 执行层仍为极简骨架，未接真实设备播放与更复杂队列治理
- 在缺少更严格观测与回退演练前，不应默认放开

---

## 4. replace 边界评审（写死）

### 4.1 cancel 后 risk 输出重新进入 submit 的最小链路是否足够

**结论：部分满足（可进入“受限实现评审/实现阶段”，但必须补齐最小闭合与观测）。**

已具备：

- submit/request/playback 事实链可用（主线可提交、可观测）
- risk 输出的最小文案与提交路径在 preempt-before-submit 中已有经验（提示类短文本）

仍缺（进入实现阶段必须补齐的硬点）：

- cancel 成功判定的“最小闭合条件”（例如必须观测到 `playback_cancelled` 才允许 replace submit）
- cancel→replace 的链路闭合率统计与误取消样本采集
- replace 使用的新 request_id 与原 request_id 的关联字段/规则（至少要能在观测侧关联）

### 4.2 哪些情况下必须退回 preempt-before-submit

写死退回条件（任一触发即退回）：

- 越界取消（非 prompt/confirmation）
- 风险不足取消（非 high/critical）
- cancel 终态混淆（cancelled 与 finished/failed 混淆）
- cancel→replace 链路无法闭合或对账失败
- 观测链断裂（request_id 无法闭合到 terminal/关键节点）

---

## 5. 评审结论（单选）

本评审给出单选结论：

- [ ] 仍不具备 cancel+replace 试点实现资格
- [x] **具备进入“只取消待执行 request”的受限实现资格**
- [ ] 已具备进入更宽边界 cancel+replace 实现资格

### 5.1 写死边界（必须随结论一起落）

- **允许进入实现的唯一范围**：只取消“待执行 request”（未出现 playback_started）  
- **明确禁止**：取消已 started playback（本轮不得进入实现）  
- replace 仍必须保持极窄：仅 prompt/confirmation + high/critical + 链路闭合后才允许提交风险提示

---

## 一句话收束

本轮评审结论为：**可进入“只取消待执行 request”的受限 cancel+replace 实现阶段**；已 started playback 的取消仍写死为禁止，必须等更严格前置补齐后再议。

