# Luna Evaluation — OCR Provider Governance Standard GO / NO-GO Pack v0

## GO

- **治理主文档 + 四级拆分文档** 均存在且可读。  
- **`configs/ocr/ocr_provider_runtime_governance_v0.example.json`** 存在且字段满足 verifier 关键闸门（含 **`orchestration_policy`、`ocr_request_contract_v0`、`ocr_dispatch_decision_contract_v0`、`provider_admission_matrix_v0`、`provider_level_response_requirements_v0`、`runtime_selection_policy_v0`** 与扩展 **`forbidden_actions`**）。  
- **README** 已增加 **OCR Provider Runtime Governance Standard-001** 索引。  
- **verifier `verdict = GO`**。

## CONDITIONAL_GO

- 主文档齐全，但 **部分预算数值或 Level 说明** 标为「待后续版本细化」；**大原则**（逐帧禁止、ROI-first、Bridge、禁止直写事实）无冲突。

## NO_GO

- **未禁止默认逐帧 OCR**（配置或文档矛盾）。  
- **未禁止整图实时 OCR 为默认**。  
- **未要求证据必经 Bridge** 或 **允许 provider 直写 MidPlatform/世界模型**。  
- **缺少** ROI / cache / runtime budget / forbidden_actions 任一整块。  
- **缺少** OCR 调度合同块（**OCRRequest / OCRDispatchDecision、orchestration_policy** 等）或主文档未写明 **OCR Orchestrator** 与 **禁止业务直连 provider**。  
- **README 无索引** 或 **将 PaddleOCR（或任一实现）写为默认 runtime provider**。  

**说明**：本 phase 的 GO **仅表示标准文档与静态闸门就绪**，**不代表**任何 OCR 质量或上线许可。
