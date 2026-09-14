# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Dry-Effect Simulation v0（第一版真实受控实现：Dry-Effect Simulation 冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_DRY_EFFECT_SIMULATION_V0.md`  
**性质**：Phase-Next-90：冻结 `release_control` 第一版真实 guarded implementation 的 **dry-effect simulation**（只模拟落点、不放权；可冻结、可回归）

基于（已具备）：
- definition（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_DEFINITION_V0.md`
- skeleton（冻结 + 骨架代码）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_SKELETON_V0.md`
- non-effect wiring（冻结 + 最小实现）：  
  `docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_NON_EFFECT_WIRING_V0.md`、  
  `docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_NON_EFFECT_WIRING_IMPLEMENTATION_V0.md`
- minimal non-effect execution（冻结 + 最小实现）：  
  `docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_NON_EFFECT_EXECUTION_V0.md`、  
  `docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_NON_EFFECT_EXECUTION_IMPLEMENTATION_V0.md`
- admission & acceptance（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_ADMISSION_AND_ACCEPTANCE_V0.md`
- side-effect release contract（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_SIDE_EFFECT_RELEASE_CONTRACT_V0.md`

---

## A. 文档定位（写死）

这份文档是：

- `release_control first live guarded implementation` 的 **dry-effect simulation** 设计文档。
- 当前目标：在 `execution_status == "first_live_guarded_non_effect_executed"` 的前提下，模拟未来真实副作用的“目标落点”与“禁止面隔离”，但当前只生成 simulation target，不做任何真实写入。

并且（本轮写死边界）：

- 当前不做真实 `release_control`。
- 当前不做真实 `rollback` / `interrupt`。
- 当前不做地图接入、不改路线。
- 当前不做语音/记忆联动。
- 当前不做中台真实迁移。
- 当前不改变现有主线行为。
- 当前 `side_effects_released` 仍强制锁死为 `false`（不允许打开）。

---

## B. 为什么现在要做 dry-effect simulation（写死理由）

- minimal non-effect execution 只证明“调用顺序可走通”，并不证明未来真实副作用仍会严格落在允许面。
- 因此必须再做一层 dry simulation：验证“未来若放开允许的三类真实副作用”，目标落点仍被 contract 限制在三类允许面内，并且不会越权触碰 route/voice/memory/migration/rollback/interrupt。
- 但当前仍不能放开任何真实副作用；simulation 只生成目标集合与禁止面检查结果。

---

## C. dry-effect simulation 的最小定义（写死）

`dry-effect simulation`：

- 不是真实 effect implementation
- 不是 minimal non-effect execution 本身

它只是：

- 未来真实副作用“目标落点”的干跑模拟层
- 只允许生成 `simulation_targets`，不允许真实写入

---

## D. 最小合法输入（写死；只允许标准化对象）

Dry-effect simulation 只允许消费：

1) `navigation_governance_action_release_control_first_live_guarded_implementation_non_effect_execution_v0`
   - 必须 `execution_status == "first_live_guarded_non_effect_executed"`
2) guarded implementation skeleton identity / capability
   - 必须在位且仍为 skeleton / simulation-safe mode（保守能力：不可放权、不可执行真实 release_control）
3) `execution_state_v0` 在位
4) `result_v0` 在位
5) failure / exit path 语义在位，可被 simulation target 引用

并明确（写死）：

- 缺任一主前提，dry-effect simulation 不成立。
- 禁止直接读取 `request_* / approved_* / raw metadata` 作为输入来源。

---

## E. 最小结果集合（写死；三态）

Dry-effect simulation 的结果必须收敛成三态之一：

- `first_live_guarded_dry_effect_simulated`
- `first_live_guarded_dry_effect_not_ready`
- `first_live_guarded_dry_effect_blocked`

并明确（写死）：

- `simulated` 只表示“未来真实副作用目标落点已被干跑模拟并通过禁止面检查”。
- 不表示真实实现已开始。
- 不表示副作用已发生。

---

## F. simulation target 范围（写死；仅三类允许目标）

未来若放开，simulation **只允许**指向以下三类目标：

1) `execution_state_update_target`
2) `result_object_update_target`
3) `failure_or_exception_path_target`

并明确（写死）：

- 不允许模拟 route / voice / memory / migration / rollback / interrupt 目标。
- 一旦出现这些目标，必须判定 `blocked`。

---

## G. 明确禁止（写死）

Dry-effect simulation 不允许直接：

- 打开 `side_effects_released`
- 执行真实 `release_control`
- 改路线
- 触发语音播报
- 写记忆
- 触发中台真实迁移
- 自动触发 `rollback` / `interrupt`
- 越过标准对象吐散字段

---

## H. 与现有链路的关系（写清；不能混用）

与 minimal non-effect execution：

- non-effect execution 负责跑通调用顺序
- dry-effect simulation 负责验证未来副作用目标落点
- `executed != simulated`

与 skeleton：

- skeleton 是未来真实实现壳子
- dry-effect simulation 是 skeleton 的副作用目标模拟层
- 两者不能混用

与 side-effect release contract：

- contract 规定未来只允许哪三类真实副作用
- dry-effect simulation 负责验证目标落点是否确实被限制在这三类

---

## I. 当前仍然不能做什么（写死）

- 不允许把 `side_effects_released` 打开
- 不允许真实 `release_control`
- 不允许真实 `rollback` / `interrupt`
- 不允许 route / voice / memory / migration
- 不允许把 `simulated` 当作真实副作用已发生

---

## J. 当前不做（写死）

- 不做真实 effect implementation
- 不做地图接入
- 不做语音/记忆联动
- 不做中台真实迁移

---

## K. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - Phase-Next-91：first live guarded implementation minimal real-effect plan v0：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_PLAN_V0.md`
  - Phase-Next-92：first live guarded implementation minimal real-effect stub v0：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_STUB_V0.md`
  - 再之后才考虑：first live guarded implementation minimal real-effect implementation
- 当前不直接落真实实现

