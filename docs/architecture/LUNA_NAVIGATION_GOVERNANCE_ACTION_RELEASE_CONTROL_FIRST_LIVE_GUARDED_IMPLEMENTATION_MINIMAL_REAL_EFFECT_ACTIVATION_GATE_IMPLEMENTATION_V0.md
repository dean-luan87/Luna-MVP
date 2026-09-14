# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Activation Gate v0（最小非动作实现说明）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_ACTIVATION_GATE_IMPLEMENTATION_V0.md`  
**性质**：Phase-Next-111：把 activation gate 从“设计冻结”推进到“统一对象的最小非动作实现”（可回归、可观察、不可放权）

关联（冻结设计）：
- activation gate v0（设计冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_ACTIVATION_GATE_V0.md`
- activation contract v0（规则冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_ACTIVATION_CONTRACT_V0.md`

---

## A. 文档定位（写死）

- 这是 `release_control first live guarded implementation minimal real-effect activation gate` 的正式实现版说明。
- 当前目标：把 gate 从冻结文档推进到最小非动作实现，首次让系统能结构化产出：
  - `first_live_minimal_real_effect_activation_admitted | first_live_minimal_real_effect_activation_not_admitted | first_live_minimal_real_effect_activation_blocked`

并且（本轮写死边界）：

- 当前不做真实 `release_control`
- 当前不做真实 `rollback` / `interrupt`
- 当前不做地图接入、不改路线
- 当前不做语音/记忆联动
- 当前不改变现有主线行为
- 当前 `side_effects_released` 必须保持 `false`

---

## B. 为什么现在要先实现 activation gate

- activation contract 已存在，但它只定义规则，不是判断对象。
- activation gate 的合法输入与结果集合已冻结。
- 若缺少最小实现，后续真实最小写入实现容易把 contract 条件或 “activation_ready” 误当成“已允许进入 side effects 受控激活”，把判断逻辑揉进真实实现而失控。

因此必须先把 activation gate 的统一对象实现出来，但当前仍不能触发任何真实治理动作。

---

## C. implemented activation gate 的最小定义（写死）

implemented activation gate：

- 不是真实最小写入实现
- 不是真实 activation signal 来源机制（本轮不实现来源，只做输入约束）

它是：

- activation contract 之后、未来 side effects 受控激活之前的统一判断门的最小非动作实现版
- 作用是把标准化输入面统一收束成 `activation_admitted / activation_not_admitted / activation_blocked` 三态对象

---

## D. 当前最小输入依据（写死；只读标准化对象）

实现只消费（只读）：

1) `result.metadata["navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_admission_gate_v0"]`（必须 admitted）
2) `result.metadata["navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_gate_v0"]`（必须 launch_admitted）
3) `result.metadata["navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_pre_commit_dry_run_v0"]`（必须 pre_commit_ready）
4) `result.metadata["navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_commit_gate_v0"]`（必须 commit_admitted）
5) `result.metadata["navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_commit_dry_run_v0"]`（必须 commit_ready）
6) `result.metadata["navigation_governance_action_release_control_first_live_enablement_approval_gate_v0"]`
7) `result.metadata["navigation_governance_action_release_control_first_live_launch_dry_run_v0"]`
8) `result.metadata["navigation_governance_action_release_control_live_release_gate_v0"]`
9) `result.metadata["navigation_governance_action_release_control_side_effect_release_gate_v0"]`
10) `result.metadata["navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0"]`
11) `result.metadata["navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_dry_run_execution_v0"]`
12) `result.metadata["navigation_governance_action_release_control_execution_state_v0"]`
13) `result.metadata["navigation_governance_action_release_control_result_v0"]`
14) implementation skeleton identity/capability（只读 `get_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_identity()`）
15) activation signal（语义占位；本轮只做输入约束，不实现来源机制）：
   - `result.metadata["navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_activation_signal_v0"]`
16) `result.metadata["side_effects_released"]`（若出现 True/异常值 => blocked）

并写死：

- 缺任一主前提，activation gate 不成立。
- 禁止直接读取 `request_* / approved_* / raw metadata`。

---

## E. 当前最小输出位（写死）

写入：

- `result.metadata["navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_activation_gate_v0"]`

最小结构（写死）：

```json
{
  "release_control_first_live_guarded_implementation_minimal_real_effect_activation_gate_attempted": true,
  "release_control_first_live_guarded_implementation_minimal_real_effect_activation_gate_scope": "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_activation_gate_v0",
  "activation_admission_status": "first_live_minimal_real_effect_activation_admitted|first_live_minimal_real_effect_activation_not_admitted|first_live_minimal_real_effect_activation_blocked",
  "side_effects_released": false,
  "reason": "..."
}
```

---

## F. 当前最小判断规则（写死；偏保守）

1) commit gate 非 admitted 或 commit dry-run 非 ready  
→ `activation_not_admitted`

2) admission / launch / pre-commit 任一未满足  
→ `activation_not_admitted`

3) approval / launch / live / side-effect 任一不 ready  
→ `activation_not_admitted`

4) dry-effect simulation 非 simulated，或 implementation dry-run execution 非 executed  
→ `activation_not_admitted`

5) skeleton identity/capability 不保守，或出现 `side_effects_released != false` 的证据  
→ `activation_blocked`

6) activation signal 缺失  
→ `activation_not_admitted`

7) 前提齐备 + activation signal 存在  
→ `activation_admitted`

并写死：

- `activation_admitted` 不等于真实写入开始。
- 当前即便 `activation_admitted`，也不应真的把 `side_effects_released` 改成 `true`。

---

## G. relevant-only 与 dispatcher 聚合写入（实现约束）

- 继续沿用 dispatcher 聚合写入：由 `voice_final_text_dispatcher.py` 读取标准化对象、调用 mid_platform 评估函数、再写回 `result.metadata[...]`。
- relevant-only：当完全无核心输入对象时，不写出 activation gate 对象；一旦核心对象在位，则写出 attempted + 三态结果。

