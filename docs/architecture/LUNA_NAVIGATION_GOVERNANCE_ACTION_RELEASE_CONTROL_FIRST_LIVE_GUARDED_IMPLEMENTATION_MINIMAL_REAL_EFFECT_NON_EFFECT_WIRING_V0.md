# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Non-Effect Wiring v0（Minimal Real-Effect Stub：非副作用接线冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_NON_EFFECT_WIRING_V0.md`  
**性质**：Phase-Next-93：冻结 `minimal real-effect stub` 至 approval / launch / gates / dry-effect simulation 的标准化链路 **non-effect wiring**（只接线、不放权；可冻结、可回归）

基于（已具备）：
- minimal real-effect plan（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_PLAN_V0.md`
- minimal real-effect stub（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_STUB_V0.md`
- dry-effect simulation（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_DRY_EFFECT_SIMULATION_V0.md`
- gates（最小实现）：approval gate / launch dry-run / live release gate / side-effect release gate
- standard objects：`execution_state_v0` / `result_v0`

---

## A. 文档定位（写死）

这份文档是：

- `minimal real-effect stub` 的 **non-effect wiring** 设计与落地文档。
- 当前目标：把 real-effect stub 与 approval / launch / live release / side-effect release / dry-effect simulation 链路正式接起来，形成 future real-write 器的 **单一合法接入入口**，但当前仍不产生任何真实写入副作用。

并且（本轮写死边界）：

- 当前不做真实 `release_control`。
- 当前不做真实 `rollback` / `interrupt`。
- 当前不做地图接入、不改路线。
- 当前不做语音/记忆联动。
- 当前不做中台真实迁移。
- 当前不改变现有主线行为。
- 当前 `side_effects_released` 仍强制锁死为 `false`（不允许打开）。

---

## B. 为什么现在要做 non-effect wiring（写死理由）

- real-effect stub 已独立存在，但仍然是“孤立写入器壳子”，缺少与其它 gate/simulation 对象的标准收束接口。
- 如果不做 non-effect wiring，后续真实写入很可能回到“各模块各读各对象”，破坏单一入口约束。
- 因此必须先做一次 **非副作用接线**，验证：唯一合法入口可以通过标准化 metadata 链路收束到 stub。
- 但当前仍不能放开任何真实写入副作用。

---

## C. non-effect wiring 的最小定义（写死）

`minimal real-effect non-effect wiring`：

- 不是真实 real-effect implementation 本身
- 不是 approval / launch / gates / simulation 本身

它只是：

- 把这些对象的判定结果收束到 minimal real-effect stub 的接线层（recognize-only / observe-only）
- 只负责判定：stub 是否已获得 future real-write 器的合法接入入口（wired_ready）

---

## D. 最小合法输入（写死；只允许标准化对象）

Non-effect wiring 只允许消费：

1. `first_live_enablement_approval_gate_v0`
   - 必须 `approval_status == "first_live_enablement_approved"`
2. `first_live_launch_dry_run_v0`
   - 必须 `launch_status == "first_live_launch_dry_run_ready"`
3. `live_release_gate_v0`
   - 必须 `live_release_status == "live_release_ready"`
4. `side_effect_release_gate_v0`
   - 必须 `side_effect_release_status == "side_effect_release_ready"`
5. `first_live_guarded_implementation_dry_effect_simulation_v0`
   - 必须 `simulation_status == "first_live_guarded_dry_effect_simulated"`
6. minimal real-effect stub identity / capability
   - 必须在位且仍为 stub / non-effect mode（保守能力：不可放权、不可真实写入）
7. `execution_state_v0`、`result_v0` 在位

并明确（写死）：

- 缺任一主前提，wiring 不成立。
- 禁止直接读取 `request_* / approved_* / raw metadata` 作为输入来源。

---

## E. 最小结果集合（写死；三态）

Non-effect wiring 的结果必须收敛成三态之一：

- `first_live_minimal_real_effect_wired_ready`
- `first_live_minimal_real_effect_wired_not_ready`
- `first_live_minimal_real_effect_wired_blocked`

并明确（写死）：

- `wired_ready` 只表示 real-effect stub 已获得 future real-write 的合法接入入口。
- 不表示真实写入已开始。
- 不表示副作用已发生。

---

## F. 明确禁止（写死）

Non-effect wiring 不允许直接：

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

与 real-effect stub：

- stub 是未来真实写入器壳子
- non-effect wiring 是它的合法入口接线层
- 两者不能混用

与 approval / launch / release gates / simulation：

- 各对象负责各自判定
- non-effect wiring 负责把这些判定结果收束到 stub
- gate/simulation ready 不等于 wiring ready

与 minimal real-effect plan：

- plan 规定未来真实副作用如何最小落地
- wiring 只负责让该计划未来拥有合法入口（但不执行计划）

---

## H. 当前仍然不能做什么（写死）

- 不允许把 `side_effects_released` 打开
- 不允许真实 `release_control`
- 不允许真实 `rollback` / `interrupt`
- 不允许改路线
- 不允许语音/记忆/中台迁移
- 不允许把 `wired_ready` 当作真实写入已开始

---

## I. 当前不做（写死）

- 不做真实 real-effect implementation
- 不做地图接入
- 不做语音/记忆联动
- 不做中台真实迁移

---

## J. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - first live guarded implementation minimal real-effect implementation
- 当前不直接落真实实现
