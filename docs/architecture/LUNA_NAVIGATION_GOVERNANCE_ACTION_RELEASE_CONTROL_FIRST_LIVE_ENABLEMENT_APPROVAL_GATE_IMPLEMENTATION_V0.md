# Luna — Navigation Governance Action Release Control First Live Enablement Approval Gate Minimal Implementation v0（最终批准门：最小非动作实现）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_ENABLEMENT_APPROVAL_GATE_IMPLEMENTATION_V0.md`  
**性质**：Phase-Next-82：把 approval gate 从冻结文档推进到“统一对象的最小非动作实现”（只产出 gate 结果对象；不放权、不触发真实治理动作）

关联：
- approval gate（冻结定义）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_ENABLEMENT_APPROVAL_GATE_V0.md`
- enablement plan（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_ENABLEMENT_PLAN_V0.md`
- enablement dry-run stub（演练层；不放权）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_ENABLEMENT_DRY_RUN_STUB_V0.md`
- live release gate（最小实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_LIVE_RELEASE_GATE_IMPLEMENTATION_V0.md`
- side-effect release gate（最小实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_SIDE_EFFECT_RELEASE_GATE_IMPLEMENTATION_V0.md`

---

## A. 文档定位（写死）

- 这是 `release_control first live enablement approval gate` 的正式实现版文档。
- 当前目标：把 gate 从冻结文档推进到最小非动作实现，形成一个标准化结果对象。
- 当前不做真实 `release_control`。
- 当前不做 `rollback` / `interrupt`。
- 当前不做地图接入。
- 当前不做语音/记忆联动。
- 当前不改变现有主线行为（不改 route/proposal）。

---

## B. 为什么现在要先实现 approval gate

- enablement dry-run stub 已存在（可演练但不放权）。
- live release gate / side-effect release gate 都已有 implemented object（资格判定链在位）。
- execution state / result object 都已有 implemented object（回传面在位）。
- approval gate 的合法输入与结果集合已冻结（Phase-Next-81）。
- 如果没有最小实现，后续真实 live implementation 仍会把 `dry_run_ready` 或 `side_effect_release_ready` 误当成“已批准”。
- 因此必须先把 approval gate 对象实现出来；但当前仍不能触发任何真实治理动作。

---

## C. implemented approval gate 的最小定义（写死）

- 它不是真实 `release_control` 执行器。
- 不是真实批准链来源机制（不绑定 UI/人审/签名系统）。
- 它是“第一次真实放权试运行之前的最终批准门”的正式实现版。
- 作用：把 dry-run 结果、live release gate、side-effect release gate、guarded candidate、execution state、result object、identity/capability、approval signal 统一收束成一个：
  - `first_live_enablement_approved|first_live_enablement_not_approved|first_live_enablement_blocked`
  的结果对象。

---

## D. 当前最小输入依据（写死：只允许消费标准化对象）

当前只允许消费（缺任一主前提则 gate 不成立；禁止直接读取 `request_* / approved_* / raw metadata`）：

1) first live enablement dry-run 结果（必须 `dry_run_ready` 或等价）  
2) `navigation_governance_action_release_control_live_release_gate_v0`（必须 `live_release_ready`）  
3) `navigation_governance_action_release_control_side_effect_release_gate_v0`（必须 `side_effect_release_ready`）  
4) guarded live stub 状态（candidate 成立且 `side_effects_released == false`）  
5) `navigation_governance_action_release_control_execution_state_v0`（在位）  
6) `navigation_governance_action_release_control_result_v0`（在位）  
7) 明确批准主体 / 批准信号（本轮只做语义占位与输入约束，不实现来源机制）  
8) minimal executor / guarded live stub identity & capability（能力边界依据）  

---

## E. 当前最小输出位（写死）

写入：

- `result.metadata["navigation_governance_action_release_control_first_live_enablement_approval_gate_v0"]`

最小结构（不加时间/空间字段、不膨胀）：

```json
{
  "release_control_first_live_enablement_approval_gate_attempted": true,
  "release_control_first_live_enablement_approval_gate_scope": "navigation_governance_action_release_control_first_live_enablement_approval_gate_v0",
  "approval_status": "first_live_enablement_approved|first_live_enablement_not_approved|first_live_enablement_blocked",
  "side_effects_released": false,
  "reason": "..."
}
```

---

## F. 当前最小判断规则（写死且保守）

- 规则 1：dry-run 不 ready → `first_live_enablement_not_approved`
- 规则 2：live release gate 不 ready 或 side-effect release gate 不 ready → `first_live_enablement_not_approved`
- 规则 3：guarded candidate 不成立或 `side_effects_released != false` → `first_live_enablement_blocked`
- 规则 4：identity / capability 不合法（不保守）→ `first_live_enablement_blocked`
- 规则 5：批准主体/批准信号缺失 → `first_live_enablement_not_approved`
- 规则 6：前提齐备且批准信号存在 → `first_live_enablement_approved`

并写死：

- 当前默认偏保守
- `approved != 动作开始`
- 即便 `approved`，也不应真的把 `side_effects_released` 改成 `true`

---

## G. 当前最小语义（写死）

当 `navigation_governance_action_release_control_first_live_enablement_approval_gate_v0` 被产出时，仅表示：

- 系统已能统一判断“是否批准第一次真实放权试运行”
- 上游治理链未来可合法消费该 gate 结果

不表示：

- 真实 `release_control` 已执行
- side effect 已发生
- 控制权已真实交还
- 路线已改变
- 中台已真实迁移
- `side_effects_released` 已经打开

---

## H. 当前不允许做什么（必须写死）

- 不允许把 `side_effects_released` 打开
- 不允许真实 `release_control`
- 不允许真实 `rollback` / `interrupt`
- 不允许直接改路线
- 不允许直接触发语音播报
- 不允许直接触发中台真实迁移
- 不允许把 `first_live_enablement_approved` 当副作用已发生

下一步（发车演练层）：
- Phase-Next-83：launch dry-run（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_LAUNCH_DRY_RUN_V0.md`
- Phase-Next-83：launch dry-run minimal implementation：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_LAUNCH_DRY_RUN_IMPLEMENTATION_V0.md`

