# OCR Runner Sandbox Integration Governance Standard V1

**Standard ID:** `OcrRunnerSandboxIntegrationGovernanceStandardV1`  
**Phase:** `Phase-P1-Midplatform-Multi-Model-Interaction-MobileSAM-OCR-Runner-Sandbox-Integration-Planning-v1-001`

## 目的

规划 OCR Controlled Execution Candidate → OCR Runner Sandbox → OCR Runtime → OCR Result Envelope 的真实执行接入边界。本阶段允许规划未来 `ocr_runner_execution=true`，但不执行 OCR。

## 上游 GO

- MobileSAM Single Model Execution Integration GO  
- MobileSAM → OCR Exploration Smoke GO  
- MobileSAM-OCR Controlled Execution Planning GO  
- MobileSAM-OCR Controlled Execution UI Execution GO  

## 本阶段终点

**OCR Runner Sandbox Integration Plan** — 不是 execution / result / fact

## Sandbox 唯一入口

`ocr_controlled_execution_candidate` — 禁止 UI / MobileSAM result / OCR task / Human Correction 直调

## 输入输出原则

| 层 | 原则 |
|----|------|
| Adapter Input | 受控裁剪 + trace；无 fact text / label |
| Execution Record | completed ≠ fact |
| Result Envelope | text_candidate；needs_fact_admission |
| Error Candidate | not_fact；不污染 Result/Fact Layer |
| Fusion | 晚于 OCR envelope；multimodal_evidence_candidate |

## Human Correction Runtime

「文字读错了」不默认 OCR 错 — 双模型归因分流，禁止用户输入作 ground truth / fact text

## 本阶段禁止

- OCR runner 调用 / 模型执行 / 真实 result 生成  
- fact 写入 / 导航决策  
- Visual Expression 变更 / 主图 OCR box  

## 下一阶段

`Phase-P1-Midplatform-Multi-Model-Interaction-MobileSAM-OCR-Runner-Sandbox-Integration-Execution-v1-001`
