# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Plan v0（第一版真实受控实现：最小真实副作用落地计划冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_PLAN_V0.md`  
**性质**：Phase-Next-91：冻结 `release_control` 第一版真实 guarded implementation 的 **minimal real-effect plan**（只写计划与边界、不落真实实现；可冻结、可回归）

基于（已具备）：
- definition（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_DEFINITION_V0.md`
- admission & acceptance（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_ADMISSION_AND_ACCEPTANCE_V0.md`
- skeleton（冻结 + 骨架）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_SKELETON_V0.md`
- non-effect wiring（冻结 + 最小实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_NON_EFFECT_WIRING_V0.md`
- minimal non-effect execution（冻结 + 最小实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_NON_EFFECT_EXECUTION_V0.md`
- dry-effect simulation（冻结 + 最小实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_DRY_EFFECT_SIMULATION_V0.md`
- gates（最小实现）：approval gate / launch dry-run / live release gate / side-effect release gate
- standard objects（实现）：`execution_state_v0` / `result_v0` / failure path 承载位

---

## A. 文档定位（写死）

这份文档是：

- `release_control first live guarded implementation` 的 **最小真实副作用落地计划**（minimal real-effect plan）。
- 当前目标：冻结“第一版真实副作用如何最小开启”的代码落地边界：只允许三类允许面、固定顺序写入、明确止损红线与回退策略。

并且（本轮写死边界）：

- 当前不做真实代码实现（不落真实 guarded implementation）。
- 当前不做真实 `rollback` / `interrupt`。
- 当前不做地图接入、不改路线。
- 当前不做语音/记忆联动。
- 当前不做中台真实迁移。
- 当前不改变现有主线行为。
- 当前不默认打开 `side_effects_released`（仍保持 `false`）。

---

## B. 为什么现在必须先定义 minimal real-effect plan（写死理由）

- 当前已经有 minimal non-effect execution（证明调用顺序可走通）。
- 当前已经有 dry-effect simulation（证明未来副作用目标落点被限制在三类允许面）。
- 但仍缺少一份明确的“第一次真实副作用如何最小开启”的落地计划（范围、顺序、止损、回退）。
- 如果不先冻结这份计划，后续真实实现容易：
  - 直接放宽副作用面；
  - 把顺序、止损、回退写散到多个模块，导致失控；
  - 把实验性受控实现滑成默认实现。

因此必须先冻结 minimal real-effect plan，再考虑是否真正开始第一版真实 guarded implementation 的最小真实写入。

---

## C. minimal real-effect plan 的最小定义（写死）

`release_control first live guarded implementation minimal real-effect plan` 是：

- 第一次真实 guarded implementation **允许最小副作用落地**的代码计划。
- 只针对三类允许面：
  1) `execution state`
  2) `result object`
  3) `exception / failure path`

它不是：

- 全量真实实现 / 常态实现
- `rollback` / `interrupt` 实现
- route / voice / memory / migration 实现

核心定义（写死一句）：

> minimal real-effect plan 只允许把三类已被批准的最小真实副作用按固定顺序落地，不允许扩展到任何其它副作用面。

---

## D. 最小进入前提（写死；少任一项不得进入真实副作用落地）

进入 minimal real-effect plan（讨论/执行“最小真实写入”）之前，以下条件必须全部满足（少任一项，不得进入）：

1) `first_live_enablement_approval_gate.approval_status == "first_live_enablement_approved"`  
2) `first_live_launch_dry_run.launch_status == "first_live_launch_dry_run_ready"`  
3) `live_release_gate.live_release_status == "live_release_ready"`  
4) `side_effect_release_gate.side_effect_release_status == "side_effect_release_ready"`  
5) `first_live_guarded_implementation_non_effect_execution.execution_status == "first_live_guarded_non_effect_executed"`  
6) `first_live_guarded_implementation_dry_effect_simulation.simulation_status == "first_live_guarded_dry_effect_simulated"`  
7) `execution_state_v0`、`result_v0`、failure path 在位  
8) guarded implementation skeleton identity / capability 合法且保守  
9) 回退路径已验证可立即执行  
10) `side_effects_released` 默认仍为 `false`；只有在本计划被单独允许后，才可讨论受控打开（且必须受 gate/contract/标准对象约束）

并明确（写死）：

- 少任一项，不得进入真实副作用落地。
- 当前阶段只冻结规则：**不允许真的开始真实实现**。

---

## E. 最小允许放开的真实副作用范围（写死；极度克制）

第一版真实 guarded implementation **最多只允许**真实副作用落地：

1) `execution state` 的真实写入  
2) `result object` 的真实写入  
3) `exception / failure path` 的真实写入  

