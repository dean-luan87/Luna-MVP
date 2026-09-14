# LUNA Offline Mainline Regression Acceptance GO/NO-GO Pack v0

## Phase

- Phase-EngineeringFlow-006 (Offline Mainline Regression Acceptance v0)

## Decision

- Decision: **TBD**（由 `regression_acceptance_summary.json` 与 `verification_result.json` 填写）

## Inputs (read-only)

- normal_root: `logs/offline_mainline_ef004_20260428_105303`
- fallback_root: `logs/offline_mainline_ef004_fallback_20260428_105303`
- observability_root: `logs/offline_mainline_observability_ef005_20260428_1100`

## Outputs

- output_root: `logs/offline_mainline_regression_ef006_<timestamp>`

Expected files:

- `regression_acceptance_summary.json`
- `regression_acceptance_matrix.json`
- `regression_gate_results.json`
- `regression_notes.md`
- `verification_result.json`

## Acceptance

### GO

- 所有硬门槛通过
- regression report 生成
- verifier 通过
- hard_blockers=[]
- 不新增 runtime / 不进入 controlled_live_stream

### CONDITIONAL_GO

- 仅存在允许波动项（例如 detection_count_total）
- 安全边界全通过
- evidence boundary 全通过
- fallback path 通过

### NO_GO

出现任一即 NO_GO：

- 任一硬门槛失败
- safety leakage 非 0
- evidence boundary 破坏
- fallback path 缺失
- EF-005 refs 断裂（broken_refs != 0）
- pending_real_sidewalk_run 被关闭
- controlled_live_stream 被开启

## Result summary (fill after run)

- output_root:
- recommendation:
- hard_thresholds_passed / total:
- hard_blockers:
- verifier:

## Explicit non-expansion statement

本阶段只做离线主链回归验收：

- 默认路径仍未开启
- 未进入 full controlled trial
- 未扩大真实 side effects 面
- 未执行 controlled_live_stream
- 未扩 Option A
- 未执行导航动作
- 未真实播报
- 不新增 runtime

