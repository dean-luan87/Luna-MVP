# LUNA YOLO Stage-1 10-Frame Approval Test Matrix v0

**Phase**：Phase-Mainline-GuardedTrial-004  
**Verifier**：`tools/verify_yolo_stage1_10_frame_approval_gate_v0.py`

---

## 1. 检查项（A–S）

| ID | 含义 |
|----|------|
| A | 预期文件齐全 |
| B | `static_config_root` 为可读目录 |
| C | `yolo_stage1_weight_snapshot.json` 存在 |
| D | 权重存在则 **sha256** 为 64 hex |
| E–J | 各 snapshot / gate report 存在 |
| K–Q | hard_audit：无 detector/推理/camera/流/下游等 |
| R | **本 phase** 不允许 `ten_frame_dry_run` |
| S | trace/replay/whitebox 非空 |

---

## 2. Approval 结论（语义）

Verifier **GO** 只保证 **闸门产物与非执行不变量**；**`approval_gate_result`** 仍可 **CONDITIONAL_GO**（见 Go/No-Go Pack）。
