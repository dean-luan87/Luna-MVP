# Luna — Navigation Governance Action Release Control Readiness Gate v0（Release Control 子动作就绪门控：设计冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_READINESS_GATE_V0.md`  
**性质**：Phase-Next-57：冻结 `release_control` 子动作从“对象已在位”走向“可进入最小真实动作实验线”前的最后门控边界（不落代码）

关联（已具备）：
- release_control 最小定义冻结：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_DEFINITION_V0.md`
- release_control skeleton：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_SKELETON_V0.md`
- release_control 输入契约（冻结/实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_INPUT_CONTRACT_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_INPUT_CONTRACT_IMPLEMENTATION_V0.md`
- release_control 状态对象（冻结/实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_STATUS_OBJECT_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_STATUS_OBJECT_IMPLEMENTATION_V0.md`
- 总治理执行器 readiness gate（冻结/实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_READINESS_GATE_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_READINESS_GATE_IMPLEMENTATION_V0.md`
- 执行器接线（冻结/实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_WIRING_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_WIRING_IMPLEMENTATION_V0.md`
- release_control 子动作接线边界（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_WIRING_V0.md`
- release_control 子动作接线最小非动作实现：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_WIRING_IMPLEMENTATION_V0.md`

---

## A. 文档定位（写死）

- 这是 `release_control` 子动作最小就绪门控（readiness gate）的设计文档。
- 当前目标：冻结 `release_control` 从对象层走向动作层前的最后门控边界（可冻结、可回归）。
- 当前不做真实 `release_control`。
- 当前不做 `rollback` / `interrupt`。
- 当前不做地图接入。
- 当前不做语音/记忆联动。
- 当前不改变现有主线行为（不改 route/proposal，不触发中台真实迁移）。

---

## B. 为什么现在必须先定义 release_control readiness gate

- 当前已经有 `release_control input contract` implemented object。
- 当前已经有 `release_control status object` implemented object。
- 当前已经有 `release_control skeleton`。
- 但还没有一个统一判断“`release_control` 是否具备进入最小真实动作前置条件”的**子动作级门控**。
- 若不先冻结这道门，后续很容易把 skeleton + input object 误当成可执行。
- 因此必须先冻结 `release_control readiness gate`，避免子动作回退到总执行器门控或散字段判断。

---

## C. release_control readiness gate 的最小定义（写死）

release_control readiness gate 是：

- 在 `release_control` 子动作真正进入未来最小真实实现前，对其输入、可用性、约束、状态承载面、上游一致性等最小前提进行统一门控判断的层。

它不是（写死）：

- 总治理动作执行器 readiness gate
- release_control skeleton 本身
- release_control 输入对象本身
- release_control 状态对象本身
- rollback / interrupt 的共享门控

核心一句（写死）：

**release_control readiness gate 只负责判断“是否具备进入 release_control 动作层候选条件”，不直接执行任何动作。**

---

## D. 当前最小合法输入（写死：只消费标准化对象）

必须输入（写死）：

1) implemented `navigation_governance_action_release_control_input_v0`（主输入）  
2) implemented `navigation_governance_action_release_control_status_v0`（子动作回传承载面在位性依据）  
3) `navigation_governance_action_executor_wiring_v0`（仍处在合法接线链上的依据）  
4) `navigation_governance_action_executor_readiness_gate_v0`（总执行器级 readiness 一致性依据）  
5) release_control skeleton identity / capability（子动作本体在位且仍为 skeleton 的可观察依据）  

可选只读（仅一致性校验，不得扩权）：

6) implemented `navigation_governance_action_approval_status_v0`

并明确（写死）：

- 没有合法 `release_control input object` 时，不得做 ready 判断。
- 禁止直接读取 `request_* / approved_* / raw metadata` 作为门控主输入。
- 必须只消费标准化对象。

---

## E. 最小门控类别（收敛为 5 类；写死）

1) **子动作输入对象门控**  
- `navigation_governance_action_release_control_input_v0` 是否存在且结构合法（implemented）

2) **子动作本体可用性门控**  
- release_control skeleton 是否在位；identity 是否正确；是否仍受硬边界约束

3) **约束满足性门控**  
- input object 内约束是否满足最小进入条件（当前默认保守）

4) **子动作状态承载面门控**  
- `navigation_governance_action_release_control_status_v0` 是否在位且结构合法（implemented）

5) **上游一致性门控**  
- 与总执行器 wiring/readiness 是否一致（不一致则硬阻断）

---

## F. 最小门控结果集合（写死）

- `ready_candidate`
- `not_ready`
- `blocked`

语义（写死）：

- `ready_candidate`：仅表示未来进入最小真实动作实验线的候选前提大体齐备；不表示动作已开始  
- `not_ready`：对象存在但前提未齐备；不允许进入动作层  
- `blocked`：存在硬阻断或一致性问题；明确不允许进入动作层

---

## G. 当前最小判断原则（克制、默认保守）

至少支持（写死）：

- 主输入对象缺失 → `not_ready`
- release_control skeleton 不在位 / identity 不匹配 → `blocked`
- 上游总 wiring / readiness 不一致 → `blocked`
- 子动作状态承载面未就绪 → `not_ready`
- 对象齐备但约束仍明确不允许进入动作层 → `not_ready`

并写死：

- 当前默认偏保守
- `ready_candidate` 只在极窄条件下出现
- 不做复杂评分模型

---

## H. 与现有链路的关系（写清）

### 与总 governance action executor readiness gate

- 总 gate 判断“总执行器是否具备候选条件”。  
- 本 gate 判断“release_control 子动作是否具备候选条件”。  
- 两者不能混用。

### 与 release_control input contract

- input object 是主输入。
- readiness gate 只判断其是否可进入未来动作层候选。

### 与 release_control status object

- status object 是未来动作后的回传面。
- readiness gate 只检查承载面是否在位，不等于动作已发生。

### 与 release_control skeleton

- skeleton 是未来子动作本体壳子。
- readiness gate 不替代 skeleton，也不让 skeleton 直接执行动作。

---

## I. 当前仍然不能做什么（必须写死）

- 不允许真实 `release_control`
- 不允许真实 `rollback` / `interrupt`
- 不允许直接改路线
- 不允许直接触发语音播报
- 不允许直接触发中台真实迁移
- 不允许把 `ready_candidate` 当动作已开始

---

## J. 当前不做（必须写死）

- 不做 `release_control readiness gate` 代码实现
- 不做真实 `release_control`
- 不做 `rollback` / `interrupt`
- 不做地图接入
- 不做语音/记忆联动
- 不做自动迁移 / 自动治理

---

## K. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - `release_control readiness gate` 的 placeholder 或 implementation
- 再之后才考虑：
  - `release_control` 最小真实实现
- 当前不跨这两步

