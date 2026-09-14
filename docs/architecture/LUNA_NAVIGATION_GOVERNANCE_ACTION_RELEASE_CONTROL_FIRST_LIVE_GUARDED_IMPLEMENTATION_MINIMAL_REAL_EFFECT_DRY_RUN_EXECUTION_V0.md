# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Dry-Run Execution v0（干跑执行链：设计冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_DRY_RUN_EXECUTION_V0.md`  
**性质**：Phase-Next-94：在 `minimal real-effect wiring` 已闭合合法入口的前提下，对 `minimal real-effect stub` 跑通**未来真实写入顺序**的零副作用干跑链（可冻结、可回归）

基于（已具备）：
- minimal real-effect plan（冻结）
- minimal real-effect stub（冻结）
- minimal real-effect non-effect wiring（已落地）

---

## A. 文档定位（写死）

这份文档是：

- `minimal real-effect stub` 的 **minimal real-effect dry-run execution** 设计与落地说明。
- 当前目标：先把未来真实写入器的调用顺序（execution state → result → failure/exception）在代码里干跑一遍，但只调用 **placeholder-safe** 路径。
- 当前不产生任何真实写入副作用。

并且（本轮写死边界）：

- 当前不做真实 `release_control`。
- 当前不做真实 `rollback` / `interrupt`。
- 当前不做地图接入、不改路线。
- 当前不做语音/记忆联动。
- 当前不做中台真实迁移。
- 当前不改变现有主线行为。
- 当前 `side_effects_released` 仍强制锁死为 `false`（不允许打开）。

---

## B. 为什么现在要做 minimal real-effect dry-run execution（写死理由）

- `minimal real-effect stub` 已承载未来三类写入接口的占位。
- `minimal real-effect wiring` 已证明**合法入口**成立，但不证明入口上的**执行顺序**可走通。
- 因此需要再一层 **dry-run execution**，验证与 `minimal real-effect plan` 一致的最小顺序与收口在零副作用模式下可调用。
- 当前仍不能放开任何真实副作用。

---

## C. dry-run execution 的最小定义（写死）

`minimal real-effect dry-run execution`：

- 不是真实 real-effect implementation
- 不是真实写入
- 只是「未来真实写入器执行顺序」的干跑执行链
- 只允许调用 `minimal real-effect stub` 的占位接口，不允许真实写入

---

## D. 最小合法输入（写死；只允许标准化对象）

Dry-run execution 只允许消费：

1. `navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_wiring_v0`
   - 必须 `wiring_status == "first_live_minimal_real_effect_wired_ready"`
2. minimal real-effect stub identity / capability
   - 必须在位且仍为 stub / dry-run safe（保守、不可放权、不可真实写入）
3. `execution_state_v0` 在位
4. `result_v0` 在位
5. failure / exception path：**语义上**由 stub 的 failure/exception 占位接口承载，可被干跑链最后一步占位调用闭合

并明确（写死）：

- 缺任一主前提，dry-run execution 不成立。
- 禁止直接读取 `request_* / approved_* / raw metadata` 作为输入来源。

---

## E. 最小结果集合（写死；三态）

Dry-run execution 的结果必须收敛成三态之一：

- `first_live_minimal_real_effect_dry_run_executed`
- `first_live_minimal_real_effect_dry_run_not_ready`
- `first_live_minimal_real_effect_dry_run_blocked`

并明确（写死）：

- `executed` 只表示「未来真实写入器的最小执行链已在零副作用模式下跑通」。
- 不表示真实写入已发生。
- 不表示副作用已发生。

---

## F. 最小执行顺序（写死）

Dry-run execution **成功**时，固定顺序必须是：

1. `execution_state_real_write_placeholder_call`
2. `result_object_real_write_placeholder_call`
3. `failure_or_exception_real_write_placeholder_closure`

并明确（写死）：

- 不允许倒序、不允许跳步。
- 不允许在干跑链中插入 route / voice / memory / migration / rollback / interrupt。

---

## G. 明确禁止（写死）

Dry-run execution 不允许直接：

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

与 minimal real-effect wiring：

- wiring 负责给 real-effect stub 合法入口。
- dry-run execution 负责在合法入口上跑通未来写入顺序。
- `wired_ready` **不等于** `dry_run_executed`。

与 minimal real-effect stub：

- stub 是未来真实写入器壳子。
- dry-run execution 是它的第一条零副作用执行链。
- 两者不能混用职责（wiring 不跑链、干跑不负责再证明入口）。

与 minimal real-effect plan：

- plan 规定未来真实写入如何最小落地。
- dry-run execution 只验证顺序与调用边界可走通。
- 当前仍不执行真实 plan。

---

## I. 当前仍然不能做什么（写死）

- 不允许把 `side_effects_released` 打开
- 不允许真实 `release_control`
- 不允许真实 `rollback` / `interrupt`
- 不允许 route / voice / memory / migration
- 不允许把 `executed` 当作真实写入已开始

---

## J. 当前不做（写死）

- 不做真实 real-effect implementation
- 不做地图接入
- 不做语音/记忆联动
- 不做中台真实迁移

---

## K. 下一步边界（写死）

- 本轮之后，下一步才考虑：first live guarded implementation minimal real-effect implementation（真实受控写入，若单独开段）。
- 当前不直接落真实实现。
