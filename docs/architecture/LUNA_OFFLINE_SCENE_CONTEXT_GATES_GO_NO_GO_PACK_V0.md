# LUNA — Offline SceneContext Gates GO/NO-GO Pack v0 (Phase-EngineeringFlow-003)

## Scope
仅覆盖：SceneContext 三道 gate 的 **offline minimal runtime 化**（只产出 gate result + gated perception candidate）。
不进入 SceneTask/Fusion/Output，不新增 runtime，不增强能力。

## Artifacts
- gates runtime：`capabilities/scene_context/offline_scene_context_gates_v0.py`
- evaluation tool：`tools/evaluate_offline_scene_context_gates_v0.py`
- verifier：`tools/verify_offline_scene_context_gates_v0.py`
- eval output_root：`logs/scene_context_gates_offline_ef003_20260428_103623`
- verifier report：`logs/offline_scene_context_gates_verify_002_20260428_1038.json`
- implementation note：`docs/architecture/LUNA_OFFLINE_SCENE_CONTEXT_GATES_IMPLEMENTATION_V0.md`
- test matrix：`docs/architecture/LUNA_OFFLINE_SCENE_CONTEXT_GATES_TEST_MATRIX_V0.md`

## Decision
**GO**

## Why GO
- 三条样本均生成 gate result（generated_rate=1.0）
- 三道 gates 均有结构化输出（各 gate rate=1.0）
- 保守处理成立：depth/motion not_available；collision not_confirmed；macro_scene 不被强制确认
- candidate-only 成立；`allows_execute_now=false`
- safety leakage=0；forbidden scan pass_rate=1.0
- evidence boundary 保持（evidence_type/controlled_live/phone_local/pending 均为 1.0）
- verifier A–I 全通过（含 depicted 场景阻断与 forbidden probe 阻断）

## Soft follow-ups（不阻断）
- v0 仍为最小规则 gate（未接 OCR/medium detector、未接 depth/motion/tracking）
- `degraded_or_uncertain` 在 v0 为保守默认 true，后续需在更高版本中引入更细化的 transition evidence 与置信度治理（仍需独立阶段）

## Recommended next phase
- EngineeringFlow-004：YOLO → SceneContext → SceneTask → Fusion → Output 一键离线主链 runner（本阶段不自动进入）

## Boundary attestations
- 默认路径仍未开启
- 未进入 full controlled trial
- 未扩大真实 side effects 面
- 未执行 controlled_live_stream
- 未扩 Option A
- 未执行导航动作
- 未真实播报
- 本阶段只做 SceneContext gates 的 offline minimal runtime 化，不进入下游

