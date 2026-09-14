# LUNA — YOLO Weights & Dependency Manifest Schema v0 (Phase-ModelPerception-013)

## Purpose
冻结 `yolo_model_manifest.json` 的 schema，用于：
- 固定权重来源与版本（pinned local 为目标路径）
- 记录权重 hash 与大小，支持一致性校验
- 记录依赖版本与平台信息，支持可复现
- 记录验证状态与回退策略

## File name / location
- 文件名：`yolo_model_manifest.json`
- 建议位置（实现阶段决定）：离线评测可访问、可审计、不可误用为 runtime 的目录（例如 `manifests/` 或 `assets/manifests/`；本阶段不落地实现）。

## Minimal required fields (v0)
以下字段必须存在（缺失则 readiness check 失败并触发 fallback）：

- manifest_version
- model_config_id
- model_family
- model_name
- model_variant
- model_task

### weights
- weights_source: one of `pinned_local` | `torch_hub_dev` | `unavailable`
- weights_path
- weights_sha256
- weights_file_size_bytes

### loader / IO
- model_loader
- expected_input_format
- expected_output_format

### dependency profile
- dependency_profile_id
- python_version
- torch_version
- torchvision_version
- opencv_version
- numpy_version
- pandas_version
- seaborn_version
- pillow_version

### platform / verification
- platform
- created_at
- verified_at
- verification_status: one of `pass` | `fail` | `partial`
- fallback_policy
- notes

## Example (schema illustration only)

```json
{
  "manifest_version": "v0",
  "model_config_id": "yolo_shadow_v0_pinned_2026_04_27",
  "model_family": "yolo",
  "model_name": "yolov5",
  "model_variant": "s",
  "model_task": "object_detection",
  "weights_source": "pinned_local",
  "weights_path": "assets/models/yolo/yolov5s.pt",
  "weights_sha256": "<sha256>",
  "weights_file_size_bytes": 0,
  "model_loader": "ultralytics_yolov5_local_weights",
  "expected_input_format": "rgb_image_tensor_or_numpy",
  "expected_output_format": "detections_xyxy_conf_cls",
  "dependency_profile_id": "yolo_shadow_v0_py3_torch",
  "python_version": "3.x",
  "torch_version": "x.y.z",
  "torchvision_version": "x.y.z",
  "opencv_version": "x.y.z",
  "numpy_version": "x.y.z",
  "pandas_version": "x.y.z",
  "seaborn_version": "x.y.z",
  "pillow_version": "x.y.z",
  "platform": "darwin-arm64",
  "created_at": "2026-04-27T00:00:00Z",
  "verified_at": "2026-04-27T00:00:00Z",
  "verification_status": "pass",
  "fallback_policy": "fallback_to_baseline_mock_on_any_mismatch",
  "notes": "offline-only; torch.hub disallowed as long-term default"
}
```

## Hard constraints
- `weights_source=torch_hub_dev` **不得**成为长期默认路径；仅允许 dev/smoke，并且必须标记 reproducibility_risk。
- hash mismatch / missing weights / missing deps => 必须 fallback baseline/mock（保留 disable/fallback/rollback）。

