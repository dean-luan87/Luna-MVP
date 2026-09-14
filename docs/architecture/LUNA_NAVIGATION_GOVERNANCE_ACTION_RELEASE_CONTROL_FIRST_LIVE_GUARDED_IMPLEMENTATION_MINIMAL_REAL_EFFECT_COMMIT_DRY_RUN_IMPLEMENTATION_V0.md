# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Commit Dry-Run v0（最小非动作实现说明）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_COMMIT_DRY_RUN_IMPLEMENTATION_V0.md`  
**性质**：Phase-Next-108：把 commit dry-run 从“设计冻结”推进到“统一对象的最小非动作实现”（可回归、可观察、不可放权）

关联（冻结设计）：
- commit dry-run v0（设计冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_COMMIT_DRY_RUN_V0.md`

---

## 1) 文档定位（写死）

这份文档是：

- `release_control first live guarded implementation minimal real-effect commit dry-run` 的**正式实现版说明**。
- 当前目标：在 `commit_gate == commit_admitted` 之后、进入第一版真实最小写入实现之前，产出一个 **commit 级最后干跑对象**，但仍保持 **全链路非动作**与 **side_effects_released=false**。

硬边界（写死）：

- 不打开 `side_effects_released`
- 不执行真实 `release_control`
- 不执行真实写入
- 不执行真实 `rollback` / `interrupt`
- 不接地图、不引入时间/空间锚点
- 不驱动语音/记忆
- 不触发中台真实迁移
- 不改变现有主线行为

---

## 2) 为什么现在必须先实现 commit dry-run

- commit gate implementation 已存在，系统能得到 `first_live_minimal_real_effect_commit_admitted`。
- 若缺失 commit dry-run，后续链路将从 `commit_admitted` **直接跳到** 真实写入，实现上缺少最后一次“按真实提交顺序预演但不落真实副作用”的统一承载位。
- 因此必须先把 commit dry-run 的统一对象实现出来，形成“最终 commit 放行后但仍不真实写入”的标准化 dry-run 出口。

---

## 3) implemented commit dry-run 的最小定义（写死）

implemented commit dry-run：

- 不是真实最小写入实现
- 不是真实提交器（commit 主体）来源机制

它是：

- commit gate 之后、真实第一版最小写入实现之前的最终 commit 级干跑层的**最小非动作实现**
- 作用是把标准化输入面统一收束成 `commit_ready / commit_not_ready / commit_blocked` 三态对象

---

## 4) 当前最小输入依据（写死；只读标准化对象）

实现只消费（只读）：

1) `result.metadata["navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_commit_gate_v0"]`（必须 commit_admitted）
2) `result.metadata["navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_admission_gate_v0"]`（必须 admitted）
3) `result.metadata["navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_gate_v0"]`（必须 launch_admitted）
4) `result.metadata["navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_pre_commit_dry_run_v0"]`（必须 pre_commit_ready）
5) `result.metadata["navigation_governance_action_release_control_first_live_enablement_approval_gate_v0"]`
6) `result.metadata["navigation_governance_action_release_control_first_live_launch_dry_run_v0"]`
7) `result.metadata["navigation_governance_action_release_control_live_release_gate_v0"]`
8) `result.metadata["navigation_governance_action_release_control_side_effect_release_gate_v0"]`
9) `result.metadata["navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0"]`
10) `result.metadata["navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_dry_run_execution_v0"]`
11) implementation skeleton identity/capability（只读 `get_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_identity()`）
12) `result.metadata["navigation_governance_action_release_control_execution_state_v0"]`
13) `result.metadata["navigation_governance_action_release_control_result_v0"]`
14) `result.metadata["side_effects_released"]`（若出现 True/异常值 => blocked）

并写死：

- 缺任一主前提，dry-run 不成立。
- 禁止直接读取 `request_* / approved_* / raw metadata`。

---

## 5) 当前最小输出位（写死）

写入：

- `result.metadata["navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_commit_dry_run_v0"]`

最小结构（写死）：

```json
{
  "release_control_first_live_guarded_implementation_minimal_real_effect_commit_dry_run_attempted": true,
  "release_control_first_live_guarded_implementation_minimal_real_effect_commit_dry_run_scope": "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_commit_dry_run_v0",
  "commit_dry_run_status": "first_live_minimal_real_effect_commit_ready|first_live_minimal_real_effect_commit_not_ready|first_live_minimal_real_effect_commit_blocked",
  "side_effects_released": false,
  "reason": "..."
}
```

---

## 6) 最小判断规则（写死；偏保守）

- commit gate 非 `commit_admitted` → `commit_not_ready`
- pre-commit 非 `pre_commit_ready` → `commit_not_ready`
- admission / guarded launch gate 任一未通过 → `commit_not_ready`
- approval / launch / live / side-effect 任一不 ready → `commit_not_ready`
- dry-effect simulation 非 simulated 或 implementation dry-run execution 非 executed → `commit_not_ready`
- skeleton identity/capability 不保守，或出现 `side_effects_released != false` 的证据 → `commit_blocked`
- 前提齐备 → `commit_ready`

并写死：

- `commit_ready` 不等于真实写入开始。
- 当前即便 `commit_ready`，也不应真的把 `side_effects_released` 改成 `true`。

---

## 7) relevant-only 与 dispatcher 聚合写入（实现约束）

- 继续沿用 dispatcher 聚合写入：由 `voice_final_text_dispatcher.py` 读取标准化对象、调用 mid_platform 评估函数、再写回 `result.metadata[...]`。
- relevant-only：当完全无核心输入对象时，不写出 commit dry-run 对象；一旦核心对象在位，则写出 attempted + 三态结果。

