# Fallback / PlanB Policy - Phase-2 完成报告

## 执行时间
2025-12-16

## 目标
填充 Fallback / PlanB Policy 模块，实现「规则驱动、可控、可复盘」的工程机制。

## 定位原则（严格遵守）

✅ **PlanB 不追求聪明，只追求不死**
- 不做自动学习，只执行写好的策略
- PlanB 是 v1.5 可靠性的核心锚点

## 完成的功能模块

### 1. fallback_policy.yaml - 策略配置文件
- ✅ 定义了三个任务域的完整策略（navigation, safety, inquiry）
- ✅ 支持四种 action：switch_model (B1), degrade_capability (B2), cross_domain (B3), abort
- ✅ 每个任务域配置了 max_attempts 和 cooldown_ms
- ✅ 支持多种 trigger：low_confidence, model_failure, conflict, timeout, invalid_output, exhausted
- ✅ 包含 default 策略作为兜底

### 2. fallback_executor.py - 执行器逻辑
- ✅ 策略加载与解析
- ✅ Trigger 匹配（支持精确匹配和部分匹配）
- ✅ 尝试次数计数与 max_attempts 检查
- ✅ 冷却时间机制
- ✅ 运行时状态管理（attempts, last_attempt_ts）
- ✅ 返回"行动描述"而不是直接执行
- ✅ 支持重置功能（用于测试或任务重启）

## 核心设计决策

1. **策略即配置**
   - 所有 fallback 路径完全来自 YAML 配置
   - 不改代码即可调整兜底策略

2. **返回行动描述而非直接执行**
   - FallbackExecutor 返回 action/target/reason/attempt 等描述
   - TaskChain 根据描述执行，保持可控

3. **冷却期机制**
   - 防止频繁 fallback
   - 冷却期内返回 wait，不增加 attempt

4. **确定性中止**
   - 达到 max_attempts 必然触发 exhausted
   - 强制中止，不继续尝试

## 验收标准验证

✅ **1. 任何 fallback 都有明确 trigger**
- 测试通过：所有 trigger 都能匹配到对应策略

✅ **2. 每一次 fallback 都能数清第几次**
- 测试通过：attempt 计数准确递增

✅ **3. 达到 max_attempts 必然中止**
- 测试通过：达到最大次数后触发 exhausted，强制中止

✅ **4. fallback 路径完全来自配置**
- 测试通过：不同 trigger 对应不同的 action/plan，完全由配置决定

✅ **5. 不改代码即可调整兜底策略**
- 通过修改 YAML 文件即可调整策略，无需改代码

## 测试结果

### 基础功能测试（test_fallback_basic.py）

✅ **测试 1: Trigger 匹配**
- 所有 trigger 都能正确匹配到策略

✅ **测试 2: 尝试次数计数**
- attempt 准确递增：1, 2, 3

✅ **测试 3: 最大尝试次数强制中止**
- 达到 max_attempts 后正确触发 exhausted

✅ **测试 4: 配置驱动的路径**
- 不同 trigger 对应不同的 action/plan

✅ **测试 5: 冷却时间**
- 冷却期检测正常工作

✅ **测试 6: 不同任务域的策略**
- 各任务域的策略独立配置

✅ **测试 7: 重置功能**
- reset() 功能正常

**所有核心测试通过 ✓**

## 代码统计

- Python 模块：1 个（fallback_executor.py）
- YAML 配置：1 个（fallback_policy.yaml）
- 测试文件：1 个（test_fallback_basic.py）
- 代码行数：~300 行（不含注释和空行）

## 与 MOC 的对接

FallbackExecutor 接收来自 MOC 的 decision.reason，返回行动描述：

```python
# MOC 返回
{
    "decision": "fallback",
    "reason": "Conflicts detected and no primary/secondary model match..."
}

# FallbackExecutor 返回
{
    "action": "switch_model",
    "target": "backup_vision_model",
    "reason": "low_confidence",
    "attempt": 1,
    "plan": "B1",
    "description": "主模型置信度低，切换到备用视觉模型"
}
```

## 下一步

✅ **Fallback / PlanB Policy 第一版结构完成**

可以进入 Phase-2 模块 3：**TaskChain 稳定化（中断 / 恢复 / 插入任务）**

因为：
- MOC 决定"要不要信模型"
- PlanB 决定"信不了怎么办"
- TaskChain 决定"系统还能不能继续跑"

## 状态

✅ **Phase-2 模块 2（Fallback / PlanB Policy）已完成**

所有功能已实现并通过测试，可以开始模块 3 的填充工作。





