# Luna — Navigation Governance Action Release Control Execution State v0（子动作执行过程状态面：设计冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_EXECUTION_STATE_V0.md`  
**性质**：Phase-Next-64：冻结 `release_control` 子动作未来进入最小真实实现时的“执行过程标准化 execution state 对象”（不落代码、不触发真实动作）

关联（已具备）：
- release_control 最小定义冻结：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_DEFINITION_V0.md`
- release_control skeleton：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_SKELETON_V0.md`
- release_control 输入契约（冻结/实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_INPUT_CONTRACT_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_INPUT_CONTRACT_IMPLEMENTATION_V0.md`
- release_control 状态对象（冻结/实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_STATUS_OBJECT_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_STATUS_OBJECT_IMPLEMENTATION_V0.md`
- release_control readiness/wiring（冻结/实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_READINESS_GATE_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_READINESS_GATE_IMPLEMENTATION_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_WIRING_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_WIRING_IMPLEMENTATION_V0.md`
- release_control result object（冻结/实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_RESULT_OBJECT_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_RESULT_OBJECT_IMPLEMENTATION_V0.md`
- release_control execution state placeholder（占位输出）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_EXECUTION_STATE_PLACEHOLDER_V0.md`
- release_control execution state implementation（正式实现版）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_EXECUTION_STATE_IMPLEMENTATION_V0.md`

---

## A. 文档定位（写死）

- 这是 `release_control` 子动作标准化**执行过程状态面**（execution state）的最小设计文档。
- 当前目标：冻结 `release_control` 执行过程状态对象边界（可冻结、可回归）。
- 当前不做真实 `release_control`。
- 当前不做 `rollback` / `interrupt`。
- 当前不做地图接入。
- 当前不做语音/记忆联动。
- 当前不改变现有主线行为（不改 route/proposal，不触发中台真实迁移）。

---

## B. 为什么现在要先定义 execution state

- 当前已有：`release_control` input contract / status object / readiness gate / wiring / result object。
- 但还没有“`release_control` 一旦真的进入动作执行过程时，过程状态如何被统一组织并回传”的正式对象边界。
- 如果不先定义 execution state，后续真实动作很容易把“过程状态（in-progress）”与“最终结果（final result）”混写在一起（例如直接把执行中状态塞进 result object）。
- 因此必须先冻结 `release_control execution state`，把**过程面**与**结果面**边界钉死。

---

## C. execution state 在系统中的位置（写死）

这个对象应位于：

- `release_control` 子动作**执行过程之中**
- `release_control input / readiness / wiring` 之后
- `release_control result object` 之前
- 治理链 / 中台消费层之前

并写清（写死）：

- 它不是 input contract
- 不是 readiness gate
- 不是 wiring 结果
- 不是 result object
- 不是总治理动作状态对象
- 它是“`release_control` 子动作执行过程**唯一应回传**的标准化 execution state 对象”

---

## D. execution state 的最小字段类别（只定义类别与语义；不做细表；不做实现）

建议至少包括这 **5 类**（收敛，不发散）：

1) **执行状态类**  
用于表示当前 `release_control` 是否处于：
- `not_started`
- `executing`
- `blocked`
- `failed`
- `completed_candidate`

并写死：
- `completed_candidate` **不等于**最终结果完成（final result），只能表达“可能接近完成/满足候选条件”。

2) **动作类型确认类**  
用于表示：
- 当前就是 `release_control`
- 不允许兼容 `rollback` / `interrupt`

3) **异常 / 阻断状态类**  
用于表示：
- 是否被阻断
- 是否失败
- 是否因前提不足或执行异常未能继续

4) **执行影响状态类（扩展占位）**  
用于表示：
- 当前执行是否只处于“控制权交还过程中的候选影响”
- 是否仍需上游进一步处理
- 当前只做语义占位，不做真实迁移

5) **回传绑定 / 路由类（扩展占位）**  
用于表示：
- 未来 execution state 如何回传到治理链 / 中台
- 当前只做绑定占位

---

## E. 哪些是“最小必需字段类别”（写死）

最小必需类别（没有这些，execution state 不成立）：

- **执行状态类**
- **动作类型确认类**
- **异常 / 阻断状态类**

并写清（写死）：
- 没有这些，`release_control execution state` 不成立。
- 执行影响类与回传绑定类当前可以占位，但未来真实接入必不可少（否则无法闭环观察与回传绑定）。

---

## F. 明确哪些东西不能直接等同于 execution state（必须写死）

以下都不能直接等同于 `navigation_governance_action_release_control_execution_state_v0`：

- 任意单个 `release_control_completed`
- 任意单个 `release_control_failed`
- 任意单个 `release_control_blocked`
- 任意单个异常回调
- 任意单个结果对象字段
- 任意单个状态对象字段
- 任意单个中台迁移状态
- 任意单个语音播报状态

解释（写死）：

- 它们只是组成依据或单点事件，不是治理链应消费的完整标准化 execution state 对象。
- execution state 必须是“过程面”的**统一回传对象**，而不是散点状态拼接。

---

## G. execution state 的最小语义（写死）

当未来系统拿到这个对象时，只表示：

- `release_control` 子动作已把自身**执行过程状态**整理成统一回传对象
- 治理链 / 中台可基于该对象做观察、记录、后续判断

它不表示（写死）：

- 中台迁移已完成
- 路线已改变
- `rollback` / `interrupt` 已执行
- 最终结果对象（`release_control result object`）已经成立

---

## H. 与现有链路的关系（写清）

### 与 release_control input contract

- input contract 是执行前输入面  
- execution state 是执行过程面  
- 两者不能混用

### 与 release_control status object

- status object 偏子动作状态观察面（更偏“治理观察/态势”）  
- execution state 偏动作执行过程面（更偏“执行中状态机回传”）  
- 两者不能混用，也不能互相替代

### 与 release_control result object

- result object 偏最终结果面  
- execution state 偏过程面  
- 不能混用，也不能用 result object 替代 execution state

### 与 release_control readiness / wiring

- readiness / wiring 是进入动作层前的门与接线  
- execution state 发生在动作过程之中  
- 不能跨层替代

---

## I. 当前仍然不能做什么（必须写死）

- 不允许真实 `release_control`
- 不允许借 execution state 顺手做 `rollback` / `interrupt`
- 不允许直接改路线
- 不允许直接触发语音播报
- 不允许直接触发中台真实迁移
- 不允许把 execution state 定义当 execution state 已实现

---

## J. 当前不做（必须写死）

- 不做 execution state 代码实现
- 不做真实 `release_control`
- 不做 `rollback` / `interrupt`
- 不做地图接入
- 不做语音/记忆联动
- 不做中台真实迁移

---

## K. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - `release_control execution state` placeholder / implementation
- 再之后才考虑：
  - `release_control` 最小真实实现
- 当前不跨这两步

---

## L. 未来 execution state 样例（仅说明，不落代码）

```json
{
  "release_control_execution_state_present": true,
  "release_control_execution_state_scope": "navigation_governance_action_release_control_execution_state_v0",
  "release_control_execution_state": "not_started|executing|blocked|failed|completed_candidate",
  "action_type_confirmed": "release_control",
  "effect_state": "unknown_not_applied",
  "route_binding_ready": false
}
```

