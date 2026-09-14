# Luna — Navigation Governance Action Release Control Minimal Executor Skeleton v0（子动作最小真实执行器骨架）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_EXECUTOR_SKELETON_V0.md`  
**性质**：Phase-Next-68：把 `release_control minimal executor` 从定义冻结推进为“不可执行、可接入、可观察”的最小模块骨架（落代码；不触发真实动作）

关联：
- minimal executor 定义冻结：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_EXECUTOR_V0.md`
- release_control 最小定义冻结：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_DEFINITION_V0.md`
- release_control 子动作 skeleton：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_SKELETON_V0.md`
- 输入契约实现版：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_INPUT_CONTRACT_IMPLEMENTATION_V0.md`
- execution state（冻结/实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_EXECUTION_STATE_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_EXECUTION_STATE_IMPLEMENTATION_V0.md`
- result object（冻结/实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_RESULT_OBJECT_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_RESULT_OBJECT_IMPLEMENTATION_V0.md`

---

## A. 文档定位（写死）

- 这是 `release_control minimal executor` 最小模块骨架的设计与落地文档。
- 当前目标：把 minimal executor 从定义推进到模块骨架。
- 当前不做真实 `release_control`。
- 当前不做 `rollback` / `interrupt`。
- 当前不做地图接入。
- 当前不做语音/记忆联动。
- 当前不触发中台真实迁移。
- 当前不改变现有主线行为。

---

## B. 为什么现在要做 skeleton

- minimal executor 定义已经冻结。
- 若没有模块骨架，后续 `release_control` 的执行输入面、`execution state`、`result object`、异常面都没有真实挂点，容易回到散字段/散函数并导致边界漂移。
- 因此必须先把 `release_control minimal executor` 实体化为模块骨架。

---

## C. skeleton 的最小定义（写死）

- 它不是可运行的 `release_control` 执行器。
- 不是 governance entry / decision / action boundary / approval boundary。
- 不是 `release_control` 子动作 skeleton 的替代物。
- 它只是一个“未来可被治理链调用的 `release_control` 最小执行单元壳子”。

---

## D. skeleton 最小能力面（写死 5 个）

1) **模块身份**  
- 固定 identity / scope，例如 `navigation_governance_action_release_control_minimal_executor_v0`

2) **输入接口占位**  
- 未来只接受合法的 `release_control` 输入对象与相关门控结果  
- 当前只做接口占位，不做真实消费

3) **execution state 回传接口占位**  
- 未来只回标准化 `execution state`  
- 当前只做接口占位，不做真实状态生成

4) **result object 回传接口占位**  
- 未来只回标准化 `result object`  
- 当前只做接口占位，不做真实结果生成

5) **异常上报接口占位**  
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

与 `release_control` 子动作 skeleton：
- 子动作 skeleton 更偏“动作壳子”  
- minimal executor skeleton 更偏“未来真实执行单元壳子”  
- 两者当前都不可执行，但职责不同，不能混用

与 `release_control input / readiness / wiring`：
- 未来只有在上游已批准、已就绪、已合法接线后才有资格被调用  
- 当前不直接消费普通 `request_release_control`

与 `release_control execution state / result object`：
- 未来它应通过这两个标准对象回传过程与结果  
- 当前不直接生成真实对象

与中台：
- 当前不直接与中台真实迁移链交互

---

## G. 当前不允许做什么（写死）

- 不允许真实 `release_control`
- 不允许借该 skeleton 顺手做 `rollback` / `interrupt`
- 不允许直接吃未批准的 recommendation / boundary
- 不允许直接改路线
- 不允许直接触发语音播报
- 不允许直接触发中台真实迁移
- 不允许绕过 `input / readiness / wiring / execution state / result object` 边界

---

## H. 代码落点（本轮落地）

- `capabilities/governance/runtime/navigation_governance_action_release_control_minimal_executor_v0.py`

