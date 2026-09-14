# LUNA Evaluation — OCR Evidence Contract Alignment GO / NO-GO Pack v0（Phase-OCR-Evidence-Contract-Alignment-001）

## GO

- **Adapter contract = GO**；**unified evidence** 生成成功。  
- **`evidence_items` 非空**、**`text_joined` 非空**、**`source_reference_chain`** 含 adapter / materialize / pinned / raw / normalized 路径。  
- 每条 item 含 **text、source_index、score（可为 null）、polygon（可为 null）、provider、call_method**（与文档一致）。  
- **审计**：`network_request_invoked=false`，**无** routing / RapidOCR / runtime / whitebox / MidPlatform / **world_model / 中台语义写入**。  
- **`alignment_verdict=GO`** 且 **verifier `verdict=GO`**。

## CONDITIONAL_GO

- 部分 **score / polygon** 缺失；或 **reading_order** 仅低置信说明；**无**硬失败；**adapter** 仍为 GO。

## NO_GO

- **Adapter 非 GO**；adapter **normalized** 缺失。  
- **raw 有识别文本但 evidence_items 为空**；**text_joined 丢失**；**source chain 缺失**。  
- **网络请求**、**routing / RapidOCR / 主线集成**、**写入世界模型 / 中台解释**。
