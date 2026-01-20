# B2 Decision Gate v0.1 设计文档

## 📋 概述

B2 = 决策节律 × 决策必要性的"策略调度层"

**核心定位**：
- B2 不决定"做什么"，只决定"要不要现在做"
- B2 是 observe() 内部的"第二道闸门"
- 在节律闸门之后、决策生成之前

## 🎯 B2 v0.1 三个智能维度（规则版）

### 维度 1：环境稳定度（Scene Stability）

**目标**：在"重复路段 / 长直行 / 熟悉环境"中自动降频

**策略**：
- 场景稳定超过 30s：心跳间隔延长到 3.0s
- 场景稳定超过 60s：心跳间隔延长到 4.0s
- 只在 STABLE 状态下应用

**实现**：
- 使用粗粒度场景 hash（state + motion_score + frame_diff）
- 追踪场景稳定持续时间

### 维度 2：决策冗余抑制（Decision Redundancy）

**目标**：同样的 decision，不要反复出现

**策略**：
- 如果当前决策类型和上次相同
- 且状态是 STABLE
- 且距离上次决策时间 < 5s
- 则抑制本次决策

**实现**：
- 记录上一次决策的类型和状态
- 检查时间间隔和决策相似度

### 维度 3：复杂度反向调节（Inverse Complexity Control）

**目标**：场景越复杂，越不应该提高决策频率

**策略**：
- 如果复杂度持续高（平均 > 0.5）且波动大（方差 > 0.1）
- 但无强信号（motion_score > 0.8 或 frame_diff > 0.8）
- 则抑制决策

**实现**：
- 维护最近 10 帧的复杂度窗口
- 计算平均复杂度和方差
- 检测强信号

## 🔧 接口设计

```python
class B2DecisionGate:
    def should_emit(
        self,
        ts: float,
        state: str,
        last_decision: Optional[Dict[str, Any]],
        motion_score: float,
        frame_diff: float,
        state_transition: bool = False,
        protection_active: bool = False,
    ) -> Tuple[bool, Dict[str, Any]]:
        """
        return:
          emit: bool
          meta: {
            "b2_reason": "...",
            "effective_heartbeat": 4.0
          }
        """
```

**关键约束**：
- B2 只返回 emit / not emit
- 不返回 decision
- 不修改 state

## 🚀 使用方法

### 启用 B2（在 C1ActiveController 中）

```python
from vision_pipeline.c1_controller.c1_active_controller import C1ActiveController
from vision_pipeline.c1_controller.b2_decision_gate import B2DecisionGate

# 创建 B2 闸门
b2_gate = B2DecisionGate()

# 创建 C1 Controller 并启用 B2
controller = C1ActiveController(
    enable_b2=True,
    b2_gate=b2_gate,
)
```

### 默认行为（B2 未启用）

如果不启用 B2，C1ActiveController 保持 v0.2 的原始行为：
- 决策数：≈ 100（6分42秒视频）
- 心跳间隔：2.0s
- 无智能降频

## 📊 验证标准（STD_ENV_VIDEO_V1）

使用 `test_video_complex_6m42s.mp4` 作为标准测试视频。

### B2 v0.1 目标指标

1. **总决策数**：
   - v0.2 baseline：100
   - B2 目标：≤ 60（第一阶段）

2. **最小间隔**：
   - 必须 ≥ v0.2 的最小间隔（2.002s）
   - 不能更激进

3. **状态切换 / Protection**：
   - 必须仍然 = 0
   - 不能因为 B2 引入新的抖动

### 验证命令

```bash
# 启用 B2 的验证（需要在代码中设置 enable_b2=True）
python3 examples/c1_v02_real_input_validation.py \
  --duration 7 \
  --video test_video_complex_6m42s.mp4
```

## 📈 统计信息

B2 提供统计信息用于验证和调试：

```python
stats = b2_gate.get_stats()
# {
#   "total_checks": 1000,
#   "suppressed_by_stability": 50,
#   "suppressed_by_redundancy": 30,
#   "suppressed_by_complexity": 20,
#   "effective_heartbeat_adjustments": 10,
# }
```

## 🔄 未来扩展

### 模型集成（B2 v0.2+）

未来可以引入小模型来预测"下一段时间是否值得频繁决策"：

```python
{
  "heartbeat_multiplier": 1.5,
  "confidence": 0.82
}
```

**前提条件**：
- B2 v0.1 规则版跑稳
- 验证指标达标
- 再引入模型层

## ⚠️ 重要约束

1. **不越权**：B2 不返回 decision，不修改 state
2. **强制事件放行**：状态切换和 Protection 触发必须产出决策
3. **向后兼容**：默认不启用 B2，保持 v0.2 行为
4. **工程级标准**：所有版本必须在 STD_ENV_VIDEO_V1 上 ≥ 当前表现

