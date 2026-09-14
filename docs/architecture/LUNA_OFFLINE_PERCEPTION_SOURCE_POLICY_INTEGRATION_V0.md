# LUNA — Offline Perception Source Policy Integration v0 (Phase-EngineeringFlow-002)

## 目标（本阶段唯一目标）
把 ModelPerception-012 定义的 `yolo_default_offline_perception_source_v0` 接入 **PerceptionEval 默认入口**（OptionA / phone_local / offline evaluation），在满足条件时默认选用 YOLO pinned_local shadow perception，否则自动回退 baseline/mock。

## 严格边界（确认）
- 只对 **offline evaluation** 生效，不进入真实 runtime
- 不进入 controlled_live_stream / full trial / 用户测试
- 不改 YOLO adapter（只在 PerceptionEval 侧做策略选择与调用）
- 不进入 SceneTask/Fusion/Output 改造
- 不执行导航动作，不真实播报
- 不移除 baseline/mock fallback、不移除 disable_yolo
- `pending_real_sidewalk_run` 必须保持 true
- YOLO 输出仍 candidate-only，unsupported 能力仍 not_available

## 接入点（实现位置）
- PerceptionEval 默认入口：`tools/evaluate_option_a_phone_local_perception_v0.py`
  - 新增参数（可选，不传保持旧行为）：
    - `--source-policy yolo_default_offline_perception_source_v0`
    - `--offline-evaluation true/false`
    - `--disable-yolo true/false`
    - `--yolo-manifest configs/models/yolo/yolo_model_manifest_v0.json`

## source selection 规则（冻结）
当满足以下全部条件：
- offline_evaluation=true
- option_scope=OptionA
- evidence_type=phone_local_controlled_capture
- controlled_live_stream=false
- pending_real_sidewalk_run=true
- disable_yolo=false
- pinned_local manifest readiness pass（weights_source=pinned_local + sha256 match + verification_status=pass）

则：
- source_selected=yolo_shadow
- fallback_used=false

否则：
- source_selected=baseline_mock
- fallback_used=true
- fallback_reason=具体原因（必填）

## 输出审计字段（新增）
在 summary 与 per-sample 中新增（至少）：
- source_policy_id / offline_evaluation / source_selected / fallback_used / fallback_reason
- disable_yolo / yolo_invoked / detection_count_total
- model_config_id / weights_source / dependency_readiness_status
- yolo_shadow_contract_valid
- scene_context_gate_required=true
- allows_execute_now=false / real_tts_invoked=false
- pending_real_sidewalk_run=true

