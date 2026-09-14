# LUNA Evaluation — PaddleOCR Candidate Line Pause v0（Phase-PaddleOCR-LinePause-001）

## 目的

在 **不下载、不推理、不改 routing** 的前提下，将 **PaddleOCR 候选线** 当前状态 **冻结为暂停**，并写明 **恢复条件** 与 **下一步允许动作**，避免在权重未齐时误开 **Controlled-Trial**。

## 工具

- `tools/evaluation/ocr/record_paddleocr_line_pause_v0.py` → 写入 `paddleocr_line_pause_summary.json` 等  
- `tools/evaluation/ocr/verify_paddleocr_line_pause_v0.py`

## 恢复条件（摘要）

- 六个计划权重文件落盘 → **`run_paddleocr_weights_snapshot_v0`** `missing_count=0` 且 **`verdict: GO`** → **`verify_paddleocr_weights_snapshot_v0` GO** → pinned manifest 中 **sha256 全非空**，且 **`runtime_default_enabled=false`**、**`mainline_provider=false`**。

## 明确禁止（直至 snapshot GO）

- **Phase-PaddleOCR-Controlled-Trial-001**  
- 使用 Paddle 推理的 **OCR-ProviderAB-001**
