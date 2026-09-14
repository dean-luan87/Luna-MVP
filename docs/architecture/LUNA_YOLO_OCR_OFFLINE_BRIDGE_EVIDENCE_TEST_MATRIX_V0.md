# LUNA — YOLO × OCR Offline Bridge Evidence Test Matrix v0

## Phase

- **Phase-ModelOCR-YOLO-Bridge-003** — evidence run 的验证矩阵冻结。

## Evidence Runs（输入）

- `tools/evaluate_yolo_ocr_offline_bridge_v0.py` 使用 `--yolo-root` 解析真实 YOLO output_root。

## Verifier（验证器）

- `tools/verify_yolo_ocr_bridge_evidence_run_v0.py`（在其内部复用 Bridge-002 的 A–Q verifier）。

## Test Matrix（验收用例）

A. `yolo_root` 可读
- `yolo_root_parse_report.json` 存在。

B. `yolo_root_parse_report.json` 存在且解析状态
- `yolo_root_parse_status` 必须为可读的状态：允许 `ok` / `ok_no_data`。

C. parsed detection 非空
- `parsed_detection_count > 0`。

D. frame refs 可追责
- `parsed_frame_refs` 非空；若根格式不支持，必须如实记录 `unsupported_or_missing_fields`。

E. OCRCropProposal / BridgeResult schema & clamp
- 复用 `tools/verify_yolo_ocr_offline_bridge_v0.py` 的 A–Q 检查（包括 crop clamping / schema / attribution / governance flags）。

F. YOLO source attribution 来自真实 root
- bridge results 中 `source_attribution` 或等价字段必须可追溯。

G. OCR offline source policy 被调用
- bridge results 中 `ocr_source_policy_id` 必须存在且与期望一致。

H. candidate-only / raw-text-only
- `candidate_only=true`。
- `semantic_interpretation_enabled=false`。
- `allows_execute_now=false`。

I. governance leakage=0
- summary 中 `governance_leakage == 0`。

J. trace/replay/whitebox 完整
- `yolo_ocr_bridge_trace.jsonl` / `yolo_ocr_bridge_replay.jsonl` / `yolo_ocr_bridge_whitebox.jsonl` 非空。

K. 禁止 evidence 欺骗（sample_matrix masquerading）
- `yolo_root_parse_report.json` 必须声明 evidence 来自真实 `--yolo-root`，而不是 sample-matrix。

L. 禁止闭环污染
- 不允许修改 `YOLO closed_v0` / `OCR closed_v0`（通过 verifier 的边界检查与禁止 marker 约束兜底）。
