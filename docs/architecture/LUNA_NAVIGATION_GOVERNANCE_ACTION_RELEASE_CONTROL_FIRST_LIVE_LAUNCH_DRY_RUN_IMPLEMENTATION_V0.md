# Luna — Navigation Governance Action Release Control First Live Launch Dry-Run Minimal Implementation v0（最终发车演练层：最小非动作实现）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_LAUNCH_DRY_RUN_IMPLEMENTATION_V0.md`  
**性质**：Phase-Next-83：把 launch dry-run 从冻结定义推进到“统一对象的最小非动作实现”（只产出三态结果对象；不放权、不触发真实治理动作）

关联：
- launch dry-run（冻结定义）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_LAUNCH_DRY_RUN_V0.md`
- approval gate（最小实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_ENABLEMENT_APPROVAL_GATE_IMPLEMENTATION_V0.md`
- live release gate / side-effect release gate（最小实现）：  
  `docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_LIVE_RELEASE_GATE_IMPLEMENTATION_V0.md`、  
  `docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_SIDE_EFFECT_RELEASE_GATE_IMPLEMENTATION_V0.md`

---

## A. 文档定位（写死）

- 这是 `release_control first live launch dry-run` 的最小非动作实现文档。
- 当前目标：在 approval 已通过之后，产出“发车前最后检查”的统一 dry-run 结果对象。
- 当前不做真实 `release_control` / `rollback` / `interrupt`。
- 当前不打开 `side_effects_released`。
- 当前不接地图、不驱动语音/记忆、不触发中台真实迁移、不改 route/proposal。

---

## B. 为什么现在要先实现 launch dry-run

- 如果从 `first_live_enablement_approved` 直接跳到真实执行，会缺少“发车前最后一次一致性检查”的可回归承载位。
- launch dry-run 的最小实现能验证：
  - 三态结果是否能结构化产出
  - 即便 ready，`side_effects_released` 是否仍锁死为 `false`
  - 该层是否会越权触发执行动作（必须不会）

---

## C. 最小输入（写死）

只允许消费标准化对象（缺任一主前提则 not_ready/blocked；禁止读取 `request_* / approved_* / raw metadata`）：

- `navigation_governance_action_release_control_first_live_enablement_approval_gate_v0`（必须 approved）
- `navigation_governance_action_release_control_live_release_gate_v0`（必须 ready）
- `navigation_governance_action_release_control_side_effect_release_gate_v0`（必须 ready）
- `navigation_governance_action_release_control_guarded_live_stub_v0`（candidate 成立；side_effects_released==false）
- `navigation_governance_action_release_control_execution_state_v0`（在位）
- `navigation_governance_action_release_control_result_v0`（在位）
- `navigation_governance_action_release_control_guarded_live_identity_v0`（保守能力）
- `navigation_governance_action_release_control_minimal_executor_identity_v0`（保守能力）

---

## D. 最小输出（写死）

写入：

- `result.metadata["navigation_governance_action_release_control_first_live_launch_dry_run_v0"]`

最小结构：

```json
{
  "release_control_first_live_launch_dry_run_attempted": true,
  "release_control_first_live_launch_dry_run_scope": "navigation_governance_action_release_control_first_live_launch_dry_run_v0",
  "launch_status": "first_live_launch_dry_run_ready|first_live_launch_dry_run_not_ready|first_live_launch_dry_run_blocked",
  "side_effects_released": false,
  "reason": "..."
}
```

---

## E. 最小判断规则（写死且保守）

- approval gate 非 `first_live_enablement_approved` → `first_live_launch_dry_run_not_ready`
- live/side-effect gate 非 ready → `first_live_launch_dry_run_not_ready`
- guarded candidate 不成立或 `side_effects_released != false` → `first_live_launch_dry_run_blocked`
- identity/capability 不保守 → `first_live_launch_dry_run_blocked`
- execution state / result 缺失 → `first_live_launch_dry_run_not_ready`
- 前提齐备 → `first_live_launch_dry_run_ready`（但仍锁死 `side_effects_released=false`）

