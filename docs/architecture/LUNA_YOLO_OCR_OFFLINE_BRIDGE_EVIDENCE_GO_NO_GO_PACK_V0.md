# LUNA — YOLO × OCR Offline Bridge Evidence Go/No-Go Pack v0

## Phase

- **Phase-ModelOCR-YOLO-Bridge-003** — evidence run 的治理判定口径冻结。

## GO（通过）条件

同时满足：

1) `--yolo-root` 真实证据解析成功
- `yolo_root_parse_report.json` 存在且 `yolo_root_parse_status == ok`。

2) parsed detection 非空
- `parsed_detection_count > 0`。

3) proposal / bridge result 生成
- `ocr_crop_proposals.json` 非空（proposal_generated_count > 0）。
- `per_sample_yolo_ocr_bridge_results.json` 中存在 bridge results（bridge_result_generated_count > 0）。

4) attribution 与 policy 被正确记录
- bridge results 提供 YOLO/ OCR source attribution（来自真实 root）。
- `ocr_source_policy_id` 存在且表明已走 offline source policy。

5) candidate-only / raw-text-only治理 flags
- `candidate_only=true`。
- `semantic_interpretation_enabled=false`。
- `allows_execute_now=false`。
- `real_tts_invoked=false`。

6) trace/replay/whitebox 完整
- 三个 jsonl 均非空。

7) governance leakage=0
- `yolo_ocr_bridge_summary.json.governance.governance_leakage == 0`。

8) verifier 通过
- `tools/verify_yolo_ocr_bridge_evidence_run_v0.py` 结论为 **GO**。

## CONDITIONAL_GO（条件通过）条件

- 真实 root 可读但部分字段缺失，导致只覆盖到部分 frame/detection。
- 仍必须满足：边界与审计字段完整，且 verifier A–Q 通过。

## NO_GO（不通过）条件

任一触发：

- 无法解析真实 `yolo-root`，且无法如实生成 evidence_run（不得伪造）。
- 使用 `sample_matrix.json` 结果伪装成真实 root evidence（verifier 会检查 parse report 声明）。
- attribution 缺失或 offline source policy 未被调用。
- 产生语义/导航建议/进入下游/执行 TTS/触发 runtime（违反冻结约束）。
- trace/replay/whitebox 缺失。
- 修改 `YOLO closed_v0` 或 `OCR closed_v0`。
