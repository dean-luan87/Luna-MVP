# Luna — CrossModal Vision OCR TestBoard Full-Chain Case Runner v0

**Phase**：`Phase-CrossModal-Vision-OCR-TestBoard-Full-Chain-Case-Runner-001`

## 目的

基于 TestBoard expansion v0，对 **execution_status=executed** 的 3 个 case 自动生成 case-level 完整链路摘要（Fixture → OCR → Reference → Fusion DryRun → Review Queue → Gate → Executor Trace Stub）。`planned_only` 保持不执行。

## 原则

- Case Runner 为测试编排器，非生产链。
- 仅处理已执行 case；不得将 planned_only 标为 executed。
- 每 case 独立 `case_run_id`；expected vs observed 对照；no-write boundary。
- 禁止自动批准、Scene Delta / WorldModel 写入、导航决策、事实层写入。

## 输入

- TestBoard expansion root（含 registry 与 case execution matrix）
- 可选 chain closure root（lineage 引用）

## 评测

[LUNA_EVALUATION_CROSS_MODAL_VISION_OCR_TESTBOARD_FULL_CHAIN_RUNNER_V0.md](../evaluation/LUNA_EVALUATION_CROSS_MODAL_VISION_OCR_TESTBOARD_FULL_CHAIN_RUNNER_V0.md)

## 建议下一跳

**Phase-CrossModal-Vision-OCR-TestBoard-Full-Chain-Runner-Update-5Cases-001**（见 [LUNA_CROSS_MODAL_VISION_OCR_TESTBOARD_FULL_CHAIN_RUNNER_UPDATE_5CASES_V0.md](./LUNA_CROSS_MODAL_VISION_OCR_TESTBOARD_FULL_CHAIN_RUNNER_UPDATE_5CASES_V0.md)）已将 full-chain 视图对齐至 5 executed case。
