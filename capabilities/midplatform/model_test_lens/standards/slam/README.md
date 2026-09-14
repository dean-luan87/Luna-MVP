# SLAM Evaluation Standard V1

SLAM 专用落地标准，桥接 MUEP 统一协议。

## 指标

| 类型 | 指标 |
|------|------|
| Task | ATE (m), Drift Rate, Tracking Stability |
| Robustness | motion blur, low light, loop closure stability |
| Structural | map consistency, trajectory smoothness, loop closure correctness |

## SLAM 评分

```
SLAM_score = 0.5*ATE_score + 0.2*stability + 0.2*drift_penalty + 0.1*structural
```

## Adapter

见 `adapters/slam/slam_evaluation_adapter_v1.py`。

## Benchmark Pack V1

- TUM RGB-D（schema-ready）
- KITTI（schema-ready）
- Luna street scene（示例已生成）
