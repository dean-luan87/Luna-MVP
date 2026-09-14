# Luna — Navigation Governance Action Release Control First Live Enablement Plan v0（第一版真实放权试运行：启用方案冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_ENABLEMENT_PLAN_V0.md`  
**性质**：Phase-Next-79：冻结 `release_control` 第一次把副作用从锁死态带入最小真实执行验证的启用、灰度与回退方案（不落代码、不触发真实动作）

基于（已具备）：
- live release gate（冻结/最小实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_LIVE_RELEASE_GATE_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_LIVE_RELEASE_GATE_IMPLEMENTATION_V0.md`
- side-effect release contract / gate（冻结/最小实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_SIDE_EFFECT_RELEASE_CONTRACT_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_SIDE_EFFECT_RELEASE_GATE_IMPLEMENTATION_V0.md`
- guarded live stub：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_GUARDED_LIVE_STUB_V0.md`
- minimal live execution definition：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_LIVE_EXECUTION_DEFINITION_V0.md`
- minimal runtime contract / stub：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_RUNTIME_CONTRACT_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_RUNTIME_STUB_V0.md`
- execution state / result（实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_EXECUTION_STATE_IMPLEMENTATION_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_RESULT_OBJECT_IMPLEMENTATION_V0.md`

---

## A. 文档定位（写死）

- 这是 `release_control` 第一版真实放权试运行（first live enablement）的启用方案文档。
- 当前目标：冻结“第一次把副作用从锁死态带入最小真实执行验证”的开启、灰度与回退方案（可冻结、可回归）。
- 当前不做真实 `release_control`。
- 当前不做 `rollback` / `interrupt`。
- 当前不做地图接入。
- 当前不做语音/记忆联动。
- 当前不做中台真实迁移。
- 当前不改变现有主线行为（不改 route/proposal）。

---

## B. 为什么现在必须先定义 enablement plan

- 当前已经有 live release gate minimal implementation。
- 当前已经有 side-effect release gate minimal implementation。
- 当前 `side_effects_released` 仍锁死为 `false`。
- 若没有单独的 first enablement plan，后续第一次打开会变成“临时决定”，无法保证灰度、回退、追踪与止损。
- 因此必须先冻结第一次真实放权的启用方案，再考虑是否真的打开。

---

## C. first live enablement 的最小定义（写死）

`release_control first live enablement plan` 是：

- 第一版真实放权试运行的启用方案
- 只针对 `release_control` 一条子动作链
- 只允许最小范围、最小环境、最小副作用面放开

它不是（写死）：

- 长期开关策略
- 全量放权策略
- `rollback` / `interrupt` 启用方案
- 中台迁移启用方案
- 业务级扩容方案

核心定义（建议写死一句）：

> first live enablement 只允许“最小、受控、可回退”的第一次真实放权试运行，不允许扩成常态执行模式。

---

## D. 最小开启前提（写死）

建议最小开启前提至少包括：

1) `navigation_governance_action_release_control_live_release_gate_v0.live_release_status == "live_release_ready"`  
2) `navigation_governance_action_release_control_side_effect_release_gate_v0.side_effect_release_status == "side_effect_release_ready"`  
3) guarded live stub 已 entered candidate  
4) `side_effects_released == false`（仍处锁死态）  
5) `execution_state_v0` 在位  
6) `result_v0` 在位  
7) exception / failure path 已验证可用（可观察、可收口、可回归）  
8) 回退路径已定义且可立即执行  
9) 默认开关仍为 `false`，必须显式批准才允许试运行  

并写清（写死）：

- 少任一项，不得进入 first live enablement。
- 当前阶段只是冻结规则，不允许真的打开。

---

## E. 最小允许放开范围（写死极度克制）

第一版真实放权最多只允许：

1) `execution state` 的真实推进  
2) `result object` 的真实写入  
3) `exception / failure path` 的真实写入  

并写死：

- 其余全部禁止。

---

## F. 明确继续禁止的 side effect（必须写死）

即使进入 first live enablement，仍禁止：

- 改路线
- 触发语音播报
- 写记忆
- 触发中台真实迁移
- 自动触发 `rollback`
- 自动触发 `interrupt`
- 越过标准对象吐散字段
- 读取地图 / 路径规划字段作为执行副作用来源

---

## G. 最小灰度策略（写清并写死）

建议最小灰度策略至少包括：

