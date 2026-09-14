# Luna — Navigation Governance Action Boundary Minimal Implementation v0（最小治理动作边界层：最小非动作实现）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_BOUNDARY_IMPLEMENTATION_V0.md`  
**性质**：Phase-Next-31：将“治理动作边界层（冻结）”推进为“统一对象的最小非动作实现”，仅产出对象，不执行治理动作  

关联（冻结/实现依据）：
- 动作边界层冻结：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_BOUNDARY_V0.md`
- 治理决策层冻结：`docs/architecture/LUNA_NAVIGATION_ROLLBACK_AND_INTERRUPTION_GOVERNANCE_DECISION_V0.md`
- 治理决策层最小非动作实现：`docs/architecture/LUNA_NAVIGATION_ROLLBACK_AND_INTERRUPTION_GOVERNANCE_DECISION_IMPLEMENTATION_V0.md`
- 治理入口冻结：`docs/architecture/LUNA_NAVIGATION_ROLLBACK_AND_INTERRUPTION_GOVERNANCE_ENTRY_V0.md`
- 治理入口最小非动作实现：`docs/architecture/LUNA_NAVIGATION_ROLLBACK_AND_INTERRUPTION_GOVERNANCE_ENTRY_IMPLEMENTATION_V0.md`

---

## A. 文档定位（写死）

- 这是“最小治理动作边界层”的**正式实现版**文档。
- 当前目标：把动作边界层从冻结文档推进到**最小非动作实现**（可冻结、可回归、可观测）。
- 当前不做真实回退动作。
- 当前不做真实中断动作。
- 当前不做真实释放控制权动作。
- 当前不做地图接入。
- 当前不做语音/记忆联动。
- 当前不改变现有主线行为（不改 route/proposal，不触发中台真实迁移）。

---

## B. 为什么现在要先实现动作边界层

- governance decision 已有 implemented object（主线可产出统一 `recommend_*` / `hold_for_governance` 等结果）。
- action boundary 的结果集合与映射规则已冻结（见冻结文档）。
- 如果没有最小实现，后续即使开始讨论真实治理动作层，也会回到“临时判断 / 散字段映射”，难以回归、容易越权。
- 因此必须先把动作边界对象实现出来，作为决策层与未来真实动作层之间的**硬边界**。
- 但当前仍不能触发任何真实治理动作：本实现只负责“映射并写出对象”，不做执行、不做接线、不做迁移。

---

## C. implemented action boundary 的最小定义（写死）

它不是：

- 真实回退执行器
- 真实中断执行器
- 真实释放控制权执行器

它是：

- “建议性治理决策”到“理论动作边界”的正式实现版对象。

作用（写死）：

- 把决策层结果统一收束为可被后续治理链消费的动作边界对象；
- 但不执行任何回退/中断/释放控制权动作。

---

## D. 当前最小输入依据（写死）

只允许消费标准化对象：

1) implemented `navigation_rollback_and_interruption_governance_decision_v0`（主输入）

可选只读一致性校验（不得扩权）：

2) implemented `navigation_rollback_and_interruption_governance_entry_v0`  
3) implemented `navigation_real_executor_status_v0`  
4) implemented `navigation_execution_monitoring_status_v0`  

并写死：

- governance decision 是主输入
- 其他对象最多只做一致性校验，不得扩权
- 没有合法治理决策对象时，不得产出动作边界结果

---

## E. 当前最小输出位（写死）

建议固定写入：

- `result.metadata["navigation_governance_action_boundary_v0"]`

最小结构（写死，不扩字段、不加时空锚点）：

```json
{
  "governance_action_boundary_attempted": true,
  "governance_action_boundary_scope": "navigation_governance_action_boundary_v0",
  "governance_action_boundary_status": "hold_executor_state|request_interrupt|request_release_control|request_rollback|action_blocked",
  "reason": "..."
}
```

约束（写死）：

- 不加时间/空间字段
- 不膨胀成复杂对象
- 只表达“最小动作边界结果”

---

## F. 当前最小判断规则（克制写死）

规则 1：`recommend_rollback` → `request_rollback`  
规则 2：`recommend_release_control` → `request_release_control`  
规则 3：`recommend_interrupt` → `request_interrupt`  
规则 4：`hold_for_governance` → `hold_executor_state`  
规则 5：`governance_decision_blocked` → `action_blocked`  

并明确（写死）：

- 当前只是决策到动作边界的映射
- 不是动作执行
- 不做复杂优先级树

---

## G. 当前最小语义（写死）

当 `navigation_governance_action_boundary_v0` 被产出时，只表示：

- 系统已能把治理决策统一映射为动作边界结果
- 上游/后续治理链未来可合法消费该对象

它不表示：

- 真实回退已执行
- 真实中断已执行
- 真实释放控制权已执行
- 路线已改变
- 中台已真实迁移

---

## H. 当前不允许做什么（必须写死）

- 不允许真实回退动作
- 不允许真实中断动作
- 不允许真实释放控制权动作
- 不允许直接改路线
- 不允许直接触发语音播报
- 不允许直接触发中台真实迁移
- 不允许把任何 `request_*` 当动作已执行

