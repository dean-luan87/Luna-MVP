# Luna Badge v1.4.2 模块实现文档

## 📋 概述

本文档描述了 v1.4.2 版本新增的模块骨架，包括视觉调度、系统恢复、任务管理等核心功能。

## 📁 文件结构

```
luna_badge_v1_2/
├── core/
│   ├── vision/
│   │   ├── camera_router.py         # ✅ 多摄像头调度
│   │   ├── vision_scheduler.py      # ✅ 视觉推理频率调度
│   │   └── vision_fail_safe.py      # ✅ 视觉 Plan-B / 降级机制
│   ├── system/
│   │   ├── __init__.py              # ✅ 系统模块导出
│   │   ├── system_recovery_center.py  # ✅ 系统级 Plan-B
│   │   └── safe_mode.py             # ✅ 安全模式
│   └── task/
│       ├── task_transition_manager.py  # ✅ 任务结束判断 × 切换
│       ├── multi_target_buffer.py      # ✅ 多目标缓存
│       └── query_bus.py                # ✅ 问询总线
└── tests/
    ├── test_vision_performance.py   # ✅ 视觉性能测试
    ├── test_plan_b.py               # ✅ Plan-B 测试
    ├── test_task_transition.py     # ✅ 任务转换测试
    └── test_query_bus.py           # ✅ 问询总线测试
```

## 🔧 模块说明

### 1. Vision 模块

#### 1.1 `camera_router.py` - 多摄像头调度

**功能**：在"前视 + 下视"多摄像头模式下，根据场景选择当前使用的摄像头。

**核心接口**：
- `select_camera(context)` - 根据上下文选择摄像头
- `get_active_camera()` - 获取当前激活的摄像头
- `switch_camera(cam)` - 手动切换摄像头
- `set_camera_available(cam, available)` - 设置摄像头可用状态

**使用示例**：
```python
router = CameraRouter()
router.set_camera_available("down", True)
router.select_camera({"need_down_view": True, "mode": "stairs"})
active = router.get_active_camera()  # "down"
```

#### 1.2 `vision_scheduler.py` - 视觉推理频率调度

**功能**：根据 CPU、移动情况、任务类型动态调节 YOLO/视觉模型的调用频率。

**核心接口**：
- `should_infer(ctx)` - 判断是否应在当前帧执行推理
- `update_mode(ctx)` - 根据上下文更新调度模式
- `get_mode()` - 获取当前调度模式

**调度模式**：
- `fast`: 每帧都可推理（间隔 0.0 秒）
- `smart`: 智能模式（间隔 0.3 秒）
- `low`: 低功耗模式（间隔 0.8 秒）

**使用示例**：
```python
scheduler = VisionScheduler()
ctx = SchedulerContext(
    cpu_load=0.6,
    motion_detected=True,
    task_priority=9,
    last_infer_ts=time.time() - 0.4,
    now_ts=time.time(),
)
if scheduler.should_infer(ctx):
    # 执行推理
    pass
```

#### 1.3 `vision_fail_safe.py` - 视觉 Plan-B / 降级机制

**功能**：当视觉管线故障或延迟过高时，触发降级策略。

**核心接口**：
- `report_infer_timeout()` - 报告推理超时
- `report_model_error()` - 报告模型错误
- `report_camera_error()` - 报告摄像头错误
- `get_state()` - 获取当前降级状态
- `get_current_strategy()` - 获取降级策略建议

**降级状态**：
- `normal`: 正常模式
- `degraded`: 降级模式（使用 Tiny 模型、降低分辨率）
- `critical`: 严重模式（进入 SafeMode）

**使用示例**：
```python
failsafe = VisionFailSafe()
failsafe.set_degraded_callback(lambda: switch_to_tiny_model())
failsafe.report_infer_timeout()
if failsafe.get_state() == "degraded":
    strategy = failsafe.get_current_strategy()
    # strategy = {"model_type": "tiny", "resolution": "half", ...}
```

### 2. System 模块

#### 2.1 `system_recovery_center.py` - 系统级 Plan-B

**功能**：统一处理"模块挂掉、CPU 超载、内存异常"等系统级问题。

**核心接口**：
- `register_module(name, timeout)` - 注册需要监控的模块
- `update_heartbeat(name)` - 更新模块心跳
- `tick()` - 周期性检查（建议每 1 秒调用一次）
- `get_health_status()` - 获取系统健康状态

**使用示例**：
```python
def get_cpu_load():
    return psutil.cpu_percent() / 100.0

def enter_safe_mode():
    safe_mode_manager.enter()

center = RecoveryCenter(
    get_cpu_load=get_cpu_load,
    safe_mode_enter=enter_safe_mode,
    restart_vision=restart_vision_module,
    restart_speech=restart_speech_module,
)

center.register_module("vision", timeout_seconds=5.0)
center.register_module("speech", timeout_seconds=5.0)

# 在主循环中
while True:
    center.update_heartbeat("vision")
    center.tick()
    time.sleep(1.0)
```

