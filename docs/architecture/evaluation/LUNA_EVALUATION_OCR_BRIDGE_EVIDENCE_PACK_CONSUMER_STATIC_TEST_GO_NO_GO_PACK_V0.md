# LUNA Evaluation — OCR Bridge Evidence Pack Consumer Static Test GO / NO-GO Pack v0（Phase-OCR-Bridge-Evidence-Pack-Consumer-Static-Test-001）

## GO

- **Bridge alignment**：`bridge_pack_verdict == GO` 且 **alignment verifier `verdict == GO`**。  
- **Candidate** 可读；**`validate_ocr_evidence_pack_v0` 通过**（`validation_passed == true`）。  
- **`eligible_text_evidence` 非空**；**text / confidence** 可访问；**bbox** 为列表或 null/缺失不判类型错（当前实现要求：若存在则须为 list）。  
- **若存在**：**polygon / score / reading_order_index** 必须仍可访问（键在则值可读）。  
- **`uncertainty.paddleocr_confidence_summary`** 在存在 eligible 项时必须为 **object** 且可访问。  
- **`paddleocr_source_reference_chain`** 含 adapter / materialize / pinned / raw / normalized 等关键键。  
- **`evaluation_flags.evaluation_only == true`**（且对象存在）。  
- **Pack `hard_audit`**：runtime / whitebox / MidPlatform / `mainline_routing_changed` / `world_write_invoked` 不得为越界真值。  
- **输入 bridge audit** 与 **本阶段 consumer audit** 均无禁止项为 true。  
- **`consumer_static_verdict == GO`** 且 **consumer verifier `verdict == GO`**。

## CONDITIONAL_GO

- Candidate 可读、eligible 非空、静态遍历无崩溃，但 **`validate_ocr_evidence_pack_v0` 未覆盖的 provisional 字段**仅能 **旁路 dict 读取**（本阶段 summary 的 `soft_warnings` 可记录骨架外顶层键）。  
- 或 **bridge alignment verifier 报告缺失**（本实现按 **NO_GO** 处理；若业务上放宽需单独 phase 约定）。

## NO_GO

- **Bridge alignment 非 GO** 或 **alignment verifier 非 GO**。  
- **Candidate 缺失** / **packs 空** / **eligible 空** / **text 或 confidence 不可访问**。  
- **Validator 失败或异常**；**`paddleocr_confidence_summary` 在 eligible 存在时缺失**。  
- **source chain 关键键缺失**；**provisional 键存在但不可读**；**evaluation_flags 缺失或 `evaluation_only` 非 true**。  
- **任一审计禁止项为 true**（含输入 bridge audit）。  
- **进入 runtime / MidPlatform / 写世界模型 / 中台语义 / 改 routing / 替换 RapidOCR**（本工具不执行；若报告或输入中显式为真则 NO_GO）。
