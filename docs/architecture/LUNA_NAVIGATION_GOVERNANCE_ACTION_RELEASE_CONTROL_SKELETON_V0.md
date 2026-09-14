# Luna — Navigation Governance Action Release Control Skeleton v0（Release Control 最小模块骨架）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_SKELETON_V0.md`  
**性质**：Phase-Next-50：把 `release_control` 从最小动作定义推进为“不可执行、可接入、可观察”的最小模块骨架（落代码；不触发真实动作）

关联：
- release_control 最小定义冻结：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_DEFINITION_V0.md`
- 治理动作执行器本体最小定义：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_MINIMAL_DEFINITION_V0.md`
- 治理动作执行器模块骨架：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_MINIMAL_MODULE_SKELETON_V0.md`
- 就绪门控（冻结/实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_READINESS_GATE_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_READINESS_GATE_IMPLEMENTATION_V0.md`
- 接线边界（冻结/实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_WIRING_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_WIRING_IMPLEMENTATION_V0.md`
- release_control 输入契约正式实现版：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_INPUT_CONTRACT_IMPLEMENTATION_V0.md`
- release_control 子动作接线边界（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_WIRING_V0.md`
- release_control 子动作接线最小非动作实现：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_WIRING_IMPLEMENTATION_V0.md`
- release_control 子动作最小真实执行器（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_EXECUTOR_V0.md`
- release_control 子动作最小真实执行器骨架：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_EXECUTOR_SKELETON_V0.md`

---

## A. 文档定位（写死）

- 这是 `release_control` 动作最小模块骨架的设计与落地文档。
- 当前目标：把 `release_control` 从定义推进到模块骨架。
- 当前不做真实 `release_control` 实现。
- 当前不做 `rollback` / `interrupt`。
- 当前不做地图接入。
- 当前不做语音/记忆联动。
- 当前不触发中台真实迁移。
- 当前不改变现有主线行为（不改 route/proposal）。

---

## B. 为什么现在要做 skeleton

- `release_control` 动作定义已经冻结。
- 若没有模块骨架，后续 `release_control` 的输入面、状态面、异常面都没有真实挂点，容易回到“散字段/散函数”并造成边界漂移。
- 因此必须先把 `release_control` 实体化为一个**不可执行**的模块骨架。

---

## C. skeleton 的最小定义（写死）

- 它不是可运行的 `release_control` 执行器。
- 不是 governance entry / decision / action boundary / approval boundary。
- 不是 governance action executor 总体。
- 它只是一个“未来可被治理动作执行器调用的 `release_control` 子动作壳子”。

---

## D. skeleton 最小能力面（写死 4 个）

1) **模块身份**  
- 固定 identity / scope，例如 `navigation_governance_action_release_control_v0`

2) **输入接口占位**  
- 未来只接受合法的 `release_control` 执行输入  
- 当前只做接口占位，不做真实消费

3) **状态回传接口占位**  
- 未来只回标准化的 `release_control` 动作状态  
- 当前只做接口占位，不做真实状态生成

4) **异常上报接口占位**  
- 未来异常必须走标准接口  
- 当前只做占位，不做真实异常处理

---

## E. skeleton 默认行为（写死）

- 默认不执行真实 `release_control`
- 默认不执行 `rollback` / `interrupt`
- 默认不改路线
- 默认不驱动语音
- 默认不驱动记忆
- 默认不触发中台真实迁移
- 默认只返回 `not_implemented / inactive / placeholder` 级别结果

---

## F. 与现有链路的关系（写清）

### 与 governance action executor

- `release_control` skeleton 是未来 governance action executor 内部可调用的一类子动作壳子。
- 当前不直接被主链调用成真实动作。

### 与 approval boundary / input object / readiness / wiring

- 未来只有在上游已批准、已就绪、已合法接线后才有资格被调用。
- 当前不直接消费普通 `request_release_control`。

### 与 governance action status object

- 未来其动作状态应收口到统一治理动作状态对象。
- 当前不直接生成真实状态（不回 `completed/failed` 的事实）。

### 与中台

- 当前不直接与中台真实迁移链交互。

---

## G. 当前不允许做什么（写死）

- 不允许真实 `release_control`
- 不允许借 `release_control` 顺手做 `rollback` / `interrupt`
- 不允许直接吃未批准的 action boundary / recommendation
- 不允许直接改路线
- 不允许直接触发语音播报
- 不允许直接触发中台真实迁移
- 不允许绕过 input object / readiness / wiring / status object 边界

---

## H. 代码落点（本轮落地）

- `capabilities/governance/runtime/navigation_governance_action_release_control_v0.py`

