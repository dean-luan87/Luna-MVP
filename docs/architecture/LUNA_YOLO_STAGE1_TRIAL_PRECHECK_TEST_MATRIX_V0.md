# LUNA YOLO Stage-1 Trial Precheck Test Matrix v0

**Phase**：Phase-Mainline-GuardedTrial-002  
**验证入口**：`tools/verify_yolo_stage1_trial_precheck_v0.py`

---

## 1. 自动化检查（摘要）

| ID | 内容 |
|----|------|
| A | 预期输出文件存在 |
| B | precheck result JSON 存在 |
| C | runner skeleton JSON 存在 |
| D | env snapshot 含 global kill 键 |
| E | YOLO entry flag 默认 false |
| F–H | detector/camera 未调用、`would_execute_detector` false |
| I–M | hard_audit 侧效应字段 |
| N | rollback plan 含 `disable_yolo_trial` 与 `commands` |
| O | abort evaluation 存在 |
| P | trace/replay/whitebox jsonl 非空 |
| Q | summary 中 OCR/Qwen entry 非 active |
| R | 无真实 trial 执行、runner 为 skeleton |

---

## 2. 手工项

- 在真实环境运行前复验 `LUNA_DISABLE_ALL_GUARDED_TRIALS` 可达性与操作手册中的 rollback 命令。
