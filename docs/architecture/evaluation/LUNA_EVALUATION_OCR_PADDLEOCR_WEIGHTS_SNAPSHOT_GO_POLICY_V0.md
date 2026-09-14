# LUNA Evaluation — PaddleOCR Weights Snapshot GO Policy v0

## Snapshot GO 的必要条件

1. `paddleocr_weights_snapshot_summary.json`：`missing_file_count == 0`，`verdict == GO`，`all_planned_files_exist == true`。  
2. `paddleocr_model_sha256_matrix.json`：凡 `exists==true` 的行 **`sha256` 非空**（64 hex）。  
3. `paddleocr_pinned_model_manifest_candidate.json`：`weights_sha256` 覆盖 **全部** `model_files_manifest` 中的 `relative_path`；**`runtime_default_enabled=false`**、**`mainline_provider=false`**。  
4. `verify_paddleocr_weights_snapshot_v0.py`：**`verdict == GO`**。

## 与 Controlled-Trial 的闸门

仅当 **Weights-003 completion**（`verify_paddleocr_weights_completion_v0.py`）为 **GO** 后，才允许进入 **Phase-PaddleOCR-Controlled-Trial-001**。

## 禁止

- **无 hash pin** 的 provider 进入正式 **RapidOCR vs PaddleOCR A/B**。  
- 将 snapshot 标为 GO 但 **sha256 未写全**（integrity **NO_GO**）。
