# LUNA YOLO Stage-1 Trial Precheck v0（Phase-Mainline-GuardedTrial-002）

**Phase**：Phase-Mainline-GuardedTrial-002  
**范围**：仅 **YOLO Stage-1** 的 **dry-run precheck**——验证试验外壳（路径、单 trial 规则、rollback/abort、TRW dry validation），**不**调用 detector、**不**读摄像头。

---

## 1. 模块

- `capabilities/guarded_trial/yolo_stage1_trial_precheck_v0.py`

依赖：`guarded_trial_gate_v0`、`guarded_trial_trw_validator_v0`、`guarded_trial_abort_rollback_hooks_v0`。

---

## 2. Precheck 结论

- **GO**：路径可写、单 trial 规则满足、TRW 校验通过、rollback/abort 就绪，且 **YOLO entry flag 已开启**（少见，仅用于壳验证）。  
- **CONDITIONAL_GO**：同上，但 **entry flag 默认 false**（预期常态），trial 本身不会执行。  
- **NO_GO**：路径不可写、OCR/Qwen trial flag 同时开启、TRW 无效等。

---

## 3. 工具

`tools/run_yolo_stage1_trial_precheck_v0.py` → `logs/yolo_stage1_trial_precheck_002_<UTC>/`。
