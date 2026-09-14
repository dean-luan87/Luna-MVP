# LUNA Offline Mainline Observability Report Test Matrix v0

## Phase

- Phase-EngineeringFlow-005 (Unified Observability Report v0)

## Verifier

- `tools/verify_offline_mainline_observability_report_v0.py`

## Test cases (A–J)

| ID | Requirement | How verified | Pass criteria |
|---|---|---|---|
| A | normal root 可读 | verifier 检查 `observability_report.json.normal_root` 目录存在 | `A_normal_root_readable = pass` |
| B | fallback root 可读 | verifier 检查 `observability_report.json.fallback_root` 目录存在 | `B_fallback_root_readable = pass` |
| C | mainline_summary 可读 | verifier 检查 `<root>/mainline_summary.json` 存在 | `C_normal_mainline_summary_readable` & `C_fallback_mainline_summary_readable` 均 pass |
| D | per_sample_mainline_results 可读 | verifier 检查 `<root>/per_sample_mainline_results.json` 存在 | `D_normal_per_sample_readable` & `D_fallback_per_sample_readable` 均 pass |
| E | trace index 可读 | verifier 检查 `<root>/mainline_trace.jsonl` 存在 | `E_normal_trace_readable` & `E_fallback_trace_readable` 均 pass |
| F | replay index 可读 | verifier 检查 `<root>/mainline_replay_index.json` 存在 | `F_normal_replay_index_readable` & `F_fallback_replay_index_readable` 均 pass |
| G | whitebox index 可读 | verifier 检查 `<root>/mainline_whitebox_index.json` 存在 | `G_normal_whitebox_index_readable` & `G_fallback_whitebox_index_readable` 均 pass |
| H | stage outputs refs 不断裂 | verifier 扫描 `sample_chain_matrix.json.samples[*].stage_refs` 路径存在 | `H_stage_output_refs_unbroken = pass` 且 `broken_count = 0` |
| I | normal/fallback 对比存在且字段齐全 | verifier 检查 `normal_vs_fallback_comparison.json` 必需 keys | `I_comparison_required_keys_present = pass` |
| J | safety/evidence boundary 聚合存在且字段齐全 | verifier 检查 `safety_boundary_summary.json` 与 `evidence_boundary_summary.json` keys | `J_safety_required_keys_present` & `J_evidence_required_keys_present` 均 pass |

## Evidence artifacts

EF-005 输出目录应包含：

- `observability_report.json`
- `observability_report.md`
- `sample_chain_matrix.json`
- `stage_artifact_index.json`
- `normal_vs_fallback_comparison.json`
- `safety_boundary_summary.json`
- `evidence_boundary_summary.json`
- `verification_result.json`（由 verifier 生成）

