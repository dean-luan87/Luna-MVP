# LUNA — YOLO × OCR Offline Bridge Future Branches v0

## Not in Bridge-004 (separate phases)

- Bridge evidence expansion
  - 扩大真实 `yolo-root` evidence run 的样本规模，形成更大回归基线
- MidPlatform Text Extraction Bridge Definition
  - 将 raw text candidates 从 offline bridge 进一步接入可控的 MidPlatform extraction
- Scene Information Delta Control
  - 注册 scene delta control 机制，用于未来复用与减少重复处理
- Task-hint Guided OCR
  - 注册基于任务提示的 OCR 触发策略（与 bridge trigger ownership boundary 对齐）
- Runtime readiness
  - 仅当定义允许后，再评估 runtime 接入条件（本阶段不接）
- Complex layout OCR branch
  - 复杂版版面/阅读顺序 OCR 作为独立分支冻结（不在本阶段混入）

