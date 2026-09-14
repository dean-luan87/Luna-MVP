# LUNA — YOLO × OCR Evidence Expansion Test Matrix v0

## Phase

- **Phase-ModelOCR-YOLO-Bridge-005** 扩样验收矩阵冻结。

## Verifier

- `tools/verify_yolo_ocr_bridge_evidence_expansion_v0.py`

## Case Matrix（硬门槛）

A. `evidence_expansion_summary.json` 存在\n- 读取成功。\n
B. `root_parse_matrix.json` 存在\n- 可追溯各 root parse 状态。\n
C. `parsed_sample_count` meets target 或 honest insufficient（不得伪造）。\n
D. `parsed_detection_count` meets target 或 honest insufficient。\n
E. `proposal_generated_count` meets target 或 honest insufficient。\n
F. `bridge_result_generated_count` meets target 或 honest insufficient。\n
G. OCR source policy 被使用（通过 evidence-run 输出的政策 id）。\n
H. YOLO/OCR attribution 完整（复用 evidence-run verifier A–Q）。\n
I. candidate_only=true（复用 A–Q）。\n
J. semantic_interpretation_enabled=false（复用 A–Q）。\n
K. allows_execute_now=false（复用 A–Q）。\n
L. real_tts_invoked=false（复用 A–Q）。\n
M. downstream_invocation_count=0（复用 A–Q）。\n
N. trace/replay/whitebox 非空完整（复用 A–Q）。\n
O. 不伪造 detection / 不用 sample_matrix masquerading。\n
P. 不接 runtime / 不进入下游（复用 A–Q）。\n

## Verdict mapping

- GO：扩样达标且 verifier A–Q 通过。
- CONDITIONAL_GO：verifier A–Q 通过但真实 roots 不足导致计数未达标；必须记录 honest insufficient。
- NO_GO：任何治理/追责硬门槛失败或接入 runtime/下游（A–Q 或 boundary 扫描失败）。

