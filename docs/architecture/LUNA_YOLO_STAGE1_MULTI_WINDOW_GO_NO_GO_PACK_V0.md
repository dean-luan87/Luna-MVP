# LUNA YOLO Stage-1 Multi-Window Go/No-Go Pack v0

**Phase**：Phase-Mainline-GuardedTrial-006

---

## 1. 单窗 GO（与 005 一致尺度）

当前窗 **`frames_processed == window_frames`**、**detector_invoked**、**`schema_invalid_count=0`**、**`detector_error_count=0`**、abort 假、 **`post_trial_recommendation=GO_next_window`**、hard_audit 无副作用。

---

## 2. 单窗 CONDITIONAL / NO_GO

- **CONDITIONAL**：短视频 EOF、部分帧、`detector_error_count>0` 等（继承 005 判决）
- **NO_GO**：abort、schema 失效、权重/ detector 不可用、推断 **`frames_processed > window_frames`**（安全违规）

CONDITIONAL：**不得**在同一 phase 自动进入更大窗口。

---

## 3. Phase 级结论（`final_recommendation`）

| 取值 | 条件 |
|------|------|
| **GO_next_phase** | **全部请求窗**均 `GO_next_window`，且无 stop / 无副作用 |
| **CONDITIONAL_GO_repeat_last_window** | 任一窗 **CONDITIONAL** 导致序列停止 |
| **NO_GO_rollback_and_fix** | 任一窗 **NO_GO**、baseline 失败、输入门控失败、abort |

---

## 4. Runner 退出码

- **`0`**：仅当 **`final_recommendation == GO_next_phase`**
- **`3`**：其他（含 CONDITIONAL / NO_GO）；便于 CI 区分「全窗通过」

---

## 5. 建议下一阶段

在多窗 **GO_next_phase** 且人工复核latency/稳定性后，再规划 **更长离线切片或非 YOLO 能力**（本 phase 不涉及 OCR）。
