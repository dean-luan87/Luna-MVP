# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Stub v0（第一版真实受控实现：最小真实副作用写入器 Stub 冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_STUB_V0.md`  
**性质**：Phase-Next-92：把 minimal real-effect plan 推进到“可进入、可观测、但仍不真正写真实副作用”的实现 stub（落代码壳子；不触发真实动作；可冻结、可回归）

基于（已具备）：
- minimal real-effect plan v0（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_PLAN_V0.md`
- guarded implementation skeleton v0（冻结 + 壳子）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_SKELETON_V0.md`
- non-effect wiring / non-effect execution / dry-effect simulation（冻结 + 最小实现）：见 plan v0 与相关文档
- standard objects（实现）：`execution_state_v0` / `result_v0` / failure path

---

## A. 文档定位（写死）

这份文档是：

- `release_control first live guarded implementation` 的 **minimal real-effect stub** 设计与落地文档。
- 当前目标：把 minimal real-effect plan 从“计划层”推进到“实现壳子层”，占住未来三类允许面真实写入接口的位置与调用顺序，但当前仍然不具备任何真实副作用写入能力。

并且（本轮写死边界）：

- 当前不做真实 `release_control`。
- 当前不做真实 `rollback` / `interrupt`。
- 当前不做地图接入、不改路线。
- 当前不做语音/记忆联动。
- 当前不做中台真实迁移。
- 当前不改变现有主线行为。
- 当前 `side_effects_released` 仍强制锁死为 `false`（不允许打开）。

---

## B. 为什么现在要做 minimal real-effect stub（写死理由）

- minimal real-effect plan 已冻结，但还没有代码侧的“真实写入器壳子”。
- 如果没有独立 stub，后续真实写入会从计划层直接跳到真实实现层，缺少最后一层“接口/顺序/收口位置占位验证”，容易把：
  - 计划
  - 实现壳子
  - 真实写入
  混在一起，边界再次变脏。

因此必须先把“未来真实写入器壳子”独立出来，但当前仍不能放开任何真实副作用。

---

## C. stub 的最小定义（写死）

minimal real-effect stub：

- 不是真实 real-effect implementation
- 不是 skeleton / non-effect execution / dry-effect simulation 本身

它只是：

- 未来“写入三类允许面（state/result/failure）”的专用代码壳子
- 只负责承载：输入接口占位、三类写入接口占位、止损收口接口占位

---

## D. stub 最小能力面（写死 5 项）

1) stub 身份：固定 identity / scope  
2) real-effect 输入接口占位：未来只接受 plan 中定义的合法前提；当前不真实消费  
3) execution state real-write 接口占位：未来允许真实写入；当前只返回 placeholder-safe / not_implemented  
4) result object real-write 接口占位：未来允许真实写入；当前只返回 placeholder-safe / not_implemented  
5) failure/exception real-write 接口占位：未来允许真实写入；当前只返回 stop-safe / reported-placeholder  

---

## E. 默认行为（写死）

- 默认不打开 `side_effects_released`
- 默认不触发真实 `release_control`
- 默认不触发 `rollback` / `interrupt`
- 默认不触发 route / voice / memory / migration
- 默认只返回 `real_effect_stub_inactive / not_implemented / placeholder-safe`

---

## F. 与现有链路的关系（写清；不能混用）

与 skeleton：

- skeleton 是未来真实实现壳子
- minimal real-effect stub 是未来真实写入壳子
- 两者不能混用

与 non-effect execution：

- non-effect execution 负责零副作用执行链
- minimal real-effect stub 负责未来真实写入接口占位

与 dry-effect simulation：

- simulation 只模拟未来真实副作用目标落点
- minimal real-effect stub 才是未来真实写入落点的代码壳子
- 当前仍不真实写入

与 minimal real-effect plan：

- plan 规定真实副作用如何最小落地（范围/顺序/止损/回退）
- stub 为其提供代码承载位
- 当前仍不执行 plan

---

## G. 当前不允许做什么（必须写死）

- 不允许把 `side_effects_released` 打开
- 不允许真实 `release_control`
- 不允许真实 `rollback` / `interrupt`
- 不允许 route / voice / memory / migration
- 不允许绕过 real-effect plan / runtime contract / standard objects

---

## H. 建议落点（写清）

Minimal real-effect stub 的最小、最连续落点是：

- `capabilities/governance/runtime/navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_stub_v0.py`

理由（写死）：

- 与 skeleton 同域（`capabilities/governance/runtime/`），语义连续。
- 与 skeleton / non-effect executor 分文件，避免把“壳子/零副作用执行/未来真实写入”混在一起。
- 通过默认返回 `not_implemented / placeholder-safe`，确保不滑向真实写入。

补充链接：
- Phase-Next-95：first live guarded implementation minimal real-effect implementation definition v0：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_IMPLEMENTATION_DEFINITION_V0.md`

