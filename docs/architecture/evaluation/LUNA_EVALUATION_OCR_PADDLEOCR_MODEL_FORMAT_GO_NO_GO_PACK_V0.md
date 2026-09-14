# LUNA Evaluation — PaddleOCR Model Format GO / NO-GO Pack v0（Phase-PaddleOCR-ModelFormat-001）

## GO（本 phase 工具链）

- `paddleocr_manifest_format_compatibility_matrix.json` 已生成且含多行有效评审维度。  
- `paddleocr_model_format_route_options.json` 含 **A、B、C** 三条路线。  
- `verify_paddleocr_model_format_review_v0.py` 输出 **`verdict: GO`**，`blockers` 为空。  
- `paddleocr_model_format_review_summary.json` 中 **`constraints`**：`network_download_invoked`、`paddleocr_constructor_invoked`、`paddleocr_inference_invoked`、`ocr_routing_changed`、`runtime_integration` 等均为 **false**（与工具实现一致）。

## CONDITIONAL_GO（评审结论 / 环境）

- **`review_verdict: CONDITIONAL_GO`**：本机未安装 `paddleocr` 或无法解析 `PaddleOCR.__init__` 签名；矩阵与路线仍应落盘，供后续人工对照官方文档与模型包。  
- **人工**：需对照 PaddleOCR / Paddle 官方说明，确认 PP-OCRv5 发布物与 **manifest v0** 是否一致。

## NO-GO（禁止项 / verifier 硬失败）

- **下载模型**（网络拉取权重）作为本 phase 工具的一部分。  
- **`PaddleOCR()` 实例化** 或 **OCR 推理** 被本工具执行。  
- **修改主线 OCR provider routing** 或替换 RapidOCR。  
- verifier 检测到 **缺文件**、**缺 A/B/C**、或 **constraints** 与「只读评审」策略不一致。

## 与 Weights phase 的关系

- **ModelFormat-001** **不替代** Weights-001/002/003；它在权重空跑失败时回答「是否 manifest/格式假设错了」。  
- Weights-003 仍为 **CONDITIONAL_GO** 直至六文件真实落盘且 snapshot/completion **GO**。
