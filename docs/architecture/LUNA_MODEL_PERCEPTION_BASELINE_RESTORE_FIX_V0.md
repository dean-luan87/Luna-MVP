# LUNA — ModelPerceptionFix-001: Restore Baseline Perception Eval Root v0

## Phase
- Phase: **Phase-ModelPerceptionFix-001**
- Type: **Fix only (restore baseline eval artifacts)**

## Problem
ModelPerception-003 comparison recorded blocker:
- `baseline_root_not_found_or_not_dir`

This prevented a real baseline vs YOLO shadow delta comparison, and therefore must be fixed before any YOLO enabled smoke run.

## Hard boundaries (confirmed)
- 不进入 YOLO enabled smoke。
- 不调用真实 YOLO（本阶段目标是 baseline restore）。
- 不扩 Option A。
- 不进入 controlled_live_stream / full controlled trial。
- 不执行导航动作、不真实播报。
- 不伪造 baseline 文件或手工补目录。

## What we did (evidence-based)
### 1) Confirm baseline root is missing
Checked:
- `logs/perception_eval_option_a_phone_local_001_20260427_113330/`
Result:
- directory missing on disk (`No such file or directory`).

### 2) Search for alternative baseline outputs
Searched under workspace for perception eval outputs.
Result:
- no existing baseline root found.

### 3) Re-run official PerceptionEval-001 tool (baseline/mock)
Tool (official):
- `tools/evaluate_option_a_phone_local_perception_v0.py`
Input:
- FieldBatch-002 sample_matrix:
  - `logs/phone_local_field_batch_002_20260427_111431/sample_matrix.json`
Output (new baseline root generated):
- `logs/perception_eval_option_a_phone_local_001_restore_20260427_1446/`
Produced required artifacts:
- `perception_evaluation_summary.json`
- `per_sample_results.json`
- `signal_trace.jsonl`
- `evaluation_notes.md`

## Result
- Baseline perception root restored by **official tool re-run**.
- This baseline remains `perception_runtime_mode=baseline_or_mock` and `not_model_claimed=true` (as expected).

## Next step (hand-off)
Re-run ModelPerception-003 comparison using the restored baseline root.

