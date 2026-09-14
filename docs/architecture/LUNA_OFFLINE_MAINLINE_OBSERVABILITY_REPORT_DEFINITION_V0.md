# LUNA Offline Mainline Observability Report Definition v0

## Phase

- Phase-EngineeringFlow-005 (Unified Observability Report v0)

## Goal

基于 EF-004 的 offline mainline `output_root`（normal + fallback 两次 run 的产物），生成统一观测总报告，用于：

- 回归测试：快速判断链路、schema、边界是否仍成立
- 问题定位：一处入口聚合 trace / replay / whitebox / stage outputs
- 对比分析：normal（yolo_shadow）vs fallback（baseline_mock）差异摘要

## Inputs

必须提供两个只读输入根目录：

- `normal_root`: EF-004 正常 run 输出根目录（例：`logs/offline_mainline_ef004_20260428_105303`）
- `fallback_root`: EF-004 fallback run 输出根目录（例：`logs/offline_mainline_ef004_fallback_20260428_105303`）

这些 root 必须已经由 EF-004 生成，且包含：

- `mainline_summary.json`
- `per_sample_mainline_results.json`
- `mainline_trace.jsonl`
- `mainline_replay_index.json`
- `mainline_whitebox_index.json`
- `stage_outputs/`（perception/scene_context/scene_task/fusion/output）

## Outputs

输出一个新的 `output_root`（只写该目录）：

```
logs/offline_mainline_observability_ef005_<timestamp>/
  observability_report.json
  observability_report.md
  sample_chain_matrix.json
  stage_artifact_index.json
  normal_vs_fallback_comparison.json
  safety_boundary_summary.json
  evidence_boundary_summary.json
  verification_result.json
```

## Hard Boundaries (must be fail-closed)

本阶段必须写死（工具实现与文档约束）：

- 只读 EF-004 产物：不得重跑模型，不得重跑主链 runner
- 不进入真实 runtime
- 不执行导航动作
- 不真实播报（real TTS）
- 不进入 `controlled_live_stream`
- 不关闭 `pending_real_sidewalk_run`
- 不改 `evidence_type`
- 不扩大 side effects 面
- 不扩 Option A 能力

## Report scope

统一观测总报告至少覆盖：

- stage outputs 汇总（存在性 + per-sample refs 不断裂）
- trace / replay / whitebox index 汇总
- source policy 汇总（normal vs fallback distribution）
- sample-level chain 状态（matrix）
- safety boundary 汇总（leakage=0 必须保持）
- evidence boundary 汇总（preserved 必须保持）
- normal vs fallback 对比（机器可读）

## Stop condition

满足以下即停止，不进入 EF-006：

- report builder 完成并能生成 md/json 双报告 + 六个派生 json
- verifier 完成并给出 A–J 结果
- schema docs 完成
- test matrix 完成
- go/no-go pack 完成
- README 索引更新完成

