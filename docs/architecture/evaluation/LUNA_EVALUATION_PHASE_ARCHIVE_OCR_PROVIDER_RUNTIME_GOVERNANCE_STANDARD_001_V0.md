# Phase 归档 — OCR-Provider-Runtime-Governance-Standard-001（独立结论，不与 PaddleOCR labeled-set 混写）

## Phase id

**Phase-OCR-Provider-Runtime-Governance-Standard-001**  
（文档副标题：**Multi-OCR Provider Dispatch & Runtime Governance Standard v0**）

## Final phase verdict（冻结）

**GO**

## 结论边界（必须与 PaddleOCR-Labeled-Set-Evaluation-001 分开理解）

本 phase **只做** 规范、合同样例、静态 schema 与 **静态 verifier**；**不** 运行 OCR、**不** 接主线、**不** 改 routing、**不** 替换 RapidOCR、**不** 进入 MidPlatform。  
**GO 表示治理与合同闸门在仓库内就绪**，**不** 表示任一 OCR（含 PaddleOCR）在全量样本上的 **质量 GO** 或 **稳定性 GO**。

## 有效 verifier 输出目录（示例）

由本地执行时指定，例如：

`/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/ocr_provider_governance_standard_v0`

（以 `verify_ocr_provider_runtime_governance_standard_v0.py` 的 `--output-root` 为准。）

## 核心结论（产品化表述，可引用）

1. **OCR 不由业务模块直接调用**；须通过 **OCRRequest** 进入 **OCR Orchestrator / OCR Runtime Controller**。  
2. **OCR Orchestrator** 依据任务、场景、ROI、缓存、隐私、资源、时效、置信度等生成 **OCRDispatchDecision / OCRExecutionPlan**。  
3. **不同 OCR Level** 对应不同 **证据深度**；**所有 provider 输出均为 evidence，不是 fact**。  
4. **所有 OCR evidence 必须经过 OCR Bridge**（统一合同路径）。  
5. **Provider 不得直写 MidPlatform / WorldModel**；**Evaluation provider 不得直接进入 production route**。  
6. **PaddleOCR** 定位为 **Level 2 Heavy Local OCR 候选**，**不是** 默认 runtime provider。  
7. **RapidOCR** 可作为 **Level 1 Light Local OCR 候选**。  
8. **Remote / VLM OCR** 属 **Level 3**，受 **隐私、网络、成本** 约束。

## 与 PaddleOCR labeled-set 的关系（一句话）

**治理标准已 GO**；**PaddleOCR 全量标注集质量评估尚未 GO**（见 **Labeled-Set-Evaluation-001 = CONDITIONAL_GO** 独立归档）。应先 **稳定性收束**，再谈全量质量结论。

## 关联文档

- `docs/architecture/ocr/LUNA_OCR_PROVIDER_RUNTIME_GOVERNANCE_STANDARD_V0.md`  
- `docs/architecture/evaluation/LUNA_EVALUATION_OCR_PROVIDER_GOVERNANCE_STANDARD_V0.md`  
- `configs/ocr/ocr_provider_runtime_governance_v0.example.json`
