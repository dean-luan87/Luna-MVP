# LUNA — YOLO Offline Perception Source Closure GO/NO-GO Pack v0 (Phase-ModelPerception-Closure-001)

## Scope
本决策包仅对 **ModelPerception-001 到 015** 的 YOLO offline 感知源形成“收口结论”，冻结正式状态、范围、禁止项与后续分支。

**本阶段不做：**
- 不新增 runtime
- 不修改 YOLO adapter
- 不重跑完整下游链路（最多引用既有证据与离线 readiness 结果）

## Artifacts
- closure review：`docs/architecture/LUNA_YOLO_OFFLINE_PERCEPTION_SOURCE_CLOSURE_REVIEW_V0.md`
- capability matrix：`docs/architecture/LUNA_YOLO_OFFLINE_PERCEPTION_CAPABILITY_STATUS_MATRIX_V0.md`
- prohibition register：`docs/architecture/LUNA_YOLO_OFFLINE_PERCEPTION_BOUNDARY_AND_PROHIBITION_REGISTER_V0.md`
- future branches：`docs/architecture/LUNA_YOLO_OFFLINE_PERCEPTION_FUTURE_BRANCHES_V0.md`

## Decision
**GO（offline-only closure）**

## Frozen statement (must-use wording)
- closure_recommendation: GO
- yolo_status: `default_offline_perception_candidate_source`
- scope: `OptionA_phone_local_offline_evaluation_only`
- pinned_local_ready: true
- runtime_allowed: false
- controlled_live_allowed: false
- real_tts_allowed: false
- navigation_execution_allowed: false
- pending_real_sidewalk_run_remains: true

## Rationale (why GO)
- 001–015 阶段证据链闭合（影子链路 E2E offline 为 GO）
- pinned_local 权重固化与 readiness 已达成（015：GO）
- candidate-only / no-real-TTS / no execution / evidence boundary 的红线保持
- 禁止项与后续分支已明确冻结，降低误解与越权风险

## Conditional notes (allowed to remain)
以下风险/缺口允许作为 soft follow-ups 保留，但不影响 offline-only closure：
- YOLOv5 代码路径的依赖自检/AutoUpdate 不确定性仍需隔离治理（见 future branches）
- phone_local 样本规模仍需扩展
- SceneContext runtime gates 尚未 runtime enforce（定义完成但执行面尚未落地）
- controlled_live_stream 未开展（且仍被禁止）

## NO_GO triggers (explicit)
出现任一即 NO_GO：
- 文档口径允许 YOLO 进入 runtime 或 controlled_live_stream
- 文档口径允许关闭/绕过 `pending_real_sidewalk_run`
- 文档口径允许执行/播报
- 混淆 offline default 与 runtime default
- 忽略关键风险（AutoUpdate / sample size / SceneContext runtime gate）并宣称“真实能力已验证”

## Boundary attestations
- 默认路径仍未开启
- 未进入 full controlled trial
- 未扩大真实 side effects 面
- 未执行 controlled_live_stream
- 未扩 Option A
- 未执行导航动作
- 未真实播报
- `pending_real_sidewalk_run` 仍保持 true
- YOLO default 只限 offline evaluation
- 本阶段只做 closure review，不新增 runtime

