# B2 Gate v0.5 实现总结

## ✅ 已完成

### 1. Gate 模块实现

#### stability_evaluator.py
- ✅ `compute_stability_score()`: 计算稳定性分数（0.0 ~ 1.0）
- ✅ `compute_view_state()`: 计算完整的 view_state 字典
- ✅ 支持 IMU 数据（首选）和视觉估计（兜底）

#### gate_evaluator.py
- ✅ `GateEvaluator`: Gate 评估器
- ✅ 5 层 Gate 判定（资源 → 稳定性 → 距离 → 可见性 → 场景）
- ✅ 阈值固定：HARD_BLOCK < 0.45, SOFT_BLOCK < 0.60
- ✅ 距离 Gate 带滞回（3.2m 进入，2.8m 退出）

#### evidence_lifecycle.py
- ✅ `EvidenceLifecycle`: 证据生命周期管理器
- ✅ 状态机：OBSERVING → CONFIRMED → DEGRADED → DROPPED
- ✅ 参数：N_CONFIRM = 8 frames, T_DROP = 1.5 sec
- ✅ 时间一致性计算

#### confidence_calculator.py
- ✅ `calculate_confidence()`: 计算拆分后的置信度
- ✅ 三个维度：perception / world / final
- ✅ 强制规则：Hard Gate fail → final = 0, READ_ONLY → final = 0

### 2. B2 集成

#### b2_v03.py 更新
- ✅ 导入所有 Gate 模块
- ✅ 初始化 `GateEvaluator` 和 `EvidenceLifecycle`
- ✅ 在 `tick()` 中集成 Gate 评估流程：
  1. 计算 `stability_score` 和 `view_state`
  2. 评估 Gate（5 层判定）
  3. 更新证据生命周期
  4. 计算拆分后的置信度
  5. 更新 trace 以包含所有新字段

### 3. Trace 字段更新

- ✅ `view_state`: 相机运动、姿态、FOV、稳定性分数
- ✅ `gate_eval`: Gate 评估结果（mode, blocked_reason）
- ✅ `evidence_state`: 证据生命周期状态
- ✅ `confidence`: 拆分后的置信度（perception / world / final）
- ✅ `impact_evaluation`: 更新格式（horizon_sec, affected_domain）
- ✅ `to_c_message`: 只有 ACTIVE Gate + CONFIRMED 证据才能发送

## 🔑 关键特性

### Gate 规则
1. **资源 Gate**（最高优先级）：C 抢占或系统 FPS < 15 → SUSPENDED
2. **稳定性 Gate**：< 0.45 → SUSPENDED, 0.45~0.60 → READ_ONLY, ≥ 0.60 → 继续
3. **距离 Gate**：< 3.2m → READ_ONLY（带滞回）
4. **可见性 Gate**：遮挡 > 0.35 → SUSPENDED
5. **场景 Gate**：室内/狭窄/电梯 → READ_ONLY

### 证据生命周期
- **OBSERVING**: 首次看到
- **CONFIRMED**: 连续 ≥ 8 帧 + 稳定 ≥ 0.60
- **DEGRADED**: 稳定性下降 < 0.45
- **DROPPED**: 长时间未再出现 > 1.5s

### 置信度计算
- **world_confidence** = stability_score × temporal_consistency
- **final_confidence** = perception_confidence × world_confidence
- 只有 CONFIRMED + ACTIVE 才能发 to_c_message

## 📊 使用示例

```python
# 设置 Gate 输入
b2.imu_data = {
    "angular_velocity_deg_s": 5.0,
    "accel_variance": 0.5,
    "linear_velocity_m_s": 0.3
}
b2.range_m = 5.0
b2.c_runtime_state = {"high_priority": False}
b2.system_fps = 30.0
b2.occlusion_ratio = 0.1
b2.context = {"indoor": False}

# 调用 tick
result = b2.tick(frame_ts=120.0, perception={...})
```

## 🎯 下一步

1. **Gate Web 可视化最小面板**
   - stability 曲线
   - gate 状态时间轴
   - OBSERVING → CONFIRMED 标记

2. **测试和验证**
   - 测试各种 Gate 场景
   - 验证证据生命周期转换
   - 验证置信度计算

3. **性能优化**
   - IMU 数据获取优化
   - 证据跟踪内存管理
