# Luna 评测 — Vision Recognition Evidence ReadOnly Consumer v0

**Phase**：`Phase-Vision-Recognition-Evidence-ReadOnly-Consumer-001`  
**Runner**：`tools/evaluation/vision/run_vision_recognition_evidence_readonly_consumer_v0.py`  
**Verifier**：`tools/evaluation/vision/verify_vision_recognition_evidence_readonly_consumer_v0.py`

## 输入（evidence pack stub 根目录）

须为 **绝对路径**，且包含：

- `vision_recognition_evidence_pack.json`  
- `vision_recognition_evidence_matrix.json`  
- `vision_recognition_provider_summary.json`  
- `vision_recognition_evidence_audit_report.json`  

## CLI

```bash
python3 tools/evaluation/vision/run_vision_recognition_evidence_readonly_consumer_v0.py \
  --evidence-pack-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/vision_recognition_evidence_pack_stub_smoke_v0 \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/vision_recognition_evidence_readonly_consumer_smoke_v0
```

Verifier：

```bash
python3 tools/evaluation/vision/verify_vision_recognition_evidence_readonly_consumer_v0.py \
  --evidence-pack-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/vision_recognition_evidence_pack_stub_smoke_v0 \
  --smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/vision_recognition_evidence_readonly_consumer_smoke_v0
```

## 产物（`--output-root`）

| 文件 | 说明 |
|------|------|
| `vision_recognition_evidence_readonly_consumer_summary.json` | 消费摘要 |
| `vision_recognition_evidence_readonly_consumer_view.json` | `vision_recognition_evidence_readonly_consumer_view_v0` |
| `vision_recognition_evidence_by_frame_matrix.json` | 按帧聚合矩阵 |
| `vision_recognition_evidence_by_roi_matrix.json` | 按 ROI 类型聚合矩阵 |
| `vision_recognition_evidence_geometry_summary.json` | bbox 统计 |
| `vision_recognition_evidence_readonly_consumer_audit_report.json` | consumer audit |
| `vision_recognition_evidence_readonly_consumer_notes.md` | 短说明 |
| `vision_recognition_evidence_readonly_consumer_verifier_report.json` | verifier 输出 |

GO / CONDITIONAL_GO / NO_GO：`LUNA_EVALUATION_VISION_RECOGNITION_EVIDENCE_READONLY_CONSUMER_GO_NO_GO_PACK_V0.md`。
