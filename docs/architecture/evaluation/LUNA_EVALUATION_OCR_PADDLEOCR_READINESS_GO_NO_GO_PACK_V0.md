# LUNA Evaluation — PaddleOCR Readiness Go/No-Go Pack v0

## GO

- `run_paddleocr_readiness_check_v0.py` 产物齐全；`verify_paddleocr_readiness_v0.py` **GO**。  
- `paddleocr` 包与 `PaddleOCR` **类可 import**；evaluation readiness **manifest 校验 GO**。  
- `runtime_default_enabled=false` 且 `mainline_provider=false`。  
- **无** OCR 推理、无 `PaddleOCR()` 构造、无主线副作用。

## CONDITIONAL_GO

- `paddleocr` **未安装**或 **import 失败**（在 summary / matrix 中已登记）。  
- 权重文件 **未落盘**（`model_files_manifest` 中 `sha256` 仍为 null）。  
- 仍可 **GO（流程）**：readiness 工具与文档、manifest 规划完成。

## NO_GO

- readiness 工具执行了 **PaddleOCR 推理** 或 **`PaddleOCR()` 权重加载 trial**。  
- 将 PaddleOCR 设为 **默认 / 主线** provider 或 **替换** RapidOCR。  
- 接入 runtime / 白盒 / MidPlatform 或 **自动**改 OCR routing。
