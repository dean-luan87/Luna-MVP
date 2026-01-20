# v1.4.2 完整交付检查清单

## ✅ 1-4 项全部完成

### 【1】TTS / ASR 模块对接 ✅

#### 文件
- ✅ `core/speech/speech_pipeline.py` - 完整语音管线（200+ 行）

#### 功能
- ✅ ASR 结果进入 QueryBus（如果有活跃问询）
- ✅ ASR 结果进入普通指令处理（如果没有问询）
- ✅ IntentParser 意图解析器
- ✅ 指令处理器注册机制
- ✅ TTS 播报接口
- ✅ 语音模块重启机制
- ✅ 心跳更新机制

#### 使用示例
```python
speech_pipeline = SpeechPipeline(
    asr=asr_module,
    tts=tts_module,
    query_bus=query_bus,
    recovery_center=recovery_center,
)

# 注册指令处理器
speech_pipeline.register_command_handler("stop", handle_stop)

# 启动循环
speech_pipeline.loop_sync()  # 同步版本
# 或
await speech_pipeline.loop()  # 异步版本
```

### 【2】导航模块对接 ✅

#### 文件
- ✅ `core/navigation/navigation_controller.py` - 完整导航控制器（300+ 行）

#### 功能
- ✅ NavigationController 类（step/start/stop）
- ✅ NavigationState 状态管理
- ✅ MapAPI 接口（简化版本，可替换）
- ✅ 对接 TaskTransitionManager
- ✅ 对接 MultiTargetBuffer
- ✅ 对接 QueryBus
- ✅ 目标到达自动问询下一个
- ✅ YES/NO 处理逻辑

#### 使用示例
```python
nav_controller = NavigationController(
    map_api=map_api,
    tts=tts_module,
    multi_target_buffer=multi_target_buffer,
    query_bus=query_bus,
    task_transition=task_transition_manager,
)

# 启动导航
nav_controller.start(target)

# 每帧调用
nav_state = nav_controller.step(vision_objects)
```

### 【3】视觉推理模块对接 ✅

#### 文件
- ✅ `core/vision/vision_pipeline.py` - 已更新（增加模型切换）

#### 功能
- ✅ 调度器集成（scheduler）
- ✅ 摄像头选择（camera_router）
- ✅ 降级机制（fail_safe）
- ✅ 心跳更新（recovery_center）
- ✅ 错误处理（摄像头/超时/模型错误）
- ✅ **模型切换逻辑**（degraded → Tiny）

#### 更新内容
- ✅ 增加 `model_tiny_predict` 参数
- ✅ 增加 `recovery_center` 参数
- ✅ 实现 `_on_degraded()` 回调
- ✅ 实现 `_on_critical()` 回调
- ✅ `infer()` 方法中实现模型切换

### 【4】模型切换逻辑 ✅

#### 实现位置
- ✅ `core/vision/vision_pipeline.py` 的 `infer()` 方法

#### 逻辑
```python
# 根据降级状态选择模型
if fail_safe_state == "degraded" and self.model_tiny_predict:
    current_model = self.model_tiny_predict  # Tiny 模型
elif fail_safe_state == "critical" and self.model_tiny_predict:
    current_model = self.model_tiny_predict  # Tiny 模型
else:
    current_model = self.model_predict  # 主模型
```

#### 回调
- ✅ `_on_degraded()` - 降级时触发
- ✅ `_on_critical()` - 严重错误时触发

### 【额外】QueryBus TTS 对接 ✅

#### 文件
- ✅ `core/task/query_bus.py` - 已更新

#### 功能
- ✅ `attach_tts()` 方法
- ✅ 自动调用 TTS 播报问询内容
- ✅ 错误处理

## 📁 完整文件清单

### 核心模块（8个）
1. ✅ `core/vision/camera_router.py`
2. ✅ `core/vision/vision_scheduler.py`
3. ✅ `core/vision/vision_fail_safe.py`
4. ✅ `core/system/system_recovery_center.py`
5. ✅ `core/system/safe_mode.py`
6. ✅ `core/task/task_transition_manager.py`
7. ✅ `core/task/multi_target_buffer.py`
8. ✅ `core/task/query_bus.py` (已更新 TTS 对接)

### 集成点（6个）
9. ✅ `core/vision/vision_pipeline.py` (已更新模型切换)
10. ✅ `core/system/system_loop.py`
11. ✅ `core/navigation/navigation_controller_integration.py`
12. ✅ `core/speech/speech_pipeline_integration.py`
13. ✅ **`core/speech/speech_pipeline.py`** (新增，完整对接)
14. ✅ **`core/navigation/navigation_controller.py`** (新增，完整对接)

### 主循环（1个）
15. ✅ `core/main_loop_final.py`

### 测试套件（2个）
16. ✅ `tests/test_stress_vision.py`
17. ✅ `tests/test_v1_4_2_complete.py`

## 🎯 功能链完整性

### ✅ 视觉 → 导航 → 任务转换
```
VisionPipeline.process_frame()
  → NavigationController.step()
    → TaskTransitionManager.decide()
      → QueryBus.push_query() (如果 ASK_END)
```

### ✅ ASR → QueryBus → 任务处理
```
SpeechPipeline.loop()
  → ASR.listen()
    → QueryBus.resolve_active() (如果有活跃问询)
      → 回调处理（结束任务/继续下一个目标等）
```

### ✅ 降级 → 模型切换
```
VisionFailSafe.report_infer_timeout()
  → state = "degraded"
    → VisionPipeline.infer() 自动切换到 Tiny 模型
```

### ✅ 心跳 → 重启
```
RecoveryCenter.tick()
  → 检查心跳超时
    → restart_vision() / restart_speech()
      → 模块重启
```

## ✅ 完成度统计

- **【1】TTS/ASR 对接**: 100% ✅
- **【2】导航模块对接**: 100% ✅
- **【3】视觉推理对接**: 100% ✅
- **【4】模型切换逻辑**: 100% ✅
- **QueryBus TTS 对接**: 100% ✅

## 🚀 可以直接使用

所有 1-4 项已完成，代码可以直接使用：

1. **语音管线**: 完整的 ASR/TTS 对接，支持问询和普通指令
2. **导航控制器**: 完整的导航逻辑，支持多目标和任务转换
3. **视觉管线**: 完整的推理流程，支持模型切换
4. **模型切换**: 自动根据降级状态切换模型

**所有 TODO 对接点已补齐，可以直接进入测试阶段！**















