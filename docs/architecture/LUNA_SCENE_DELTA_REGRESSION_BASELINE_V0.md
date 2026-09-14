# LUNA — Scene Delta Regression Baseline v0

## Phase

- **Phase-MidPlatform-SceneDelta-003**

## Purpose

冻结 Scene Delta 回归的 baseline：输入 root、硬门槛、允许波动项、不允许波动项。

## Baseline input root

- `logs/scene_delta_control_002_fix_20260430_104403`

## Hard gates（必须满足）

- input root 可读
- base verifier=GO
- required output files present
- `processed_count >= 9`
- `anchors_count >= 9`
- `decisions_count >= 9`
- `compression_records_count >= 2`
- `content_replaced` present
- `content_removed` present
- status/action 覆盖：same/new/expired/task_context/uncertain/duplicate/block 至少各出现一次
- compression audit fields present（canonical_evidence_ref/duplicate_count/first_seen_at/last_seen_at）
- trace/replay/whitebox non-empty
- 禁止项无回退：
  - `world_model_write_invoked=false`
  - `hive_upload_invoked=false`
  - `navigation_action=null`
  - `real_tts_invoked=false`
  - `runtime_invoked=false`

## Allowed to fluctuate（允许波动）

- decision distribution count
- content_signature 的具体值
- trace line ordering
- duplicate_count 的具体数值（只要满足最小审计字段）

## Must not fluctuate（不允许波动）

- 缺 `content_replaced`
- 缺 `content_removed`
- compression audit 缺失
- trace/replay/whitebox 缺失或为空
- `world_model_write_invoked=true`
- `hive_upload_invoked=true`
- `navigation_action` 非 null
- `real_tts_invoked=true`
- `runtime_invoked=true`

