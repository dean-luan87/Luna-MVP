# Luna — GO/NO_GO: CrossModal Fusion Review Queue v0

**Phase**：`Phase-CrossModal-Vision-OCR-Fusion-Candidate-Review-Queue-001`

## GO

- fusion candidate 进入 review queue；`queue_item_count > 0`；
- 全部 `pending_review` / `not_approved`；无 auto-approve；audit 边界完整。

## CONDITIONAL_GO

- 队列为空但上游 dry-run 合法且记录 `empty_queue_reason`；
- 无越界行为。

## NO_GO

- 自动批准或 `approval_granted=true`；
- 标为 confirmed fact；写 MidPlatform / Scene Delta / WorldModel；
- 调用 AI interpretation / 导航；audit 缺失。
