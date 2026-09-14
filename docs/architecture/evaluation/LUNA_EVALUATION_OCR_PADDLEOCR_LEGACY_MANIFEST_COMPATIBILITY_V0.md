# LUNA Evaluation — PaddleOCR Legacy Manifest Compatibility v0（Phase-PaddleOCR-ManifestV1-Design-001）

## Legacy 路线（v0）

| 构件 | 路径 | 作用 |
|------|------|------|
| Readiness manifest | `configs/models/ocr/paddleocr_evaluation_readiness_manifest_v0.json` | `det_model_dir` / `rec_model_dir` / `cls_model_dir` + `model_files_manifest` 指针。 |
| 六文件 manifest | `configs/models/ocr/paddleocr_ppocrv5_model_files_manifest_v0.json` | 期望 **det/rec/cls** 各 `inference.pdmodel` + `inference.pdiparams`。 |
| Adapter contract v0 | `docs/architecture/evaluation/LUNA_EVALUATION_OCR_PADDLEOCR_ADAPTER_CONTRACT_V0.md` | 评测输出形状（设计-only）。 |

## v1 与 legacy 的并存策略

- **不删除** v0 文件；v1 example 通过 **`legacy_manifest_ref`**（及可选 **`legacy_model_files_manifest_ref`**）指向 legacy。  
- **`model_format: paddle_inference_legacy`**：声明本 evaluation 包仍走六文件 + Weights-001/002/003 工具链。  
- **`model_format: paddleocr_current_api`**：声明以当前 PaddleOCR API / 官方缓存布局为主；**hash / snapshot 工具需后续 v1 专用 phase**，本 Design-001 **仅**冻结字段与矩阵。

## 兼容性矩阵（语义）

| 维度 | Legacy v0 | Manifest v1 |
|------|-----------|----------------|
| 权重文件命名 | 强制六文件 inference 命名 | 不强制；由 `model_format` + 官方实际布局决定 |
| 与 `PaddleOCR()` 参数 | 隐含 `*_model_dir` 目录内含 pdmodel | 显式 `*_model_ref` + `model_root`，映射到 `__init__` |
| Weights snapshot | `run_paddleocr_weights_snapshot_v0` 绑定 v0 manifest | v1 需新 snapshot schema（后续 phase） |
| 默认 provider | 必须为 false | 同样必须为 false |

## 迁移提示

在选定 ModelFormat **B**（新格式）后：优先补齐 **v1 字段语义 + adapter v1 设计**，再实现 **v1 prepare/snapshot**；legacy 保留给 **A/C** 与回滚对照。
