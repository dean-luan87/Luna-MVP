# Luna — GO/NO_GO: CrossModal Vision OCR TestBoard Full-Chain Case Runner v0

**Phase**：`Phase-CrossModal-Vision-OCR-TestBoard-Full-Chain-Case-Runner-001`

## GO

- run plan：`case_count=10`，`selected_case_count=3`，`planned_only_case_count=7`。
- case run matrix 3 行（POSITIVE / EMPTY / MULTI_LINES）；planned-only 7 行且无 `case_run_id`。
- expected vs observed 对齐；risk coverage 与 no-write boundary 全通过；audit 完整。

## CONDITIONAL_GO

- executed case 少于 3 但 registry / planned-only / boundary 完整；无越界。

## NO_GO

- planned_only 被标为 executed；写事实层；真实 executor；自动批准；缺 boundary / audit。
