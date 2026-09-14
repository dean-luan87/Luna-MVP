# LUNA YOLO Stage-1 10-Frame Input Video Policy v0

**Phase**：Phase-Mainline-GuardedTrial-005

---

## 1. CLI 参数

必须传入：`--input-video <path>`

实现入口：`validate_yolo_stage1_input_video_for_execution_v0()`（`capabilities/guarded_trial/yolo_stage1_10_frame_executor_v0.py`）。

---

## 2. 硬规则

| 规则 | 说明 |
|------|------|
| 路径非空 | 空路径 → `valid=false` |
| 禁止网络流 | `rtsp://`、`http://`、`https://`、`rtp://` 等 → `stream_scheme_forbidden=true` |
| 禁止摄像头 index | 纯数字且长度 ≤2（如 `0`）→ `camera_like=true` |
| 必须为普通文件 | `Path.resolve()` 后 `is_file()` |
| 扩展名白名单 | **仅** `.mp4`、`.mov`、`.mkv`、`.avi` |
| 占位/文档类扩展名 | `.md`、`.txt`、`.json`、图像类等 → **拒绝**（即使误命名为「视频」） |

不满足上述任一条件：**NO_GO**，**不得**调用 detector。

---

## 3. 与 Phase-004 占位材料的区别

004 可为 gate 登记传入占位路径以满足「文件存在」类检查；**005 执行前必须替换为真实离线容器格式视频**，否则 dry-run 无判别意义。

---

## 4. 采样策略

顺序读取 `cv2.VideoCapture(path)`，最多缓冲 **10** 帧 ndarray；读完或 EOF 即释放 capture，再在内存上对每帧调用 detector（避免 capture 与模型生命周期交错）。
