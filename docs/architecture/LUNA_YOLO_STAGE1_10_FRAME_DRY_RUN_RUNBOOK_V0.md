# LUNA YOLO Stage-1 10-Frame Dry-Run Runbook v0

**Phase**：Phase-Mainline-GuardedTrial-003  
**声明**：runbook **已生成且不执行**。`execution_allowed_by_this_phase` = **false**。

---

## 1. 目的

在满足 Gate-001 顺序与 Gate-002 precheck 后，为未来 **恰好 10 帧** 的受控本地 trial 列出 **必需 env、校验项、熔断、rollback、期望产物**。本文件为人类可读摘要；冻结 JSON 见工具输出 `yolo_stage1_10_frame_dry_run_runbook.json`。

---

## 2. 关键标记（必须与 JSON 一致）

- `LUNA_ENABLE_YOLO_GUARDED_TRIAL_V1=true`  
- `LUNA_YOLO_TRIAL_MODE=guarded_local`  
- `LUNA_DISABLE_ALL_GUARDED_TRIALS=false`（运行窗口内）  
- `LUNA_YOLO_TRIAL_MAX_FRAMES=10`（与 Controlled Trial Plan 对齐）  

Adapter 侧须 **显式**将 `disable_yolo=False`（与「默认安全第一」分层，不得在本文档或未批准阶段自动写入）。

---

## 3. 期望产物（每 sample 目录）

- `per_sample_yolo_shadow_results.json`  
- `yolo_shadow_trace.jsonl` / `yolo_shadow_replay.jsonl` / `yolo_shadow_whitebox.jsonl`  

并满足 `must_remain_false`：`real_tts_invoked`、`playback_invoked`、`navigation_action`、`world_write_invoked`、`downstream_invocation_count`。
