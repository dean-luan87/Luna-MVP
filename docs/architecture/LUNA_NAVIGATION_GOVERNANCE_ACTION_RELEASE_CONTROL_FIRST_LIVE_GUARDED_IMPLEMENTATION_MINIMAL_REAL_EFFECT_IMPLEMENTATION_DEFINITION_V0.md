# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Implementation Definition v0（第一版真实受控实现：最小真实写入实现定义冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_IMPLEMENTATION_DEFINITION_V0.md`  
**性质**：Phase-Next-95：冻结 `release_control first live guarded implementation` 的 **minimal real-effect implementation definition**（只冻结“真实写入层边界与顺序”，不落真实实现；可冻结、可回归）

基于（已具备）：
- minimal real-effect plan（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_PLAN_V0.md`
- minimal real-effect stub（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_STUB_V0.md`
- minimal real-effect non-effect wiring（冻结 + 最小实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_NON_EFFECT_WIRING_V0.md`
- minimal real-effect dry-run execution（冻结 + 最小实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_DRY_RUN_EXECUTION_V0.md`
- dry-effect simulation（冻结 + 最小实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_DRY_EFFECT_SIMULATION_V0.md`
- minimal non-effect execution（冻结 + 最小实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_NON_EFFECT_EXECUTION_V0.md`
- gates（最小实现）：approval gate / launch dry-run / live release gate / side-effect release gate
- standard objects（实现）：`execution_state_v0` / `result_v0`
- admission & acceptance（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_ADMISSION_AND_ACCEPTANCE_V0.md`

---

## A. 文档定位（写死）

这份文档是：

- `release_control first live guarded implementation` 的 **minimal real-effect implementation definition**（最小真实副作用实现定义冻结）。
- 当前目标：冻结“第一版真实 guarded implementation 若真的开始写真实副作用代码，它在代码层到底是什么、只允许写什么、绝对不能写什么、它与 plan / stub / dry-run 的边界是什么”。

并且（本轮写死边界）：

- 当前不做真实代码实现（不落真实 minimal real-effect implementation）。
- 当前不做真实 `release_control`。
- 当前不做真实 `rollback` / `interrupt`。
- 当前不做地图接入、不改路线。
- 当前不做语音/记忆联动。
- 当前不做中台真实迁移。
- 当前不改变现有主线行为。

---

## B. 为什么现在必须先定义 implementation definition（写死理由）

- 当前已经有 minimal real-effect plan（冻结范围与顺序）。
- 当前已经有 minimal real-effect stub（占位未来真实写入接口，但不具备真实写入能力）。
- 当前已经有 minimal real-effect non-effect wiring（证明 stub 已获得合法入口，但不放权）。
- 当前已经有 minimal real-effect dry-run execution（证明固定三步顺序可在零副作用模式下走通）。
- 但当前仍缺少一份单独的“真实实现层定义”（implementation definition），用于把 **plan / stub / dry-run / 真实实现** 四层在语义与代码边界上拆开。
- 如果不先冻结这份定义，后续一旦开始写真实 state/result/failure path 的写入逻辑，容易把真实写入侵入到 stub、计划层或 dry-run 层，造成边界混乱与扩权滑坡。

因此必须先冻结 minimal real-effect implementation definition，再考虑任何真实代码实现（甚至是 skeleton/gate 级别的承接层）。

---

## C. minimal real-effect implementation 的最小定义（写死）

`release_control first live guarded implementation minimal real-effect implementation` 是：

- 第一次真实 guarded implementation 中，**负责最小真实副作用写入**的实现层。
- 只允许写入三类真实副作用：
  1) `execution state`
  2) `result object`
  3) `exception / failure path`

它不是：

- plan
- stub
- non-effect wiring
- dry-run execution
- 全量真实实现
- `rollback` / `interrupt` 实现
- route / voice / memory / migration 实现

核心定义（写死一句）：

> minimal real-effect implementation 只负责把已批准的三类最小真实副作用按固定顺序真正写入，不负责任何其它业务动作或系统副作用。

---

## D. 最小进入前提（写死；少任一项不得进入真实实现层）

进入 minimal real-effect implementation（真实写入层）之前，以下条件必须全部满足（少任一项，不得进入）：

1) `approval_gate.approval_status == "first_live_enablement_approved"`  
2) `launch_dry_run.launch_status == "first_live_launch_dry_run_ready"`  
3) `live_release_gate.live_release_status == "live_release_ready"`  
4) `side_effect_release_gate.side_effect_release_status == "side_effect_release_ready"`  
5) `first_live_guarded_implementation_non_effect_execution.execution_status == "first_live_guarded_non_effect_executed"`  
6) `first_live_guarded_implementation_dry_effect_simulation.simulation_status == "first_live_guarded_dry_effect_simulated"`  
7) `first_live_guarded_implementation_minimal_real_effect_wiring.wiring_status == "first_live_minimal_real_effect_wired_ready"`  
8) `first_live_guarded_implementation_minimal_real_effect_dry_run_execution.execution_status == "first_live_minimal_real_effect_dry_run_executed"`  
9) `execution_state_v0`、`result_v0`、failure/exception path 承载位在位  
10) 回退路径已验证可立即执行（包含可恢复到 `side_effects_released=false` 的可达性验证）  
11) `side_effects_released` 默认仍为 `false`；只有进入真实实现层时，才允许讨论“受控开启”的语义，但**不允许在本阶段发生任何真实开启**。

并明确（写死）：

- 少任一项，不得进入真实实现层。
- 当前阶段只冻结规则：不允许真的开始真实实现。

---

## E. 最小允许真实写入范围（写死；与 plan 保持一致）

第一版真实 guarded implementation 的 minimal real-effect implementation **最多只允许**真实写入：

1) `execution_state_real_write`
2) `result_object_real_write`
3) `exception_or_failure_real_write`

并明确（写死）：

- 这三类以外的任何真实写入，全部视为越权。

---

## F. 明确继续禁止的真实副作用面（必须写死）

即使进入 minimal real-effect implementation，仍然禁止：

- route change
- voice output
- memory write
- mid-platform real migration
- `rollback`
- `interrupt`
- map/path planning side-effect source
- 越过标准对象吐散字段

---

## G. 真实写入最小顺序（写死；禁止倒序/跳步/补写）

### 正常路径（写死）

1) `execution_state_real_write`
2) `result_object_real_write`
3) 交还治理链

### 异常路径（写死）

1) 立即恢复 `side_effects_released=false`
2) `execution_state_real_write`（失败/退出态）
3) `result_object_real_write`（失败结果）
4) `exception_or_failure_real_write`
5) 交还治理链

并明确（写死）：

- 不允许倒序。
- 不允许跳步。
- 不允许先 result 后 state。
- 不允许先做额外动作再补写标准对象。

---

## H. 与现有链路的关系（写清；不能混用）

与 plan：

- plan 是落地计划（范围/顺序/止损/回退的计划冻结）。
- implementation definition 是真实代码边界定义（真实写入层是什么、允许/禁止什么）。
- 两者不能混用；plan 不是实现，definition 也不是实现。

与 stub：

- stub 是未来真实写入器壳子（占位接口，不具备真实写入能力）。
- implementation definition 是该壳子未来真正填充的边界（允许面/禁止面/顺序/进入前提）。
- 当前 stub 不等于 implementation。

与 dry-run execution：

- dry-run execution 只验证顺序与调用边界可走通（零副作用、placeholder-safe）。
- implementation definition 才定义“真实写入层”是什么，以及真实写入必须遵守什么边界与顺序。
- `dry_run_executed` 不等于真实实现已存在，更不等于真实写入已发生。

---

## I. 当前仍然不能做什么（必须写死）

- 不允许现在就开始真实代码实现。
- 不允许默认打开 `side_effects_released`。
- 不允许真实 `rollback` / `interrupt`。
- 不允许 route / voice / memory / migration。
- 不允许把 definition 文档当作“真实实现已存在”。

---

## J. 当前不做（必须写死）

- 不做 minimal real-effect implementation 代码实现。
- 不做真实 `release_control`。
- 不做地图接入。
- 不做语音/记忆联动。
- 不做中台真实迁移。
- 不做扩展业务逻辑。

---

## K. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - Phase-Next-96：first live guarded implementation minimal real-effect implementation skeleton v0：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_IMPLEMENTATION_SKELETON_V0.md`
  - 在 skeleton 独立且仍不可放权后，才考虑：minimal real-effect implementation non-effect wiring
  - 或真实实现方案（仍需受控、可回归）
- 当前不直接落真实实现。

补充链接（冻结链路）：

- Phase-Next-99：Minimal Real-Effect Admission Gate v0（最终准入门：设计冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_ADMISSION_GATE_V0.md`
- Phase-Next-104：Minimal Real-Effect Pre-Commit Dry-Run v0（最后预提交干跑层：设计冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_PRE_COMMIT_DRY_RUN_V0.md`
- Phase-Next-106：Minimal Real-Effect Commit Gate v0（最终 commit 放行门：设计冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_COMMIT_GATE_V0.md`
- Phase-Next-109：Minimal Real-Effect Activation Contract v0（side effects 受控激活合同：设计冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_ACTIVATION_CONTRACT_V0.md`
- Phase-Next-110：Minimal Real-Effect Activation Gate v0（side effects 受控激活判断门：设计冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_ACTIVATION_GATE_V0.md`
- Phase-Next-114：Minimal Real-Effect Live Implementation Definition v0（第一版真实最小写入实现本体：定义冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_DEFINITION_V0.md`

