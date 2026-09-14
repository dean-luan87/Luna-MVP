# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Definition v0（第一版真实实现：guarded 落地定义冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_DEFINITION_V0.md`  
**性质**：Phase-Next-84：冻结 `release_control` 第一版真实 live implementation 的 “guarded 落地定义”（只定义、不落代码、不触发真实动作；可冻结、可回归）

基于（已具备）：
- approval gate（冻结/最小实现）：  
  `docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_ENABLEMENT_APPROVAL_GATE_V0.md`、  
  `docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_ENABLEMENT_APPROVAL_GATE_IMPLEMENTATION_V0.md`
- launch dry-run（冻结/最小实现）：  
  `docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_LAUNCH_DRY_RUN_V0.md`、  
  `docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_LAUNCH_DRY_RUN_IMPLEMENTATION_V0.md`
- enablement plan（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_ENABLEMENT_PLAN_V0.md`
- side-effect release contract / gate（冻结/最小实现）：  
  `docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_SIDE_EFFECT_RELEASE_CONTRACT_V0.md`、  
  `docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_SIDE_EFFECT_RELEASE_GATE_IMPLEMENTATION_V0.md`
- live release gate（冻结/最小实现）：  
  `docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_LIVE_RELEASE_GATE_V0.md`、  
  `docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_LIVE_RELEASE_GATE_IMPLEMENTATION_V0.md`
- guarded live stub（准 live 态承载位；不放权）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_GUARDED_LIVE_STUB_V0.md`
- minimal live execution definition（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_LIVE_EXECUTION_DEFINITION_V0.md`
- minimal runtime contract / stub（冻结/承载位）：  
  `docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_RUNTIME_CONTRACT_V0.md`、  
  `docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_RUNTIME_STUB_V0.md`
- execution state / result（实现）：  
  `docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_EXECUTION_STATE_IMPLEMENTATION_V0.md`、  
  `docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_RESULT_OBJECT_IMPLEMENTATION_V0.md`

---

## A. 文档定位（写死）

- 这是 `release_control` 第一版真实 live implementation 的 **guarded 落地定义**文档。
- 当前目标：冻结“第一次真实实现如何受控落地”的边界（可冻结、可回归）。
- 当前不做真实代码实现。
- 当前不做 `rollback` / `interrupt`。
- 当前不做地图接入。
- 当前不做语音/记忆联动。
- 当前不做中台真实迁移。
- 当前不改变现有主线行为（不改 route/proposal）。

---

## B. 为什么现在必须先定义 guarded implementation

- 当前已经有 approval gate implementation。
- 当前已经有 launch dry-run implementation。
- 当前 `side_effects_released` 仍然锁死为 `false`。
- 如果不先定义 guarded implementation，后续第一次真实实现会缺少“只允许极小放权、可立即止损、不可扩散”的单独边界，容易从受控验证滑向半正式实现。
- 因此必须先冻结 guarded implementation，再考虑是否落第一版真实实现。

---

## C. guarded implementation 的最小定义（写死）

`release_control first live guarded implementation` 是：

- 第一次真实 live execution 的受控实现形态
- 只允许在既定 gate 全通过、approval 已给、launch dry-run 已 ready 的前提下，放开最小范围真实 side effect

它不是：

- 常态正式实现
- 全量放权实现
- `rollback` / `interrupt` 实现
- route / voice / memory / migration 实现

核心定义（写死一句）：

> guarded implementation 只允许在最小、单点、可立即止损的条件下，验证第一版真实执行边界本身。

---

## D. 最小进入前提（写死）

进入 guarded implementation 前，最小前提必须全部满足（少任一项，不得进入）：

1) `first_live_enablement_approval_gate.approval_status == "first_live_enablement_approved"`  
2) `first_live_launch_dry_run.launch_status == "first_live_launch_dry_run_ready"`  
3) `live_release_gate.live_release_status == "live_release_ready"`  
4) `side_effect_release_gate.side_effect_release_status == "side_effect_release_ready"`  
5) guarded live candidate 已建立（candidate entered）  
6) `side_effects_released == false`（进入前仍处锁死态）  
7) `execution_state_v0`、`result_v0`、failure path 在位  
8) executor identity / capability 合法且保守  
9) 回退路径已验证可立即执行  

并明确（写死）：

- 当前阶段只是冻结规则，不允许真的进入。

---

## E. 最小允许放开的真实 side effect（写死极度克制）

guarded implementation **唯一允许**放开的真实 side effect 面只有：

1) `execution state` 的真实推进  
2) `result object` 的真实写入  
3) `exception / failure path` 的真实写入  

并写死：

- 这是 guarded implementation 唯一允许的真实 side effect 面。
- 其余全部禁止。

---

## F. 明确继续禁止的 side effect（必须写死）

即使进入 guarded implementation，仍禁止：

- 改路线
- 触发语音播报
- 写记忆
- 触发中台真实迁移
- 自动触发 `rollback`
- 自动触发 `interrupt`
- 越过标准对象吐散字段
- 读取地图 / 路径规划字段作为执行副作用来源

---

## G. 最小成功判定（写死）

最小成功判定至少包括：

- 在最小放权范围内完成真实 `execution state` 推进
- 在最小放权范围内完成真实 `result object` 写入
- failure path 未被误触发
- 未触碰任何禁止面
- 可完整追踪
- 可立即止损并回退

并明确（写死）：

- “成功”只表示 guarded implementation 验证通过。
- 不表示业务全链路完成。
- 不表示中台迁移完成。

---

## H. 最小失败判定（写死）

最小失败判定至少包括：

- 任一进入前提缺失
- 任一越权 side effect
- `execution state / result object` 未按顺序推进/写出
- failure path 不完整
- 任一无法立即回退到 `side_effects_released=false`
- 任一试图顺手做 `rollback` / `interrupt` / route / voice / memory / migration

---

## I. 最小止损 / 退出策略（必须写死）

一旦 guarded implementation 失败，顺序必须是：

1) 立即终止本次 guarded implementation  
2) 恢复 `side_effects_released=false`  
3) 写 `execution state`  
4) 写 `result object`  
5) 走 `exception / failure path`  
6) 交还治理链  

并明确（写死）：

- 止损必须优先于任何额外动作。
- 不允许失败后尝试扩权补救。

---

## J. 与现有链路的关系（写清）

与 approval gate：
- approval gate 决定“是否批准第一次试运行”
- guarded implementation 是批准之后的真实受控执行形态
- 两者不能混用

与 launch dry-run：
- launch dry-run 只做发车前最后检查
- guarded implementation 才是第一版真实受控执行线
- `launch_ready != 已进入 guarded implementation`

与 side-effect release contract：
- contract 决定“哪些副作用未来允许受控放开”
- guarded implementation 是这些副作用第一次被真实放开的具体执行形态
- 不得扩出 contract 之外

---

## K. 当前仍然不能做什么（必须写死）

- 不允许现在就落真实 guarded implementation 代码
- 不允许真实 `rollback` / `interrupt`
- 不允许改路线
- 不允许语音/记忆/中台迁移
- 不允许把定义文档当成已实现

---

## L. 当前不做（必须写死）

- 不做 guarded implementation 代码实现
- 不做地图接入
- 不做语音/记忆联动
- 不做中台真实迁移
- 不做扩展业务逻辑

---

## M. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - first live guarded implementation stub
- 再之后才考虑：
  - 第一版真实 live implementation
- 当前不跨这两步

补充链接：
- Phase-Next-85：first live guarded implementation stub v0：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_STUB_V0.md`
- Phase-Next-86：first live guarded implementation admission & acceptance v0：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_ADMISSION_AND_ACCEPTANCE_V0.md`
- Phase-Next-87：first live guarded implementation skeleton v0：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_SKELETON_V0.md`
- Phase-Next-91：first live guarded implementation minimal real-effect plan v0：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_PLAN_V0.md`

---

## N. 未来 guarded implementation 样例（仅说明，不落代码）

```json
{
  "release_control_first_live_guarded_implementation_scope": "navigation_governance_action_release_control_first_live_guarded_implementation_definition_v0",
  "entry_conditions": [
    "approval_gate_approved",
    "launch_dry_run_ready",
    "live_release_ready",
    "side_effect_release_ready",
    "execution_state_present",
    "result_present"
  ],
  "allowed_real_side_effects": [
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

