# Luna — Navigation Governance Action Executor Readiness Gate v0（治理动作执行器就绪门控：设计冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_READINESS_GATE_V0.md`  
**性质**：Phase-Next-45：治理动作执行器从“对象层（可识别/可回传）”走向“未来最小真实动作实现”之前的最后就绪门控（设计冻结；不落代码）

关联（已具备）：
- 治理动作执行器本体最小定义：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_MINIMAL_DEFINITION_V0.md`
- 治理动作执行器模块骨架：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_MINIMAL_MODULE_SKELETON_V0.md`
- 治理动作执行器输入对象（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_INPUT_OBJECT_V0.md`
- 治理动作执行器输入对象（正式实现版）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_INPUT_OBJECT_IMPLEMENTATION_V0.md`
- 治理动作状态对象（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_STATUS_OBJECT_V0.md`
- 治理动作状态对象（正式实现版）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_STATUS_OBJECT_IMPLEMENTATION_V0.md`
- 已批准治理动作边界（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_APPROVAL_BOUNDARY_V0.md`
- 已批准治理动作边界（最小非动作实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_APPROVAL_BOUNDARY_IMPLEMENTATION_V0.md`
- 批准边界状态对象（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_APPROVAL_STATUS_OBJECT_V0.md`
- 批准边界状态对象（正式实现版）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_APPROVAL_STATUS_OBJECT_IMPLEMENTATION_V0.md`
- 治理动作执行器接线边界（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_WIRING_V0.md`
- 治理动作执行器接线最小非动作实现：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_WIRING_IMPLEMENTATION_V0.md`

---

## A. 文档定位（写死）

- 这是「**治理动作执行器最小就绪门控（readiness gate）**」的设计文档。
- 当前目标：冻结治理动作执行器从对象层走向动作层前的最后门控边界（可冻结、可回归）。
- 当前不做真实治理动作实现。
- 当前不做真实批准链执行。
- 当前不做地图接入。
- 当前不做语音/记忆联动。
- 当前不改变现有主线行为（不改 route/proposal，不触发中台真实迁移）。

---

## B. 为什么现在必须先定义 readiness gate

- 当前已经有：approved boundary、approval status object、executor input object、action status object、executor skeleton。
- 但还没有一个统一判断「治理动作执行器是否具备进入动作层前置条件」的门控层。
- 若不先定义这道门，后续很容易把 `executor skeleton + input object` **误当成可执行**，造成越权与语义漂移。
- 因此必须先冻结 readiness gate，让“是否可进入动作层候选条件”的判断有统一边界与最小结果集合。

---

## C. readiness gate 的最小定义（写死）

readiness gate 是：

- 在治理动作执行器真正进入未来动作实现前，对**主输入对象**、执行器可用性、约束、回传面等最小前提进行统一门控判断的层。

它不是（写死）：

- governance entry
- governance decision
- governance action boundary
- governance action approval boundary
- governance action executor 本体
- 真实治理动作执行器
- formal decision
- readiness gate（导航执行器那套）的替代品

核心一句（写死）：

**governance action executor readiness gate 只负责判断「是否具备进入动作层候选条件」，不直接执行任何治理动作。**

---

## D. 当前最小合法输入（写死）

readiness gate **只允许消费标准化对象**，禁止直接用散字段/原始枚举作为主输入。

主输入（必须）：

1) implemented `navigation_governance_action_executor_input_v0`  
- **主输入**；没有它不得做 ready 判断（不得以 request/approved 枚举替代）。

在位性/承载面依据（必须）：

2) implemented `navigation_governance_action_status_v0`  
- 作为未来执行后状态承载面的在位性依据（只检查“承载面是否在位”，不等于动作已发生）。

3) implemented `navigation_governance_action_approval_status_v0`  
- 作为批准层状态一致性依据（只做一致性门控，不等于批准链已执行）。

4) governance action executor skeleton identity / capability  
- 作为执行器本体在位与“当前仍为 skeleton”的可观察依据（identity 必须匹配；且明确仍受硬边界约束）。

可选只读一致性校验（不得扩权）：

5) implemented `navigation_governance_action_approval_boundary_v0`  
- 仅用于一致性校验，不作为主输入替代。

明确禁止（写死）：

