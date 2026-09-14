# Luna Evaluation — Scene Delta Generic Chain Closure v0

**Phase**：`Phase-MidPlatform-SceneDelta-Generic-Chain-Closure-001`  
**Runner**：`tools/evaluation/midplatform/run_scene_delta_generic_chain_closure_v0.py`  
**Verifier**：`tools/evaluation/midplatform/verify_scene_delta_generic_chain_closure_v0.py`

## 前置（须均为 GO）

- Generic dry-run（OCR + Vision）  
- Generic trace stub（OCR + Vision）  
- Generic mock handshake（OCR + Vision）  
- Generic contract conformance（OCR + Vision）  

## 命令

```bash
python3 tools/evaluation/midplatform/run_scene_delta_generic_chain_closure_v0.py \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/scene_delta_generic_chain_closure_smoke_v0

python3 tools/evaluation/midplatform/verify_scene_delta_generic_chain_closure_v0.py \
  --smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/scene_delta_generic_chain_closure_smoke_v0
```

可选 `--roots-json` 覆盖默认的 `roots_by_source` 映射。

## 产物

| 文件 | 说明 |
|------|------|
| `scene_delta_generic_chain_closure_summary.json` | 摘要、`source_types`、roots、errors |
| `scene_delta_generic_chain_phase_matrix.json` | 按 `source_type` 的四层 root + verifier |
| `scene_delta_generic_chain_lineage_matrix.json` | `entries[]` 血缘 ID |
| `scene_delta_generic_no_write_boundary_matrix.json` | 按源的 no-write 聚合 |
| `scene_delta_generic_capability_closure_report.json` | 已证明能力 |
| `scene_delta_generic_non_claims_report.json` | 非宣称 |
| `scene_delta_generic_open_followups.json` | 开放跟进 |
| `scene_delta_generic_chain_closure_verifier_report.json` | meta-verifier |

GO / NO_GO：见 [LUNA_EVALUATION_SCENE_DELTA_GENERIC_CHAIN_CLOSURE_GO_NO_GO_PACK_V0.md](./LUNA_EVALUATION_SCENE_DELTA_GENERIC_CHAIN_CLOSURE_GO_NO_GO_PACK_V0.md)。
