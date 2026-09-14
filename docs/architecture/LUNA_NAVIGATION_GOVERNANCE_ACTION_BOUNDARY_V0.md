# Luna — Navigation Governance Action Boundary v0（最小治理动作边界层：设计冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_BOUNDARY_V0.md`  
**性质**：Phase-Next-30：治理决策之后的最小治理动作边界层（冻结“理论允许的动作类别边界/语义/禁止项”，不执行动作）  

关联：
- 治理入口边界冻结：`docs/architecture/LUNA_NAVIGATION_ROLLBACK_AND_INTERRUPTION_GOVERNANCE_ENTRY_V0.md`
- 治理入口最小非动作实现版：`docs/architecture/LUNA_NAVIGATION_ROLLBACK_AND_INTERRUPTION_GOVERNANCE_ENTRY_IMPLEMENTATION_V0.md`
- 治理决策层边界冻结：`docs/architecture/LUNA_NAVIGATION_ROLLBACK_AND_INTERRUPTION_GOVERNANCE_DECISION_V0.md`
- 治理决策最小非动作实现版：`docs/architecture/LUNA_NAVIGATION_ROLLBACK_AND_INTERRUPTION_GOVERNANCE_DECISION_IMPLEMENTATION_V0.md`
- 治理动作执行器本体最小定义（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_MINIMAL_DEFINITION_V0.md`
- 治理动作状态对象（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_STATUS_OBJECT_V0.md`
- 已批准治理动作边界层（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_APPROVAL_BOUNDARY_V0.md`
- 治理动作：Release Control 最小定义冻结：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_DEFINITION_V0.md`
- 执行期监控闭环实现版：`docs/architecture/LUNA_EXECUTION_MONITORING_MINIMAL_LOOP_IMPLEMENTATION_V0.md`
- 接入就绪评审（v0）：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_INTEGRATION_READINESS_REVIEW_V0.md`

---

## A. 文档定位（写死）

- 这是“**最小治理动作边界层**”的设计文档。
- 当前目标：冻结治理决策层之后的动作边界（动作类别的最小允许集合与严格禁止项）。
- 当前不做真实回退动作。
- 当前不做真实中断动作。
- 当前不做真实释放控制权动作。
- 当前不做地图接入。
- 当前不做语音/记忆联动。
- 当前不改变现有主线行为（不改 route/proposal，不触发中台真实迁移）。

---

## B. 为什么现在必须先定义动作边界层

- 当前 governance entry 已有 implemented object。
- 当前 governance decision 已有 implemented object。
- 但在 `recommend_*` 之后，系统“理论上允许进入什么动作层”还没有统一边界。
- 若不先定义动作边界，后续很容易把“建议性结果”误当“执行动作”，造成越权与不可回归。
- 因此必须先冻结动作边界，再谈真实动作实现。

---

## C. 动作边界层的最小定义（写死）

动作边界层是：

- 在治理决策已形成的前提下，对“未来可能采取的治理动作类型”进行最小边界约束的层。

它不是：

- 真实回退执行器
- 真实中断执行器
- 真实释放控制权执行器
- formal decision
- readiness gate
- takeover authorization
- 路线改写器
- 语音输出器

核心一句（写死）：

**动作边界层负责限定“系统理论上可进入什么治理动作类别”，但不直接执行动作。**

---

## D. 当前最小合法输入（写死）

动作边界层只允许消费：

1) implemented `navigation_rollback_and_interruption_governance_decision_v0`（主输入）

可选只读（仅一致性校验，不得扩权）：

2) implemented `navigation_rollback_and_interruption_governance_entry_v0`  
3) implemented `navigation_real_executor_status_v0`  
4) implemented `navigation_execution_monitoring_status_v0`  

并写死：

- governance decision 是主输入
- 其他对象最多用于一致性校验，不得扩权
- 没有合法治理决策对象时，不得形成动作边界结果

---

## E. 最小治理动作边界结果集合（写死）

最小允许形成的动作边界结果（不发散）：

- `hold_executor_state`
- `request_interrupt`
- `request_release_control`
- `request_rollback`
- `action_blocked`

并写死“意味着什么 / 不意味着什么”：

1) `hold_executor_state`
- 表示：当前允许的最小动作边界是“维持当前执行器状态，等待上游进一步治理”
- 不表示：执行器状态已改变

2) `request_interrupt`
- 表示：当前允许进入“请求中断”的动作边界
- 不表示：中断已执行

3) `request_release_control`
- 表示：当前允许进入“请求释放控制权”的动作边界
- 不表示：控制权已释放

4) `request_rollback`
- 表示：当前允许进入“请求回退”的动作边界
- 不表示：回退已执行

5) `action_blocked`
- 表示：当前虽有治理决策，但动作边界条件不足或禁止更强动作
- 不允许进入后续动作层

---

## F. 当前最小判断原则（克制写死）

规则 1：`recommend_rollback` → `request_rollback`  
规则 2：`recommend_release_control` → `request_release_control`  
规则 3：`recommend_interrupt` → `request_interrupt`  
规则 4：`hold_for_governance` → `hold_executor_state`  
规则 5：`governance_decision_blocked` → `action_blocked`  

并明确（写死）：

- 当前只是“决策到动作边界”的映射
- 不是动作执行
- 不做复杂优先级树

---

## G. 动作边界层与现有链路的关系（写清）

### 与 governance decision

- governance decision 负责建议性分类
- action boundary 负责把建议性分类约束为“理论允许的动作边界”

### 与未来真实治理动作实现

- action boundary 只是未来真实治理动作之前的一层
- 不直接执行回退 / 中断 / 释放控制权

### 与 executor 本体

- action boundary 不直接控制 executor
- 未来真实动作层才可能作用于 executor

### 与中台/治理链

- action boundary 结果未来可供中台/治理链消费
- 当前不触发真实迁移

---

## H. 当前仍然不能做什么（必须写死）

- 不允许真实回退动作
- 不允许真实中断动作
- 不允许真实释放控制权动作
- 不允许直接改路线
- 不允许直接触发语音播报
- 不允许直接触发中台真实迁移
- 不允许把任何 `request_*` 当动作已执行

---

## I. 当前阶段结论（写死一句）

**当前阶段只适合冻结最小治理动作边界；即使未来落最小实现，也只能先输出“请求型动作边界结果”，不能直接执行治理动作。**

---

## J. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - governance action boundary 的最小实现
- 再之后才考虑：
  - 真实回退 / 中断 / 释放控制权动作的最小实现
- 当前不跨这两步

---

## K. 未来动作边界结果样例（仅说明，不落代码）

```json
{
  "governance_action_boundary_attempted": true,
  "governance_action_boundary_scope": "navigation_governance_action_boundary_v0",
  "governance_action_boundary_status": "hold_executor_state|request_interrupt|request_release_control|request_rollback|action_blocked",
  "reason": "..."
}
```

