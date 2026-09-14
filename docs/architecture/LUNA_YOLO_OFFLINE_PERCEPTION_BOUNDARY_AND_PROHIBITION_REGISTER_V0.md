# LUNA — YOLO Offline Perception Boundary & Prohibition Register v0 (Phase-ModelPerception-Closure-001)

## 目的
冻结 YOLO 在 Luna 体系中的 **offline-only** 适用边界与**禁止项**，防止被误解为 runtime 能力或执行权限扩展。

## 正式状态（冻结）
- yolo_status: `default_offline_perception_candidate_source`
- scope: `OptionA_phone_local_offline_evaluation_only`
- pinned_local_ready: true（manifest+sha256+readiness 已成立）

## 必须保持的安全约束（不得移除）
- `side_effects_released` 默认必须为 **false**
- baseline/mock fallback 必须保留（fail-closed）
- disable_yolo 必须保留
- `pending_real_sidewalk_run` 必须保持 **true**（不得关闭/不得被置 false）
- candidate-only：所有输出必须是 candidate，不得触发执行
- evidence_type 不得被改写为“真实执行证据”

## 明确禁止项（prohibited）
YOLO 当前无条件禁止：
- 进入真实 runtime 默认路径（runtime default-on）
- 进入 controlled_live_stream（任何默认/自动启用）
- 进入 full controlled trial
- 开放真实用户测试
- 执行导航动作（execute / actuation）
- 触发真实播报（real TTS emit）
- 打开 default path / default-on
- 扩大真实 side effects 面
- 关闭或绕过 `pending_real_sidewalk_run`
- 绕过 SceneContext gates / governance

## 不得声称（not-claimed）
不得声称下列能力已成立或已验证：
- OCR
- depth
- dynamic event（可靠动态事件识别/预测）
- collision risk（可执行级别碰撞风险判定）
- stable tracking（稳定跟踪）
- real navigation correctness（真实导航正确性）
- real-time performance / latency SLO
- user-facing reliability（用户可用性与长期稳定性）

## 允许项（allowed, 严格限定）
仅允许：
- 在 Option A / phone_local / offline evaluation 中作为 perception candidate source（默认源）
- 仅输出候选链路产物（Perception/SceneTask/Fusion/Output candidate），用于离线评测与审计
- pinned_local 权重固化与 readiness（依赖/sha/dry-run/smoke）属于离线工程可复现性治理的一部分

