# B2 Gate v0.5 结构文档

## ✅ 已完成

### 1. 配置文件
- **`gate_config.yaml`**: 完整的 Gate 配置，包含所有阈值和规则
- 支持 Hard Gate 和 Soft Gate 的独立配置
- 包含人类可读转译映射

### 2. Gate 评估器结构
- **`gate_evaluator_v05.py`**: 完善的 Gate 评估器实现
- 分层设计：Hard Gate（Layer A）和 Soft Gate（Layer B）
- 支持从配置文件加载阈值
- 包含人类可读转译

## 📊 Gate 分层结构

### Layer A: Hard Gate（硬 Gate，一票否决）

1. **资源 Gate**
   - C 优先级检查
   - 系统 FPS 检查（< 15fps → SUSPENDED）

2. **稳定性 Gate**
   - stability_score >= 0.60 → 允许 ACTIVE
   - 0.45 ~ 0.60 → READ_ONLY
   - < 0.45 → SUSPENDED

3. **距离 Gate**
   - 滞回设计：3.2m 进入，2.8m 退出
   - 不满足 → READ_ONLY 或 SUSPENDED

4. **可见性 Gate**
   - 遮挡比例 > 0.35 → SUSPENDED
   - 模糊度检查（v0.5 先不启用）

5. **场景 Gate**
   - 室内/狭窄/电梯 → READ_ONLY
   - 由 C 提供 context 标志

### Layer B: Soft Gate（软 Gate，影响 OBSERVING）

1. **证据连续性**
   - 连续 ≥ 8 帧 + 稳定 ≥ 0.60 → CONFIRMED
   - 不满足 → 只进入 OBSERVING

2. **冷却/去重**
   - 同一 impact 最小间隔 2.0 秒
   - 置信度变化阈值 0.12

## 🔑 Gate 输出结构

### gate_eval（写入 trace）

```json
{
  "can_trigger": false,
  "blocked_by": "camera_shake",
  "details": {
    "stability_score": 0.34,
    "threshold": 0.60,
    "shake_level": "HIGH",
    "human_readable": "镜头晃动过大，B暂停工作"
  }
}
```

### gate_mode 映射

- **Hard gate fail** → SUSPENDED
- **Hard gate pass，但 Soft gate 不满足** → READ_ONLY
- **全部满足** → ACTIVE

## 📝 人类可读转译

所有 Gate fail 都有对应的中文解释：
- "镜头晃动过大，B暂停工作"
- "目标距离<3m，B让权给C"
- "画面遮挡严重，B无法可靠判断"
- "系统帧率过低，B暂停工作"
- "C占用高优先级资源，B让权给C"
- "当前场景由C主导，B只读模式"
- "稳定性处于临界值，B只读模式"

## 🎯 使用方式

```python
# 初始化（使用配置文件）
gate_evaluator = GateEvaluator(config_path="gate_config.yaml")

# 评估 Gate
mode, reason, gate_eval_dict = gate_evaluator.evaluate(
    stability_score=0.65,
    range_m=5.0,
    c_runtime_state={"high_priority": False},
    system_fps=30.0,
    occlusion_ratio=0.1,
    context={"indoor": False},
    evidence_state="CONFIRMED",
    temporal_consistency=0.8,
    impact_key="path_slow_down",
    current_ts=120.0
)

# gate_eval_dict 可直接写入 trace
trace["gate_eval"] = gate_eval_dict
```

## 🔄 下一步

1. 将 `gate_evaluator_v05.py` 集成到 `b2_v03.py`
2. 更新 trace 结构以包含 `gate_eval` 字段
3. 实现 Web Viewer 的最小指标布局
