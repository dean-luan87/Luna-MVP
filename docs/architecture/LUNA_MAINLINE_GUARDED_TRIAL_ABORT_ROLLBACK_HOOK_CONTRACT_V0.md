# LUNA Guarded Trial Abort / Rollback Hook 合同 v0

**Phase**：Phase-Mainline-RuntimeReadiness-003  
**实现模块**：`capabilities/runtime_readiness/guarded_trial_abort_rollback_hooks_v0.py`

---

## 职责边界

- **仅返回结构化计划**，不修改进程 env、不调用 provider、不执行回滚 I/O。
- 供后续阶段在 **真实 trial orchestrator** 中调用。

---

## evaluate_guarded_trial_abort_conditions_v0

**输入**：`gate_decision`、`trial_capability`、可选 `signals`（如 `detector_exception`、`schema_invalid` 等）。

**输出**：`abort_required`、`abort_reason`、`gate_decision_snapshot`、`trial_capability`。

默认 `signals` 为空时 → `abort_required=false`。

---

## build_guarded_trial_rollback_plan_v0

**输出字段**：

- `rollback_action`: `none` | `disable_trial`（abort 时倾向 disable）  
- `safe_default`: 按 capability 粗粒度占位（yolo→shadow、ocr→not_available、qwen→offline_only）  
- `shadow_evidence_retained`: 默认 true  

生成矩阵见：`mainline_guarded_trial_abort_rollback_hook_matrix.json`。
