# Luna Evaluation — VisionDetectionEvidence Schema Alignment v0

**Phase**：`Phase-VisionDetectionEvidence-Schema-Alignment-001`  
**Runner**：`tools/evaluation/vision/run_vision_detection_evidence_schema_alignment_v0.py`  
**Verifier**：`tools/evaluation/vision/verify_vision_detection_evidence_schema_alignment_v0.py`

## 输入

- **Supervision structure reference root**：`_eval_out/supervision_structure_reference_analysis_smoke_v0/`  
- **Vision recognition evidence pack root**：`_eval_out/vision_recognition_evidence_pack_stub_smoke_v0/`

## 命令

```bash
python3 tools/evaluation/vision/run_vision_detection_evidence_schema_alignment_v0.py \
  --supervision-structure-reference-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/supervision_structure_reference_analysis_smoke_v0 \
  --vision-evidence-pack-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/vision_recognition_evidence_pack_stub_smoke_v0 \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/vision_detection_evidence_schema_alignment_smoke_v0

python3 tools/evaluation/vision/verify_vision_detection_evidence_schema_alignment_v0.py \
  --smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/vision_detection_evidence_schema_alignment_smoke_v0
```

## 产物

| 文件 | 说明 |
|------|------|
| `vision_detection_evidence_schema_v0.json` | Schema 定义与 example_shape |
| `vision_detection_evidence_schema_example.json` | 单条示例 |
| `vision_detection_evidence_stub_compat_fixture.json` | 从 pack stub 转换的样本 |
| `vision_detection_evidence_supervision_mapping_matrix.json` | Supervision → Luna 映射表 |
| `vision_detection_evidence_boundary_report.json` | 风险边界 |
| `vision_detection_evidence_schema_alignment_audit_report.json` | no-write audit |

GO / NO_GO：见 [LUNA_EVALUATION_VISION_DETECTION_EVIDENCE_SCHEMA_ALIGNMENT_GO_NO_GO_PACK_V0.md](./LUNA_EVALUATION_VISION_DETECTION_EVIDENCE_SCHEMA_ALIGNMENT_GO_NO_GO_PACK_V0.md)。
