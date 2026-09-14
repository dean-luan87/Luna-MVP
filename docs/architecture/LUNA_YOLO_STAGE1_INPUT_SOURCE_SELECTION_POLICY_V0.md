# LUNA YOLO Stage-1 Input Source Selection Policy v0

**Phase**：Phase-Mainline-GuardedTrial-004

---

## 1. 优先级（10-frame dry-run）

| 优先级 | 类型 | 说明 |
|--------|------|------|
| 1 | `video_file` | 本地/离线视频路径；**仅此**作为默认合格输入 |
| 2 | `sample_frame` | 由离线视频抽样得到的帧序列（仍源于文件，而非 live camera） |
| 3 | `offline_dataset` | 归档数据路径（由运行手册明确） |

---

## 2. 禁止（本线默认）

- **摄像头 index**（如 `0`、`1`）  
- **实时 camera / webcam 别名**  
- **unknown stream** 未在白盒登记  

若 **唯一** 可选输入为上述类型 → **`approval_gate_result=NO_GO`**。

---

## 3. 工具行为

`validate_yolo_input_source_snapshot_v0` 仅检验路径字符串与 **`Path.is_file()`**；**不开 `VideoCapture`**、不读帧。
