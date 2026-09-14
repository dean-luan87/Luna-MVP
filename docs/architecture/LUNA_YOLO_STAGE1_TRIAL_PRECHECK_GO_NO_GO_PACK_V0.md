# LUNA YOLO Stage-1 Trial Precheck Go/No-Go Pack v0

**Phase**：Phase-Mainline-GuardedTrial-002

---

## GO

- precheck runner + runner skeleton 落盘；detector/camera **未**调用；hard_audit 全否定侧效应；rollback / abort 结构完整；trace/replay/whitebox 非空；verifier 通过。

---

## CONDITIONAL_GO

- **默认 env** 下 **entry flag false** → `precheck_result=CONDITIONAL_GO`（外壳完整，真实 trial 仍不执行）——属预期。

---

## NO_GO

- detector/camera 任一为 true；下游/导航/世界写入异常；OCR 与 Qwen trial 与 YOLO precheck **并行开启**；路径不可写；缺 rollback/abort；真实 trial 被执行。

---

## 推荐下一阶段

- **Phase-Mainline-GuardedTrial-003**（示例）：在保持默认关闭前提下扩展 **frame/detector 路径配置校验**（仍可不调用真实 detector），或 Stage-1 **controlled local trial** 运行手册（单独 GO）。
