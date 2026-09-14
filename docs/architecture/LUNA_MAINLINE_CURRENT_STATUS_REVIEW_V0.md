# LUNA Mainline — Current Status Review v0 (Phase-Mainline-StatusReview-001)

## 目的

在 **YOLO / OCR / Voice / OCRBridge / Evaluation Tools** 多阶段并行推进后，做一次 **只读状态复盘**，生成 **状态矩阵** 与 **design vs runtime 边界**，避免后续接线时混淆。

## 边界（硬）

- **不**实现新功能、**不**改 runtime、**不**调用 provider、**不**接 MidPlatform / 白盒 / SceneDelta / WorldContext。  
- **不**把 Evaluation Tools 产物误认为主线已接线能力。

## 工具

- `tools/run_mainline_current_status_review_v0.py` — 生成矩阵与 summary（嵌入基线登记 + 锚点文档存在性检查）。  
- `tools/verify_mainline_current_status_review_v0.py` — 验收产物与一致性期望。

## 长期原则（登记）

- MidPlatform **仅**消费 **`OcrEvidencePackV0`**；**禁止** `raw_text_joined` 直通。  
- OCR provider **无事实解释权**；OCRBridge **只做证据封装**；中台 **治理与准入**。
