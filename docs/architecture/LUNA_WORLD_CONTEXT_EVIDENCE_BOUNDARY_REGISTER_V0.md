# LUNA — WorldContextEvidence Boundary Register v0

## Phase

- **Phase-WorldModel-ContextEvidence-004**

## Purpose

登记并冻结 WorldContextEvidence candidate 链路的硬禁止项，确保它永远不会“越权变成 runtime”。

## Hard boundaries（强制禁止）

- 不接真实 runtime
- 不写入真实世界模型（`world_model_write_invoked=false`）
- 不上传蜂巢（`hive_upload_invoked=false`）
- 不接推荐系统（`recommendation_invoked=false`）
- 不进入 SceneTask/Fusion/Output
- 不执行导航动作（`navigation_action=null`）
- 不真实播报（`real_tts_invoked=false`）
- 不生成最终语义事实（candidate-only）
- **不伪造 GPS**：无 gps/map 输入时不得填写 `lat/lng`
- **不伪造证据链**：缺失上游必须记录 `missing_source_refs`，不得猜测补齐

## Enforced by

- per-root verifier：`tools/verify_world_context_evidence_candidate_v0.py`（含 no fabricated GPS、source_evidence_refs hard gate）
- regression verifier：`tools/verify_world_context_evidence_regression_v0.py`

