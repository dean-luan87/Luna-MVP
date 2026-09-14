# LUNA — Scene Delta Skeleton v0

## Phase

- **Phase-MidPlatform-SceneDelta-002**

## Purpose

实现 Scene Delta 的离线 skeleton（可运行、可验收、可追责），用于验证：

- input/state/decision/anchor/compression 的 schema 形状
- deterministic 的分流规则（可复现）
- trace/replay/whitebox 完整
- strict governance boundaries（不接真实中台、不写世界模型、不上传蜂巢、不进下游、不导航、不播报）

## Non-governance boundaries（硬边界）

- 不接真实 runtime / 真实中台
- 不进入 SceneTask/Fusion/Output
- 不做最终语义提炼
- 不执行导航动作（`navigation_action=null`）
- 不真实播报（`real_tts_invoked=false`）
- 不写入真实世界模型（`world_model_write_invoked=false`）
- 不上传蜂巢（`hive_upload_invoked=false`）
- 不接推荐系统

## Code artifacts（新增）

- `capabilities/mid_platform/scene_delta_control_v0.py`
- `tools/evaluate_scene_delta_control_v0.py`
- `tools/verify_scene_delta_control_v0.py`
- `datasets/scene_delta_samples_v0/sample_matrix.json`

## CLI

```bash
python3 tools/evaluate_scene_delta_control_v0.py \
  --sample-input datasets/scene_delta_samples_v0/sample_matrix.json \
  --output-root logs/scene_delta_control_002_<timestamp>

python3 tools/verify_scene_delta_control_v0.py \
  --output-root logs/scene_delta_control_002_<timestamp>
```

