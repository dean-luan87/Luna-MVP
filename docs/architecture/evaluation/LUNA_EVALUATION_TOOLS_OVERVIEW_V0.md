# LUNA Evaluation Tools — Overview v0 (Phase-EvaluationTools-Foundation-001)

## Purpose

Evaluation Tools / Test Harness 是 **离线测评与验收基础设施**，用于后续：

- OCR provider 升级验证与回归验收
- 多 provider 横向对照（RapidOCR / PaddleOCR / CnOCR / future）
- 数据集质量门控（synthetic / real-world / human review）
- 单模块深测（batch / stress / long-run）
- 全链路抗压前的数据质量评估与失败样本归档

## Non-goals

- 不属于 Luna runtime 主线
- 不属于 whitebox
- 不作为自动化线上决策引擎，不得自动改变主线 provider 选择

## Core artifacts

- dataset manifests + ground truth
- evaluation reports（统一 schema）
- failure case bundles（可回放/可人工复核）
- human review packages（contact sheet + annotations template）

## Boundaries (must hold)

参见：`docs/architecture/evaluation/LUNA_EVALUATION_TOOLS_BOUNDARY_CONTRACT_V0.md`

