# LUNA Evaluation — PaddleOCR Current API Cache Policy v0（Phase-PaddleOCR-ManifestV1-Snapshot-001）

## 定位

定义 **manifest v1 / `model_format: paddleocr_current_api`** 路线下，**离线模型缓存** 的探测与 pin 策略边界；**不**规定具体官方目录名（随 PaddleOCR 版本变化），由 **`det_model_ref` / `rec_model_ref` / `cls_model_ref`** 与可选 **`model_root`** 描述。

## 解析顺序（snapshot 工具实现）

对 **相对路径** ref：

1. **`repo-root / ref`**  
2. **`repo-root / model_root / ref`**（当 `model_root` 非占位）  
3. 若提供 **`cache-root`**：`**cache-root / ref**`  
4. 若提供 **`cache-root`** 且 `model_root` 非占位：`**cache-root / <model_root 末级目录名> / ref**`

**绝对路径** ref：仅解析该绝对路径。

首个 **存在** 的路径被选为 **resolved_path**。

## 目录与 sha256

- **文件**：计算该文件 sha256，计入 `sha256_by_file`。  
- **目录**：对目录下文件（`rglob`，默认最多 **512** 个）计算 sha256；超过 cap 记 **`sha256_cap_incomplete`**，`pinning_complete=false`。  
- **空目录**：记 **`empty_directory`**，视为未完成 pin。

## 与 legacy 路线关系

- **Legacy 六文件**仍由 v0 manifests + Weights 工具链管理；**本 snapshot 不替代**该链。  
- v1 example 中 **`legacy_manifest_ref`** 仅作双轨指针；**current API** 路线优先检查 **ref 所指缓存**，不盲跑旧六文件。

## 禁止项

- **不**自动下载或创建「伪成功」缓存。  
- **不** `PaddleOCR()`、**不** OCR 推理。  
- **不**改 OCR routing、**不**将 PaddleOCR 设为默认 provider。
