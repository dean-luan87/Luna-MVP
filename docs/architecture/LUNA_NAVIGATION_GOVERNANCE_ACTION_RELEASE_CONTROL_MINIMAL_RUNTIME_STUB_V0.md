# Luna — Navigation Governance Action Release Control Minimal Runtime Stub v0（最小运行时 stub）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_RUNTIME_STUB_V0.md`  
**性质**：Phase-Next-72：把 `release_control minimal runtime contract` 推进为“不可执行、可观察、可回归”的最小 runtime stub（落代码；不触发真实动作）

关联：
- runtime contract（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_RUNTIME_CONTRACT_V0.md`
- minimal executor（冻结/骨架）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_EXECUTOR_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_EXECUTOR_SKELETON_V0.md`
- executor input bridge（冻结/最小实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_EXECUTOR_INPUT_BRIDGE_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_EXECUTOR_INPUT_BRIDGE_IMPLEMENTATION_V0.md`
- execution state / result（实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_EXECUTION_STATE_IMPLEMENTATION_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_RESULT_OBJECT_IMPLEMENTATION_V0.md`

---

## A. 文档定位（写死）

- 这是 `release_control minimal runtime` 的最小 stub 设计与落地文档。
- 当前目标：把 runtime contract 推进到 runtime stub（仅占位验证，不产生真实副作用）。
- 当前不做真实 `release_control`。
- 当前不做 `rollback` / `interrupt`。
- 当前不接地图。
- 当前不驱动语音/记忆。
- 当前不触发中台真实迁移。
- 当前不改变现有主线行为。

---

## B. 为什么现在要做 runtime stub

- runtime contract 已冻结，但仍缺少“代码里的 runtime 承载位”。
- 若直接进入第一版真实最小实现，会跳过对以下关键点的可回归验证：
  - runtime 入口是否真的被占住（不等于真实执行）
  - execution state / result / exception path 的更新顺序是否能被保留
  - runtime 是否真的不触碰路线、语音、记忆、中台迁移
  - 失败时是否真的按合同顺序收口
- 因此必须先把 runtime contract 变成一个最小 stub。

---

## C. stub 的最小定义（写死）

- 它不是可运行的真实 `release_control`。
- 它不是 minimal executor 本体。
- 它只是一个“未来真实 runtime 执行入口”的代码壳子。
- 只负责占住运行时入口与回传顺序，不负责任何真实 side effect。

---

## D. stub 最小能力面（写死 5 个）

1) **runtime 身份**  
- 固定 identity / scope

2) **runtime 输入接口占位**  
- 未来只接受 bridge-ready 的最终执行输入  
- 当前不真实消费

3) **execution state 更新接口占位**  
- 未来按合同顺序推进  
- 当前只回 placeholder-safe / not_started-safe

4) **result object 更新接口占位**  
- 未来按合同顺序写结果  
- 当前只回 placeholder-safe / not_executed-safe

5) **exception / failure path 占位**  
- 未来按合同顺序收口  
- 当前只回 reported_placeholder

---

## E. 默认行为（写死）

- 默认不进入真实 runtime
- 默认不触发真实 `release_control`
- 默认不更新任何真实 side effect
- 默认不改路线 / 不播报 / 不写记忆 / 不迁移中台
- 默认只返回 `not_implemented / inactive / placeholder-safe`

---

## F. 与现有链路的关系（写清）

与 minimal executor skeleton：
- skeleton 是执行器骨架  
- runtime stub 是执行器未来运行态入口骨架  
- 两者职责不同，不能混用

与 executor input bridge：
- bridge 未来决定 runtime 是否可形成最终输入  
- runtime stub 未来只接受 bridge 输出  
- 当前不真实消费 bridge

与 execution state / result object：
- runtime stub 未来必须通过这两个标准面回传  
- 当前不生成真实状态与真实结果

---

## G. 当前不允许做什么（写死）

- 不允许真实 `release_control`
- 不允许借 stub 顺手做 `rollback` / `interrupt`
- 不允许直接改路线
- 不允许直接触发语音播报
- 不允许直接触发中台真实迁移
- 不允许绕过 runtime contract

---

## H. 代码落点（本轮落地）

- `capabilities/governance/runtime/navigation_governance_action_release_control_minimal_runtime_stub_v0.py`

