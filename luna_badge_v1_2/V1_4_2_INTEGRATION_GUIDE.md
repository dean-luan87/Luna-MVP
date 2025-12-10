# v1.4.2 集成指南

## 📋 已完成模块

### ✅ 步骤 1：视觉管线性能基线重构

1. **camera_router.py** ✅
   - 接入真实摄像头（cv2）
   - 提供统一接口 `get_frame()`
   - 支持前视/下视摄像头切换
   - 配置项：`camera.front.id`, `camera.down.id`, `camera.down.enabled`

2. **vision_scheduler.py** ✅
   - 集成配置中心，支持动态间隔
   - 根据 CPU、移动、任务优先级调整模式
   - 配置项：`scheduler.interval.fast`, `scheduler.interval.smart`, `scheduler.interval.low`

3. **vision_fail_safe.py** ✅
   - 增加日志记录
   - 完善降级回调机制
   - 支持 degraded 和 critical 两种降级状态

### ✅ 步骤 2：系统级 Plan-B 架构注入

1. **system_recovery_center.py** ✅
   - 完善日志记录
   - 实现模块心跳监控
   - CPU 过载检测和 SafeMode 触发

2. **safe_mode.py** ✅
   - 增加日志记录
   - 完善安全模式处理逻辑

### ✅ 步骤 5：主循环重写

1. **main_loop_v1_4_2.py** ✅
   - 多轨调度主循环示例
   - 整合所有 v1.4.2 模块
   - 提供完整的集成框架

## 🔧 待完成集成点

### 步骤 3：任务切换与问询机制接入

#### 3.1 TaskTransitionManager 集成

**需要对接的模块**：
- 导航模块：获取 `distance_to_target`, `at_target`
- 语义理解模块：获取用户意图（`want_stop`, `want_continue`）

**集成示例**：
```python
# 在导航循环中
position_state = PositionState(
    at_target=navigation.is_at_target(),
    distance_to_target=navigation.get_distance_to_target(),
    stationary_seconds=navigation.get_stationary_seconds(),
)

intent_state = UserIntentState(
    want_stop=asr_result.get("intent") == "stop",
    want_continue=asr_result.get("intent") == "continue",
)

task_ctx = TransitionTaskContext(
    position=position_state,
    intent=intent_state,
)
decision = task_transition_manager.decide(task_ctx)
```

#### 3.2 QueryBus 集成

**需要对接的模块**：
- TTS 模块：播报问询内容
- ASR 模块：接收用户回答并调用 `resolve_active()`

**集成示例**：
```python
# 在 ASR 结果处理中
def on_asr_result(text, intent, slots):
    # 检查是否有活跃的问询
    active_query = query_bus.get_active_query()
    if active_query:
        # 解析用户回答
        if intent == "confirm" or "是" in text or "yes" in text.lower():
            query_bus.resolve_active({"answer": "yes"})
        elif intent == "deny" or "否" in text or "no" in text.lower():
            query_bus.resolve_active({"answer": "no"})

# 在主循环中
query_bus.tick()  # 每帧调用
```

### 步骤 4：多目标缓存体系

**集成示例**：
```python
# 添加多个目标
target1 = Target(id="1", name="711", lat=39.9, lng=116.4)
target2 = Target(id="2", name="医院", lat=39.91, lng=116.41)
multi_target_buffer.add_target(target1)
multi_target_buffer.add_target(target2)

# 开始第一个目标
current = multi_target_buffer.start()

# 当目标完成时
def on_target_complete():
    next_target = multi_target_buffer.complete_current()
    if next_target:
        # 问询用户是否继续下一个目标
        query_bus.push_query(
            f"是否前往下一个目的地：{next_target.name}？",
            priority=7,
            on_resolved=lambda r: start_next_target() if r.get("answer") == "yes" else go_idle(),
        )
```

## 📝 配置文件更新

已在 `config/default.yaml` 中添加：

```yaml
# v1.4.2: 多摄像头配置
camera:
  front:
    id: 0
  down:
    id: 1
    enabled: false

# v1.4.2: 视觉调度器配置
scheduler:
  interval:
    fast: 0.0
    smart: 0.3
    low: 0.8
```

## 🧪 测试建议

1. **单元测试**：所有模块都有对应的测试文件
2. **集成测试**：使用 `main_loop_v1_4_2.py` 作为测试框架
3. **压力测试**：见步骤 7

## ⚠️ 注意事项

1. **TODO 标记**：代码中保留了 TODO 注释，标记需要对接的实际模块
2. **回调函数**：部分模块需要外部提供回调（如 TTS、模型切换等）
3. **配置依赖**：确保 ConfigCenter 已初始化
4. **日志系统**：确保 LogManager 已初始化

## 🚀 下一步

1. 对接实际导航模块到 TaskTransitionManager
2. 对接实际 TTS/ASR 模块到 QueryBus
3. 实现视觉模块重启逻辑
4. 实现模型切换逻辑（降级时）
5. 完善日志体系（步骤 6）
6. 创建压力测试脚本（步骤 7）




