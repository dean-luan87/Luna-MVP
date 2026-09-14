# Luna 评测 — Vision Recognition Evidence Pack Stub v0

**Phase**：`Phase-Vision-Recognition-Evidence-Pack-Stub-001`  
**Runner**：`tools/evaluation/vision/run_vision_recognition_evidence_pack_stub_v0.py`  
**Verifier**：`tools/evaluation/vision/verify_vision_recognition_evidence_pack_stub_v0.py`

## 输入（adapter selection smoke 根目录）

须为 **绝对路径**，且包含：

- `vision_provider_stub_result.json`  
- `vision_recognition_candidate_matrix.json`  
- `vision_provider_selection_report.json`  
- `vision_recognition_adapter_selection_audit_report.json`  
- `vision_recognition_adapter_selection_summary.json`（内含 `vision_roi_proposal_root`，用于回读 `vision_provider_input_pack.json`）

## CLI

```bash
python3 tools/evaluation/vision/run_vision_recognition_evidence_pack_stub_v0.py \
  --adapter-selection-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/vision_lightweight_recognition_adapter_selection_smoke_v0 \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/vision_recognition_evidence_pack_stub_smoke_v0
```

Verifier：

```bash
python3 tools/evaluation/vision/verify_vision_recognition_evidence_pack_stub_v0.py \
  --smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/vision_recognition_evidence_pack_stub_smoke_v0
```

## 产物（`--output-root`）

| 文件 | 说明 |
|------|------|
| `vision_recognition_evidence_pack_summary.json` | 条目数、adapter / ROI 根引用 |
| `vision_recognition_evidence_pack.json` | `vision_recognition_evidence_pack_v0` |
| `vision_recognition_evidence_matrix.json` | 逐条证据矩阵行 |
| `vision_recognition_provider_summary.json` | 选中 provider 与 reason_codes |
| `vision_recognition_evidence_audit_report.json` | audit |
| `vision_recognition_evidence_pack_notes.md` | 短说明 |
| `vision_recognition_evidence_pack_verifier_report.json` | verifier 输出 |

GO / CONDITIONAL_GO / NO_GO：`LUNA_EVALUATION_VISION_RECOGNITION_EVIDENCE_PACK_STUB_GO_NO_GO_PACK_V0.md`。
