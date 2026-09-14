# Luna — Navigation Governance Action Release Control Minimal Live Execution Definition v0（第一版真实最小执行：定义冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_LIVE_EXECUTION_DEFINITION_V0.md`  
**性质**：Phase-Next-73：冻结 `release_control` 第一版真实最小执行（live execution）的边界与验收口径（不落代码、不触发真实动作）

基于（已具备）：
- minimal executor（冻结/骨架）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_EXECUTOR_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_EXECUTOR_SKELETON_V0.md`
- executor input bridge（冻结/最小实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_EXECUTOR_INPUT_BRIDGE_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_EXECUTOR_INPUT_BRIDGE_IMPLEMENTATION_V0.md`
- minimal runtime contract / stub：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_RUNTIME_CONTRACT_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_RUNTIME_STUB_V0.md`
- input contract（冻结/实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_INPUT_CONTRACT_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_INPUT_CONTRACT_IMPLEMENTATION_V0.md`
- execution state（冻结/实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_EXECUTION_STATE_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_EXECUTION_STATE_IMPLEMENTATION_V0.md`
- result object（冻结/实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_RESULT_OBJECT_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_RESULT_OBJECT_IMPLEMENTATION_V0.md`

---

## A. 文档定位（写死）

- 这是 `release_control` 第一版真实最小执行（minimal live execution）的定义文档。
- 当前目标：冻结“第一版 live execution”的边界与验收口径（可冻结、可回归）。
- 当前不做 live implementation。
- 当前不做 `rollback` / `interrupt`。
- 当前不做地图接入。
- 当前不做语音/记忆联动。
- 当前不做中台真实迁移。
- 当前不改变现有主线行为（不改 route/proposal）。

---

## B. 为什么现在必须先定义 minimal live execution

- 当前已经有 minimal executor、executor input bridge、runtime contract、runtime stub、execution state、result object。
- 但还没有一份明确的“第一版真实执行”定义与验收口径。
- 若不先定义 live execution，后续容易把最小真实执行做成半业务动作，越权触碰路线、播报、记忆或中台迁移。
- 因此必须先冻结 minimal live execution 边界，再考虑是否落代码。

---

## C. minimal live execution 的最小定义（写死）

`release_control minimal live execution` 是：

- 第一版真实执行验证线
- 只验证“控制权交还动作边界”本身是否能在 runtime contract 约束下被真实推进

它不是（写死）：

- 完整业务动作
- `rollback`
- `interrupt`
- 路线改写
- 语音播报
- 记忆写入
- 中台真实迁移

核心定义（建议写死一句）：

> `release_control minimal live execution` 只允许验证执行边界本身，不允许扩展为完整业务动作。

---

## D. 最小进入条件（写死）

建议最小进入条件至少包括：

1) `navigation_governance_action_release_control_executor_input_bridge_v0.bridge_status == "executor_input_bridge_ready"`  
2) `consumable_by_executor` 仅在 live execution 方案中才允许被**显式打开**（当前阶段不允许真的开启）  
3) `release_control minimal executor identity / capability` 合法  
4) `navigation_governance_action_release_control_execution_state_v0` 在位  
5) `navigation_governance_action_release_control_result_v0` 在位  
6) runtime contract 已定义且 runtime stub 已存在  

并写清（写死）：

- 少任一项，不得进入 live execution。
- 当前阶段只是冻结规则，不允许真的开启。

---

## E. 最小允许 side effect（写死极克制）

第一版 live execution 唯一允许的 side effect 面只允许：

1) 真实更新 `execution state`  
2) 真实更新 `result object`  
3) 真实进入 `exception / failure path`  

并写清（写死）：

- 这是第一版 live execution 唯一允许面，其余全部禁止。

---

## F. 明确禁止的 side effect（必须写死）

第一版 live execution 不允许直接：

- 改路线
- 触发语音播报
- 写记忆
- 触发中台真实迁移
- 自动触发 `rollback`
- 自动触发 `interrupt`
- 越过标准对象吐散字段
- 读取地图 / 路径规划字段

---

## G. 最小成功判定（写死）

最小成功判定建议至少包括：

- runtime 入口条件合法成立
- `execution state` 按合同顺序推进
- `result object` 合法写出
- 没有越权触碰禁止 side effect 面
- `failure path` 未被误触发

并写清（写死）：

- “成功”仅表示第一版真实执行边界验证通过。
- 不表示业务全链路完成。
- 不表示中台迁移完成。

---

## H. 最小失败判定（写死）

最小失败判定建议至少包括：

- 任一进入前提缺失
- `execution state` 未按顺序推进
- `result object` 未按顺序写出
- 越权触碰禁止面
- `failure path` 收口不完整
- 发生任何试图顺手做 `rollback` / `interrupt` / route change / voice / memory / migration 的行为

---

## I. 失败收口原则（写死）

- 失败先写 `execution state`
- 再写 `result object`
- 再走 `exception / failure path`
- 再把处置权交还治理链
- live execution 自身不得决定 `rollback` / `interrupt`

---

## J. 与现有链路的关系（写清）

与 executor input bridge：
- bridge 决定最终执行输入是否可形成  
- live execution 只允许在 bridge ready 后进入  
- 不允许绕过 bridge

与 runtime contract：
- runtime contract 规定运行态内行为边界  
- live execution 是在该合同之下的第一版真实执行线  
- 不允许违背 contract

与 runtime stub：
- stub 是当前不可执行承载位  
- live execution 是未来要替代 stub 的最小真实执行方案  
- 当前不直接替代

与 execution state / result object：
- 两者是 live execution 必须使用的标准回传面  
- 不允许绕过它们

---

## K. 当前仍然不能做什么（必须写死）

- 不允许现在就落真实 live implementation
- 不允许真实 `rollback` / `interrupt`
- 不允许改路线
- 不允许触发语音播报
- 不允许写记忆
- 不允许触发中台真实迁移
- 不允许把定义文档当成 live execution 已实现

---

## L. 当前不做（必须写死）

- 不做 live execution 代码实现
- 不做地图接入
- 不做语音/记忆联动
- 不做中台真实迁移
- 不做扩展业务逻辑

---

## M. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - `release_control minimal live execution` stub/guarded implementation 方案
- 再之后才考虑：
  - 第一版真实 live execution 落地
- 当前不跨这两步

补充（已进入下一步）：
- Phase-Next-74：`release_control guarded live stub`（准 live 态受控 stub）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_GUARDED_LIVE_STUB_V0.md`
- Phase-Next-75：`release_control live release gate`（受控 live → 真实 live 放行门冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_LIVE_RELEASE_GATE_V0.md`
- Phase-Next-77：`side-effect release contract`（副作用放权合同冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_SIDE_EFFECT_RELEASE_CONTRACT_V0.md`
- Phase-Next-79：`first live enablement plan`（第一次真实放权试运行启用方案冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_ENABLEMENT_PLAN_V0.md`

---

## N. 未来 live execution 验收样例（仅说明，不落代码）

```json
{
  "release_control_live_execution_scope": "navigation_governance_action_release_control_minimal_live_execution_definition_v0",
  "entry_conditions": [
    "executor_input_bridge_ready",
    "execution_state_present",
    "result_object_present",
    "executor_identity_valid"
  ],
  "allowed_side_effects": [
    "execution_state_update",
    "result_object_update",
    "exception_path"
  ],
  "forbidden_side_effects": [
    "route_change",
    "voice_output",
    "memory_write",
    "mid_platform_real_migration",
    "rollback",
    "interrupt"
  ]
}
```

