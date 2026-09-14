# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Implementation Skeleton v0（第一版真实受控实现：最小真实写入实现骨架冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_IMPLEMENTATION_SKELETON_V0.md`  
**性质**：Phase-Next-96：冻结 `release_control first live guarded implementation` 的 **minimal real-effect implementation skeleton**（独立“未来真实写入实现壳子”，仍不可放权、不可真实写入；可冻结、可回归）

基于（已具备）：
- minimal real-effect implementation definition（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_IMPLEMENTATION_DEFINITION_V0.md`
- minimal real-effect plan（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_PLAN_V0.md`
- minimal real-effect stub（冻结 + 落代码）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_STUB_V0.md`
- minimal real-effect non-effect wiring（冻结 + 最小实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_NON_EFFECT_WIRING_V0.md`
- minimal real-effect dry-run execution（冻结 + 最小实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_DRY_RUN_EXECUTION_V0.md`
- approval / launch / live release / side-effect release gates（最小实现）
- standard objects（实现）：`execution_state_v0` / `result_v0`

---

## A. 文档定位（写死）

这份文档是：

- `release_control first live guarded implementation minimal real-effect` 的 **专用代码骨架（implementation skeleton）** 设计与落地文档。
- 当前目标：把 definition / stub 之后的“未来真实写入实现壳子”独立出来，形成一个可冻结、可回归的实现承载位，但当前仍保持 **不可放权、不可真实写入**。

并且（本轮写死边界）：

- 当前不做真实 `release_control`。
- 当前不做真实 `rollback` / `interrupt`。
- 当前不做地图接入、不改路线。
- 当前不做语音/记忆联动。
- 当前不做中台真实迁移。
- 当前不改变现有主线行为。

---

## B. 为什么现在要做 skeleton（写死理由）

- implementation definition 已冻结：真实写入层的进入前提 / 允许面 / 禁止面 / 固定顺序已经写死。
- minimal real-effect stub 已存在：但它是“未来真实写入器壳子占位”，不是“未来真实写入实现壳子”。
- 如果没有独立 skeleton，后续真实实现只能在 stub 上硬改，容易把：
  - stub 语义（占位/非实现）
  - implementation definition 语义（边界定义/非实现）
  - 真实实现语义（受控真实写入）
  混在一起，边界会脏且更难回归与止损。

因此必须先把“未来真实写入实现壳子”独立出来，保持与 stub 分离，并继续保持不可放权。

---

## C. skeleton 的最小定义（写死）

minimal real-effect implementation skeleton：

- 不是 stub
- 不是 plan
- 不是 dry-run execution
- 不是最终真实实现

它只是：

- “未来第一版真实 minimal real-effect implementation 的专用代码骨架（实现壳子）”
- 用于承接 implementation definition 所规定的边界与顺序
- 当前仍只提供占位接口，不具备真实写入能力

---

## D. skeleton 最小能力面（写死 5 项）

1) skeleton 身份：固定 identity / scope  
2) minimal real-effect 输入接口占位：未来只接受 implementation definition 中定义的合法前提；当前不真实消费  
3) execution state 真实写入接口占位：未来允许真实写入；当前只返回 placeholder-safe / not_implemented  
4) result object 真实写入接口占位：未来允许真实写入；当前只返回 placeholder-safe / not_implemented  
5) failure/exception real-write 接口占位：未来允许真实写入；当前只返回 stop-safe / reported-placeholder  

---

## E. 默认行为（写死）

- 默认不打开 `side_effects_released`
- 默认不触发真实 `release_control`
- 默认不触发真实 `rollback` / `interrupt`
- 默认不触发 route / voice / memory / migration
- 默认只返回 `implementation_skeleton_inactive / not_implemented / placeholder-safe`

---

## F. 与现有链路的关系（写清；不能混用）

与 stub：

- stub 是未来真实写入器壳子占位（写入器接口占位）。
- implementation skeleton 是未来真实写入实现壳子（实现承载位）。
- 两者不能混用，也不能互相替代；当前任何真实写入不得落入 stub。

与 implementation definition：

- definition 规定真实写入层边界（进入前提/允许面/禁止面/顺序）。
- skeleton 是未来承接该边界的模块位置（代码壳子）。
- 当前 skeleton 不等于真实实现。

与 dry-run execution：

- dry-run execution 只跑零副作用执行顺序（调用 stub 的 placeholder 链）。
- implementation skeleton 才是未来真实写入层的专用壳子。
- `dry_run_executed` 不等于 skeleton 已具备真实写入能力。

---

## G. 当前不允许做什么（必须写死）

- 不允许把 `side_effects_released` 打开
- 不允许真实 `release_control`
- 不允许真实 `rollback` / `interrupt`
- 不允许 route / voice / memory / migration
- 不允许绕过 implementation definition / runtime contract / standard objects

