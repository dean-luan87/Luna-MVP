# LUNA Evaluation — PaddleOCR Manifest v1 GO / NO-GO Pack v0（Phase-PaddleOCR-ManifestV1-Design-001）

## GO

- `configs/models/ocr/paddleocr_current_api_model_manifest_v1.example.json` 存在且含 **必选字段**（见 verifier）。  
- `review_paddleocr_manifest_v1_design_v0.py` 产出 **field matrix / legacy matrix / route matrix / summary / notes**。  
- `verify_paddleocr_manifest_v1_design_v0.py`：**verdict GO**，`blockers` 为空。  
- **design summary** 中 `constraints`：`network_download_invoked`、`paddleocr_constructor_invoked`、`paddleocr_inference_invoked`、`ocr_routing_changed`、`rapidocr_replaced`、`runtime_integration` 等均为 **false**。  
- Example 中：`runtime_default_enabled`、`mainline_provider`、`network_required` 均为 **false**。

## CONDITIONAL_GO

- **`review_verdict: CONDITIONAL_GO`**：`paddleocr` 未安装或无法解析 `PaddleOCR.__init__`，导致「API 映射」行仅部分填充；**仍允许** verifier GO（若结构检查全过），但文档需标注 **待人工对照官方说明**。  
- **`model_root` / `*_model_ref`** 仍为 **PLACEHOLDER**：预期在后续「官方格式确认」phase 替换。

## NO-GO

- 本 phase **下载**模型或 `download_authorized: true` 作为落盘要求。  
- **`PaddleOCR()`** 或 **OCR 推理**。  
- **替换 RapidOCR**、**修改 OCR routing**、**将 PaddleOCR 设为默认 provider**。  
- Verifier 检测到 example **缺字段**、legacy ref **不存在**、或 **constraints** 与只读设计策略不一致。

## 与上下游 phase 关系

- **ModelFormat-001**：输入（A/B/C 结论）。  
- **ManifestV1-Design-001**（本包）：输出 v1 **设计**与矩阵，**不**替代 Weights 工具实现。  
- **后续**：实现 v1 prepare/snapshot、或 controlled trial，须单独开 phase。
