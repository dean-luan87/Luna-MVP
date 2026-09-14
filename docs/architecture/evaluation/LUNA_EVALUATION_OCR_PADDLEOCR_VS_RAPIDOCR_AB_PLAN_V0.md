# LUNA Evaluation — PaddleOCR vs RapidOCR A/B Plan v0

## 输入数据集（未来 trial）

- OCR **中文质量门控**集（既有 synthetic / gate 产物路径）。  
- **RealSamples-001** 真实困难样本目录（`ocr_realworld_difficult_v0_*`）。  
- OCR **capability boundary** 数据集（OCR-006 边界测评）。

## 指标（建议）

- CER、中文召回、空串率、乱码率  
- symbol false positive、layout grouping support  
- latency、failure cases、provider resource 备注（CPU/GPU/内存）

## 未来产物（Evaluation Tools only）

- `rapidocr_vs_paddleocr_summary.json`  
- `provider_ab_sample_matrix.json`  
- `provider_strength_weakness_report.json`  
- `provider_routing_recommendation_draft.json`（**仅**人工评审材料，**不**自动写回主线 routing）

## 边界

- A/B **仅**在 Evaluation；**不**替换 RapidOCR；**不**自动切换默认 provider。
