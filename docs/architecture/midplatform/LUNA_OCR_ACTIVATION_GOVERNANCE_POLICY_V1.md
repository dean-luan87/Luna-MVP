# Luna — OCR Activation Governance Policy v1

**Phase**：`OCR-Activation-Governance-Policy-v1-001`

## 目的

统一收口 OCR **启动 / 降级 / 恢复 / 停止** 权，并固化 **Expired Information Value Principle**（四维价值，本阶段不写 WM/事实）：

| 维度 | 含义 |
|------|------|
| **Action Freshness** | 能否用于当前任务、导航、OCR、播报、事实写入；过期后通常不可用 |
| **World Historical Value** | 用户所处世界变化（店铺、施工、标识、路径环境） |
| **User Profile Context Value** | 生活环境、活动范围、常见场景、认知偏好 |
| **Emotional Context Value** | 未来情感计算的环境背景（嘈杂、通勤、医院、消费、孤独、压力等） |

**原则**：过期只表示不适合当前行动，**不等于任务废料、不应简单丢弃**。

**正确流转**（policy）：

`stale observation` → `block current action` → `keep source_chain` → `decay confidence` → `time/spatial anchor` → `classify long_term_value` → 路由至：

- `expired_observation_candidate`
- `world_change_hint_candidate`
- `user_environment_context_candidate`
- `user_profile_context_candidate`
- `emotional_context_background_candidate`

候选须保留：`source_chain`、`time_anchor`、`spatial_anchor`、`original_task_context`、`stale_reason`、`confidence_decay`、`privacy_sensitivity`、`future_usage_scope`。

## 双触发（继承 STC v1）

**A. Safety-triggered** — 后台默认短标识扫描（非全文 OCR）  
**B. Task-triggered** — 中台 + STC + 地理位置/路径进度预判（`ocr_self_activation_allowed=false`）

## 前置

- [LUNA_STC_SAMPLING_GUIDANCE_POLICY_V1.md](./LUNA_STC_SAMPLING_GUIDANCE_POLICY_V1.md)
- [LUNA_USER_GUIDANCE_RECOVERY_POLICY_V1.md](./LUNA_USER_GUIDANCE_RECOVERY_POLICY_V1.md)
- [LUNA_OCR_TASK_ORIENTED_CAPABILITY_PRINCIPLE_V0.md](../ocr/LUNA_OCR_TASK_ORIENTED_CAPABILITY_PRINCIPLE_V0.md)

## 边界

`policy_only=true`；不 OCR、不采样、不 TTS、不硬件、不写事实。

## 实现

- `capabilities/midplatform/ocr_activation_governance_policy_v1.py`
- `tools/evaluation/midplatform/run_ocr_activation_governance_policy_v1.py`
- `tools/evaluation/midplatform/verify_ocr_activation_governance_policy_v1.py`

## 评测

[LUNA_EVALUATION_OCR_ACTIVATION_GOVERNANCE_POLICY_V1.md](../evaluation/LUNA_EVALUATION_OCR_ACTIVATION_GOVERNANCE_POLICY_V1.md)

## 建议下一 phase

- `Vision-Capture-Runtime-DryRun-v1`（Vision Capture Governance v1 已完成）
- `User-Guidance-Recovery-Runtime-DryRun-v1`
