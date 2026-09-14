# Luna 评测 — Vision Recognition Adapter Selection Smoke v0

**Phase**：`Phase-Vision-Lightweight-Recognition-Adapter-Selection-001`  
**Runner**：`tools/evaluation/vision/run_vision_lightweight_recognition_adapter_selection_smoke_v0.py`  
**Verifier**：`tools/evaluation/vision/verify_vision_lightweight_recognition_adapter_selection_smoke_v0.py`

## 输入（ROI proposal stub 根目录）

须为 **绝对路径**，且包含：

- `vision_provider_input_pack.json`  
- `vision_roi_proposal_candidate.json`  
- `vision_roi_proposal_audit_report.json`  

## CLI

```bash
python3 tools/evaluation/vision/run_vision_lightweight_recognition_adapter_selection_smoke_v0.py \
  --roi-proposal-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/vision_roi_proposal_stub_smoke_v0 \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/vision_lightweight_recognition_adapter_selection_smoke_v0
```

Verifier（需同时传入 ROI stub 根与本 phase 输出根）：

```bash
python3 tools/evaluation/vision/verify_vision_lightweight_recognition_adapter_selection_smoke_v0.py \
  --roi-proposal-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/vision_roi_proposal_stub_smoke_v0 \
  --smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/vision_lightweight_recognition_adapter_selection_smoke_v0
```

## 产物（`--output-root`）

| 文件 | 说明 |
|------|------|
| `vision_recognition_adapter_selection_summary.json` | pack 数、input_units 数、stub item 数等 |
| `vision_provider_registry_snapshot.json` | registry 快照 |
| `vision_provider_selection_report.json` | `vision_provider_selection_report_v0` |
| `vision_provider_stub_result.json` | 合并后的 synthetic stub 结果 |
| `vision_recognition_candidate_matrix.json` | 候选矩阵（与 units 对齐） |
| `vision_recognition_adapter_selection_audit_report.json` | audit |
| `vision_recognition_adapter_selection_notes.md` | 短说明 |
| `vision_recognition_adapter_selection_verifier_report.json` | verifier 输出 |

GO / CONDITIONAL_GO / NO_GO：`LUNA_EVALUATION_VISION_RECOGNITION_ADAPTER_SELECTION_SMOKE_GO_NO_GO_PACK_V0.md`。
