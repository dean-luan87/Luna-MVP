# LUNA Offline Engineering Mainline Closure Review v0

## Phase

- Phase-EngineeringFlow-Closure（Offline Engineering Mainline Closure v0）

## Purpose

对 EF-001 ~ EF-006 做总收口 review，冻结当前离线工程主链的正式状态、能力范围、禁止项、回归验收基线与后续分支，防止被误解为真实 runtime 或 controlled live。

## Covered phases (inputs)

- EF-001 Offline Mainline Integration Plan v0：GO
- EF-002 YOLO Default Offline Source → PerceptionEval 默认入口接入 v0：GO
- EF-003 SceneContext Gates Minimal Offline Runtime v0：GO
- EF-004 Unified Offline Mainline Runner v0：GO
- EF-005 Unified Observability Report v0：GO
- EF-006 Offline Mainline Regression Acceptance v0：GO

## Current official status (frozen)

必须覆盖的当前正式状态（写死）：

- `offline_mainline_status`: **closed_v0**
- `scope`: **OptionA_phone_local_offline_evaluation_only**
- `default_perception_source`: **yolo_shadow_pinned_local**
- `fallback_source`: **baseline_mock**
- `scene_context_gates`: **minimal_offline_runtime_v0**
- `runner`: **unified_offline_mainline_v0**
- `observability`: **unified_report_v0**
- `regression_baseline`: **EF006_GO**
- `runtime_allowed`: **false**
- `controlled_live_allowed`: **false**
- `real_tts_allowed`: **false**
- `navigation_execution_allowed`: **false**
- `pending_real_sidewalk_run_remains`: **true**

## What this closure is NOT

必须写死（避免误解）：

- 这是 **offline engineering mainline closure**，不是“真实产品闭环”
- 不是真实导航能力验收
- 不是 controlled_live
- 不是 runtime
- 不是开放测试
- 不允许直接进入用户侧

## What is closed (capability scope)

离线工程主链 v0 闭环范围仅包括：

- PhoneLocal sample_matrix → PerceptionEval（YOLO pinned_local / fallback baseline）
- SceneContext gates（最小离线 runtime 化）
- SceneTask / Fusion / Output candidate（最小规则）
- trace / replay / whitebox index + stage refs
- EF-005 unified observability report
- EF-006 regression acceptance baseline（复用产物验收）

## Hard boundaries (must remain true)

- 不新增 runtime
- 不重跑主链（本 closure 阶段）
- 不重跑模型（本 closure 阶段）
- 不扩 Option A
- 不进入 controlled_live_stream
- 不进入 full controlled trial
- 不开放真实用户测试
- 不执行导航动作
- 不真实播报
- 不做 tracking/depth/OCR/dynamic 能力增强
- 不改变主链 runner 的安全边界

## Regression baseline requirement

后续任何改动（YOLO / SceneContext / SceneTask / Fusion / Output / source policy / schema）：

- **必须通过 EF-006 regression acceptance**（硬门槛与禁止项不允许退化）
- regression fail 必须阻断后续 closure/发布路径（离线工程闭环治理）

## Evidence snapshot (current baseline roots)

本 closure 仅记录已成立事实（只读）：

- EF-004 normal run：`logs/offline_mainline_ef004_20260428_105303`
- EF-004 fallback run：`logs/offline_mainline_ef004_fallback_20260428_105303`
- EF-005 observability：`logs/offline_mainline_observability_ef005_20260428_1100`
- EF-006 regression：`logs/offline_mainline_regression_ef006_20260428_1112`

## Next authorized work style

后续任何推进必须以“分支 + 入口 + 验收”方式进行：

- 新能力/新链路必须先定义入口与禁止项，再接入离线主链或并行主链
- 任何与 runtime 或 controlled live 相关的工作必须走明确的治理入口（本 closure 不授权）

