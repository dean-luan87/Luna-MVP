# Luna Evaluation — Scene Delta Write Candidate Dry-Run from Vision Smoke v0

**Phase**：`Phase-MidPlatform-Scene-Delta-Write-Candidate-DryRun-Verifier-From-Vision-001`  
**Runner**：`tools/evaluation/midplatform/run_scene_delta_write_candidate_dryrun_from_vision_v0.py`  
**Verifier**：`tools/evaluation/midplatform/verify_scene_delta_write_candidate_dryrun_from_vision_v0.py`

## 目的

对 **Vision 来源 Scene Delta write candidate stub** 产物运行 **dry-run verifier**：生成 summary、字段完备性、映射矩阵、风险报告与 **no-write audit**；并运行 **meta-verifier** 确认无写路径、无执行器调用、**gate_status** 仍为 **not_evaluated**、无 **confirmed_fact** / **confirmed_object** / **navigation_action**。

## 前置

- `Phase-MidPlatform-Scene-Delta-Write-Candidate-From-Vision-Ingest-Stub-001` = GO  
- `Phase-Vision-Ingest-to-Product-Bus-ReadOnly-Replay-001` = GO  
- `Phase-MidPlatform-Vision-Recognition-Evidence-ReadOnly-Ingest-Candidate-001` = GO  

**默认输入 write candidate 根目录**：`_eval_out/scene_delta_write_candidate_from_vision_ingest_stub_smoke_v0/`

## 命令

```bash
python3 tools/evaluation/midplatform/run_scene_delta_write_candidate_dryrun_from_vision_v0.py \
  --write-candidate-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/scene_delta_write_candidate_from_vision_ingest_stub_smoke_v0 \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/scene_delta_write_candidate_dryrun_from_vision_smoke_v0

python3 tools/evaluation/midplatform/verify_scene_delta_write_candidate_dryrun_from_vision_v0.py \
  --smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/scene_delta_write_candidate_dryrun_from_vision_smoke_v0
```

## 读取的 Stub 输入

| 文件 | 作用 |
|------|------|
| `scene_delta_write_candidate_from_vision.json` | 主候选载荷 |
| `scene_delta_write_candidate_vision_evidence_matrix.json` | 行数与 `evidence_items` 对齐校验 |
| `scene_delta_write_candidate_vision_gate_stub.json` | gate 字段完备性 |
| `scene_delta_write_candidate_vision_audit_report.json` | Vision 侧 audit 存在性 |

## 产物

| 文件 | 说明 |
|------|------|
| `scene_delta_write_candidate_dryrun_from_vision_summary.json` | `dry_run_id`、源候选 / event / ingest id、`source_type`、证据数、dry-run 状态、写闸门摘要字段。 |
| `scene_delta_write_candidate_from_vision_field_completeness_report.json` | 字段检查表与 `overall_complete`。 |
| `scene_delta_write_candidate_from_vision_mapping_matrix.json` | Vision → Scene Delta 概念路径映射（不落库）。 |
| `scene_delta_write_candidate_from_vision_risk_report.json` | 风险代码列表。 |
| `scene_delta_write_candidate_from_vision_no_write_audit_report.json` | dry-run no-write audit。 |
| `scene_delta_write_candidate_dryrun_from_vision_notes.md` | 短说明。 |
| `scene_delta_write_candidate_dryrun_from_vision_verifier_report.json` | Meta-verifier 报告。 |

## Verifier 退出码

- **GO** / **CONDITIONAL_GO**：**0**；**NO_GO**：**2**。

GO / NO_GO 语义见 [LUNA_EVALUATION_SCENE_DELTA_WRITE_CANDIDATE_DRYRUN_FROM_VISION_GO_NO_GO_PACK_V0.md](./LUNA_EVALUATION_SCENE_DELTA_WRITE_CANDIDATE_DRYRUN_FROM_VISION_GO_NO_GO_PACK_V0.md)。
