# B2 Gate v0.5 最终版总结

## ✅ 已完成

### 1. 配置文件（最终版）
- **`gate_config.yaml`**: 完整的 Gate 配置
  - Layer A: Hard Gate（5 个硬 Gate）
  - Layer B: Soft Gate（3 个软 Gate）
  - Gate Mode Mapping
  - Trace 语义映射

### 2. Gate 评估器（最终工程版）
- **`gate_evaluator_v05.py`**: 纯函数 + 配置驱动
  - 不依赖 B2 具体实现，可复用
  - 每一帧都能生成完整 Gate Trace
  - 支持从 YAML 配置文件加载

## 🔑 关键特性

### 三条铁律满足

✅ **可视**
- 每一帧都有 Gate 结果
- Gate Mode + blocked_by + human_readable

✅ **可追溯**
- 配置在 YAML
- 规则在 evaluator
- 结果在 trace

✅ **抗视角污染**
- 镜头晃动、角度、距离 先 gate 再判断
- B 不再被迫在垃圾视角下说话

### Gate 输出结构

```python
{
    "can_trigger": False,
    "blocked_by": "camera_shake",
    "details": {
        "stability_score": 0.34
    },
    "human_readable": "镜头晃动过大，无法稳定感知环境"
}
```

## 📊 使用示例

```python
from vision_pipeline.b2.v03.gate.gate_evaluator_v05 import GateEvaluatorV05

# 初始化
evaluator = GateEvaluatorV05(config_path="gate_config.yaml")

# 评估 Gate
mode, gate_trace = evaluator.evaluate(
    stability_score=0.65,
    pitch_deg=5.0,
    roll_deg=2.0,
    range_m=5.0,
    visibility_score=0.8,
    allow_runtime=True,
    evidence_frames=20,
    final_confidence=0.7,
    now_ts=100.0
)

# gate_trace 可直接写入 trace
trace["gate_eval"] = gate_trace
```

## 🎯 下一步选择

你现在有 3 条完全合理的路线：

1. **回到 Step 1，正式定义 stability_score 的计算公式**
   - 完善 stability_evaluator.py
   - 定义 IMU 数据处理流程

2. **把 Gate Trace 接入你们之前的 Web Viewer**
   - 可视化 Gate 状态时间轴
   - 显示 blocked_by 原因

3. **让 B2 在真实运行中先"闭嘴一段时间"，观察 gate 分布**
   - 集成到 b2_v03.py
   - 运行测试，收集 Gate 统计数据

## 📝 配置说明

### Hard Gate（一票否决）
- `camera_stability`: 稳定性门槛（stability_score_min: 0.60）
- `camera_pose`: 镜头角度（pitch_deg_max: 20, roll_deg_max: 15）
- `distance_range`: 距离门槛（min_m: 3.0）
- `visibility`: 可见度门槛（min_score: 0.40）
- `runtime_yield`: 资源让渡（由 C 控制）

### Soft Gate（降级）
- `evidence_continuity`: 证据连续性（min_confirm_frames: 15）
- `cooldown`: 冷却期（min_interval_sec: 3.0）
- `confidence_floor`: 置信度下限（min_final_confidence: 0.55）
