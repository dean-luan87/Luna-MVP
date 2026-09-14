# Luna — Navigation Rollback And Interruption Governance Entry v0（最小回退/中断治理入口：设计冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_ROLLBACK_AND_INTERRUPTION_GOVERNANCE_ENTRY_V0.md`  
**性质**：Phase-Next-26：最小回退 / 中断治理入口（冻结“哪些事件可进入、消费什么、输出什么、仍不能做什么”）  

关联：
- takeover → executor skeleton 接线边界（冻结）：`docs/architecture/LUNA_NAVIGATION_EXECUTOR_TAKEOVER_WIRING_V0.md`
- takeover → executor 最小接线实现版（非动作）：`docs/architecture/LUNA_NAVIGATION_EXECUTOR_TAKEOVER_WIRING_IMPLEMENTATION_V0.md`
- 治理决策层（冻结）：`docs/architecture/LUNA_NAVIGATION_ROLLBACK_AND_INTERRUPTION_GOVERNANCE_DECISION_V0.md`
- 执行期最小监控闭环（冻结）：`docs/architecture/LUNA_EXECUTION_MONITORING_MINIMAL_LOOP_V0.md`
- 执行期最小监控闭环实现版：`docs/architecture/LUNA_EXECUTION_MONITORING_MINIMAL_LOOP_IMPLEMENTATION_V0.md`
- 执行器状态对象边界冻结：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_STATUS_OBJECT_V0.md`
- 执行器状态对象实现版：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_STATUS_OBJECT_IMPLEMENTATION_V0.md`
- 接入就绪评审（v0）：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_INTEGRATION_READINESS_REVIEW_V0.md`

---

## A. 文档定位（写死）

- 这是“**最小回退 / 中断治理入口**”的设计文档。
- 当前目标：冻结治理入口边界（哪些事件可进入、入口消费对象、输出结果、明确禁止项）。
- 当前不做真实回退动作。
- 当前不做真实中断治理实现。
- 当前不做地图接入。
- 当前不做语音/记忆联动。
- 当前不改变现有主线行为与裁决边界。

---

## B. 为什么现在必须先定义治理入口

- 当前 executor skeleton 已可被最小非动作接线（可进入安全接线态，但不执行）。
- 当前 executor status object 已有实现版（implemented `navigation_real_executor_status_v0`，不伪装运行事实）。
- 当前 monitoring minimal loop 已有实现版（implemented `navigation_execution_monitoring_status_v0`，不触发治理）。
- 但如果没有“回退 / 中断治理入口”，后续即使能观测到异常，也无法**合法收权**或把事件进入治理链（会导致越权、不可回收、不可回归）。
- 因此治理入口是继续推进前的重要安全边界：先写死“什么事件有资格被治理链看见”，但仍禁止直接回退/中断。

---

## C. 哪些事件有资格进入治理入口（写死最小集合）

治理入口只承认来自**标准化状态/监控对象**的治理候选事件，最小集合至少包括：

1) `execution_failed`  
2) `execution_interrupted`  
3) `execution_degraded`  
4) 明确偏航  
5) 明确不可执行  
6) takeover 异常释放  
7) 其他明确要求上游介入的异常状态

写死约束：

- 这些事件必须来自标准化对象（implemented `navigation_real_executor_status_v0` / implemented `navigation_execution_monitoring_status_v0`）。
- 不能来自零散临时字段。
- 不能由 executor 自己直接决定回退（executor 只能上报状态/异常，不能裁决回退）。

---

## D. 治理入口最小合法输入（写死）

治理入口当前只允许消费标准化对象：

1) implemented `navigation_real_executor_status_v0`  
2) implemented `navigation_execution_monitoring_status_v0`  
3) 可选只读：`navigation_executor_takeover_wiring_v0`（仅用于“接线态一致性校验”，不得扩权）

并写死：

- 治理入口不直接读取 `candidate / gate / stub / raw metadata`。
- 治理入口只消费已标准化的执行器侧对象（以及可选的接线一致性对象）。

---

## E. 治理入口的最小职责（写清）

治理入口只负责：

- 识别是否出现“有资格进入治理”的事件（基于标准化对象）
- 把事件收束成统一治理入口结果（稳定、可回归）
- 把控制权保留在上游治理链，不让 executor 自治

治理入口不负责：

- 直接执行回退动作
- 直接改变路线
- 直接播报
- 直接写记忆
- 替代 formal decision / readiness / takeover

---

## F. 治理入口最小输出结果（写死最小集合）

治理入口最小输出状态只允许：

- `governance_entry_open`
- `governance_entry_not_applicable`
- `governance_entry_blocked`

语义（写死）：

1) `governance_entry_open`
- 已检测到符合条件的回退/中断治理候选事件
- 上游治理链应有机会消费该事件
- **不等于已经执行回退**

2) `governance_entry_not_applicable`
- 当前没有进入治理入口的充分事件
- 不触发治理

3) `governance_entry_blocked`
- 虽有异常/问题，但治理入口条件不完整或对象不合法
- 不允许进入治理链，保持保守

---

## G. 治理入口与现有链路的关系（写清）

### 与 executor 本体

- executor 只上报状态/异常（通过标准化状态对象语义）
- executor 不直接触发回退治理

### 与 monitoring loop

- monitoring loop 负责形成可治理信号（标准化监控对象）
- governance entry 负责识别这些信号是否足以打开治理入口

### 与 formal decision / readiness / takeover

- 这些层发生在执行前
- governance entry 发生在执行器/监控链之后
- 不得反向替代前置裁决层

### 与未来回退治理实现

- 本入口只是“回退/中断治理的合法入口”
- 不是完整回退治理器

---

## H. 当前仍然不能做什么（必须写死）

- 不允许真实回退动作
- 不允许真实中断治理动作
- 不允许直接改路线
- 不允许直接触发语音播报
- 不允许直接触发中台真实迁移
- 不允许把 `governance_entry_open` 当回退已发生

---

## I. 当前阶段结论（写死一句）

**当前阶段只适合冻结最小回退 / 中断治理入口；即使未来允许落最小实现，也只能先打开治理入口，不允许直接执行回退动作。**

---

## J. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - rollback / interruption governance entry 的最小实现
- 再之后才考虑：
  - 真实回退 / 中断治理最小实现
- 当前不跨这两步

---

## K. 未来治理入口结果样例（仅说明，不落代码）

```json
{
  "governance_entry_attempted": true,
  "governance_entry_scope": "navigation_rollback_and_interruption_governance_entry_v0",
  "governance_entry_status": "governance_entry_open|governance_entry_not_applicable|governance_entry_blocked",
  "reason": "..."
}
```

