# LUNA YOLO Stage-1 10-Frame Dry-run Approval Gate v0

**Phase**：Phase-Mainline-GuardedTrial-004

---

## 1. 工具

| 脚本 | 作用 |
|------|------|
| `tools/prepare_yolo_stage1_10_frame_approval_gate_v0.py` | 读 003 的 `static_config_root`，产出 weight/dep/entry/input/env/abort/gate 快照与 TRW 行 |
| `tools/verify_yolo_stage1_10_frame_approval_gate_v0.py` | 校验产物与 hard_audit |

**CLI 示例**：

```bash
python3 tools/prepare_yolo_stage1_10_frame_approval_gate_v0.py \
  --static-config-root logs/yolo_stage1_static_config_validation_003_<UTC> \
  --output-root logs/yolo_stage1_10_frame_approval_gate_004_<UTC> \
  --input-video /path/to/offline_video.mp4
```

`--input-video` 可选；**省略**时 gate 多为 **CONDITIONAL_GO**（需人工补路径）。**禁止**传摄像头 index（如 `0`）。

---

## 2. 闸门输出状态字段

- `yolo_stage1_trial_preparation_status`：`ready_for_10_frame_dry_run_review`  
- `real_yolo_execution` / `ten_frame_dry_run_execution`：**NO_GO**  
- `ten_frame_dry_run_allowed_by_this_phase`：**false**  

**005** 才可进入真正 10-frame dry-run（需单独 phase GO）。

---

## 3. 下一 phase 建议 output 命名

`logs/yolo_stage1_10_frame_dry_run_execution_005_<UTC>/`（本文档与 gate report 一致登记）。
