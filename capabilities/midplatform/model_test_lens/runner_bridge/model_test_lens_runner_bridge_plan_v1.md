# Model Test Lens — Runner Bridge Plan V1

## 流水线

```
local asset → manifest → job request → runner bridge request
→ runner execution phase (独立审批) → raw output
→ adapter → MUEP envelope → Lens display
```

## Runner Bridge

- `runner_allowed_to_execute_model` 仅在独立 execution phase + owner approval 后为 true
- Lens **may read** runner output，**may not execute** or **modify** runner

## SLAM 视频路由

```
video/frame_sequence → manifest → SLAM job → runner_bridge
→ ORB-SLAM3/VINS/Kimera runner phase → trajectory
→ SLAM Evaluation Adapter V1 → SLAM Diagnostic Engine V1 → envelope
```

### 无 GT 约束

- 有 GT：ATE / RPE / drift heatmap
- 无 GT：仅 limited diagnostics（轨迹可视化、tracking timeline、smoothness proxy、lost frame ratio）
- **禁止伪造 GT**；无 GT 结果不得与 GT benchmark 直接比较

## 图片路由

```
image → manifest → segmentation/OCR/depth/VLM job → runner_bridge
→ model runner phase → adapter → envelope
```

MobileSAM 必须走 segmentation runner，页面不得直跑模型。

## Schema

- `runner_bridge_request_schema_v1.json`
- `asset_to_envelope_route_schema_v1.json`

## 下一步

`Phase-P1-Midplatform-Model-Test-Lens-Local-Asset-Import-UI-Patch-Execution-And-Post-Review-v1-001`
