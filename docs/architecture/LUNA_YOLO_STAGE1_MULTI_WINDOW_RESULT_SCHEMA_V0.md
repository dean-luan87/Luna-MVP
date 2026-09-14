# LUNA YOLO Stage-1 Multi-Window Result Schema v0

**Phase**：Phase-Mainline-GuardedTrial-006

---

## 1. 单窗口报告 `yolo_stage1_window_<N>_report.json`

由 `validate_yolo_window_trial_result_v0` 自 Phase-005 原始结果映射，字段包括：

- **`window_frames`**：请求窗宽（50 / 100 / 200）
- **`execution_mode`**：固定 **`offline_slice_trial`**
- **`frames_processed` / `frames_attempted`**、**`detector_invoked`**、**`schema_*`**、**`detector_error_count`**
- **`latency`**：`avg_ms`、`p50_ms`、`p95_ms`、`max_ms`
- **`post_trial_recommendation`**：`GO_next_window` | `CONDITIONAL_GO_repeat` | `NO_GO_rollback_and_fix`
- **`hard_audit`**：与 005 同形（camera、下游、OCR、Qwen、TTS、navigation、world、hive）

未执行的窗（未请求或未跑到）仍可落盘占位：`{"window_frames": N, "executed": false}`。

---

## 2. 汇总 `yolo_stage1_multi_window_summary.json`

由 `build_yolo_multi_window_summary_v0`，含：

- **`windows_requested` / `windows_executed` / `windows_skipped`**
- **`final_window_completed`**、**`stop_reason`**、**`final_recommendation`**
  - 全窗 **`GO_next_window`** → **`GO_next_phase`**
  - 半途 **CONDITIONAL** → **`CONDITIONAL_GO_repeat_last_window`**
  - **NO_GO** / abort / baseline 不满足 → **`NO_GO_rollback_and_fix`**
