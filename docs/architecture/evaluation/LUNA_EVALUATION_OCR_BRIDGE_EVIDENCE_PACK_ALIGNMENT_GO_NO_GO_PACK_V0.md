# LUNA Evaluation — OCR Bridge Evidence Pack Alignment GO / NO-GO Pack v0（Phase-OCR-Bridge-Evidence-Pack-Alignment-001）

## GO

- **上游**：`OCR-Evidence-Contract-Alignment-001` 的 **`alignment_verdict == GO`**。  
- **既有 contract**：`LUNA_OCR_EVIDENCE_PACK_CONTRACT_V0.md` 与 **`ocr_evidence_pack_contract_v0.py` 均可找到**（`contract_reference_found=true`）。  
- **unified** 可读；**`evidence_items` 非空**；**`text_joined` 非空**。  
- **bridge candidate** 生成成功；**`eligible_text_evidence` 非空**；由 text 拼接的 bridge **text_joined 非空**。  
- **text / score / polygon / reading_order_index** 在逐项对照中不丢失（`score` 可与 `confidence` 并存；`polygon` / `reading_order_index` 可为扩展字段）。  
- **`paddleocr_source_reference_chain`**（或等价链）含 adapter / materialize / pinned / raw / normalized 路径。  
- **`confidence_summary`** 在 pack 的 **`uncertainty.paddleocr_confidence_summary`**（或等价路径）保留或可验证映射。  
- **审计**：`network_request_invoked=false`，无 routing / RapidOCR 替换 / runtime / whitebox / MidPlatform / **world_model_written** / **midplatform_semantics_written**。  
- **`evaluation_flags`**：`evaluation_only`、`not_runtime_input`、`not_midplatform_input` 均为 **true**。  
- **`bridge_pack_verdict=GO`** 且 **verifier `verdict=GO`**；**`lost_fields` 为空**（骨架顶层键不缺失）。

## CONDITIONAL_GO

- **unified 与 candidate 均生成成功**，但 **Bridge contract 参照缺失其一**（仅文档或仅实现），或 **`missing_contract_reference`**。  
- 存在 **provisional / extension** 字段需后续 contract 版本吸收；**无**硬失败、**无**越界审计。  
- **骨架键缺失已修复说明**但仍有 **schema migration** 跟进项。

## NO_GO

- **上游 alignment 非 GO**；**unified 缺失**；**`evidence_items` 为空**；**`text_joined` 丢失**。  
- **candidate 缺失**；**source chain 关键键缺失**；**逐项丢失 text / polygon / reading_order_index / provider** 且无 migration 说明。  
- **`lost_fields` 非空**（骨架顶层键在 candidate 中缺失）。  
- **审计越界**：网络、routing、RapidOCR 替换、runtime、白盒、MidPlatform、世界模型写入、中台语义、PaddleOCR 调用、OCR 推理。  
- **在找不到既有 Bridge contract 的情况下仍宣称 GO**。
