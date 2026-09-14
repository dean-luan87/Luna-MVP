# LUNA Evaluation — PaddleOCR Model Format Route Options v0（Phase-PaddleOCR-ModelFormat-001）

## 机器可读来源

`paddleocr_model_format_route_options.json`（由 `review_paddleocr_model_format_compatibility_v0.py` 生成）。

## 路线 A — 继续旧式 Paddle Inference 六文件

- **含义**：保留当前 `paddleocr_ppocrv5_model_files_manifest_v0.json` 的 **det/rec/cls** 各 `inference.pdmodel` + `inference.pdiparams` 规划。  
- **适用**：能拿到与 **PaddleOCR `det_model_dir` / `rec_model_dir` / `cls_model_dir`** 兼容的旧式推理目录时。  
- **风险**：PP-OCRv5 官方主线包若不再提供该文件名组合，会长期卡在 Weights CONDITIONAL_GO。

## 路线 B — 新版模型目录 / 上游加载方式

- **含义**：以 **当前安装的 `paddleocr` 实际支持的参数与权重布局** 为准，演进 **manifest v1**、prepare/snapshot、adapter。  
- **适用**：确认 v5 以 ONNX、新 Paddle 存储或其它目录结构分发时。  
- **风险**：工具链与 hash pin 策略需重做；evaluation 与主线隔离仍须保持。

## 路线 C — Evaluation 候选降级到 PP-OCRv4 / v3 inference 包

- **含义**：evaluation 侧 Paddle 路径先对齐 **已知提供 .pdmodel/.pdiparams** 的 v4/v3 推理包；主线 RapidOCR 不变。  
- **适用**：需要尽快恢复「可 pin 的 evaluation candidate」而不等待 v5 包装统一。  
- **风险**：能力 headline 不是 PP-OCRv5；后续仍可并行开 v5 格式 phase。

## 建议的下一 phase（概念）

在选定 A/B/C 之一并**人工确认**官方文件树后，再进入 **权重获取 / snapshot GO** 或 **adapter + manifest v1** 的专门 phase；避免在格式未确认前重复空跑 Weights 工具链。
