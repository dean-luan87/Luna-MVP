# LUNA — Provisional Write & Suspicion-First Commit Policy v0

## Phase

- **Phase-WorldModel-WriteReadiness-002**

## Purpose

把 Commit Layer 的默认原则写死为：**默认谨慎，占位优先，事实提交滞后**。

即使 evidence 通过了 `WriteReadinessCheck`，也不代表可以直接写成“世界事实/稳定记忆”。

本阶段只定义，不实现 runtime，不写真实世界模型。

## Core principles（硬约束）

1. Commit Layer 默认不直接写稳定事实（stable/persistent）
2. 通过 `WriteReadinessCheck` 的 evidence，默认优先进入 `provisional_world_memory`
3. `provisional_world_memory` 必须带：
   - `suspicion_status`
   - `commit_confidence_level`
   - `requires_revalidation=true`
   - `ttl_policy`
   - `source_reference_chain`
   - `rollback_policy`
4. provisional 不可强驱动任务路径
5. provisional 不可作为 hive verified fact 下发
6. provisional 可被低优先级读取，用于：
   - 世界变化观察
   - 体感补充
   - 用户请求时提示
   - 后续复核
7. 只有满足更高门槛后才能升级为 verified / persistent

## Provisional fields（建议）

```json
{
  "suspicion_status": "suspected | plausible | likely | verified | contradicted",
  "commit_confidence_level": "low | medium | high",
  "provisional_reason": "...",
  "upgrade_requirements": {
    "requires_multi_source_validation": true,
    "requires_repeated_observation": true,
    "requires_user_confirmation": false,
    "requires_time_recheck": true
  },
  "allowed_usage": {
    "task_planning": "none | weak_candidate_only",
    "recommendation": "none",
    "speech": "user_requested_only",
    "hive_share": false
  }
}
```

## Default mapping examples（v0）

### commercial_activity

- `provisional_world_memory` 或 `ephemeral_scene_cache`
- `suspicion_status=plausible`
- `requires_revalidation=true`
- `ttl_policy=short_ttl`
- 禁止改变导航路径

### new storefront / new place_hint

- `provisional_world_memory`
- `upgrade_requirements.requires_repeated_observation=true`
- 多次出现或地图/用户确认后 → `verified_scene_local_memory`

### visual_symbol

- meaning 未确认：停留 `candidate_only`（不得 provisional/commit）
- meaning 已确认：允许进入 provisional，但仍需 fraud/risk/复核门控

### human_feedback

- `factual_confirmation` 可提升到 plausible/likely（仍是 provisional/verified 语义，不等于事实写入）
- `metaphorical_mapping/emotional_truth` 不进入事实世界记忆（参见 Human Interaction Validation Layer）

## NO_GO（禁止项）

- provisional 被当作 verified fact 使用
- 存疑信息强驱动导航
- 存疑信息默认播报
- 存疑信息上传蜂巢作为事实
- 无复核条件却升级为 persistent

