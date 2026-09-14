# Luna 评测 — MidPlatform Vision Recognition Evidence ReadOnly Ingest Candidate v0

**Phase**：`Phase-MidPlatform-Vision-Recognition-Evidence-ReadOnly-Ingest-Candidate-001`  
**Runner**：`tools/evaluation/midplatform/run_midplatform_vision_recognition_evidence_readonly_ingest_candidate_v0.py`  
**Verifier**：`tools/evaluation/midplatform/verify_midplatform_vision_recognition_evidence_readonly_ingest_candidate_v0.py`

## 输入（Vision read-only consumer 根目录）

须为 **绝对路径**，且包含：

- `vision_recognition_evidence_readonly_consumer_view.json`  
- `vision_recognition_evidence_by_frame_matrix.json`  
- `vision_recognition_evidence_by_roi_matrix.json`  
- `vision_recognition_evidence_geometry_summary.json`  
- `vision_recognition_evidence_readonly_consumer_audit_report.json`  
- `vision_recognition_evidence_readonly_consumer_summary.json`（提供 `vision_recognition_evidence_pack_root` 以加载 `vision_recognition_evidence_matrix.json`）

## CLI

```bash
python3 tools/evaluation/midplatform/run_midplatform_vision_recognition_evidence_readonly_ingest_candidate_v0.py \
  --vision-consumer-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/vision_recognition_evidence_readonly_consumer_smoke_v0 \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/midplatform_vision_recognition_evidence_readonly_ingest_candidate_smoke_v0
```

Verifier：

```bash
python3 tools/evaluation/midplatform/verify_midplatform_vision_recognition_evidence_readonly_ingest_candidate_v0.py \
  --smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/midplatform_vision_recognition_evidence_readonly_ingest_candidate_smoke_v0
```

## 产物（`--output-root`）

| 文件 | 说明 |
|------|------|
| `midplatform_vision_recognition_ingest_candidate_summary.json` | 摘要、校验状态、candidate 路径 |
| `midplatform_vision_recognition_ingest_candidate.json` | `midplatform_vision_recognition_ingest_candidate_v0` |
| `midplatform_vision_recognition_ingest_matrix.json` | 逐条 ingest 矩阵 |
| `midplatform_vision_recognition_ingest_source_chain_summary.json` | 中台层 source chain 包装 |
| `midplatform_vision_recognition_ingest_audit_report.json` | audit |
| `midplatform_vision_recognition_ingest_notes.md` | 短说明 |
| `midplatform_vision_recognition_ingest_verifier_report.json` | verifier 输出 |

GO / CONDITIONAL_GO / NO_GO：`LUNA_EVALUATION_MIDPLATFORM_VISION_RECOGNITION_EVIDENCE_READONLY_INGEST_CANDIDATE_GO_NO_GO_PACK_V0.md`。
