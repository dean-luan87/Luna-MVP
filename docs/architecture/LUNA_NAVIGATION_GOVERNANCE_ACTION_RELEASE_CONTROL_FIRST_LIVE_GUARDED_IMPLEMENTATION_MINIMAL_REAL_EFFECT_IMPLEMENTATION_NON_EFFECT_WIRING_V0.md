# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Implementation Non-Effect Wiring v0（Implementation Skeleton：非副作用接线冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_IMPLEMENTATION_NON_EFFECT_WIRING_V0.md`  
**性质**：Phase-Next-97：冻结 `minimal real-effect implementation skeleton` 至 approval / launch / release / dry-effect / minimal real-effect dry-run execution 的标准化链路 **implementation non-effect wiring**（只接线、不放权；可冻结、可回归）

基于（已具备）：
- implementation definition（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_IMPLEMENTATION_DEFINITION_V0.md`
- implementation skeleton（冻结 + 落代码）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_IMPLEMENTATION_SKELETON_V0.md`
- minimal real-effect stub / non-effect wiring / dry-run execution（已落地）
- dry-effect simulation（已落地）
- gates（最小实现）：approval gate / launch dry-run / live release gate / side-effect release gate
- standard objects：`execution_state_v0` / `result_v0`

---

## A. 文档定位（写死）

这份文档是：

- `release_control first live guarded implementation minimal real-effect implementation skeleton` 的 **non-effect wiring** 设计与落地文档。
- 当前目标：把 implementation skeleton 与 approval / launch / live release / side-effect release / dry-effect simulation / minimal real-effect dry-run execution 链路正式接起来，形成 future real-effect implementation 的 **单一合法接入入口**，但当前仍不产生任何真实写入副作用。

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

- implementation skeleton 已存在，但仍是“孤立骨架”，缺少与 gate/simulation/dry-run 的标准收束入口。
- 如果不做 implementation non-effect wiring，后续真实实现仍可能走向“各模块各读各对象”的直读模式，破坏单入口约束。
- 因此必须先让 implementation skeleton 通过标准化对象接收到唯一合法入口（wired_ready 可被识别/输出）。
- 但当前仍不能放开任何真实副作用。

---

## C. non-effect wiring 的最小定义（写死）

`minimal real-effect implementation non-effect wiring`：

- 不是真实 real-effect implementation 本身
- 不是 approval / launch / release gates 本身
- 不是 dry-effect simulation / minimal real-effect dry-run execution 本身

它只是：

- 把这些门控/模拟/干跑对象的判定结果**收束**到 implementation skeleton 的接线层（recognize-only / observe-only）
- 只负责决定：implementation skeleton 是否已获得 future real-effect implementation 的合法接入入口（wired_ready）

---

## D. 最小合法输入（写死；只允许标准化对象）

Implementation non-effect wiring 只允许消费（只读）：

1) `navigation_governance_action_release_control_first_live_enablement_approval_gate_v0`
   - 必须 `approval_status == "first_live_enablement_approved"`
2) `navigation_governance_action_release_control_first_live_launch_dry_run_v0`
   - 必须 `launch_status == "first_live_launch_dry_run_ready"`
3) `navigation_governance_action_release_control_live_release_gate_v0`
   - 必须 `live_release_status == "live_release_ready"`
4) `navigation_governance_action_release_control_side_effect_release_gate_v0`
   - 必须 `side_effect_release_status == "side_effect_release_ready"`
5) `navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0`
   - 必须 `simulation_status == "first_live_guarded_dry_effect_simulated"`
6) `navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_dry_run_execution_v0`
   - 必须 `execution_status == "first_live_minimal_real_effect_dry_run_executed"`
7) implementation skeleton identity / capability
   - 必须在位且仍为 skeleton / non-effect mode（保守、不可放权、不可真实写入）
8) `execution_state_v0` 与 `result_v0`
   - 必须在位（作为未来真实写入标准对象承载位）

并明确（写死）：

- 缺任一主前提，wiring 不成立。
- 禁止直接读取 `request_* / approved_* / raw metadata` 作为输入来源。

---

## E. 最小结果集合（写死；三态）

Implementation non-effect wiring 的结果必须收敛成三态之一：

- `first_live_minimal_real_effect_implementation_wired_ready`
- `first_live_minimal_real_effect_implementation_wired_not_ready`
- `first_live_minimal_real_effect_implementation_wired_blocked`

并明确（写死）：

- `wired_ready` 只表示「implementation skeleton 已获得未来真实写入的合法接入入口」。
- 不表示真实写入已开始。
- 不表示副作用已发生。

---

## F. 明确禁止（写死）

Implementation non-effect wiring 不允许直接：

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

与 implementation skeleton：

- skeleton 是未来真实写入层壳子（实现承载位）。
- non-effect wiring 是它的合法入口接线层。
- 两者不能混用。

与 approval / launch / release gates / dry-effect simulation / minimal real-effect dry-run execution：

- 各 gate 与 simulation / dry-run 负责各自判定与非动作输出。
- non-effect wiring 负责把这些判定结果收束到 implementation skeleton 的“单一入口对象”。
- gate/simulation/dry-run ready 不等于 wiring ready。

与 implementation definition：

- definition 规定未来真实写入层边界（进入前提/允许面/禁止面/顺序）。
- wiring 只负责让该边界未来拥有合法入口（不放权、不执行）。

---

## H. 当前仍然不能做什么（写死）

- 不允许把 `side_effects_released` 打开。
- 不允许真实 `release_control`。
- 不允许真实 `rollback` / `interrupt`。
- 不允许改路线。
- 不允许语音/记忆/中台迁移。
- 不允许把 `wired_ready` 当作真实写入已开始。

---

## I. 当前不做（写死）

- 不做真实 real-effect implementation。
- 不做地图接入。
- 不做语音/记忆联动。
- 不做中台真实迁移。

---

## J. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - first live guarded implementation minimal real-effect implementation dry-run execution（implementation 侧干跑执行链，若单独开段）
- 当前不直接落真实实现。