- 禁止直接读取 `candidate / request_* / approved_* / raw metadata` 作为 readiness gate 主输入。

---

## E. 最小门控类别（收敛为 5 类，写死）

只允许以下 5 类门控，不发散：

1) **输入对象门控**  
- `navigation_governance_action_executor_input_v0` 是否存在且结构合法（implemented）。

2) **执行器可用性门控**  
- executor skeleton 是否在位；identity 是否正确；能力面是否仍处于硬边界约束下（例如仍为 skeleton/不可真实执行）。

3) **约束满足性门控**  
- input object 内的执行约束/前提是否满足最小进入条件。  
- 当前默认偏保守（即便对象齐备，也不默认可进入动作层）。

4) **状态回传面门控**  
- `navigation_governance_action_status_v0` 是否具备作为回传承载面的基础条件（implemented 在位）。

5) **批准一致性门控**  
- `navigation_governance_action_approval_status_v0` 与 input object（及可选 approval boundary）是否一致；不一致即硬阻断。

---

## F. 最小门控结果集合（收敛，写死）

结果集合最小为：

- `ready_candidate`
- `not_ready`
- `blocked`

语义（写死）：

1) `ready_candidate`  
- 仅表示：未来若进入最小真实治理动作实验线，**候选前提大体齐备**。  
- **不表示**真实动作已开始/已执行。

2) `not_ready`  
- 对象存在，但前提尚未齐备。  
- 不允许进入动作层。

3) `blocked`  
- 存在硬阻断或一致性问题。  
- 明确不允许进入动作层。

---

## G. 当前最小判断原则（克制、默认保守）

不做复杂评分模型，只做最小规则集（写死）：

规则 1：主输入对象缺失  
→ `not_ready`（保守：缺失即不评估，且不允许进入动作层）

规则 2：executor skeleton 不在位 / identity 不匹配  
→ `blocked`

规则 3：批准状态与输入对象不一致  
→ `blocked`

规则 4：状态回传面未就绪（action status object 不在位/不合法）  
→ `not_ready`

规则 5：对象齐备但约束仍明确不允许进入动作层  
→ `not_ready`

总体原则（写死）：

- 当前默认偏保守。  
- `ready_candidate` 只在极窄条件下出现。  
- readiness gate 的通过不等于“允许真实执行”，只等于“具备进入动作层候选条件”。

---

## H. 与现有链路的关系（写清）

### 与 governance action approval boundary / approval status

- 它们提供“是否被批准、批准层当前状态”的依据。
- 但它们不直接等于 readiness gate 结果；readiness gate 仍必须检查执行器在位、输入完整性、回传承载面与一致性。

### 与 governance action executor input object

- input object 是 readiness gate 的**主输入**。
- readiness gate 只判断其是否可进入未来动作层候选，不替代 input object，更不允许用散字段替代。

### 与 governance action status object

- status object 是未来动作执行后的**回传承载面**。
- readiness gate 只检查其承载面是否在位，不等于动作已发生。

### 与 governance action executor skeleton

- skeleton 是未来执行器本体壳子。
- readiness gate 不替代 skeleton，也不让 skeleton 直接执行动作。

---

## I. 当前仍然不能做什么（必须写死）

- 不允许真实回退动作
- 不允许真实中断动作
- 不允许真实释放控制权动作
- 不允许直接改路线
- 不允许直接触发语音播报
- 不允许直接触发中台真实迁移
- 不允许把 `ready_candidate` 当作动作已开始/已执行

---

## J. 当前不做（必须写死）

- 不做 readiness gate 代码实现
- 不做真实治理动作实现
- 不做真实批准链执行
- 不做地图接入
- 不做语音/记忆联动
- 不做自动迁移 / 自动治理

---

## K. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - governance action executor readiness gate 的 placeholder 或 implementation
- 再之后才考虑：
  - 真实治理动作最小实现
- 当前不跨这两步

---

## L. 未来门控结果样例（仅说明，不落代码、不改现有链路）

```json
{
  "governance_action_executor_readiness_attempted": true,
  "governance_action_executor_readiness_scope": "navigation_governance_action_executor_readiness_gate_v0",
  "governance_action_executor_readiness_status": "ready_candidate|not_ready|blocked",
  "reason": "..."
}
```

