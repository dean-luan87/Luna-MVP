# Luna — CrossModal Vision OCR TestBoard Full-Chain Runner Update (5 Cases) v0

**Phase**：`Phase-CrossModal-Vision-OCR-TestBoard-Full-Chain-Runner-Update-5Cases-001`

## 目的

将 full-chain case runner 视图从 3 executed 更新为 **5 executed / 5 planned_only**，与 TestBoard + LowQuality/Partial 执行状态对齐。

## 原则

- 视图更新：前 3 case 复用 prior full-chain runner；`LOW_QUALITY_TEXT` / `PARTIAL_TEXT` 自 partial execution 观测构建完整链，**不重新跑 RapidOCR**。
- 不强行解释低质量空文本；不补全残缺文本；全程 `not_fact` / `no_write`。

## 评测

[LUNA_EVALUATION_CROSS_MODAL_VISION_OCR_TESTBOARD_FULL_CHAIN_RUNNER_UPDATE_5CASES_V0.md](../evaluation/LUNA_EVALUATION_CROSS_MODAL_VISION_OCR_TESTBOARD_FULL_CHAIN_RUNNER_UPDATE_5CASES_V0.md)

## 建议下一跳

**Phase-CrossModal-Vision-OCR-TestBoard-Full-Chain-Runner-Update-7Cases-001**（见 [LUNA_CROSS_MODAL_VISION_OCR_TESTBOARD_FULL_CHAIN_RUNNER_UPDATE_7CASES_V0.md](./LUNA_CROSS_MODAL_VISION_OCR_TESTBOARD_FULL_CHAIN_RUNNER_UPDATE_7CASES_V0.md)）已对齐 7 executed case 视图。
