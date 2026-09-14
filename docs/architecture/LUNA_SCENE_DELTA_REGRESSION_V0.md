# LUNA — Scene Delta Regression v0

## Phase

- **Phase-MidPlatform-SceneDelta-003**

## Purpose

对 SceneDelta-002/002-Fix 的离线 skeleton 做**只读回归验收**，以便将：

- `Phase-MidPlatform-SceneDelta-001`（definition）/ `001-Fix`（verifier matrix）
- `Phase-MidPlatform-SceneDelta-002`（skeleton）/ `002-Fix`（explicit replacement/removal）

收口为 `closed_v0`（offline skeleton only）。

## Non-governance boundaries（写死）

- 不接真实 runtime / 中台
- 不进 SceneTask/Fusion/Output
- 不写真实世界模型
- 不上传蜂巢
- 不导航、不播报
- 不接推荐系统

## Regression input（只读 output_root）

- `logs/scene_delta_control_002_fix_20260430_104403`

## Tools（新增）

### Regression runner

`tools/run_scene_delta_regression_v0.py`

输出：

- `scene_delta_regression_summary.json`
- `scene_delta_regression_matrix.json`
- `scene_delta_status_action_matrix.json`
- `scene_delta_compression_audit_summary.json`
- `scene_delta_boundary_summary.json`
- `scene_delta_trace_replay_whitebox_summary.json`
- `regression_notes.md`

### Regression verifier

`tools/verify_scene_delta_regression_v0.py`

覆盖：A–Q（见用户指令中的硬门槛集合）。

