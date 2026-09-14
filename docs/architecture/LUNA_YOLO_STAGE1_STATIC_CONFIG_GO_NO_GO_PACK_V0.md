# LUNA YOLO Stage-1 Static Config Go/No-Go Pack v0

**Phase**：Phase-Mainline-GuardedTrial-003

---

## GO

- Shadow adapter **入口**、**video_file** 帧路径合同、manifest/adapter **模型字段**可查。  
- **detection schema** 与 **TRW/output** 合同在代码与 manifest 层成立。  
- **10-frame runbook** 已生成且 `execution_allowed_by_this_phase=false`。  
- **未**推理、未开流、hard_audit 否定侧效应；verifier **GO**。

---

## CONDITIONAL_GO

- **`models/yolo/yolov5n.pt` 缺失**（常见：gitignore）— 运行前运维落盘即可。  
- **Luna_Badge MVP detector** 仅在完整工作区中存在 — Luna-Core-only 检视属预期落差。

---

## NO_GO

- 调用 detector/camera/video stream。  
- schema 合同或 TRW 合同无法在仓库侧解析。  
- 缺 rollback/abort/runbook。

---

## 推荐下一阶段

- **Phase-Mainline-GuardedTrial-004**（示例）：权重落盘与环境变量 **冻结 snapshot**；或 **离线 10-frame** 试运行（单独 GO）。
