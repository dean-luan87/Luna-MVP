# Luna — Navigation Governance Action Executor Minimal Definition v0（治理动作执行器本体最小定义：设计冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_MINIMAL_DEFINITION_V0.md`  
**性质**：Phase-Next-32：治理动作执行器本体最小定义（冻结“执行器是什么/不是什么/最小能力面/最小运行状态/关系与禁止项”，不落真实动作实现）  

关联（上游链路已具备）：
- 治理入口冻结：`docs/architecture/LUNA_NAVIGATION_ROLLBACK_AND_INTERRUPTION_GOVERNANCE_ENTRY_V0.md`
- 治理入口最小非动作实现：`docs/architecture/LUNA_NAVIGATION_ROLLBACK_AND_INTERRUPTION_GOVERNANCE_ENTRY_IMPLEMENTATION_V0.md`
- 治理决策冻结：`docs/architecture/LUNA_NAVIGATION_ROLLBACK_AND_INTERRUPTION_GOVERNANCE_DECISION_V0.md`
- 治理决策最小非动作实现：`docs/architecture/LUNA_NAVIGATION_ROLLBACK_AND_INTERRUPTION_GOVERNANCE_DECISION_IMPLEMENTATION_V0.md`
- 治理动作边界冻结：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_BOUNDARY_V0.md`
- 治理动作边界最小非动作实现：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_BOUNDARY_IMPLEMENTATION_V0.md`
- 治理动作执行器模块骨架（不可执行）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_MINIMAL_MODULE_SKELETON_V0.md`
- 治理动作状态对象（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_STATUS_OBJECT_V0.md`
- 已批准治理动作边界层（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_APPROVAL_BOUNDARY_V0.md`
- 治理动作执行器标准化输入对象（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_INPUT_OBJECT_V0.md`
- 治理动作执行器输入对象只读占位：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_INPUT_OBJECT_PLACEHOLDER_V0.md`
- 治理动作执行器就绪门控（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_READINESS_GATE_V0.md`
- 治理动作执行器就绪门控最小非动作实现：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_READINESS_GATE_IMPLEMENTATION_V0.md`
- 治理动作执行器接线边界（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_WIRING_V0.md`
- 治理动作执行器接线最小非动作实现：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_WIRING_IMPLEMENTATION_V0.md`
- 治理动作：Release Control 最小定义冻结：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_DEFINITION_V0.md`

---

## A. 文档定位（写死）

- 这是“**治理动作执行器本体最小定义**”的设计文档。
- 当前目标：冻结治理动作执行器边界（可冻结、可回归）。
- 当前不做真实回退动作。
- 当前不做真实中断动作。
- 当前不做真实释放控制权动作。
- 当前不做地图接入。
- 当前不做语音/记忆联动。
- 当前不改变现有主线行为（不改 route/proposal，不触发中台真实迁移）。

---

## B. 为什么现在必须先定义治理动作执行器本体

- 当前治理链已经具备：entry → decision → action boundary（且已有最小非动作实现可产出统一对象）。
- 但仍缺少一个明确的“**谁来真正执行治理动作**”的本体定义。
- 若不先冻结本体边界，后续极易出现越权与语义漂移：
  - action boundary 被直接当执行器（把 `request_*` 误当“已执行”）
  - 中台/外部链路越权直接执行治理动作（绕过边界与审计）
  - navigation executor 本体越权承担治理职责（执行与治理耦合、不可回归）
- 因此必须先冻结：治理动作执行器是什么、不是什么、以及它的最小能力与禁止项。

---

## C. 治理动作执行器本体的最小定义（写死）

治理动作执行器本体是：

- 在 governance action boundary 已明确（且经上游批准）的前提下，负责把“被批准的治理动作边界”转换为**真实治理动作执行**的能力单元。

它处理的是：

- **治理动作执行**（interrupt / release control / rollback request 的真实执行）

它不处理的是：

- 治理入口识别（entry）
- 治理决策分类（decision）
- 动作边界判断（action boundary）
- formal decision
- readiness
- takeover authorization

核心一句（写死）：

**治理动作执行器只负责执行已被上游批准的治理动作；是否允许执行、何时执行、执行哪类动作，均由上游治理链决定。**

---

## D. 治理动作执行器明确不是什么（必须写死）

治理动作执行器不是：

1) governance entry  
- **为什么不是**：entry 只负责打开治理入口，提供“有资格进入治理”的判定与统一对象；它不具备执行面。

2) governance decision  
- **为什么不是**：decision 只负责建议性分类（recommend/hold/blocked），不具备执行面，也不得把建议当执行。

