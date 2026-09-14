# LUNA YOLO Stage-1 Multi-Window Offline Slice Trial v0

**Phase**：Phase-Mainline-GuardedTrial-006

---

## 1. 范围

在同一 phase 内串行执行 **50 / 100 / 200** 帧离线切片试跑；仅 YOLO detector、仅离线视频；禁止 camera、OCR、MidPlatform、下游、导航、TTS、Qwen、世界模型、蜂巢。

**前置**：Phase-005 十帧 dry-run 目录必须 **GO**（`post_trial_recommendation=GO_next_window` 等），且与本试跑 `--input-video` 解析路径一致。

---

## 2. 编排器与 CLI

| 组件 | 路径 |
|------|------|
| Executor | `capabilities/guarded_trial/yolo_stage1_multi_window_executor_v0.py` |
| Runner | `tools/run_yolo_stage1_multi_window_offline_trial_v0.py` |
| Verifier | `tools/verify_yolo_stage1_multi_window_offline_trial_v0.py` |

```bash
python3 tools/run_yolo_stage1_multi_window_offline_trial_v0.py \
  --baseline-10-root logs/.../yolo_stage1_10_frame_dry_run_execution_005_rerun \
  --input-video /path/to/same_offline.mp4 \
  --windows 50,100,200 \
  --output-root logs/yolo_stage1_multi_window_offline_trial_006_<UTC>
```

---

## 3. 产物

除各 `yolo_stage1_window_<N>_report.json`、汇总与健康 JSON 外，另写 **`yolo_stage1_multi_window_full_result.json`** 供 verifier 复盘门控与 baseline 快照。
