# Luna — CrossModal Vision OCR TestBoard Expansion v0

**Phase**：`Phase-CrossModal-Vision-OCR-TestBoard-Expansion-001`

## 目的

建立 CrossModal Vision-OCR **TestBoard v0**：10 类场景 registry、fixture manifest、期望行为矩阵、边界矩阵与局部 case 执行（3 个真实 fixture + RapidOCR via bridge）。

## 原则

- TestBoard 为 evaluation-only；不写入事实层；不调用 Scene Delta executor。
- `planned_only` case 不得冒充 `executed`。

## 评测

[LUNA_EVALUATION_CROSS_MODAL_VISION_OCR_TESTBOARD_EXPANSION_V0.md](../evaluation/LUNA_EVALUATION_CROSS_MODAL_VISION_OCR_TESTBOARD_EXPANSION_V0.md)

## 建议下一跳

**Phase-CrossModal-Vision-OCR-TestBoard-Full-Chain-Case-Runner-001**（见 [LUNA_CROSS_MODAL_VISION_OCR_TESTBOARD_FULL_CHAIN_RUNNER_V0.md](./LUNA_CROSS_MODAL_VISION_OCR_TESTBOARD_FULL_CHAIN_RUNNER_V0.md)）：对已执行 3 case 跑 case-level 完整链，仍 no-write。
