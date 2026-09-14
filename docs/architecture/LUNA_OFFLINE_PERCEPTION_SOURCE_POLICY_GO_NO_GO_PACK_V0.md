# LUNA — Offline Perception Source Policy GO/NO-GO Pack v0 (Phase-EngineeringFlow-002)

## Scope
仅覆盖：将 `yolo_default_offline_perception_source_v0` 接入 PerceptionEval 默认入口（offline-only）。
不进入 SceneTask/Fusion/Output，不新增 runtime，不做能力增强。

## Artifacts
- policy module：`capabilities/model_perception/offline_source_policy_v0.py`
- PerceptionEval integration：`tools/evaluate_option_a_phone_local_perception_v0.py`
- verifier：`tools/verify_offline_perception_source_policy_v0.py`
- integration note：`docs/architecture/LUNA_OFFLINE_PERCEPTION_SOURCE_POLICY_INTEGRATION_V0.md`
- test matrix：`docs/architecture/LUNA_OFFLINE_PERCEPTION_SOURCE_POLICY_TEST_MATRIX_V0.md`

## Decision
**GO**

### Why
- 已实现 source policy selection + pinned_local manifest readiness gate
- PerceptionEval 入口已接入且保持“无参数时不破坏旧 baseline/mock”
- 已提供 verifier 覆盖 policy 层 A–G 基本选择/回退路径与 manifest readiness

### Conditional notes (v0 limitations)
- 已通过 EF-002-Fix 补齐 PerceptionEval 集成运行证据（见 Evidence runs）。

## Evidence runs（EF-002-Fix）
- Evidence run record：`docs/architecture/LUNA_OFFLINE_PERCEPTION_SOURCE_POLICY_INTEGRATION_EVIDENCE_RUN_V0.md`
- Evidence matrix：`docs/architecture/LUNA_OFFLINE_PERCEPTION_SOURCE_POLICY_INTEGRATION_EVIDENCE_MATRIX_V0.md`

结论要点：
- YOLO selected run：source_selected=yolo_shadow；五类 signal schema 完整；safety leakage=0；审计字段齐全
- fallback run（disable_yolo=true）：source_selected=baseline_mock；fallback_reason present；五类 signal schema 完整；safety leakage=0

## Hard blockers (NO_GO triggers)
- 无法 fallback baseline/mock
- source policy 允许 controlled_live_stream 使用 YOLO
- 关闭/绕过 pending_real_sidewalk_run
- 产生 execute/default-on/side-effects 泄漏
- 审计字段缺失严重
- 不传 source-policy 时旧 baseline/mock 行为被破坏

## Recommended next phase
- EngineeringFlow-003：SceneContext gates 最小 runtime 化（仅 offline runner gate，不进入真实 runtime）

## Boundary attestations
- 默认路径仍未开启
- 未进入 full controlled trial
- 未扩大真实 side effects 面
- 未执行 controlled_live_stream
- 未扩 Option A
- 未执行导航动作
- 未真实播报
- YOLO default 只限 offline evaluation
- 本阶段只把 source policy 接入 PerceptionEval 入口，不进入下游链路

