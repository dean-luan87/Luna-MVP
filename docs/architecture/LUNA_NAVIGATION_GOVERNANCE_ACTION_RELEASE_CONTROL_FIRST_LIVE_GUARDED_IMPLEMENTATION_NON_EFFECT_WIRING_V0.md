# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Non-Effect Wiring v0（第一版真实受控实现：非副作用接线冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_NON_EFFECT_WIRING_V0.md`  
**性质**：Phase-Next-88：冻结 `release_control` 第一版真实 guarded implementation 的 **non-effect wiring**（只接线、不放权；可冻结、可回归）

基于（已具备）：
- definition（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_DEFINITION_V0.md`
- stub（承载位）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_STUB_V0.md`
- admission & acceptance（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_ADMISSION_AND_ACCEPTANCE_V0.md`
- skeleton（冻结 + 骨架代码）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_SKELETON_V0.md`

以及已在 metadata 链路具备的门控/对象面（均为非动作/最小实现或已实现对象）：
- approval gate / launch dry-run / live release gate / side-effect release gate
- runtime contract / runtime stub
- executor input bridge
- execution state / result object / readiness / wiring

---

## A. 文档定位（写死）

这份文档是：

- `release_control first live guarded implementation` 的 **非副作用接线（non-effect wiring）**设计文档。
- 当前目标：把 skeleton 与 approval / launch / gates / contract 链路正式接起来，形成“未来真实实现可接入的唯一合法入口”，但当前仍不进入任何真实治理动作实现。

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

- skeleton 已存在，但仍然是孤立模块。
- 如果没有 non-effect wiring，后续真实实现仍可能回退到“多个对象各读各的”，破坏前面建立的边界（标准对象 / gate / 准入验收）。
- 因此必须先让 skeleton 通过标准化对象接收到 **唯一合法入口**，并把“是否已具备未来可接入入口”的结论收束为一个 wiring 对象。
- 但当前仍不能放开任何真实副作用；wiring 只做 recognize / wire / observe。

---

## C. non-effect wiring 的最小定义（写死）

`non-effect wiring`：

- 不是 guarded implementation 本身
- 不是 approval gate / launch dry-run / release gate 本身
- 不是 runtime contract 本身

它只是：

- 把这些 gate 的判定结果与 skeleton **接起来**的非副作用接线层
- 只负责决定：**skeleton 是否已获得未来真实实现可接入的合法入口**

---

## D. 最小合法输入（写死；只允许消费标准化对象）

Non-effect wiring 只允许消费以下标准化对象（缺任一主前提，wiring 不成立）：

1) `first_live_enablement_approval_gate_v0`
   - 必须 `approval_status == "first_live_enablement_approved"`
2) `first_live_launch_dry_run_v0`
   - 必须 `launch_status == "first_live_launch_dry_run_ready"`
3) `live_release_gate_v0`
   - 必须 `live_release_status == "live_release_ready"`
4) `side_effect_release_gate_v0`
   - 必须 `side_effect_release_status == "side_effect_release_ready"`
5) guarded implementation skeleton identity / capability
   - 必须在位且仍为 skeleton / non-effect mode（保守能力：不可放权、不可执行真实 release_control）
6) `execution_state_v0`、`result_v0`
   - 回传面在位

并明确（写死）：

- 禁止直接读取 `request_* / approved_* / raw metadata` 作为输入来源。

---

## E. 最小结果集合（写死；三态）

Non-effect wiring 的结果必须收敛成三态之一：

- `first_live_guarded_wired_ready`
- `first_live_guarded_wired_not_ready`
- `first_live_guarded_wired_blocked`

并明确（写死）：

- `wired_ready` 只表示 skeleton 已获得未来真实实现的合法接入入口。
- 不表示真实实现已开始。
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

与 skeleton：

- skeleton 是未来真实实现壳子
- non-effect wiring 是 skeleton 的合法入口接线层
- 两者不能混用

与 approval / launch / release gates：

- gate 负责各自的判定
- non-effect wiring 负责把这些判定结果收束到 skeleton
- gate ready 不等于 wiring ready

与 runtime contract：

- runtime contract 约束将来进入真实实现后的行为
- non-effect wiring 只负责接入前的合法入口（不执行合同中的真实副作用）

---

## H. 当前仍然不能做什么（写死）

- 不允许把 `side_effects_released` 打开
- 不允许真实 `release_control`
- 不允许真实 `rollback` / `interrupt`
- 不允许改路线
- 不允许语音/记忆/中台迁移
- 不允许把 `wired_ready` 当作动作已开始

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

