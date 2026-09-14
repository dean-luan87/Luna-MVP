# LUNA — Scene Delta Explicit Content Replacement Branch Fix v0

## Phase

- **Phase-MidPlatform-SceneDelta-002-Fix**

## Purpose

补齐 Scene Delta skeleton 对“同一载体上的内容生命周期变化”的显式分支：

- `new_content_same_place`（空白→新内容）
- `content_replaced`（A→B）
- `content_removed`（A→空白/marked_missing）

动机：从世界变化分析角度，“新出现/替换/下架”的语义不同，不应全部折叠为 `new_content_same_place`。

## Non-governance boundaries（保持不变）

- 不接真实中台、不进下游
- 不写真实世界模型、不上传蜂巢
- 不导航、不播报、不触发 runtime

## Changes

- `capabilities/mid_platform/scene_delta_control_v0.py`
  - 引入 `marked_missing` 支持
  - 在同一 anchor 下显式区分 `content_replaced/content_removed/new_content_same_place`
  - 将 `previous_content_ref/current_content_ref` 写入 `change_summary`
- `datasets/scene_delta_samples_v0/sample_matrix.json`
  - 新增 poster_board A→B（`content_replaced`）样本
  - 新增 poster_board A→empty（`content_removed`）样本
- `tools/verify_scene_delta_control_v0.py`
  - verifier 要求 `content_replaced` / `content_removed` 可触发

