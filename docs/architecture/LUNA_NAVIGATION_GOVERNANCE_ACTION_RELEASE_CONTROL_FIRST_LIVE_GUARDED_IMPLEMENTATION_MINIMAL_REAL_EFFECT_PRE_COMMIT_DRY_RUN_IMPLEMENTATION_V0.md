# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Pre-Commit Dry-Run Minimal Implementation v0（正式实现版说明）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_PRE_COMMIT_DRY_RUN_IMPLEMENTATION_V0.md`  
**性质**：Phase-Next-105：把 pre-commit dry-run 从“设计冻结”推进到“统一对象的最小非动作实现”（可回归、可观察、不可放权）

关联（冻结设计）：
- pre-commit dry-run v0（设计冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_PRE_COMMIT_DRY_RUN_V0.md`

---

## A. 文档定位（写死）

这份文档是：

- `release_control first live guarded implementation minimal real-effect pre-commit dry-run` 的**正式实现版文档**。
- 当前目标：把 dry-run 从冻结文档推进到最小非动作实现，首次让系统能结构化产出：
  - `first_live_minimal_real_effect_pre_commit_ready | first_live_minimal_real_effect_pre_commit_not_ready | first_live_minimal_real_effect_pre_commit_blocked`

并且（本轮写死边界）：

- 当前不做真实 `release_control`。
- 当前不做真实 `rollback` / `interrupt`。
- 当前不做地图接入、不改路线。
- 当前不做语音/记忆联动。
- 当前不触发中台真实迁移。
- 当前不改变现有主线行为。
- 当前 `side_effects_released` 必须保持 `false`。

---

## B. 为什么现在要先实现 pre-commit dry-run（写死理由）

- guarded launch gate implementation 已存在（可结构化产出 `launch_admitted/not_admitted/blocked`）。
- pre-commit dry-run 的合法输入与结果集合已冻结。
- 若缺少最小实现，后续真实最小写入实现仍可能把 `launch_admitted` 误当作“已完成最后预提交检查”。

因此必须先把 pre-commit dry-run 的统一对象实现出来，但当前仍不能触发任何真实治理动作。

---

## C. implemented pre-commit dry-run 的最小定义（写死）

implemented pre-commit dry-run：

- 不是真实最小写入实现
- 不是真实预提交执行器（本轮不做真实写入/真实预提交）

它是：

- guarded launch gate 之后、真实第一版最小写入实现之前的“最后预提交检查层”的最小非动作实现版
- 作用是把标准化输入面统一收束成 `pre_commit_ready / pre_commit_not_ready / pre_commit_blocked` 三态对象

---

## D. 当前最小输入依据（写死；只读标准化对象）

实现只消费（只读）：

1) `result.metadata["navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_admission_gate_v0"]`（必须 admitted）
2) `result.metadata["navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_gate_v0"]`（必须 launch_admitted）
3) `result.metadata["navigation_governance_action_release_control_first_live_enablement_approval_gate_v0"]`
4) `result.metadata["navigation_governance_action_release_control_first_live_launch_dry_run_v0"]`
5) `result.metadata["navigation_governance_action_release_control_live_release_gate_v0"]`
6) `result.metadata["navigation_governance_action_release_control_side_effect_release_gate_v0"]`
7) `result.metadata["navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0"]`
8) `result.metadata["navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_dry_run_execution_v0"]`
9) `result.metadata["navigation_governance_action_release_control_execution_state_v0"]`
10) `result.metadata["navigation_governance_action_release_control_result_v0"]`
11) implementation skeleton identity/capability（只读 `get_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_identity()`）
12) `result.metadata["side_effects_released"]`（若出现 True/异常值 => blocked）

并写死：

- 缺任一主前提，dry-run 不成立。
- 禁止直接读取 `request_* / approved_* / raw metadata`。

---

## E. 当前最小输出位（写死）

写入：

- `result.metadata["navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_pre_commit_dry_run_v0"]`

最小结构（写死）：

```json
{
  "release_control_first_live_guarded_implementation_minimal_real_effect_pre_commit_dry_run_attempted": true,
  "release_control_first_live_guarded_implementation_minimal_real_effect_pre_commit_dry_run_scope": "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_pre_commit_dry_run_v0",
  "pre_commit_status": "first_live_minimal_real_effect_pre_commit_ready|first_live_minimal_real_effect_pre_commit_not_ready|first_live_minimal_real_effect_pre_commit_blocked",
  "side_effects_released": false,
  "reason": "..."
}
```

---

## F. 当前最小判断规则（写死；偏保守）

1) guarded launch gate 非 launch_admitted  
→ `pre_commit_not_ready`

2) approval / launch / live / side-effect 任一不 ready  
→ `pre_commit_not_ready`

3) dry-effect simulation 非 simulated，或 implementation dry-run execution 非 executed  
→ `pre_commit_not_ready`

4) skeleton identity/capability 不保守，或出现 `side_effects_released != false` 的证据  
→ `pre_commit_blocked`

5) 前提齐备  
→ `pre_commit_ready`

并写死：

- `pre_commit_ready` 不等于真实写入开始。
- 当前即便 ready，也不应真的把 `side_effects_released` 改成 `true`。

---

## G. 当前最小语义（写死）

当 pre-commit dry-run 对象被产出时，只表示：

- 系统已能统一判断“是否具备进入真实最小写入实现前的最后预提交条件”
- 上游治理链未来可合法消费该结果

不表示：

- 真实 `release_control` 已执行
- 真实写入已发生
- 控制权已真实交还
- 路线已改变
- 中台已真实迁移
- `side_effects_released` 已打开

---

## H. 当前不允许做什么（写死）

- 不允许把 `side_effects_released` 打开
- 不允许真实 `release_control`
- 不允许真实写入
- 不允许真实 `rollback` / `interrupt`
- 不允许直接改路线
- 不允许直接触发语音播报
- 不允许直接触发中台真实迁移
- 不允许把 `first_live_minimal_real_effect_pre_commit_ready` 当真实写入已发生

