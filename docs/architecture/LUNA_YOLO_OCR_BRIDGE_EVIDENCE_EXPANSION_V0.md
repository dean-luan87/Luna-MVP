# LUNA — YOLO × OCR Evidence Expansion v0

## Phase

- **Phase-ModelOCR-YOLO-Bridge-005** — 只做真实 YOLO `yolo-root` evidence 的离线扩样，形成更稳的回归基线。

## Non-governance boundaries（冻结约束）

- 不接真实 runtime、不接中台、不进入下游、不执行导航、不真实播报、不触发 real TTS、不进入 controlled_live_stream。
- 不做文本语义提炼。
- 不修改 `YOLO closed_v0` / `OCR closed_v0`。
- 不伪造 detection，只在解析阶段进行“bridge input label 归一化”（用于触发 proposal 资格）。

## Entry / Output（入口与输出）

- 扩样 runner：`tools/run_yolo_ocr_bridge_evidence_expansion_v0.py`
- verifier：`tools/verify_yolo_ocr_bridge_evidence_expansion_v0.py`

默认输出目录：

- `logs/yolo_ocr_bridge_evidence_expansion_005_<timestamp>`

该输出 root 必须包含：

- `evidence_expansion_summary.json`
- `root_parse_matrix.json`
- `selected_roots.json`
- `expanded_bridge_results.json`
- `expanded_ocr_crop_proposals.json`
- `yolo_ocr_bridge_trace.jsonl` / `yolo_ocr_bridge_replay.jsonl` / `yolo_ocr_bridge_whitebox.jsonl`
- `expansion_notes.md`

并且保留 Bridge-003 evidence-run 的基础产物（用于复用 schema/治理 verifier）：

- `yolo_ocr_bridge_summary.json`
- `yolo_root_parse_report.json`
- `per_sample_yolo_ocr_bridge_results.json`
- `ocr_crop_proposals.json`

## Success definition（成功定义）

- 扩样达到最低目标（或真实 roots 不足导致 honest insufficient，并完整记录）。
- governance leakage = 0，trace/replay/whitebox 完整。
- verifier 通过（GO / CONDITIONAL_GO）。

