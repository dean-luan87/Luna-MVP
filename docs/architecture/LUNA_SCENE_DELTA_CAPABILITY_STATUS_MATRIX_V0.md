# LUNA — Scene Delta Capability Status Matrix v0

## Phase

- **Phase-MidPlatform-SceneDelta-003**

## Purpose

矩阵化 Scene Delta 的能力状态，作为 `closed_v0` 收口口径。

## Capability status（冻结）

| capability | status | notes |
|---|---|---|
| definition | done | SceneDelta-001 |
| verifier_matrix | done | SceneDelta-001-Fix（A–R + hard blockers） |
| skeleton | done | SceneDelta-002（离线可运行） |
| explicit_content_replacement | done | SceneDelta-002-Fix（new/replaced/removed） |
| spatiotemporal_anchor | done_skeleton | anchor 生成与引用（离线占位） |
| repeated_compression | done_skeleton | canonical + duplicate 记录 + 审计字段 |
| individual_storage_policy | done_skeleton | 默认 individual_local |
| hive_upload | not_allowed | 禁止 |
| world_model_write | not_allowed | 禁止 |
| downstream | not_allowed | 禁止 |
| runtime | not_allowed | 禁止 |
| navigation_action | not_allowed | 必须为 null |
| real_tts | not_allowed | 禁止 |

