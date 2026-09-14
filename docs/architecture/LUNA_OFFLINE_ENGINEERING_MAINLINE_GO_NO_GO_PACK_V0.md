# LUNA — Offline Engineering Mainline GO/NO-GO Pack v0 (Phase-EngineeringFlow-001)

## Scope
本决策包仅对 **EngineeringFlow-001（离线主链集成计划）** 给出 GO/NO-GO。它不实现 runtime，不改变现有模块行为，不运行链路。

## Artifacts（本阶段输出）
- 集成计划：`docs/architecture/LUNA_OFFLINE_ENGINEERING_MAINLINE_INTEGRATION_PLAN_V0.md`
- 模块状态矩阵：`docs/architecture/LUNA_OFFLINE_MAINLINE_MODULE_STATUS_MATRIX_V0.md`
- 接入顺序：`docs/architecture/LUNA_OFFLINE_MAINLINE_INTEGRATION_SEQUENCE_V0.md`
- 无扩展边界政策：`docs/architecture/LUNA_OFFLINE_MAINLINE_BOUNDARY_AND_NO_EXPANSION_POLICY_V0.md`

## Decision
**GO**

## Why GO
- 主链拓扑已完整定义（从 phone_local archive 到统一总报告）
- 模块“done / definition_only / runtime_needed / integration_needed / test_needed / out_of_scope”已矩阵化
- 后续 EF-002/003/004/005/006 的顺序已冻结，避免局部优化偏航
- 闭合前禁止扩展项与红线边界已写死（不入 controlled_live/runtime、不增强能力、不执行不播报、不移除 fallback/disable/pending/candidate-only）
- 本阶段未新增 runtime、未改 adapter、未跑链路

## Hard blockers（本阶段）
- none

## Soft follow-ups（进入后续阶段的前置提醒）
- EF-002 必须把 source policy 接入 PerceptionEval 默认入口，且保持 fail-closed 与 disable_yolo
- EF-003 需要将 SceneContext definitions 落成 offline runner gates（仍不进入真实 runtime）
- EF-004/005 要求“一键 runner + 单入口观测”，否则回归与验收无法规模化

## Recommended next phase
- **EngineeringFlow-002**：YOLO default offline source 接入 PerceptionEval 默认入口（实现级别，仍 offline-only）

## Boundary attestations
- 默认路径仍未开启
- 未进入 full controlled trial
- 未扩大真实 side effects 面
- 未执行 controlled_live_stream
- 未扩 Option A
- 未执行导航动作
- 未真实播报
- 本阶段只做 offline engineering mainline integration plan，不实现 runtime

