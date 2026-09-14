# MobileSAM → OCR Controlled Execution Governance Standard V1

**Standard ID:** `MobileSamOcrControlledExecutionGovernanceStandardV1`  
**Phase:** `Phase-P1-Midplatform-Multi-Model-Interaction-MobileSAM-OCR-Controlled-Execution-Planning-v1-001`

## 目的

规划第一个真实双模型受控执行链路：MobileSAM → Midplatform → OCR。本阶段终点为 **OCR Controlled Execution Candidate**。

## 上游 GO

- MobileSAM Single Model Execution Integration GO  
- Single Model Interaction Validation UI Execution GO  
- MobileSAM → OCR Exploration Smoke GO  

## 冻结链路

见 `mobile_sam_ocr_controlled_execution_plan_v1.md`

## 本阶段允许

- 规划 OCR invocation request / admission / execution candidate schema  
- 规划 OCR result envelope / error candidate / fusion policy  

## 本阶段禁止

- 调用 OCR runner / 生成 OCR result / 写 fact  
- MobileSAM 直调 OCR / bypass midplatform  
- 修改 Visual Expression / MobileSAM 结果  

## OCR 输入原则

接受：「值得做文字观察」  
拒绝：confirmed text / fact label / 路牌断言

## Human Correction

双模型归因分流 — 禁止直接训练、改 mask、用户输入作 OCR truth

## 下一阶段

`Phase-P1-Midplatform-Multi-Model-Interaction-MobileSAM-OCR-Controlled-Execution-UI-Execution-v1-001`
