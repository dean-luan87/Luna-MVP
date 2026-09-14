# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Activation Dry-Run v0（最小非动作实现说明）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_ACTIVATION_DRY_RUN_IMPLEMENTATION_V0.md`  
**性质**：Phase-Next-113：把 activation dry-run 从“设计冻结”推进到“统一对象的最小非动作实现”（可回归、可观察、不可放权）

关联（冻结设计）：
- activation dry-run v0（设计冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_ACTIVATION_DRY_RUN_V0.md`
- activation gate v0（设计冻结/实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_ACTIVATION_GATE_V0.md`
- activation contract v0（规则冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_ACTIVATION_CONTRACT_V0.md`

---

## A. 文档定位（写死）

- 这是 `release_control first live guarded implementation minimal real-effect activation dry-run` 的正式实现版说明。
- 当前目标：把 dry-run 从冻结文档推进到最小非动作实现，首次让系统能结构化产出：
  - `first_live_minimal_real_effect_activation_ready | first_live_minimal_real_effect_activation_not_ready | first_live_minimal_real_effect_activation_blocked`

并且（本轮写死边界）：

- 当前不做真实 `release_control`
- 当前不做真实 `rollback` / `interrupt`
- 当前不做地图接入、不改路线
- 当前不做语音/记忆联动
- 当前不改变现有主线行为
- 当前 `side_effects_released` 必须保持 `false`

---

## B. 为什么现在要先实现 activation dry-run

- activation gate 已存在，activation contract 已存在。
- activation dry-run 的合法输入与结果集合已冻结。
- 若缺少最小实现，后续真实最小写入实现可能把 `activation_admitted` 误当成“已完成最后 activation 级演练”，从而跳过最后的零副作用收口层。

因此必须先把 activation dry-run 对象实现出来，但当前仍不能触发任何真实治理动作。

---

## C. implemented activation dry-run 的最小定义（写死）

implemented activation dry-run：

- 不是真实最小写入实现
- 不是真实 activation 执行器

它是：

- activation gate 之后、真实第一版最小写入实现之前的最后 activation 级零副作用演练层的最小非动作实现版
- 作用是把标准化输入面统一收束成 `activation_ready / activation_not_ready / activation_blocked` 三态对象

---

## D. 当前最小输入依据（写死；只读标准化对象）

实现只消费（只读）：

1) `result.metadata["navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_admission_gate_v0"]`（必须 admitted）
2) `result.metadata["navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_gate_v0"]`（必须 launch_admitted）
3) `result.metadata["navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_pre_commit_dry_run_v0"]`（必须 pre_commit_ready）
4) `result.metadata["navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_commit_gate_v0"]`（必须 commit_admitted）
5) `result.metadata["navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_commit_dry_run_v0"]`（必须 commit_ready）
6) `result.metadata["navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_activation_gate_v0"]`（必须 activation_admitted）
7) `result.metadata["navigation_governance_action_release_control_first_live_enablement_approval_gate_v0"]`
8) `result.metadata["navigation_governance_action_release_control_first_live_launch_dry_run_v0"]`
9) `result.metadata["navigation_governance_action_release_control_live_release_gate_v0"]`
10) `result.metadata["navigation_governance_action_release_control_side_effect_release_gate_v0"]`
11) `result.metadata["navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0"]`
12) `result.metadata["navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_dry_run_execution_v0"]`
13) `result.metadata["navigation_governance_action_release_control_execution_state_v0"]`
14) `result.metadata["navigation_governance_action_release_control_result_v0"]`
15) implementation skeleton identity/capability（只读 `get_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_identity()`）
16) `result.metadata["side_effects_released"]`（若出现 True/异常值 => blocked）

并写死：

- 缺任一主前提，activation dry-run 不成立。
- 禁止直接读取 `request_* / approved_* / raw metadata`。

---

## E. 当前最小输出位（写死）

写入：

- `result.metadata["navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_activation_dry_run_v0"]`

最小结构（写死）：

```json
{
  "release_control_first_live_guarded_implementation_minimal_real_effect_activation_dry_run_attempted": true,
  "release_control_first_live_guarded_implementation_minimal_real_effect_activation_dry_run_scope": "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_activation_dry_run_v0",
  "activation_dry_run_status": "first_live_minimal_real_effect_activation_ready|first_live_minimal_real_effect_activation_not_ready|first_live_minimal_real_effect_activation_blocked",
  "side_effects_released": false,
  "reason": "..."
}
```

---

## F. 当前最小判断规则（写死；偏保守）

1) activation gate 非 admitted  
→ `activation_not_ready`

2) commit gate / commit dry-run / pre-commit 任一未满足  
→ `activation_not_ready`

3) approval / launch / live / side-effect 任一不 ready  
→ `activation_not_ready`

4) dry-effect simulation 非 simulated，或 implementation dry-run execution 非 executed  
→ `activation_not_ready`

5) skeleton identity/capability 不保守，或出现 `side_effects_released != false` 的证据  
→ `activation_blocked`

6) 前提齐备  
→ `activation_ready`

并写死：

- `activation_ready` 不等于真实写入开始。
- 当前即便 `activation_ready`，也不应真的把 `side_effects_released` 改成 `true`。

---

## G. relevant-only 与 dispatcher 聚合写入（实现约束）

- 继续沿用 dispatcher 聚合写入：由 `voice_final_text_dispatcher.py` 读取标准化对象、调用 mid_platform 评估函数、再写回 `result.metadata[...]`。
- relevant-only：当完全无核心输入对象时，不写出 activation dry-run 对象；一旦核心对象在位，则写出 attempted + 三态结果。

