# D1 权重范围表（可冻结）

仅 Layer0 weights 可调；阈值/alpha/hysteresis/lookahead policy 不可动。

## 默认值（与 a3/config.A3Weights 一致）

| 键 | 默认值 |
|----|--------|
| weights.risk_density | 0.30 |
| weights.redline_hit | 0.25 |
| weights.occlusion_ratio | 0.12 |
| weights.roi_load | 0.20 |
| weights.path_instability | 0.30 |
| weights.motion_instability | 0.30 |
| weights.branch_load | 0.20 |
| weights.speak_pressure | 0.05 |
| weights.reject_pressure | 0.03 |

## 采样范围（第一版：0.5× ~ 2.0× default）

| 键 | min | max |
|----|-----|-----|
| weights.risk_density | 0.15 | 0.60 |
| weights.redline_hit | 0.125 | 0.50 |
| weights.occlusion_ratio | 0.06 | 0.24 |
| weights.roi_load | 0.10 | 0.40 |
| weights.path_instability | 0.15 | 0.60 |
| weights.motion_instability | 0.15 | 0.60 |
| weights.branch_load | 0.10 | 0.40 |
| weights.speak_pressure | 0.025 | 0.10 |
| weights.reject_pressure | 0.015 | 0.06 |

实现见 `simulation/d1/weights_schema.py`。