- 仅单动作：只允许 `release_control`
- 仅单链路：只允许当前链路，不扩散到其它治理动作
- 仅单环境：只允许受控环境 / 试运行环境
- 仅单版本：仅限本次 enablement 试运行版本
- 仅显式批准后开启：默认不开

并写死：

- 不允许一开始就多动作、多环境、多版本放开。

---

## H. 最小成功判定（写死）

最小成功判定建议至少包括：

- 放权后仍严格遵守 runtime contract
- `execution state` 按顺序推进
- `result object` 按顺序写出
- failure path 可正常收口
- 未触碰禁止面
- 可完整追踪（可通过标准对象回放）
- 可立即回退（能恢复到 `side_effects_released=false`）

并写清（写死）：

- “成功”仅表示第一版真实放权试运行验证通过。
- 不表示业务全链路完成。
- 不表示中台迁移完成。

---

## I. 最小失败判定（写死）

最小失败判定建议至少包括：

- 任一进入前提缺失
- 任一越权 side effect
- `execution state / result object` 未按顺序推进/写出
- failure path 不完整
- 任一无法回退到 `side_effects_released=false`
- 任一试图顺手做 `rollback` / `interrupt` / route / voice / memory / migration

---

## J. 最小回退策略（必须写死）

当试运行失败时，最小回退顺序必须是：

1) 立即终止本次试运行  
2) 恢复 `side_effects_released=false`  
3) 写 `execution state`  
4) 写 `result object`  
5) 走 `exception / failure path`  
6) 交还治理链  

并写死：

- 回退必须优先于任何额外动作。
- 不允许失败后再尝试扩权补救。

---

## K. 与现有链路的关系（写清）

与 live release gate：
- live release gate 决定是否具备进入真实执行线的资格  
- enablement plan 决定是否在本次试运行中真的启用

与 side-effect release gate：
- side-effect release gate 决定是否具备未来副作用放权资格  
- enablement plan 决定是否把这个资格用于第一次真实试运行

与 runtime contract：
- runtime contract 约束试运行中的执行顺序与禁止面  
- enablement plan 约束“这次试运行能否开始”

---

## L. 当前仍然不能做什么（必须写死）

- 不允许现在就把 `side_effects_released` 打开
- 不允许真实 `rollback` / `interrupt`
- 不允许改路线
- 不允许语音/记忆/中台迁移
- 不允许把启用方案当成已启用

---

## M. 当前不做（必须写死）

- 不做 enablement plan 代码实现
- 不做真实 `release_control`
- 不做 `rollback` / `interrupt`
- 不做地图接入
- 不做语音/记忆联动
- 不做中台真实迁移

---

## N. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - first live enablement 的 minimal stub / dry-run guard
  - Phase-Next-80：first live enablement dry-run stub v0：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_ENABLEMENT_DRY_RUN_STUB_V0.md`
  - Phase-Next-81：first live enablement approval gate v0：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_ENABLEMENT_APPROVAL_GATE_V0.md`
  - Phase-Next-82：first live enablement approval gate minimal implementation v0：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_ENABLEMENT_APPROVAL_GATE_IMPLEMENTATION_V0.md`
  - Phase-Next-83：first live launch dry-run v0：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_LAUNCH_DRY_RUN_V0.md`
  - Phase-Next-83：first live launch dry-run minimal implementation v0：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_LAUNCH_DRY_RUN_IMPLEMENTATION_V0.md`
  - Phase-Next-84：first live guarded implementation definition v0：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_DEFINITION_V0.md`
  - Phase-Next-85：first live guarded implementation stub v0：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_STUB_V0.md`
  - Phase-Next-86：first live guarded implementation admission & acceptance v0：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_ADMISSION_AND_ACCEPTANCE_V0.md`
- 再之后才考虑：
  - 第一版真实 live implementation
- 当前不跨这两步

---

## O. 未来启用方案样例（仅说明，不落代码）

```json
{
  "release_control_first_live_enablement_scope": "navigation_governance_action_release_control_first_live_enablement_plan_v0",
  "entry_conditions": [
    "live_release_ready",
    "side_effect_release_ready",
    "guarded_candidate_entered",
    "execution_state_present",
    "result_present",
    "rollback_path_verified"
  ],
  "allowed_live_side_effects": [
    "execution_state_update",
    "result_object_update",
    "exception_path"
  ],
  "still_forbidden": [
    "route_change",
    "voice_output",
    "memory_write",
    "mid_platform_real_migration",
    "rollback",
    "interrupt"
  ]
}
```

