# Phase 归档 — PaddleOCR-Labeled-Set-Evaluation-001（独立结论，不与治理 phase 混写）

## Phase id

**Phase-PaddleOCR-Labeled-Set-Evaluation-001**

## Final phase verdict（冻结）

**CONDITIONAL_GO**

## 结论边界（必须与 OCR-Provider-Runtime-Governance-Standard-001 分开理解）

本 phase 只评价 **受控标注集 + 既有 labeled-set runner/verifier 工具链** 下的 **质量闸门与产物完整性**，**不**等价于 **OCR 多 provider 治理标准** 的 verdict，也 **不** 推翻 **OCR-Provider-Runtime-Governance-Standard-001 = GO**。

## 判 CONDITIONAL_GO 的直接原因

- **工具链未失败**：`run_paddleocr_labeled_set_evaluation_v0.py` / `verify_paddleocr_labeled_set_evaluation_v0.py` 在 **smoke 规模** 上可联验。  
- **全量 20 张正式样本集未完整产出**：在本机全量 manifest 运行时出现 **SIGSEGV / exit 139**，导致 **正式 labeled set 未跑完**，不满足「全样本可审计完成」的严格 GO。  
- **smoke（3 张）manifest**：按闸门设计 **必然** 因 `n<20`、类别覆盖等落入 **CONDITIONAL_GO**（runner / verifier 与文档一致）。

## 可记录状态（审计摘要）

| 项 | 状态 |
|----|------|
| runner 工具链 | **可用** |
| smoke 联验 | **CONDITIONAL_GO**（符合小样本闸门） |
| full 20 张 labeled set | **未完成**（exit 139 / 进程级崩溃） |
| final phase verdict | **CONDITIONAL_GO** |

## 工程含义（非本 phase 修复承诺）

- 在当前 **CPU / 内存** 条件下，PaddleOCR **连续全量** 推理存在 **稳定性风险**；与 benchmark 观测的 **高 RSS（量级约 6.9GB）** 一并考虑时，**后续全量标注集不应无拆批、无进程隔离地直接扩大**。  
- **质量结论（识别好坏）尚未具备「全量 GO」前提**；须先由 **Phase-PaddleOCR-Labeled-Set-Stability-Recovery-001** 收束崩溃与拆批可复现性。

## 关联文档（过程说明，非本归档替代）

- `LUNA_EVALUATION_OCR_PADDLEOCR_LABELED_SET_EVALUATION_V0.md`  
- `LUNA_EVALUATION_OCR_PADDLEOCR_LABELED_SET_EVALUATION_GO_NO_GO_PACK_V0.md`
