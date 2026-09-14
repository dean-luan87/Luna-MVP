# Luna 评测 — Vision Frame ROI Proposal Stub + Input Pack v0

**Phase**：`Phase-Vision-Frame-ROI-Proposal-And-Segmentation-Stub-001`  
**Runner**：`tools/evaluation/vision/run_vision_roi_proposal_stub_smoke_v0.py`  
**Verifier**：`tools/evaluation/vision/verify_vision_roi_proposal_stub_smoke_v0.py`

## 输入（frame input governance 根目录）

须为 **绝对路径**，且包含：

- `vision_provider_input_candidate.json`  
- `vision_frame_input_governance_matrix.json`  
- `vision_frame_input_governance_summary.json`  
- `vision_frame_input_governance_audit_report.json`  

候选中的 `image_ref` 须指向可读帧图（通常来自上游 minimal ingest 输出）。

## CLI

```bash
python3 tools/evaluation/vision/run_vision_roi_proposal_stub_smoke_v0.py \
  --governance-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/vision_frame_input_governance_smoke_v0 \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/vision_roi_proposal_stub_smoke_v0
```

Verifier：

```bash
python3 tools/evaluation/vision/verify_vision_roi_proposal_stub_smoke_v0.py \
  --governance-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/vision_frame_input_governance_smoke_v0 \
  --smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/vision_roi_proposal_stub_smoke_v0
```

## 产物（`--output-root`）

| 文件 | 说明 |
|------|------|
| `vision_roi_proposal_stub_summary.json` | 帧数、ROI 数、unit 数、pack 数、governance 根引用 |
| `vision_roi_proposal_candidate.json` | 全部 `roi_items`（`vision_roi_proposal_candidate_v0`） |
| `vision_provider_input_pack.json` | `vision_provider_input_pack_bundle_v0`（`packs[]`） |
| `vision_roi_proposal_matrix.json` | 逐 ROI 行（含 `crop_image_ref`） |
| `vision_provider_input_unit_matrix.json` | 逐 `input_unit` 行 |
| `vision_roi_source_chain_summary.json` | 每帧 `source_chain` |
| `vision_roi_proposal_audit_report.json` | audit（禁止项须为 false） |
| `vision_roi_proposal_stub_notes.md` | 短说明 |
| `crops/*.png` | 每 ROI 一张 crop |
| `vision_roi_proposal_stub_verifier_report.json` | verifier 输出 |

GO / CONDITIONAL_GO / NO_GO：`LUNA_EVALUATION_VISION_FRAME_ROI_PROPOSAL_STUB_SMOKE_GO_NO_GO_PACK_V0.md`。
