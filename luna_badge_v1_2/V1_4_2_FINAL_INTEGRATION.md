# v1.4.2 最终集成完成清单

## ✅ 已完成：1-4 项完整对接

### 【1】TTS / ASR 模块对接 ✅

#### 1.1 ASR 对接
- ✅ `core/speech/speech_pipeline.py` - 完整语音管线
- ✅ 支持 QueryBus 问询回答
- ✅ 支持普通指令处理
- ✅ 意图解析器（IntentParser）

#### 1.2 TTS 对接
- ✅ `query_bus.py` 增加 `attach_tts()` 方法
- ✅ 自动调用 TTS 播报问询内容

#### 1.3 语音故障 Recovery 接口
- ✅ `speech_pipeline.py` 增加 `restart()` 方法
- ✅ 心跳更新机制
- ✅ 对接 RecoveryCenter

### 【2】导航模块对接 ✅

#### 2.1 NavigationController
- ✅ `core/navigation/navigation_controller.py` - 完整导航控制器
- ✅ 对接 MapAPI（简化版本）
- ✅ 对接 MultiTargetBuffer
- ✅ 对接 QueryBus
- ✅ 对接 TaskTransitionManager

#### 2.2 TaskTransition 联动
- ✅ 在 `step()` 中自动调用 `task_transition_manager.decide()`
- ✅ 自动处理 END/ASK_END 决策

#### 2.3 目标切换
- ✅ 目标到达时自动问询下一个目标
- ✅ YES/NO 处理逻辑完整

### 【3】视觉推理模块对接 ✅

#### 3.1 VisionPipeline 完整对接
- ✅ 调度器集成（scheduler）
- ✅ 摄像头选择（camera_router）
- ✅ 降级机制（fail_safe）
- ✅ 心跳更新（recovery_center）

#### 3.2 错误处理
- ✅ 摄像头错误上报
- ✅ 推理超时上报
- ✅ 模型错误上报

### 【4】模型切换逻辑 ✅

#### 4.1 降级模型切换
- ✅ `vision_pipeline.py` 中实现模型切换
- ✅ degraded 模式 → Tiny 模型
- ✅ critical 模式 → Tiny 模型
- ✅ normal 模式 → 主模型

#### 4.2 降级回调
- ✅ `_on_degraded()` 回调实现
- ✅ `_on_critical()` 回调实现

## 📁 新增文件清单

1. ✅ `core/speech/speech_pipeline.py` - 语音管线完整对接
2. ✅ `core/navigation/navigation_controller.py` - 导航控制器完整对接
3. ✅ 更新 `core/vision/vision_pipeline.py` - 增加模型切换逻辑
4. ✅ 更新 `core/task/query_bus.py` - 增加 TTS 对接

## 🔌 集成点说明

### 语音管线集成
```python
# 初始化
speech_pipeline = SpeechPipeline(
    asr=asr_module,
    tts=tts_module,
    query_bus=query_bus,
    recovery_center=recovery_center,
)

# 注册指令处理器
speech_pipeline.register_command_handler("stop", handle_stop_command)

# 启动循环
speech_pipeline.loop_sync()  # 或 loop() 异步版本
```

### 导航控制器集成
```python
# 初始化
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

### 视觉管线集成
```python
# 初始化（带模型切换）
vision_pipeline = VisionPipeline(
    camera_router=camera_router,
    vision_scheduler=vision_scheduler,
    vision_fail_safe=vision_fail_safe,
    model_predict=main_model.predict,
    model_tiny_predict=tiny_model.predict,  # 新增
    recovery_center=recovery_center,  # 新增
)

# 处理帧
results = vision_pipeline.process_frame(...)
```

### QueryBus TTS 对接
```python
# 附加 TTS
query_bus.attach_tts(tts_manager)

# 或初始化时传入
query_bus = QueryBus(tts_say=tts_manager.speak)
```

## 🎯 完整功能链

### 1. 视觉 → 导航 → 任务转换
```
VisionPipeline.process_frame()
  → NavigationController.step()
    → TaskTransitionManager.decide()
      → QueryBus.push_query() (如果 ASK_END)
```

### 2. ASR → QueryBus → 任务处理
```
SpeechPipeline.loop()
  → ASR.listen()
    → QueryBus.resolve_active() (如果有活跃问询)
      → 回调处理（结束任务/继续下一个目标等）
```

### 3. 降级 → 模型切换
```
VisionFailSafe.report_infer_timeout()
  → state = "degraded"
    → VisionPipeline.infer() 自动切换到 Tiny 模型
```

### 4. 心跳 → 重启
```
RecoveryCenter.tick()
  → 检查心跳超时
    → restart_vision() / restart_speech()
      → 模块重启
```

## ⚠️ 待实现的具体逻辑（TODO）

以下部分需要根据实际项目实现：

1. **MapAPI.update_with_vision()** - 实际地图和定位逻辑
2. **ASR.listen()** - 实际 ASR 识别
3. **TTS.speak()** - 实际 TTS 播报
4. **模型加载** - 实际模型加载逻辑
5. **GPS/定位** - 实际位置获取

## ✅ 完成度

- **ASR/TTS 对接**: 100% ✅
- **导航模块对接**: 100% ✅
- **视觉推理对接**: 100% ✅
- **模型切换逻辑**: 100% ✅
- **心跳和重启**: 100% ✅

**所有 1-4 项已完成，可以直接进入测试阶段！**




