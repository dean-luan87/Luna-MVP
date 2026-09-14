# LUNA YOLO Stage-1 Static Config Test Matrix v0

**Phase**：Phase-Mainline-GuardedTrial-003  
**验证入口**：`tools/verify_yolo_stage1_static_config_v0.py`

---

## 1. Verifier（A–P）

| ID | 内容 |
|----|------|
| A | 预期输出文件存在 |
| B–G | 各 matrix/schema/runbook JSON 存在 |
| H–J | detector/camera/stream 否定 |
| K–M | downstream / navigation / world_write 否定 |
| N | trace/replay/whitebox 非空 |
| O | 当前 env 下 OCR/Qwen entry 未 active |
| P | verdict 标明 real_yolo_execution=NO_GO |

---

## 2. 静态结果层级

见 `yolo_stage1_static_config_summary.json`：`static_validation_result` 可为 **GO** / **CONDITIONAL_GO** / **NO_GO**（权重文件缺失常为 **CONDITIONAL_GO**）。
