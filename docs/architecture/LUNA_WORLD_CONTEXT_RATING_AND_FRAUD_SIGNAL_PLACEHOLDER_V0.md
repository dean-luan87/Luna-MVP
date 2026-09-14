# LUNA — World Context Rating & Fraud Signal Placeholder v0

## Phase

- Phase-WorldModel-ContextEvidence-001

## Purpose

定义世界证据层中用于：
- 店铺/服务质量的评分与可信度（rating）
- 用户反馈与跨个体共享的欺诈/误导风险信号（fraud signals）

这些字段在本阶段只作为占位合同，不接推荐系统、不接真实共享网络。

## Non-governance boundary

- 不实现 runtime，不执行任务/导航/播报。

## Rating signal（占位结构）

建议用于填充 `WorldContextEvidence.content` 或 `world_model_policy` 的扩展字段：

```json
{
  "rating_source": "user_feedback | system_observation | map_listing | cross_luna_aggregate",
  "rating_score": 0.0,
  "rating_confidence": 0.0,
  "privacy_redaction_applied": true
}
```

## Fraud signal（占位结构）

```json
{
  "fraud_signal_source": "text_pattern | contradictory_evidence | user_report | cross_luna_alert",
  "fraud_risk_strength": 0.0,
  "fraud_risk_status": "unknown | suspected | verified_safe | suspected_fraud",
  "requires_user_confirmation": true,
  "shareable_to_hive": false
}
```

## Sharing & privacy placeholder

跨 Luna 共享必须满足占位策略：
- 若 `fraud_risk_status != verified_safe`：默认 `shareable_to_hive=false`
- 若存在隐私敏感来源：必须声明 `privacy_redaction_applied=true`

