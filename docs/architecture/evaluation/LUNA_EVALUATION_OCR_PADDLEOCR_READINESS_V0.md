# LUNA Evaluation — PaddleOCR Readiness v0（Phase-PaddleOCR-Readiness-001）

## 定位

在 **Evaluation Tools** 范畴内，对 **PaddleOCR（PP-OCRv5 候选）** 做 **依赖 / import / manifest / adapter 合同 / A-B 计划** 的 readiness；**不**替换 RapidOCR，**不**作为主线默认 provider，**不**跑真实 OCR 推理。

## 事实边界

- **RapidOCR** 仍为 OCR 主线 provider；PaddleOCR 为 **中文增强候选**。  
- **不**接 runtime / 白盒 / MidPlatform / SceneDelta / WorldContext。  
- **不**自动改变 OCR routing；**不**执行 provider trial（需单独授权 phase）。

## 工具与产物

- `tools/evaluation/ocr/run_paddleocr_readiness_check_v0.py` → `~/LunaRuntime/logs/evaluation/paddleocr_readiness_001_<UTC>/`  
- `tools/evaluation/ocr/verify_paddleocr_readiness_v0.py`  
- `tools/evaluation/ocr/verify_paddleocr_model_manifest_v0.py`  

策略：**仅 import 探测**，不调用 `PaddleOCR()`，不加载权重推理。