3) governance action boundary  
- **为什么不是**：action boundary 只负责把建议性决策约束为“理论允许进入的动作类别边界”（`request_*`），明确不执行动作。

4) formal decision  
- **为什么不是**：formal decision 是主线放行/阻断的裁决层，不是治理动作执行单元。

5) readiness gate  
- **为什么不是**：readiness gate 负责真实执行前最后门控，不负责治理动作执行。

6) takeover authorization  
- **为什么不是**：takeover authorization/接管层负责控制权合法入口与接线语义，不等同治理动作执行。

7) 路线决策器  
- **为什么不是**：治理动作执行器不负责改 route/proposal；路线改写属于上游规划/决策域，必须与治理执行解耦。

8) 语音输出器  
- **为什么不是**：语音输出是输出平面能力；治理动作执行器不应直接触发播报，避免“执行/输出耦合”与越权外显。

9) 记忆模块  
- **为什么不是**：记忆写入/检索属于长期状态系统；治理动作执行器不应隐式写记忆以免产生不可回归副作用。

10) 中台调度器  
- **为什么不是**：中台负责批准/编排/审计/迁移（未来可能），治理动作执行器只是被调用的执行单元；中台不得用“调度器身份”绕过边界直接执行。

---

## E. 治理动作执行器最小能力面（只定义，不实现）

> 本节只定义“能力面”，不代表当前可以执行。

1) 消费被批准的动作边界结果  
- 只消费后续被正式批准的 action boundary 结果（例如 `request_*` 被批准为可执行）。
- 当前不允许直接消费 recommendation（decision）或 entry 对象。

2) 执行最小治理动作类型（能力面定义）  
- interrupt 执行动作（执行“中断”）
- release control 执行动作（执行“释放控制权”）
- rollback request 执行动作（执行“回退请求”）

3) 输出治理动作执行状态（未来必须有标准化回传面）  
- 未来必须存在统一的 action execution status 对象/接口。
- 当前不实现。

4) 异常上报（未来必须具备）  
- 执行失败 / 被阻断 / 无法完成时必须回传可审计结果。
- 当前不实现。

---

## F. 治理动作执行器最小运行状态（语义框架，写死）

> 当前只是语义框架；不做代码实现；不表示系统已经进入这些状态。

建议最小运行状态集合（不发散）：

- `idle`
- `action_ready`
- `action_blocked`
- `action_executing`
- `action_failed`
- `action_completed`
- `released`

语义约束（写死）：

- `action_ready` 不等于“已执行”，只表示“具备执行前置条件（且已被批准）”。
- `action_completed` 只描述治理动作执行完成，不隐含路线改变、语音播报或中台迁移已发生。

---

## G. 治理动作执行器与各层关系（写清）

### 与 governance entry

- entry 只负责打开治理入口，不执行动作。

### 与 governance decision

- decision 只负责分类判断，不执行动作。

### 与 governance action boundary

- action boundary 只负责限制“理论允许进入的动作类别”，不执行动作。
- 治理动作执行器必须位于其后，且只能执行**已被批准**的动作边界结果。

### 与 executor 本体（navigation real executor）

- executor 本体负责导航执行（走/停/状态上报），不负责治理动作执行。
- 治理动作执行器负责治理动作（中断/释放/回退），不负责导航执行。
- 两者不能混为一个模块（避免耦合、越权与不可回归）。

### 与中台/治理链

- 中台/治理链负责批准动作边界（未来）与编排/审计（未来）。
- 治理动作执行器在“批准发生后”才可能被调用执行。
- 当前不实现批准流程与真实动作执行。

---

## H. 当前仍然不能做什么（必须写死）

- 不允许真实回退动作
- 不允许真实中断动作
- 不允许真实释放控制权动作
- 不允许直接改路线
- 不允许直接触发语音播报
- 不允许直接触发中台真实迁移
- 不允许把“执行器定义”当“执行器已实现”

---

## I. 当前阶段结论（写死一句）

**当前阶段只适合冻结治理动作执行器本体定义；即使后续进入最小实现，也必须在 action boundary 之后、真实批准链之前小心推进；当前仍然不进入真实治理动作实现。**

---

## J. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - governance action executor 的最小模块骨架
- 再之后才考虑：
  - 真实治理动作的最小实现
- 当前不跨这两步

---

## K. 未来治理动作执行器能力样例（仅说明，不落代码）

```json
{
  "governance_action_executor_identity": "navigation_governance_action_executor_v0",
  "can_consume_approved_action_boundary": true,
  "can_execute_interrupt_action": true,
  "can_execute_release_control_action": true,
  "can_execute_rollback_request_action": true,
  "can_self_authorize_action": false
}
```

