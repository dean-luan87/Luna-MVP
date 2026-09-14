# LUNA Evaluation — PaddleOCR Model Manifest v0（Readiness）

## 文件

- **规划 manifest（Evaluation readiness）**：`configs/models/ocr/paddleocr_evaluation_readiness_manifest_v0.json`  
- **计划内权重文件清单**：`configs/models/ocr/paddleocr_ppocrv5_model_files_manifest_v0.json`（`sha256` 可为 null，待授权下载/固定后再填）

## 必填字段（readiness）

`provider_id`、`det_model_dir`、`rec_model_dir`、`cls_model_dir`、`model_files_manifest`、`network_required=false`、`runtime_default_enabled=false`、`mainline_provider=false`、`evaluation_candidate=true`。

## 与既有 ModelOCR manifest 的关系

`paddleocr_ppocrv5_model_manifest_v0.json` 仍供 **权重获取 / adapter skeleton** 等路径使用；本 **evaluation_readiness** manifest 专供 **测评 readiness / A-B 规划**，避免混用字段语义。
