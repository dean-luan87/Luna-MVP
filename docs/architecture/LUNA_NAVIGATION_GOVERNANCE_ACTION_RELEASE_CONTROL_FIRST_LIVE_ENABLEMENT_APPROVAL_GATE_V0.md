# Luna — Navigation Governance Action Release Control First Live Enablement Approval Gate v0（第一次真实放权试运行：最终批准门冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_ENABLEMENT_APPROVAL_GATE_V0.md`  
**性质**：Phase-Next-81：冻结 `release_control` 第一次真实放权试运行（first live enablement）在 **dry-run ready 之后、真实试运行之前** 的最终批准门（只定义、不落代码、不触发真实动作）

基于（已具备）：
- enablement plan（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_ENABLEMENT_PLAN_V0.md`
- enablement dry-run stub（已落 stub；不放权）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_ENABLEMENT_DRY_RUN_STUB_V0.md`
- live release gate（冻结/最小实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_LIVE_RELEASE_GATE_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_LIVE_RELEASE_GATE_IMPLEMENTATION_V0.md`
- side-effect release contract / gate（冻结/最小实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_SIDE_EFFECT_RELEASE_CONTRACT_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_SIDE_EFFECT_RELEASE_GATE_IMPLEMENTATION_V0.md`
- guarded live stub：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_GUARDED_LIVE_STUB_V0.md`
- minimal live execution definition：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_LIVE_EXECUTION_DEFINITION_V0.md`
- minimal runtime contract / stub：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_RUNTIME_CONTRACT_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_RUNTIME_STUB_V0.md`
- execution state / result（实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_EXECUTION_STATE_IMPLEMENTATION_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_RESULT_OBJECT_IMPLEMENTATION_V0.md`

---

## A. 文档定位（写死）

- 这是 `release_control` 第一次真实放权试运行（first live enablement）的**最终批准门**设计文档。
- 当前目标：冻结“从 dry-run candidate / dry-run ready 到真实第一次放权试运行”的最终批准边界（可冻结、可回归）。
- 当前不做真实 `release_control`。
- 当前不做 `rollback` / `interrupt`。
- 当前不做地图接入。
- 当前不做语音/记忆联动。
- 当前不触发中台真实迁移。
- 当前不改变现有主线行为（不改 route/proposal）。

---

## B. 为什么现在必须先定义 approval gate

- 当前已具备 enablement plan（规则已冻结）。
- 当前已具备 enablement dry-run stub（流程可演练但不放权）。
- 当前已具备 live release gate 与 side-effect release gate（资格判定链已在位）。
- 但仍缺少一个明确的“**谁来最终批准第一次真实放权试运行**”的门控边界。
- 如果不先定义 approval gate，后续容易把 `dry_run_ready` 或 `side_effect_release_ready` **误当成**可直接进入真实放权试运行。
- 因此必须先冻结最终批准门，再考虑是否进入第一版真实 live implementation。

---

## C. approval gate 的最小定义（写死）

`release_control first live enablement approval gate` 是：

- `first live enablement dry-run` 之后、真实第一次放权试运行之前的**最终批准门**
- 只负责判断“是否批准第一次真实放权试运行”

它不是：

- enablement plan 本身
- dry-run stub 本身
- live release gate 本身
- side-effect release gate 本身
- 真实执行器本身
- `rollback` / `interrupt` 审批门

核心定义（写死一句）：

> approval gate 只决定“是否批准第一次真实放权试运行”，不直接执行任何动作，也不直接打开 `side_effects_released`。

---

## D. 最小合法输入（写死只允许消费）

approval gate **只允许消费**以下输入（缺一不可；缺任一则 gate 不成立）：

1) **first live enablement dry-run 结果**
- 必须为 `dry_run_ready` 或等价的“试运行前提演练已通过”状态

2) **`navigation_governance_action_release_control_live_release_gate_v0`**
- 必须 `live_release_status == "live_release_ready"`

3) **`navigation_governance_action_release_control_side_effect_release_gate_v0`**
- 必须 `side_effect_release_status == "side_effect_release_ready"`

