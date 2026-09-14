# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Live Implementation Admission & Acceptance v0（准入与验收红线：冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_ADMISSION_AND_ACCEPTANCE_V0.md`  
**性质**：Phase-Next-117：冻结第一版真实最小写入实现（live implementation）的**准入条件、验收口径、失败红线、固定回退顺序**（只冻结，不落真实实现；可回归）

基于（已具备）：
- live implementation definition v0：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_DEFINITION_V0.md`
- live implementation skeleton v0：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_SKELETON_V0.md`
- live implementation stub v0：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_STUB_V0.md`
- activation contract / gate / dry-run（冻结 + 最小实现）
- commit / pre-commit / launch / admission 全链路对象（最小实现）
- 当前 `side_effects_released` 仍强制锁死为 `false`

---

## 1. 文档定位（写死）

这份文档是：

- `release_control first live guarded implementation minimal real-effect live implementation` 的**准入与验收**设计冻结文档。
- 当前目标：冻结“从 live implementation stub 到未来 live implementation minimal implementation”的准入红线与验收口径。

并且（本轮写死边界）：

- 当前不做真实代码实现（不落 live implementation minimal implementation）。
- 当前不做真实 `rollback` / `interrupt`。
- 当前不做地图接入、不改路线。
- 当前不做语音/记忆联动。
- 当前不做中台真实迁移。
- 当前不改变现有主线行为。

---

## 2. 为什么现在必须先定义 admission & acceptance（写死理由）

- 当前已经有 live implementation definition（本体边界）。
- 当前已经有 live implementation skeleton（代码壳子）。
- 当前已经有 live implementation stub（runtime 占位层）。
- 但还没有一份明确的“什么时候才允许真正开始 live implementation minimal implementation”的准入和验收文档。
- 如果不先冻结 admission & acceptance，后续最容易在实现过程中扩面或放松红线，尤其是在 `side_effects_released` 的打开与失败收口上。

因此必须先冻结准入与验收，再考虑 live implementation minimal implementation。

---

## 3. admission 的最小定义（写死）

`release_control first live guarded implementation minimal real-effect live implementation admission` 是：

- 允许第一版真实最小写入实现开始进入代码落地的前置门槛
- 只决定“是否允许开始第一版真实最小写入实现”

它不是：

- activation gate / activation dry-run
- live implementation definition / skeleton / stub

---

## 4. 最小准入条件（写死；少任一项不得进入真实实现）

以下条件必须全部满足（少任一项不得进入 live implementation minimal implementation）：

- admission gate == admitted
- guarded launch gate == launch_admitted
- pre-commit dry-run == pre_commit_ready
- commit gate == commit_admitted
- commit dry-run == commit_ready
- activation gate == activation_admitted
- activation dry-run == activation_ready
- approval / launch / live release / side-effect release 全部 ready/approved
- dry-effect simulation == simulated
- implementation dry-run execution == executed
- `execution_state_v0 / result_v0 / exception_or_failure path` 在位
- activation contract 已冻结
- live implementation definition 已冻结
- live implementation skeleton 已存在
- live implementation stub 已存在并验证通过
- 回退路径已定义且可立即执行
- 默认开关仍为 false
- `side_effects_released` 仍为 false
- 显式批准信号存在（语义在位；不得由 raw metadata 直驱）
- 严禁读取 `request_* / approved_* / raw metadata` 作为直驱依据

---

## 5. 最小允许实现范围（写死）

未来真实实现仅允许覆盖三类真实副作用：

1) `execution_state_real_write`
2) `result_object_real_write`
3) `exception_or_failure_real_write`

除此以外全部视为越权。

---

## 6. 最小验收条件（写死）

最小验收需同时满足：

- 只触达三类允许面
- 顺序符合 activation contract 与 live implementation definition（state → result；异常按固定收口）
- 未触碰任何禁止面
- 失败路径可触发、可收口、可追踪
- 任意时刻可恢复 `side_effects_released=false`
- 白盒可复盘
- 不得把实验实现扩成业务动作或默认实现

---

## 7. 最小止损红线（写死；触碰任一即失败）

触碰任一即失败：

- 打开了不该打开的副作用面
- 顺序错误
- `side_effects_released` 无法恢复为 false
- failure path 缺失或不可收口
- 试图顺手做 `rollback / interrupt / route / voice / memory / migration`
- 越过标准对象吐散字段

---

## 8. 最小回退判据与固定顺序（写死）

- 触碰红线或准入不满足：立即判定 fail。
- 固定回退顺序（写死）：
  1) 恢复 `side_effects_released=false`
  2) 写失败/退出态 `execution_state`
  3) 写失败 `result_object`
  4) 写 `exception_or_failure`
  5) 交还治理链

并明确（写死）：

- 不允许失败后补救扩权
- 不允许失败后保留半开启状态

---

## 9. 明确禁止（写死）

admission & acceptance 不允许放行：

- route change
- voice output
- memory write
- mid-platform real migration
- rollback
- interrupt
- map/path planning side-effect source
- 越过标准对象吐散字段

---

## 10. 与现有链路的关系（写清）

- 与 live implementation definition：definition 定边界；admission & acceptance 定准入和验收。
- 与 live implementation skeleton / stub：它们是承载壳子与运行时占位；admission & acceptance 是进入真实实现前的闸口与验收标准。
- 与 activation contract / gate / dry-run：这些负责进入受控激活前的判断和演练；admission & acceptance 负责真实实现本体开始前的最终门槛。

---

## 11. 当前仍然不能做什么（写死）

- 不允许现在就把 `side_effects_released` 打开
- 不允许真实写入
- 不允许真实 `release_control`
- 不允许真实 `rollback` / `interrupt`
- 不允许 `route / voice / memory / migration`
- 不允许把 admission & acceptance 当成真实实现已存在

---

## 12. 当前不做（写死）

- 不做 live implementation minimal implementation 代码实现
- 不做真实最小写入实现
- 不做地图接入
- 不做语音/记忆联动
- 不做中台真实迁移

---

## 13. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - minimal real-effect live implementation minimal implementation v0
- 当前不直接落真实实现

补充链接（冻结链路）：

- Phase-Next-122：First Real Write Rollout Plan v0（第一次真实最小写入试运行上线方案冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_FIRST_REAL_WRITE_ROLLOUT_PLAN_V0.md`
- Phase-Next-123：Real-Write Go/No-Go Gate v0（真实写入启动最终闸门冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_REAL_WRITE_GO_NO_GO_GATE_V0.md`

