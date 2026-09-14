# SLAM Evaluation Adapter V1

将 ORB-SLAM / VINS / Kimera / 未来 VEGA 的统一输出转为 Model Test Lens MUEP envelope。

## 用法

```bash
# 生成示例 envelope（Luna street scene 合成轨迹）
python3 -m capabilities.midplatform.model_test_lens.adapters.slam.slam_evaluation_adapter_v1

# 从 Python 调用
from capabilities.midplatform.model_test_lens.adapters.slam.slam_evaluation_adapter_v1 import (
    adapt_slam_run_to_envelope,
)
```

## 输入（slam_run）

```json
{
  "backend": "orb_slam",
  "dataset": "luna_street_scene_v1",
  "trajectory": [[x,y,z], ...],
  "ground_truth_trajectory": [[x,y,z], ...],
  "per_frame_tracking_state": ["OK", "OK", "LOST", ...],
  "keyframes": [0, 30, 60],
  "map": {},
  "map_consistency_score": 0.87,
  "loop_closure_correct": true
}
```

## 输出

- `muep` 块：统一三层 metric + final_score
- `metrics.slam`：ATE / drift / stability / SLAM_score
- `visualization_layers`：trajectory + drift_metrics（供静态页读取）

## 评分

```
SLAM_score = 0.5*ATE_score + 0.2*stability + 0.2*drift_penalty + 0.1*structural
MUEP final  = 0.6*task + 0.25*robustness + 0.15*structural
```

## Benchmark Pack V1（规划）

| Dataset | 状态 |
|---------|------|
| TUM RGB-D | schema-ready |
| KITTI | schema-ready |
| Luna street scene | 示例已生成 |

## 治理

- candidate-only，不授予 runtime_ready
- 不触发 navigation / fact write