#### 2.2 `safe_mode.py` - 安全模式

**功能**：在严重异常时，仍能提供最低限度的安全能力。

**核心接口**：
- `enter()` - 进入安全模式
- `exit()` - 退出安全模式
- `is_active()` - 检查是否处于安全模式
- `handle_frame(ctx)` - 处理单帧信息，做基本防撞提示

**使用示例**：
```python
def tts_say(text):
    tts_manager.speak(text)

safe_mode = SafeModeManager(tts_say=tts_say)
safe_mode.enter()

ctx = SafeModeContext(obstacle_distance=0.8)
safe_mode.handle_frame(ctx)  # 会播报"前方一米内有障碍物，请小心。"
```

### 3. Task 模块

#### 3.1 `task_transition_manager.py` - 任务结束判断 × 切换

**功能**：判断当前导航任务是否应该结束、暂停、切换。

**核心接口**：
- `decide(ctx)` - 根据上下文决定任务状态
- `set_distance_threshold(threshold)` - 设置距离阈值
- `set_stationary_threshold(threshold)` - 设置原地停留阈值

**决策结果**：
- `TaskDecision.KEEP` - 保持任务
- `TaskDecision.ASK_END` - 向用户发起问询
- `TaskDecision.END` - 结束任务

**使用示例**：
```python
def ask_user_if_end():
    query_bus.push_query("您是否已到达目的地？")

mgr = TaskTransitionManager(ask_end_callback=ask_user_if_end)
ctx = TaskContext(
    position=PositionState(
        at_target=True,
        distance_to_target=0.5,
        stationary_seconds=0,
    ),
    intent=UserIntentState(want_stop=False, want_continue=False),
)
decision = mgr.decide(ctx)  # TaskDecision.ASK_END
```

#### 3.2 `multi_target_buffer.py` - 多目标缓存

**功能**：支持"多个目标顺序执行"的缓存结构。

**核心接口**：
- `add_target(target)` - 添加目标到队列
- `start()` - 开始执行第一个目标
- `complete_current()` - 标记当前目标完成，返回下一个
- `get_current()` - 获取当前正在执行的目标
- `get_next()` - 获取下一个目标
- `is_finished()` - 检查是否所有目标都已完成

**使用示例**：
```python
buffer = MultiTargetBuffer(max_targets=3)

target1 = Target(id="1", name="711", lat=39.9, lng=116.4)
target2 = Target(id="2", name="医院", lat=39.91, lng=116.41)

buffer.add_target(target1)
buffer.add_target(target2)
current = buffer.start()  # target1

# 完成第一个目标
next_target = buffer.complete_current()  # target2
```

#### 3.3 `query_bus.py` - 问询总线

**功能**：统一管理所有"向用户发起问询"的需求。

**核心接口**：
- `push_query(text, priority, timeout, on_resolved, on_timeout)` - 添加问询
- `tick()` - 定期调用，驱动问询流程
- `resolve_active(result)` - 解决当前活跃的问询
- `cancel_query(query_id)` - 取消指定的问询

**使用示例**：
```python
def tts_say(text):
    tts_manager.speak(text)

bus = QueryBus(tts_say=tts_say)

def on_resolved(result):
    if result.get("answer") == "yes":
        task_manager.end_current_task()

query_id = bus.push_query(
    "您是否已到达目的地？",
    priority=8,
    timeout_seconds=15.0,
    on_resolved=on_resolved,
)

# 在主循环中
while True:
    bus.tick()
    # 如果用户回答了
    if user_said_yes:
        bus.resolve_active({"answer": "yes"})
    time.sleep(0.1)
```

## 🧪 测试

所有模块都提供了对应的测试文件：

- `test_vision_performance.py` - 测试视觉调度器
- `test_plan_b.py` - 测试降级机制和恢复中心
- `test_task_transition.py` - 测试任务转换管理器
- `test_query_bus.py` - 测试问询总线

运行测试：
```bash
cd luna_badge_v1_2
python -m pytest tests/test_vision_performance.py
python -m pytest tests/test_plan_b.py
python -m pytest tests/test_task_transition.py
python -m pytest tests/test_query_bus.py
```

## 📝 下一步建议

1. **集成到主循环**：将新模块集成到现有的主循环中
2. **配置参数调优**：根据实际运行情况调整阈值和参数
3. **日志和监控**：添加详细的日志记录和监控指标
4. **完善回调逻辑**：实现降级回调中的具体逻辑（切换模型、降低分辨率等）

## 🔗 相关文档

- 主循环集成示例（待补充）
- 与现有 navigation / tts_manager / memory_store 的集成点（待补充）















