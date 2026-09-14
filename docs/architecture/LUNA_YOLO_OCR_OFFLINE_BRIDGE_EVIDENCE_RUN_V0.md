# LUNA — YOLO × OCR Offline Bridge Evidence Run v0

## Phase

- **Phase-ModelOCR-YOLO-Bridge-003** — 用真实 YOLO offline `output_root` 做证据跑批（evidence run）。

## Goal（本阶段唯一目标）

- 不接入真实 runtime / 不接中台 / 不进入下游。
- 不做语义提炼 / 不执行导航动作 / 不真实播报 / 不触发 real TTS。
- 仅把真实 YOLO offline 产物解析为桥接输入：
  - frame / detection（class/bbox/frame_id）
  - OCRCropProposal
  - OCR raw text candidates
  - YOLOOCRBridgeResult
- 产生可审计的 trace / replay / whitebox 证据链。

## Non-governance boundaries（冻结约束）

- **raw-text-only**：OCR 只输出 raw text candidates。
- **candidate-only**：只生成候选与证据，不触发执行/动作。
- **禁止** SceneTask / Fusion / Output / 导航 / TTS / controlled_live_stream。
- **禁止** 修改 `YOLO closed_v0` 与 `OCR closed_v0`。

## 实施入口与 CLI

- Evidence 跑批入口：`tools/evaluate_yolo_ocr_offline_bridge_v0.py`
- 真实证据模式必须使用：`--yolo-root <output_root>`

示例（按实际 root 选择其一）：

```shell
python3 tools/evaluate_yolo_ocr_offline_bridge_v0.py \
  --yolo-root logs/offline_mainline_ef004_20260428_105303 \
  --output-root logs/yolo_ocr_offline_bridge_003_<timestamp> \
  --ocr-source-policy ocr_default_offline_raw_text_source_policy_v0 \
  --max-bridge-samples 2
```

## 必须产出（output_root）

- `yolo_ocr_bridge_summary.json`
- `yolo_root_parse_report.json`
- `per_sample_yolo_ocr_bridge_results.json`
- `ocr_crop_proposals.json`
- `yolo_ocr_bridge_trace.jsonl`
- `yolo_ocr_bridge_replay.jsonl`
- `yolo_ocr_bridge_whitebox.jsonl`
- `evaluation_notes.md`

## 验证入口（verifier）

- `tools/verify_yolo_ocr_bridge_evidence_run_v0.py`

## 建议 Evidence 选择（来源）

- 优先使用已通过 closure 的 YOLO / offline mainline 产物（见用户建议的三个 candidates）。

## 成功判定

- `tools/verify_yolo_ocr_bridge_evidence_run_v0.py`：**GO**。
- 验证必须证明：解析自真实 `yolo-root`、proposal/result 生成、OCR policy 调用、归因字段存在、trace/replay/whitebox 完整、治理泄漏为 0。
