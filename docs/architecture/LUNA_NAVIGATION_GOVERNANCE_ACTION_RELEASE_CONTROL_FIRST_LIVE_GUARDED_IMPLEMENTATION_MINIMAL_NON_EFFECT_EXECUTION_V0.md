# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Non-Effect Execution v0（第一版真实受控实现：最小非副作用执行链冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_NON_EFFECT_EXECUTION_V0.md`  
**性质**：Phase-Next-89：冻结 `release_control` 第一版真实 guarded implementation 的 **minimal non-effect execution**（只跑顺序、不放权；可冻结、可回归）

基于（已具备）：
- skeleton v0（冻结 + 骨架代码）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_SKELETON_V0.md`
- non-effect wiring v0（冻结 + 最小实现）：  
  `docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_NON_EFFECT_WIRING_V0.md`、  
  `docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_NON_EFFECT_WIRING_IMPLEMENTATION_V0.md`
- admission & acceptance v0（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_ADMISSION_AND_ACCEPTANCE_V0.md`
- runtime contract v0（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_RUNTIME_CONTRACT_V0.md`
- execution state / result object（实现）：  
  `docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_EXECUTION_STATE_IMPLEMENTATION_V0.md`、  
  `docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_RESULT_OBJECT_IMPLEMENTATION_V0.md`

---

## A. 文档定位（写死）

这份文档是：

- `release_control first live guarded implementation` 的 **最小非副作用执行链（minimal non-effect execution）**设计文档。
- 当前目标：在 `wiring_status == "first_live_guarded_wired_ready"` 的前提下，让 skeleton 第一次把“执行顺序”跑通，但全程只允许 placeholder-safe / stop-safe / exit-safe 路径。

并且（本轮写死边界）：

- 当前不做真实 `release_control`。
- 当前不做真实 `rollback` / `interrupt`。
- 当前不做地图接入、不改路线。
- 当前不做语音/记忆联动。
- 当前不做中台真实迁移。
- 当前不改变现有主线行为。
- 当前 `side_effects_released` 仍强制锁死为 `false`（不允许打开）。

---

## B. 为什么现在要做 minimal non-effect execution（写死理由）

- skeleton 已存在，non-effect wiring 已存在，但 skeleton 仍可能停留在“静态壳子”。
- 如果没有最小执行链验证，未来真实实现一落地可能同时踩到：入口衔接、调用顺序、止损收口三类问题。
- 因此必须先让 skeleton 在 **零副作用模式**下把“调用顺序”跑通，验证未来真实实现的函数边界与调用顺序可用。
- 但当前仍不能放开任何真实 side effect。

---

## C. minimal non-effect execution 的最小定义（写死）

`minimal non-effect execution`：

- 不是真实 guarded implementation
- 不是 runtime contract 本身

它只是：

- 让未来真实实现的调用顺序先在代码里跑通的最小非副作用执行链
- 只允许调用 placeholder-safe / stop-safe / exit-safe 路径

---

## D. 最小合法输入（写死；只允许标准化对象）

Minimal non-effect execution 只允许消费：

1) `navigation_governance_action_release_control_first_live_guarded_implementation_wiring_v0`
   - 必须 `wiring_status == "first_live_guarded_wired_ready"`
2) guarded implementation skeleton identity / capability
   - 必须在位且仍为 skeleton / non-effect mode
3) `execution_state_v0`
   - 在位
4) `result_v0`
   - 在位
5) failure / exit path
   - 语义在位，可被占位调用（stop-safe / exit-safe）

并明确（写死）：

- 缺任一主前提，minimal non-effect execution 不成立。
- 禁止直接读取 `request_* / approved_* / raw metadata` 作为输入来源。

---

## E. 最小结果集合（写死；三态）

Minimal non-effect execution 的结果必须收敛成三态之一：

- `first_live_guarded_non_effect_executed`
- `first_live_guarded_non_effect_not_ready`
- `first_live_guarded_non_effect_blocked`

并明确（写死）：

- `executed` 只表示“最小执行链已在零副作用模式下跑通”。
- 不表示真实实现已开始。
- 不表示副作用已发生。

---

## F. 明确禁止（写死）

Minimal non-effect execution 不允许直接：

- 打开 `side_effects_released`
- 执行真实 `release_control`
- 改路线
- 触发语音播报
- 写记忆
- 触发中台真实迁移
- 自动触发 `rollback` / `interrupt`
- 越过标准对象吐散字段

---

## G. 与现有链路的关系（写清；不能混用）

与 skeleton：

- skeleton 是未来真实实现壳子
- minimal non-effect execution 是 skeleton 的第一次零副作用执行链
- 两者不能混用

与 non-effect wiring：

- wiring 负责给 skeleton 一个合法入口
- minimal non-effect execution 负责在合法入口上跑通调用顺序
- `wired_ready != executed`

与 runtime contract：

- runtime contract 约束未来真实执行顺序
- minimal non-effect execution 只用 placeholder-safe 路径验证顺序可走通（不执行真实副作用）

---

## H. 当前仍然不能做什么（写死）

- 不允许把 `side_effects_released` 打开
- 不允许真实 `release_control`
- 不允许真实 `rollback` / `interrupt`
- 不允许 route / voice / memory / migration
- 不允许把 `executed` 当作真实实现已开始

---

## I. 当前不做（写死）

- 不做真实 guarded implementation
- 不做地图接入
- 不做语音/记忆联动
- 不做中台真实迁移

---

## J. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - first live guarded implementation minimal implementation
- 当前不直接落真实实现

