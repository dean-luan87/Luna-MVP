# LUNA — Offline Mainline Runner GO/NO-GO Pack v0 (Phase-EngineeringFlow-004)

## Scope
只覆盖“一键离线主链 runner”（offline evaluation only）。
不进入 controlled_live_stream / runtime，不执行动作、不真实播报，不做能力增强。

## Artifacts
- runner core：`capabilities/offline_mainline/offline_mainline_runner_v0.py`
- CLI：`tools/run_offline_mainline_v0.py`
- verifier：`tools/verify_offline_mainline_runner_v0.py`
- implementation：`docs/architecture/LUNA_OFFLINE_MAINLINE_RUNNER_IMPLEMENTATION_V0.md`
- test matrix：`docs/architecture/LUNA_OFFLINE_MAINLINE_RUNNER_TEST_MATRIX_V0.md`
- normal run：`logs/offline_mainline_ef004_20260428_105303`
- fallback run：`logs/offline_mainline_ef004_fallback_20260428_105303`
- verifier report：`logs/offline_mainline_runner_verify_001_20260428_1058.json`

## Decision
**GO**

## Why GO
- normal 与 fallback 两条路径均全链路跑通（stage_complete_rates 全 1.0）
- schema_valid_rates 全 1.0
- candidate-only 全链路成立
- `allows_execute_now=false`；`real_tts_invoked=false`
- safety leakage=0
- evidence boundary 全保持（evidence_type/controlled_live/phone_local/pending=1.0）
- trace/replay/whitebox index 存在且 per-sample stage refs 可解析
- verifier 全通过（20/20）

## Soft follow-ups（不阻断）
- v0 runner 的 SceneTask/Fusion/Output 仍为最小离线候选规则（不声称真实导航能力）
- 后续可在 EF-005 做统一总观测入口收口（报告聚合与索引稳定化）

## Recommended next phase
- EngineeringFlow-005：统一 trace/replay/whitebox 总报告（观测收口）

## Boundary attestations
- 默认路径仍未开启
- 未进入 full controlled trial
- 未扩大真实 side effects 面
- 未执行 controlled_live_stream
- 未扩 Option A
- 未执行导航动作
- 未真实播报
- 本阶段只做一键离线主链 runner，不进入真实 runtime

