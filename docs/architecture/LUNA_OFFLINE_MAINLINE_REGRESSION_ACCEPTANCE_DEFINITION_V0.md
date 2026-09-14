# LUNA Offline Mainline Regression Acceptance Definition v0

## Phase

- Phase-EngineeringFlow-006 (Offline Mainline Regression Acceptance v0)

## Goal

把 EF-004（统一离线主链 runner）+ EF-005（统一观测总报告）固化成 **回归验收基线**：

- 以后任何改动（YOLO / SceneContext / SceneTask / Fusion / Output / source policy / schema）都必须跑同一套回归
- 回归失败必须阻断后续 closure（不允许“先合再说”）

## Inputs

v0 最小实现（只读复用已有产物）必须提供：

- `--normal-root`：EF-004 normal run 输出根目录
- `--fallback-root`：EF-004 fallback run 输出根目录
- `--observability-root`：EF-005 observability 输出根目录（针对上述 normal/fallback）
- `--output-root`：本次 EF-006 输出目录（写入）

## Outputs

输出目录（示例）：

```
logs/offline_mainline_regression_ef006_<timestamp>/
  regression_acceptance_summary.json
  regression_acceptance_matrix.json
  regression_gate_results.json
  regression_notes.md
  verification_result.json
```

## Hard boundaries

必须写死（fail-closed）：

- 本阶段是 regression acceptance，不是功能增强
- 不新增模型能力
- 不接 `controlled_live_stream`
- 不接真实 runtime
- 不执行导航动作
- 不真实播报
- 不关闭 `pending_real_sidewalk_run`
- 不改变 `evidence_type`
- 不扩大 side effects

## Stop condition

满足以下即停止，不进入 EngineeringFlow-Closure：

- regression acceptance tool 完成
- verifier 完成
- contract docs 完成
- matrix 完成
- go/no-go pack 完成
- README 索引完成
- 给出 go/conditional_go/no_go 结论

