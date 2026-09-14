# LUNA YOLO Stage-1 10-Frame Dry-run Test Matrix v0

**Phase**：Phase-Mainline-GuardedTrial-005

---

## 1. 自动化 verifier 覆盖

脚本：`tools/verify_yolo_stage1_10_frame_dry_run_v0.py`，对一次 **已执行完毕** 的 `output-root` 做静态验收（文件存在、`hard_audit`、帧数、`schema_invalid_count`、TRW 非空等）。

---

## 2. 矩阵（概念用例）

| ID | 输入 | 期望 `frames_processed` | 期望 `detector_invoked` | `schema_invalid_count` | 期望 recommendation |
|----|------|-------------------------|--------------------------|---------------------------|----------------------|
| T-005-01 | 合法 `.mp4`，≥10 帧，权重就绪 | 10 | true | 0 | `GO_next_window` |
| T-005-02 | 合法但 <10 帧 | <10，>0 | true（若可读帧>0） | 0 | `CONDITIONAL_GO_repeat` |
| T-005-03 | README.md | 0 | false | — | `NO_GO_rollback_and_fix` |
| T-005-04 | 摄像头 index `0` | 0 | false | — | `NO_GO_rollback_and_fix` |
| T-005-05 | `http://...` | 0 | false | — | `NO_GO_rollback_and_fix` |
| T-005-06 | 权重文件缺失 | 0（或已缓冲帧但不推理） | false | — | `NO_GO_rollback_and_fix` |
| T-005-07 | detector 连续异常 ≥2 | <=10 | 视中断点 | — | abort + `NO_GO...` |

---

## 3. TRW / RequestTrace（005 最小集）

执行工具至少追加一行 `.jsonl` 到：

- `yolo_stage1_10_frame_trace.jsonl`
- `yolo_stage1_10_frame_replay.jsonl`
- `yolo_stage1_10_frame_whitebox.jsonl`

Whitebox 中登记 shadow stages：`request_trace.stage.perception.yolo.*`。

---

## 4. 下游零调用

验收要求：`hard_audit.downstream_invocation_count == 0`，且导航 / TTS / Qwen / OCR / 世界模型 / 蜂巢等标志位为 false 或 null（与 verifier 一致）。
