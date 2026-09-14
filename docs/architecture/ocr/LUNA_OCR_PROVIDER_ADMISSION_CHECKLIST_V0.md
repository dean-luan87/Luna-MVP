# Luna OCR Provider Admission Checklist v0

用于 **任意 OCR provider**（含 RapidOCR、PaddleOCR、云端、VLM、设备内置）准入评审的 **静态检查清单**。不涉及运行 OCR。

## 0. OCR Orchestrator 与调用链

- [ ] 已明确 **业务模块仅提交 OCRRequest**，**禁止** `business module → provider` 直连  
- [ ] 已明确 **唯一调度入口** 为 **OCR Orchestrator / OCR Runtime Controller**（与 `orchestration_policy` 对齐）  
- [ ] 调度产物为 **OCRDispatchDecision / OCRExecutionPlan**，非裸 provider 名字符串  

## A. 分级与定位

- [ ] 明确 Level 0–3 中 **默认运行层级** 与 **升级条件**  
- [ ] 声明 **非** 默认逐帧、**非** 默认同帧整图实时路径  

## B. 触发与 ROI

- [ ] Trigger Gate 输入/输出字段定义或与标准对齐  
- [ ] ROI 来源、配额、`min_roi_confidence` 策略文档化  

## C. 预算与降级

- [ ] `expected_latency_ms`、`memory_budget_mb`、`max_frequency` 等已声明  
- [ ] CPU/内存/电量降级路径与 **Level 3 最先关闭** 已写明  

## D. 证据与 Bridge

- [ ] 输出形态符合 **OCR evidence / OcrEvidencePack** 合同路径  
- [ ] **禁止**直写 MidPlatform / 世界模型；**禁止**绕过 Bridge  

## E. 评测与主线

- [ ] evaluation / shadow 与 **runtime routing** 隔离说明  
- [ ] 未将 **benchmark GO** 等同于 **上线许可**  

## F. 隐私与网络（Level 3）

- [ ] 数据出境、留存、用户授权与超时策略（若适用）  

## G. Provider Admission Matrix（矩阵行）

准入材料中含 **一行可审计矩阵**，字段与 `provider_admission_matrix_v0.required_declarations_per_provider` 对齐：`provider_name`、`provider_level`、`supported_input_type`、`supported_output_depth`、`latency_class`、`memory_class`、`offline_capability`、`remote_dependency`、`privacy_risk`、`fallback_policy`、`evidence_contract_supported`、`bridge_pack_supported`。  
