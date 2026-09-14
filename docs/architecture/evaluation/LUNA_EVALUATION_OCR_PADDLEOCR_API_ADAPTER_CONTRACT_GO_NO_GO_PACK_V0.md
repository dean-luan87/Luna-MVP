# LUNA Evaluation — PaddleOCR API Adapter Contract GO / NO-GO Pack v0（Phase-PaddleOCR-API-Adapter-Contract-001）

## GO

- **materialize = GO**，**constructor_ok**，**predict 或 ocr fallback 成功**，**raw / normalized 可序列化**。  
- 若 raw 中存在 **`rec_texts` 文本**，则 **normalized `text_items` / `text_joined` 必须非空**（与 verifier 一致）。  
- **审计**：`network_request_invoked=false`，**无** routing / RapidOCR / runtime / whitebox / MidPlatform / **model_cache_modified**。  
- **样本 ≤3**；**`adapter_contract_verdict=GO`** 且 **verifier `verdict=GO`**。

## CONDITIONAL_GO

- **`--constructor-only`** 且 constructor 成功。  
- 或 **adapter_contract_verdict=CONDITIONAL_GO**（例如仅 fallback、或 cls 仍待专向验证），**无** verifier 硬 blockers。

## NO_GO

- **materialize 非 GO**、pinned 不可读、**constructor 失败**。  
- **网络请求**、**模型缓存被改**、**样本 >3**、**routing / RapidOCR / 主线集成标志为真**。  
- **raw 有字但 normalized 空**（verifier blocker）。  
- **adapter 宣称 GO 与 constructor 或规范化矛盾**。
