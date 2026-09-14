# LUNA — Scene Delta Closure Review v0

## Phase

- **Phase-MidPlatform-SceneDelta-003**

## Purpose

将 Scene Delta 主线收口为 `closed_v0`，冻结：

- 定义机制（001）
- verifier matrix（001-Fix）
- 离线 skeleton（002）
- 显式内容替换/移除分支（002-Fix）

并明确 `closed_v0` 仍为 **offline skeleton only**，不代表 runtime readiness。

## Closed status（冻结建议）

```json
{
  "scene_delta_status": "closed_v0",
  "scope": "offline_skeleton_only",
  "definition": "done",
  "verifier_matrix": "done",
  "skeleton": "done",
  "explicit_content_replacement": "done",
  "spatiotemporal_anchor": "done_skeleton",
  "repeated_evidence_compression": "done_skeleton",
  "individual_storage_policy": "done_skeleton",
  "hive_storage_policy": "definition_only",
  "runtime_allowed": false,
  "real_midplatform_connected": false,
  "world_model_write_allowed": false,
  "hive_upload_allowed": false,
  "downstream_allowed": false,
  "navigation_action_allowed": false,
  "real_tts_allowed": false
}
```

## Evidence basis（回归证据）

以 SceneDelta-003 regression（只读）为闭环证据入口：

- `docs/architecture/LUNA_SCENE_DELTA_REGRESSION_V0.md`

## What is frozen（冻结内容）

- `SceneDeltaInput/State/Decision` schema 与硬边界
- `SpatiotemporalDeltaAnchor` 主机制（同一载体的内容演替语义）
- `RepeatedEvidenceCompression` 主机制（canonical/delta/审计链）
- `content_replaced/content_removed/new_content_same_place` 的显式区分
- trace/replay/whitebox 最小可观测性要求

## What is not claimed（不声明）

- 不声明真实中台接线完成
- 不声明 hive 上传/共享实现
- 不声明世界模型事实写入 readiness
- 不声明矛盾证据的高级解决策略（仅占位）