4) **guarded live stub 状态**
- 必须已进入 candidate
- 且 `side_effects_released == false`

5) **`navigation_governance_action_release_control_execution_state_v0`**
- 回传面在位

6) **`navigation_governance_action_release_control_result_v0`**
- 回传面在位

7) **明确的批准主体 / 批准信号**
- 必须存在
- 当前只做语义定义，不实现来源机制（不绑定 UI/人审/签名系统）

8) **minimal executor / guarded live stub identity & capability**
- 本体在位与能力边界依据（避免“假对象/假能力”通过）

并写死：

- 缺任一主前提，approval gate 不成立。
- 禁止直接读取 `request_* / approved_* / raw metadata` 作为前提来源（避免绕过标准对象）。

---

## E. 最小结果集合（写死收敛）

approval gate 的结果集合必须收敛为最小集合：

- `first_live_enablement_approved`
- `first_live_enablement_not_approved`
- `first_live_enablement_blocked`

语义（写死）：

1) `first_live_enablement_approved`
- 仅表示：允许进入第一版真实最小放权试运行线
- 不表示动作已执行
- 不表示副作用已发生
- 不表示 `side_effects_released` 已变为 `true`

2) `first_live_enablement_not_approved`
- 当前审批信号缺失或条件未满足
- 不允许进入真实放权试运行

3) `first_live_enablement_blocked`
- 当前存在硬阻断 / 身份问题 / 一致性问题
- 明确不允许进入真实放权试运行

---

## F. 明确禁止（必须写死）

approval gate 不允许直接：

- 打开 `side_effects_released`
- 执行真实 `release_control`
- 改路线
- 触发语音播报
- 写记忆
- 触发中台真实迁移
- 自动触发 `rollback` / `interrupt`
- 越过标准对象吐散字段

---

## G. 与现有链路的关系（写清）

与 first live enablement dry-run stub：
- dry-run stub 负责演练前提、灰度与回退路径
- approval gate 负责最终批准是否进入第一次真实放权试运行
- 两者不能混用

与 live release gate：
- live release gate 决定“是否具备进入真实执行线的资格”
- approval gate 决定“是否批准这次真的进入”
- `live_release_ready != approved`

与 side-effect release gate：
- side-effect release gate 决定“是否具备未来副作用放权资格”
- approval gate 决定“是否批准将这次资格用于第一次真实放权试运行”
- `side_effect_release_ready != approved`

与 runtime contract / live execution definition：
- runtime contract 约束试运行中的执行顺序与禁止面
- live execution definition 规定第一版真实执行边界
- approval gate 只决定这次是否批准进入，不替代运行时合同

---

## H. 当前仍然不能做什么（必须写死）

- 不允许现在就把 `side_effects_released` 打开
- 不允许真实 `release_control`
- 不允许真实 `rollback` / `interrupt`
- 不允许改路线
- 不允许语音/记忆/中台迁移
- 不允许把 `first_live_enablement_approved` 当作副作用已发生

---

## I. 当前不做（必须写死）

- 不做 approval gate 代码实现
- 不做真实 `release_control`
- 不做 `rollback` / `interrupt`
- 不做地图接入
- 不做语音/记忆联动
- 不做中台真实迁移

---

## J. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - first live enablement approval gate 的 minimal implementation
- 再之后才考虑：
  - 第一版真实 live implementation
- 当前不跨这两步

补充链接：
- Phase-Next-82：approval gate minimal implementation v0：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_ENABLEMENT_APPROVAL_GATE_IMPLEMENTATION_V0.md`

---

## K. 未来 approval gate 样例（仅说明，不落代码）

```json
{
  "release_control_first_live_enablement_approval_gate_scope": "navigation_governance_action_release_control_first_live_enablement_approval_gate_v0",
  "approval_status": "first_live_enablement_approved|first_live_enablement_not_approved|first_live_enablement_blocked",
  "side_effects_released": false,
  "reason": "..."
}
```

