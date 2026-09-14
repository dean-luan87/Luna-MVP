# LUNA Evaluation — OCR Real-World Difficult Samples v0（Phase-EvaluationTools-OCR-RealSamples-001）

## 目的

为 OCR-006 **困难 content_type**（`icon_text_mix`、`multi_panel_layout`、`artistic_text`、`stylized_digits`、`decorative_graphic_non_text` 等）建立 **真实/占位** 样本目录、**manifest**、**annotation 模板** 与 **人工复核包**；提升边界测评可信度，**不**跑 OCR provider。

## 边界

- **不**进入 Luna 主线、白盒、runtime、MidPlatform、SceneDelta、WorldContext。  
- **不**调用 OCR、**不**改 OCR routing、**不**做 Paddle trial。  
- **占位**样本必须 `sample_source=placeholder`，**不得**伪装为真实采集。

## 工具与模块

- `tools/evaluation/ocr/prepare_ocr_realworld_difficult_samples_v0.py`  
- `tools/evaluation/ocr/verify_ocr_realworld_difficult_samples_v0.py`  
- `capabilities/evaluation/ocr/ocr_realworld_sample_registry_v0.py`  
- `capabilities/evaluation/ocr/ocr_realworld_human_review_pack_v0.py`

## 数据集根路径

默认：`~/LunaRuntime/datasets/evaluation/ocr_realworld_difficult_v0_<UTC>/`（可用 `--output-root` 覆盖）。
