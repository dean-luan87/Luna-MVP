# LUNA YOLO Stage-1 Dependency & Weight Snapshot v0（Phase-Mainline-GuardedTrial-004）

**Phase**：Phase-Mainline-GuardedTrial-004  
**定位**：在 **003 静态材料齐** 的前提下，对 **权重文件（含 sha256）/ Python 依赖 import 状态 / detector 入口 import 状态 / 输入源路径 / env 与 rollback 冻结副本** 做一次 **执行前闸门**，**仍不**跑推理、不开流、不读 camera。

---

## 1. 模块

`capabilities/guarded_trial/yolo_stage1_dependency_snapshot_v0.py`

- `compute_file_sha256_v0`：整文件 SHA-256（不写 torch 模型句柄）。  
- `check_python_import_available_v0`：`importlib.import_module`，仅版本探测。  
- `validate_yolo_weight_snapshot_v0`：`configs/models/yolo/yolo_model_manifest_v0.json` + 解析 `weights_path`。  
- `validate_yolo_input_source_snapshot_v0`：**仅 `Path.is_file()`**，不调用 `VideoCapture`。  
- `run_yolo_stage1_dependency_snapshot_v0`：聚合为 approval gate 载荷。

---

## 2. 与 003 的关系

**003**：材料在仓库/合同层面可追溯。  
**004**：把 **具体权重 hash、依赖 import、可选输入视频路径、runbook 节选** 写成 **可审计快照**；通过后状态可记为 **`ready_for_10_frame_dry_run_review`**（**仍非**执行授权）。
