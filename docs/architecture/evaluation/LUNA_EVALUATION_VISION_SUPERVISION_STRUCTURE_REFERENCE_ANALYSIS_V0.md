# Luna Evaluation — Vision Supervision Structure Reference Analysis v0

**Phase**：`Phase-Vision-Supervision-Structure-Reference-Analysis-001`  
**Runner**：`tools/evaluation/vision/run_supervision_structure_reference_analysis_v0.py`  
**Verifier**：`tools/evaluation/vision/verify_supervision_structure_reference_analysis_v0.py`

## 输入

**Supervision experiment root**（须含 `external_supervision_availability_probe.json` 等）：

`/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/external_supervision_adapter_experiment_smoke_v0_after_install/`

## 命令

```bash
python3 tools/evaluation/vision/run_supervision_structure_reference_analysis_v0.py \
  --supervision-experiment-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/external_supervision_adapter_experiment_smoke_v0_after_install \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/supervision_structure_reference_analysis_smoke_v0

python3 tools/evaluation/vision/verify_supervision_structure_reference_analysis_v0.py \
  --smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/supervision_structure_reference_analysis_smoke_v0
```

## 产物

| 文件 | 说明 |
|------|------|
| `supervision_structure_reference_summary.json` | 摘要、version、errors |
| `supervision_capability_structure_report.json` | Detections / mask / tracker / zone 能力探测 |
| `supervision_to_luna_mapping_matrix.json` | Supervision → Luna 映射 |
| `supervision_reuse_classification_report.json` | 复用分类 |
| `supervision_architecture_risk_report.json` | 架构风险与 must_not |
| `supervision_recommended_adoption_plan.json` | 短/中/长期采纳计划 |
| `supervision_ab_test_plan.json` | A/B 变体与指标 |
| `supervision_structure_reference_audit.json` | no-write audit |
| `supervision_structure_reference_verifier_report.json` | meta-verifier |

GO / NO_GO：见 [LUNA_EVALUATION_VISION_SUPERVISION_STRUCTURE_REFERENCE_ANALYSIS_GO_NO_GO_PACK_V0.md](./LUNA_EVALUATION_VISION_SUPERVISION_STRUCTURE_REFERENCE_ANALYSIS_GO_NO_GO_PACK_V0.md)。
