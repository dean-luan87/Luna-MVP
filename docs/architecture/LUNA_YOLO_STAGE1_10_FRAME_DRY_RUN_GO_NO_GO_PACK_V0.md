# LUNA YOLO Stage-1 10-Frame Dry-run Go/No-Go Pack v0

**Phase**：Phase-Mainline-GuardedTrial-005

---

## 1. 推荐字段（`post_trial_recommendation`）

| 值 | 含义 |
|----|------|
| `GO_next_window` | 满 10 帧、schema 全过、无 abort、无不可恢复 detector 错误、侧效应审计干净 |
| `CONDITIONAL_GO_repeat` | 帧数不足 10（短视频）、或存在可恢复的 detector 误差、或需换更好输入再跑 |
| `NO_GO_rollback_and_fix` | abort、schema 失败、非法输入、权重/加载失败、或硬审计发现侧效应 |

逻辑见：`compute_post_trial_recommendation_v0()`。

---

## 2. Phase 级 GO（人工 + verifier）

**GO**（建议进入下一窄窗）需同时满足：

- 真实离线视频通过 §input policy
- `frames_processed == 10`（若业务接受短视频例外则降为 CONDITIONAL）
- `detector_invoked == true`
- `schema_invalid_count == 0`
- `tools/verify_yolo_stage1_10_frame_dry_run_v0.py` 全通过
- `post_trial_recommendation == GO_next_window`

**CONDITIONAL_GO**：短视频或 recoverable detector 噪声；**不得**默认为全量主线放开。

**NO_GO**：任一 hard blocker（见矩阵文档 T-005-03～07 类）。

---

## 3. Hard blockers（摘录）

- 使用摄像头或流式 URL
- `frames_processed > 10`（执行器内 `max_frames=10` 上限）
- `schema_invalid_count > 0`
- `downstream_invocation_count > 0` 或非空 `navigation_action`
- `real_tts_invoked`、`qwen_invoked`、`ocr_invoked`、`world_write_invoked`、`hive_upload_invoked` 任一为 true

---

## 4. 建议下一阶段

005 **GO** 后：在保持「不接 OCR / 不接下游」前提下，规划 **更长离线切片** 或 **Phase-006** 类影子接入评审（本文档不展开具体编号）。
