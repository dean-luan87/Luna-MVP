# LUNA Offline Mainline Observability GO/NO-GO Pack v0

## Phase

- Phase-EngineeringFlow-005 (Unified Observability Report v0)

## Decision

- Decision: **TBD** (待生成 EF-005 实际报告与 verifier 结果后填写)

## Inputs (read-only)

- normal_root: `logs/offline_mainline_ef004_20260428_105303`
- fallback_root: `logs/offline_mainline_ef004_fallback_20260428_105303`

## Outputs (EF-005)

- output_root: `logs/offline_mainline_observability_ef005_<timestamp>`

Expected files:

- `observability_report.json`
- `observability_report.md`
- `sample_chain_matrix.json`
- `stage_artifact_index.json`
- `normal_vs_fallback_comparison.json`
- `safety_boundary_summary.json`
- `evidence_boundary_summary.json`
- `verification_result.json`

## Acceptance (from spec)

### GO

允许进入 EF-006 的必要条件：

- 报告生成（md/json 双报告）
- normal/fallback roots 均可读
- stage artifact refs 完整（不出现 refs 断裂）
- sample chain matrix 完整
- normal/fallback comparison 完整
- safety boundary summary 完整且 leakage=0
- evidence boundary summary 完整且保持
- verifier A–J 通过

### CONDITIONAL_GO

允许（仍是 v0 最小结构），但必须满足：

- 机器可读报告完整
- 人可读 markdown 报告完整
- refs 不断裂
- verifier A–J 通过

### NO_GO

出现任一即 NO_GO：

- normal/fallback root 缺失
- mainline_summary 缺失
- stage refs 断裂
- trace/replay/whitebox index 缺失
- safety leakage 非 0
- evidence boundary 破坏
- report 缺失关键字段
- verifier 失败

## Result summary (to fill after run)

- output_root:
- generated files:
- sample_count:
- broken_refs_count:
- safety leakage:
- evidence boundary ok:
- verifier:

## Hard blockers

- TBD

## Soft follow-ups

- v0 minimal report only (no UI)

## Explicit non-expansion statement

本阶段只做统一观测报告：

- 默认路径仍未开启
- 未进入 full controlled trial
- 未扩大真实 side effects 面
- 未执行 controlled_live_stream
- 未扩 Option A
- 未执行导航动作
- 未真实播报
- 未重跑主链/模型

