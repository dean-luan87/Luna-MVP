# LUNA YOLO Stage-1 Trial Runner Skeleton v0（Phase-Mainline-GuardedTrial-002）

**Phase**：Phase-Mainline-GuardedTrial-002  
**模块**：`capabilities/guarded_trial/yolo_stage1_trial_runner_skeleton_v0.py`

---

## 1. 行为

- `runner_mode`: **`skeleton_only`**  
- `detector_execution_enabled`: **`false`**  
- `camera_execution_enabled`: **`false`**  
- `execution_result`: **`not_executed_skeleton_only`**  
- `max_frames_planned`: 默认 **10**（与 Phase-001 dry-run 窗口对齐占位）

---

## 2. 边界

本 phase **不**接入真实 detector runtime；后续 phase 可在同一 runner_id/trial_id 合同下替换实现，且仍需 gate/TRW 门禁。
