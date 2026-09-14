# Luna — Navigation Governance Action Release Control Status Object v0（Release Control 子动作状态对象：设计冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_STATUS_OBJECT_V0.md`  
**性质**：Phase-Next-53：冻结 `release_control` 子动作未来唯一应回传的标准化状态对象（不落代码、不触发真实动作）

关联：
- release_control 最小定义冻结：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_DEFINITION_V0.md`
- release_control skeleton：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_SKELETON_V0.md`
- release_control 输入契约冻结/占位：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_INPUT_CONTRACT_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_INPUT_CONTRACT_PLACEHOLDER_V0.md`
- 状态对象正式实现版：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_STATUS_OBJECT_IMPLEMENTATION_V0.md`
- 结果对象（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_RESULT_OBJECT_V0.md`
- 总治理动作状态对象（冻结/实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_STATUS_OBJECT_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_STATUS_OBJECT_IMPLEMENTATION_V0.md`

---

## A. 文档定位（写死）

- 这是 `release_control` 子动作标准化状态对象的最小设计文档。
- 当前目标：冻结 `release_control` 状态回传对象边界（可冻结、可回归）。
- 当前不做真实 `release_control`。
- 当前不做 `rollback` / `interrupt`。
- 当前不做地图接入。
- 当前不做语音/记忆联动。
- 当前不改变现有主线行为（不改 route/proposal，不触发中台真实迁移）。

---

## B. 为什么现在要先定义状态对象

- 当前已有 `release_control` skeleton。
- 当前已有 `release_control` input contract（以及占位输出）。
- 但还没有“`release_control` 自身状态如何被统一组织并回传”的正式对象。
- 若不先定义状态对象，后续最小真实实现会退回散字段，或直接污染总治理动作状态对象（子动作语义不清、不可回归）。
- 因此必须先冻结 `release_control` 子动作状态对象。

---

## C. 状态对象在系统中的位置（写死）

这个对象应位于：

- `release_control` 子动作之后
- 治理链 / 中台消费层之前
- **不直接替代**总治理动作状态对象，但未来应可向其汇总或映射

并写清（写死）：

- 它不是总治理状态对象本身
- 不是 input contract
- 不是 action boundary / approval boundary
- 它是“`release_control` 子动作唯一应回传的标准化状态对象”

---

## D. 状态对象的最小字段类别（只定义类别与语义；不做细表；不做实现）

建议至少包括这 **5 类**（收敛，不发散）：

1) **子动作状态类**  
- 表达 `release_control` 是否处于 `requested / blocked / completed / failed / inactive` 等状态类别

2) **动作类型确认类**  
- 必须明确当前就是 `release_control`  
- 不允许兼容 `rollback` / `interrupt`

3) **异常 / 阻断状态类**  
- 是否被阻断、是否失败、是否因前提不足未能继续

4) **结果影响状态类（扩展占位）**  
- 是否只是“控制权交还语义成立”  
- 是否需要上游继续处理  
- 当前只做语义占位，**不做真实迁移**

5) **回传绑定 / 路由类（扩展占位）**  
- 未来如何回传到治理链 / 中台  
- 当前只做绑定占位

---

## E. 哪些是“最小必需字段类别”（写死）

最小必需类别（没有这些，状态对象不成立）：

- **子动作状态类**
- **动作类型确认类**
- **异常 / 阻断状态类**

并写清（写死）：

- 结果影响类与回传绑定类当前可以占位，但未来真实接入必不可少（否则无法闭环观测与回传绑定）。

---

## F. 明确哪些东西不能直接等同于状态对象（必须写死）

以下都不能直接等同于 `navigation_governance_action_release_control_status_v0`：

- 任意单个 `release_control_requested`
- 任意单个 `release_control_completed`
- 任意单个 `release_control_failed`
- 任意单个异常回调
- 任意单个治理动作总状态对象字段
- 任意单个中台迁移状态
- 任意单个语音播报状态

解释（写死）：

- 它们只是组成依据或单点事件，不是治理链应消费的完整标准化状态对象。

---

## G. 状态对象的最小语义（写死）

当未来系统拿到这个对象时，只表示：

- `release_control` 子动作已把自身当前状态整理成统一回传对象
- 治理链 / 中台可基于该对象做观察、记录、后续判断

它不表示：

- 真实中台迁移已完成
- 路线已改变
- `rollback` / `interrupt` 已执行

---

## H. 与现有链路的关系（写清）

### 与 release_control input contract

- input contract 是执行前输入面
- status object 是执行后回传面
- 两者不能混用

### 与 release_control skeleton

- skeleton 未来应通过该对象回传状态
- 当前 skeleton 仍不执行真实动作

### 与总治理动作状态对象

- 总体对象是上位汇总面
- `release_control` 状态对象是子动作专属面
- 未来可映射或汇总，但当前不实现

---

## I. 当前仍然不能做什么（必须写死）

- 不允许真实 `release_control`
- 不允许借状态对象顺手做 `rollback` / `interrupt`
- 不允许直接改路线
- 不允许直接触发语音播报
- 不允许直接触发中台真实迁移
- 不允许把状态对象定义当状态对象已实现

---

## J. 当前不做（必须写死）

- 不做状态对象代码实现
- 不做真实 `release_control`
- 不做 `rollback` / `interrupt`
- 不做地图接入
- 不做语音/记忆联动
- 不做中台真实迁移

---

## K. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - `release_control status object` placeholder / implementation
- 再之后才考虑：
  - `release_control` 最小真实实现
- 当前不跨这两步