并写死：

- 除上述三类之外，其他一律视为越权副作用（直接触发失败与止损）。

---

## F. 真实写入最小顺序（写死；禁止倒序/跳步/补写）

### 正常路径（写死）

1) 真实写 `execution state`  
2) 真实写 `result object`  
3) 正常结束后交还治理链  

### 异常路径（写死）

1) 立即恢复 `side_effects_released=false`  
2) 真实写 `execution state`（失败/退出态）  
3) 真实写 `result object`（失败结果）  
4) 真实写 `exception / failure path`  
5) 交还治理链  

并明确（写死）：

- 不允许倒序。
- 不允许跳步。
- 不允许先写 result 再写 state。
- 不允许先做额外动作再补写标准对象。

---

## G. 明确继续禁止的副作用面（必须写死）

即使进入 minimal real-effect plan，仍然禁止：

- route change
- voice output
- memory write
- mid-platform real migration
- `rollback`
- `interrupt`
- map/path planning side-effect source
- 越过标准对象吐散字段

---

## H. 最小成功判定（写死）

最小成功判定至少包括：

- 三类允许面按固定顺序真实写入（state → result →（必要时 failure path））
- 未触碰任何禁止面
- failure path 未被误触发
- 白盒可追踪
- 可立即止损并回退
- 未把实验性实现扩成默认实现或业务动作

---

## I. 最小失败判定（写死）

最小失败判定至少包括：

- 任一进入前提缺失
- 任一顺序错误（倒序/跳步/先 result 后 state）
- 任一越权副作用
- 任一 failure path 缺失或不可收口
- 任一无法恢复 `side_effects_released=false`
- 任一试图顺手做 `rollback` / `interrupt` / route / voice / memory / migration

---

## J. 最小止损 / 回退策略（写死）

一旦失败，顺序必须是：

1) 立即终止本次真实副作用落地  
2) 立即恢复 `side_effects_released=false`  
3) 写 `execution state`  
4) 写 `result object`  
5) 写 `exception / failure path`  
6) 交还治理链  

并明确（写死）：

- 止损优先于任何额外动作。
- 不允许失败后扩权补救。
- 不允许失败后保留半开启副作用状态。

---

## K. 与现有链路的关系（写清；不能混用）

与 dry-effect simulation：

- simulation 只模拟未来目标落点
- minimal real-effect plan 才定义第一次真实写入怎么发生（范围/顺序/止损/回退）
- `simulated != 可直接真实写入`

与 admission & acceptance：

- admission & acceptance 规定什么时候允许开始真实实现、什么算通过、什么必须止损
- minimal real-effect plan 规定真实副作用第一次怎么最小落地
- 两者不能混用

与 runtime contract：

- runtime contract 规定运行时顺序与禁止面
- minimal real-effect plan 必须受其约束
- 不得越过 contract 自行定义副作用顺序或扩大副作用面

---

## L. 当前仍然不能做什么（必须写死）

- 不允许现在就开始真实代码实现。
- 不允许把 `side_effects_released` 默认打开。
- 不允许真实 `rollback` / `interrupt`。
- 不允许 route / voice / memory / migration。
- 不允许把计划文档当成实现已存在。

---

## M. 当前不做（必须写死）

- 不做 minimal real-effect plan 代码实现。
- 不做真实 `release_control`。
- 不做地图接入。
- 不做语音/记忆联动。
- 不做中台真实迁移。
- 不做扩展业务逻辑。

---

## N. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - Phase-Next-92：first live guarded implementation minimal real-effect stub v0：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_STUB_V0.md`
  - 再之后才考虑：
    - Phase-Next-95：first live guarded implementation minimal real-effect implementation definition v0：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_IMPLEMENTATION_DEFINITION_V0.md`
    - 以及在 definition 冻结后：first live guarded implementation minimal real-effect implementation skeleton / gate 或真正实现方案
- 当前不直接落真实实现

补充链接（最终准入门：设计冻结）：

- Phase-Next-99：Minimal Real-Effect Admission Gate v0：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_ADMISSION_GATE_V0.md`

---

## O. 未来计划样例（仅说明，不落代码）

```json
{
  "release_control_first_live_guarded_implementation_minimal_real_effect_plan_scope": "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_plan_v0",
  "entry_conditions": [
    "approval_gate_approved",
    "launch_dry_run_ready",
    "live_release_ready",
    "side_effect_release_ready",
    "non_effect_execution_executed",
    "dry_effect_simulation_simulated"
  ],
  "allowed_real_effects": [
    "execution_state_real_write",
    "result_object_real_write",
    "exception_or_failure_real_write"
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

