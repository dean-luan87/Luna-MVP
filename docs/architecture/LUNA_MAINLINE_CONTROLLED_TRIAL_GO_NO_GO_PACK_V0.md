# LUNA Mainline Controlled Trial Plan Go/No-Go Pack v0

**Phase**：Phase-Mainline-GuardedTrial-001

---

## GO

- Trial **顺序**（YOLO→OCR→Qwen Voice）与 **禁止并行**、**单 capability active** 已定义。  
- 三条 trial 的 **范围 / 样本窗口 / 验收 / abort / rollback** 已写入矩阵。  
- Precheck 与 post-report **schema** 完备。  
- Qwen Voice **3C（controlled playback）** 标明 **未来项**，本 phase **不批准**。  
- **未**执行真实 trial；**未**真实调用 Qwen/TTS/playback；verifier 通过。

---

## CONDITIONAL_GO

- 样本量、p95 阈值等可在后续运行前微调；**顺序与安全规则**冻结不变。

---

## NO_GO

- 允许并发 trial、或允许跳过顺序直接从 Voice 开始。  
- 在本 phase **批准**真实 playback 或默认真实 Qwen/TTS。  
- 未定义 rollback / global kill；或本 phase **执行**真实 trial / 下游 / 导航 / 世界模型。

---

## 推荐下一阶段

- **Phase-Mainline-GuardedTrial-002**（示例）：Stage 1 YOLO **dry-run precheck** 运行手册与环境门禁（仍可按默认关闭策略）；或专门 **trial runner** 脚手架（仍 no-op 默认）。
