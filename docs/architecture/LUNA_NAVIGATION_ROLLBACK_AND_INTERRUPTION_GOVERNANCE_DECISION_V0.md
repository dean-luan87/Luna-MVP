# Luna — Navigation Rollback And Interruption Governance Decision v0（最小回退/中断治理决策层：设计冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_ROLLBACK_AND_INTERRUPTION_GOVERNANCE_DECISION_V0.md`  
**性质**：Phase-Next-28：治理入口之后的最小治理决策层（冻结“允许的决策结果集合/语义/禁止项”，不执行治理动作）  

关联：
- 治理入口边界冻结：`docs/architecture/LUNA_NAVIGATION_ROLLBACK_AND_INTERRUPTION_GOVERNANCE_ENTRY_V0.md`
- 治理入口最小非动作实现版：`docs/architecture/LUNA_NAVIGATION_ROLLBACK_AND_INTERRUPTION_GOVERNANCE_ENTRY_IMPLEMENTATION_V0.md`
- 治理动作边界层（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_BOUNDARY_V0.md`
- 执行期最小监控闭环（冻结）：`docs/architecture/LUNA_EXECUTION_MONITORING_MINIMAL_LOOP_V0.md`
- 执行期最小监控闭环实现版：`docs/architecture/LUNA_EXECUTION_MONITORING_MINIMAL_LOOP_IMPLEMENTATION_V0.md`
- 执行器状态对象边界冻结：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_STATUS_OBJECT_V0.md`
- 执行器状态对象实现版：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_STATUS_OBJECT_IMPLEMENTATION_V0.md`

---

## A. 文档定位（写死）

- 这是“最小回退 / 中断治理决策层”的设计文档。
- 当前目标：冻结治理入口之后的**最小决策结果边界**（可冻结、可回归）。
- 当前不做真实回退动作。
- 当前不做真实中断治理动作。
- 当前不做地图接入。
- 当前不做语音/记忆联动。
- 当前不改变现有主线行为（不改 route/proposal，不触发中台真实迁移）。

---

## B. 为什么现在必须先定义治理决策层

- 当前已存在 implemented governance entry object（入口可被打开，并有统一对象承载）。
- 但入口打开后，“下一步如何分类判断”还没有统一结果层。
- 若没有治理决策层，后续很容易变成不同模块各自解释 `governance_entry_open`，导致：
  - 结果集合发散、不可回归
  - 语义漂移、越权执行风险
- 因此必须先冻结“最小治理决策结果集合”。

---

## C. 治理决策层的最小定义（写死）

治理决策层是：

- 在治理入口已打开的前提下，对异常/中断/回退候选进行**最小分类判断**的层。

它不是：

- 真实回退执行器
- 真实中断治理器
- formal decision
- readiness gate
- takeover authorization
- 路线改写器
- 语音输出器

核心一句（写死）：

**治理决策层负责给出“该类问题更像什么类型的治理候选”，但不直接执行治理动作。**

---

## D. 当前最小合法输入（写死）

治理决策层只允许消费：

1) implemented `navigation_rollback_and_interruption_governance_entry_v0`
   - 且 `governance_entry_status == "governance_entry_open"`
2) implemented `navigation_real_executor_status_v0`（事实状态参考）
3) implemented `navigation_execution_monitoring_status_v0`（监控事实参考）

可选只读：

- `navigation_executor_takeover_wiring_v0`（仅作接线状态一致性校验，不得扩权）

并写死：

- 不得直接读取 `candidate / gate / stub / raw metadata`
- 没有合法治理入口对象时，不得自行产出治理决策

---

## E. 最小治理决策结果集合（写死）

最小允许形成的治理决策结果（不发散）：

- `hold_for_governance`
- `recommend_interrupt`
- `recommend_rollback`
- `recommend_release_control`
- `governance_decision_blocked`

并写死“意味着什么 / 不意味着什么”：

1) `hold_for_governance`
- 表示：问题已被识别，但更适合挂起等待上游治理链进一步处理
- 不表示：已中断/已回退/已释放控制权

2) `recommend_interrupt`
- 表示：当前问题更接近“应考虑中断执行”的治理候选
- 不表示：中断已执行

3) `recommend_rollback`
- 表示：当前问题更接近“应考虑回退”的治理候选
- 不表示：回退已执行

4) `recommend_release_control`
- 表示：当前问题更接近“应考虑释放执行器控制权回上游”的治理候选
- 不表示：控制权已释放

5) `governance_decision_blocked`
- 表示：虽然入口打开或存在异常，但对象不完整或决策前提不足，不允许形成更强结论
- 不表示：已经采取任何治理动作

---

## F. 当前最小判断原则（克制写死）

> 说明：这是“分类倾向”，不是执行指令；不做复杂优先级推理树。

规则 1：明确失败 / 明确不可执行  
→ 倾向 `recommend_rollback`

规则 2：明确中断 / 明确 takeover 异常释放  
→ 倾向 `recommend_release_control` 或 `recommend_interrupt`

规则 3：明确退化 / 偏航 / 需上游介入，但不足以判定回退  
→ 倾向 `hold_for_governance` 或 `recommend_interrupt`

规则 4：对象不完整 / 一致性不足  
→ `governance_decision_blocked`

写死约束：

- 当前不扩复杂原因树
- 先保证最小分类结果稳定、可回归

---

## G. 治理决策层与现有链路的关系（写清）

### 与 governance entry

- governance entry 负责打开治理入口
- governance decision 负责对入口内问题做最小分类

### 与 monitoring loop

- monitoring loop 提供异常/状态事实
- governance decision 不替代监控层

### 与 executor 本体

- executor 本体不做治理决策
- executor 只上报状态/异常

### 与未来真实治理器

- 当前决策层只是未来真实治理器之前的最小决策层
- 不直接执行回退/中断/释放控制权

---

## H. 当前仍然不能做什么（必须写死）

- 不允许真实回退动作
- 不允许真实中断动作
- 不允许真实释放控制权动作
- 不允许直接改路线
- 不允许直接触发语音播报
- 不允许直接触发中台真实迁移
- 不允许把 `recommend_*` 当治理已执行

---

## I. 当前阶段结论（写死一句）

**当前阶段只适合冻结最小治理决策结果集合；即使未来落最小实现，也只能先输出“建议性治理决策”，不能直接执行治理动作。**

---

## J. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - rollback / interruption governance decision 的最小实现
- 再之后才考虑：
  - 真实回退 / 中断治理最小实现
- 当前不跨这两步

---

## K. 未来治理决策结果样例（仅说明，不落代码）

```json
{
  "governance_decision_attempted": true,
  "governance_decision_scope": "navigation_rollback_and_interruption_governance_decision_v0",
  "governance_decision_status": "hold_for_governance|recommend_interrupt|recommend_rollback|recommend_release_control|governance_decision_blocked",
  "reason": "..."
}
```

