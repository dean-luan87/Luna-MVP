# Simulation Lab crash_recovery × PaddleOCR — GO / NO_GO Pack v0

## GO

- contract / command suggestion / merge report / classification / action matrix / boundary / audit 完整
- `child_execution_invoked_by_this_phase=false`
- 未提供 child summary 时：`recovery_status=pending_child_execution`（**不**声称 batch recovery 已完成）
- 提供 child summary 且 merge 通过时：`recovery_status=child_summary_merged`
- verifier **GO**

## CONDITIONAL_GO

- contract 完整但 child summary 缺失且团队希望显式 pending 标签（本实现默认仍 **GO** + pending 状态）

## NO_GO

- 本 phase 自动运行 PaddleOCR heavy；改 routing；缺 contract 字段；输出 OCR accuracy / benchmark claim；写事实层

## 下一 phase

`Phase-PaddleOCR-BatchRecovery-Manual-Execution-001` 或 Poster real OCR gated execution
