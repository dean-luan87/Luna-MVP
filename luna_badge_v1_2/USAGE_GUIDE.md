# Luna Badge v1.4.2 使用指南

## 🚀 快速开始

### 1. 验证安装

```bash
cd luna_badge_v1_2

# 验证所有模块
python3 verify_v1_4_2.py
```

预期输出：
```
✅ 所有模块导入成功！
✅ 所有模块实例化成功！
🎉 验证通过！所有模块正常！
```

### 2. 运行测试

```bash
# 运行所有 v1.4.2 测试
pytest -q tests/test_vision_scheduler.py tests/test_vision_fail_safe.py tests/test_task_transition.py tests/test_query_bus.py tests/test_stress_vision.py
```

预期输出：
```
============================== 6 passed in 0.09s ===============================
```

### 3. 运行主程序

```bash
python3 main.py
```

## 📖 详细使用说明

### 主程序使用

#### 基本运行

```bash
cd luna_badge_v1_2
python3 main.py
```

#### 程序行为

1. **自动启动导航**
   - 程序启动后会自动创建一个示例目标："示例地点"
   - 自动开始导航

2. **导航过程**
   - 系统会持续读取摄像头（Dummy 模式）
   - 计算距离并播报导航提示
   - 当距离 < 3.0 米时，会播报距离信息

3. **到达目标**
   - 当距离 < 1.5 米时，系统会问询："您已经接近目的地，需要结束当前任务吗？"
   - 等待用户回答（15 秒超时）

4. **用户交互**
   - **ASR 输入**：在终端中输入文本
     - 输入"是"、"好的"、"结束" → 结束任务
     - 输入"否"、"不要"、"继续" → 继续导航
   - **TTS 输出**：查看日志中的 `[TTS]` 标记

5. **退出程序**
   - 按 `Ctrl+C` 退出

#### 运行示例

```bash
$ python3 main.py

[TTS] 开始前往 示例地点
[NAV] distance to 示例地点: 9.5
...
[TTS] 距离 示例地点 还有 2.5 米。
[TTS] 您已经接近目的地，需要结束当前任务吗？

# 此时在终端输入：
是

[TTS] 好的，已结束任务。
```

### 模块使用

#### 1. 系统监控 (SystemMonitor)

```python
from core.system.system_monitor import SystemMonitor

monitor = SystemMonitor()
cpu_usage = monitor.cpu_usage()  # 返回 0.0-1.0 的 CPU 使用率
```

#### 2. 安全模式 (SafeModeManager)

```python
from core.system.safe_mode import SafeModeManager, SafeModeContext

def tts_say(text: str):
    print(f"[TTS] {text}")

safe_mode = SafeModeManager(tts_say)
safe_mode.enter()  # 进入安全模式
safe_mode.handle_frame(SafeModeContext(obstacle_distance=0.8))  # 处理障碍物
safe_mode.exit()  # 退出安全模式
```

#### 3. 系统恢复中心 (RecoveryCenter)

```python
from core.system.system_recovery_center import RecoveryCenter

recovery = RecoveryCenter(
    get_cpu_load=lambda: 0.5,
    safe_mode_enter=safe_mode.enter,
    restart_vision=lambda: print("重启视觉"),
    restart_speech=lambda: print("重启语音"),
)

recovery.register_module("vision", timeout_seconds=5.0)
recovery.update_heartbeat("vision")
recovery.tick()  # 每秒调用一次
```

#### 4. 摄像头路由 (CameraRouter)

```python
from core.vision.camera_router import CameraRouter, DummyCameraManager

router = CameraRouter()
router.set_camera_available("down", True)  # 启用下视摄像头
cam_id = router.select_camera(context={"need_down_view": True})
active_cam = router.get_active_camera()  # 获取当前激活的摄像头

# 读取帧
camera_manager = DummyCameraManager()
frame = camera_manager.read(active_cam)
```

#### 5. 视觉调度器 (VisionScheduler)

```python
from core.vision.vision_scheduler import VisionScheduler, SchedulerContext
import time

scheduler = VisionScheduler()
ctx = SchedulerContext(
    cpu_load=0.3,
    motion_detected=True,
    task_priority=8,
    last_infer_ts=time.time() - 0.5,
    now_ts=time.time(),
)

if scheduler.should_infer(ctx):
    # 执行推理
    print(f"当前模式: {scheduler.mode}")  # fast/smart/low
```

#### 6. 视觉降级 (VisionFailSafe)

```python
from core.vision.vision_fail_safe import VisionFailSafe, FailSafeConfig

config = FailSafeConfig(
    timeout_threshold=3,
    model_error_threshold=2,
    camera_error_threshold=2,
    cooldown_seconds=10,
)

fail_safe = VisionFailSafe(config)
fail_safe.report_infer_timeout()  # 报告推理超时
fail_safe.report_model_error()    # 报告模型错误
fail_safe.report_camera_error()   # 报告摄像头错误

state = fail_safe.get_state()  # "normal" 或 "degraded"
if state == "degraded":
    # 切换到 Tiny 模型
    model = tiny_model
```

#### 7. 任务转换管理器 (TaskTransitionManager)

```python
from core.task.task_transition_manager import (
    TaskTransitionManager,
    TaskContext,
    PositionState,
    UserIntentState,
    TaskDecision,
)

def ask_end_callback():
    print("询问用户是否结束任务")

manager = TaskTransitionManager(ask_end_callback)

ctx = TaskContext(
    position=PositionState(
        at_target=False,
        distance_to_target=1.0,
        stationary_seconds=0.0,
    ),
    intent=UserIntentState(
        want_stop=False,
        want_continue=True,
    ),
)

decision = manager.decide(ctx)  # TaskDecision.KEEP/ASK_END/END
```

#### 8. 多目标缓存 (MultiTargetBuffer)

```python
from core.task.multi_target_buffer import MultiTargetBuffer, Target

buffer = MultiTargetBuffer()

# 添加目标
target1 = Target(id="1", name="目的地A", lat=34.0, lng=118.0, extra={})
target2 = Target(id="2", name="目的地B", lat=34.1, lng=118.1, extra={})
buffer.add_target(target1)
buffer.add_target(target2)

# 开始第一个目标
current = buffer.start()  # 返回 target1

# 完成当前目标，获取下一个
next_target = buffer.complete_current()  # 返回 target2
```

#### 9. 问询总线 (QueryBus)

```python
from core.task.query_bus import QueryBus, Query
import time

def tts_say(text: str):
    print(f"[TTS] {text}")

query_bus = QueryBus(tts_say)

# 推送问询
query = Query(
    id="end_task",
    priority=10,
    created_ts=time.time(),
    text="您已经接近目的地，需要结束当前任务吗？",
    timeout_seconds=15.0,
    on_resolved=lambda result: print(f"用户回答: {result}"),
    on_timeout=lambda: print("超时，使用默认策略"),
)

query_bus.push_query(query)

# 在主循环中调用
query_bus.tick()  # 每秒调用一次

# 当用户回答时
if query_bus.has_active_query():
    query_bus.resolve_active({"answer": "yes"})
```

#### 10. 导航控制器 (NavigationController)

```python
from navigation.navigation_controller import NavigationController, NavState

def tts_say(text: str):
    print(f"[TTS] {text}")

nav = NavigationController(tts_say)

# 开始导航
target = Target(id="1", name="目的地A", lat=34.0, lng=118.0, extra={})
nav.start(target)

# 导航步骤
vision_objects = [{"type": "obstacle", "distance": 1.2}]
nav_state: NavState = nav.step(vision_objects)

if nav_state.at_target:
    nav.stop()
```

#### 11. 意图解析器 (IntentParser)

```python
from speech.intent_parser import IntentParser

parser = IntentParser()

# 解析用户输入
result = parser.parse("是的，结束任务")
# {"intent": "answer", "answer": "yes"}

result = parser.parse("不要，继续导航")
# {"intent": "answer", "answer": "no"}

result = parser.parse("停止导航")
# {"intent": "stop_navigation"}
```

#### 12. 语音管线 (SpeechPipeline)

```python
from speech.speech_pipeline import SpeechPipeline, DummyASR, DummyTTS
from core.task.query_bus import QueryBus

tts = DummyTTS()
asr = DummyASR()
query_bus = QueryBus(tts.speak)
intent_parser = IntentParser()

pipeline = SpeechPipeline(
    asr=asr,
    tts=tts,
    query_bus=query_bus,
    intent_parser=intent_parser,
)

# 在后台线程运行
import threading
thread = threading.Thread(target=pipeline.loop, daemon=True)
thread.start()
```

## 🔧 配置说明

### 视觉调度器配置

在代码中修改 `VisionScheduler` 的间隔：

```python
scheduler = VisionScheduler()
scheduler._intervals = {
    "fast": 0.0,   # 快速模式：无延迟
    "smart": 0.3,  # 智能模式：0.3 秒间隔
    "low": 0.8,    # 低功耗模式：0.8 秒间隔
}
```

### 降级配置

```python
config = FailSafeConfig(
    timeout_threshold=3,        # 超时阈值：3 次
    model_error_threshold=2,    # 模型错误阈值：2 次
    camera_error_threshold=2,  # 摄像头错误阈值：2 次
    cooldown_seconds=10,       # 冷却时间：10 秒
)
```

### 恢复中心配置

```python
recovery.register_module("vision", timeout_seconds=5.0)   # 视觉模块：5 秒超时
recovery.register_module("speech", timeout_seconds=5.0)    # 语音模块：5 秒超时
recovery.register_module("navigation", timeout_seconds=10.0)  # 导航模块：10 秒超时
```

## 🧪 测试使用

### 运行单个测试

```bash
# 测试视觉调度器
pytest tests/test_vision_scheduler.py -v

# 测试视觉降级
pytest tests/test_vision_fail_safe.py -v

# 测试任务转换
pytest tests/test_task_transition.py -v

# 测试问询总线
pytest tests/test_query_bus.py -v

# 压力测试
pytest tests/test_stress_vision.py -v
```

### 运行所有测试

```bash
pytest -q tests/test_vision_scheduler.py tests/test_vision_fail_safe.py tests/test_task_transition.py tests/test_query_bus.py tests/test_stress_vision.py
```

## 📝 常见问题

### Q1: 如何替换 Dummy 模块？

**A**: 替换对应的实现：

```python
# 替换 DummyCameraManager
class RealCameraManager:
    def read(self, camera_id):
        cap = cv2.VideoCapture(0 if camera_id == "front" else 1)
        ret, frame = cap.read()
        return frame if ret else None

# 替换 DummyASR
class RealASR:
    def listen(self):
        # 使用真实的 ASR 实现
        return recognize_speech()

# 替换 DummyTTS
class RealTTS:
    def speak(self, text):
        # 使用真实的 TTS 实现
        synthesize_speech(text)
```

### Q2: 如何添加更多目标？

**A**: 使用 `MultiTargetBuffer`：

```python
buffer = MultiTargetBuffer()
buffer.add_target(Target(id="1", name="地点A", lat=34.0, lng=118.0, extra={}))
buffer.add_target(Target(id="2", name="地点B", lat=34.1, lng=118.1, extra={}))
buffer.add_target(Target(id="3", name="地点C", lat=34.2, lng=118.2, extra={}))
```

### Q3: 如何自定义问询超时时间？

**A**: 在创建 Query 时设置：

```python
query = Query(
    id="custom_query",
    priority=5,
    created_ts=time.time(),
    text="自定义问询",
    timeout_seconds=30.0,  # 30 秒超时
    on_resolved=lambda r: print("已解决"),
    on_timeout=lambda: print("超时"),
)
```

### Q4: 如何调整 CPU 过载阈值？

**A**: 在 `RecoveryCenter` 中修改：

```python
recovery._cpu_threshold = 0.9  # 90% CPU 使用率触发
```

### Q5: 如何禁用下视摄像头？

**A**: 在 `CameraRouter` 中设置：

```python
router.set_camera_available("down", False)
```

## 🎯 最佳实践

1. **主循环频率**
   - 建议主循环 sleep 时间：0.05 秒
   - 避免过于频繁的循环导致 CPU 过载

2. **心跳更新**
   - 每个模块执行后立即更新心跳
   - 确保恢复中心能及时检测到模块状态

3. **问询管理**
   - 避免同时推送多个问询
   - 使用优先级控制问询顺序

4. **错误处理**
   - 所有模块调用都应该有 try-except
   - 及时报告错误到 FailSafe

5. **日志记录**
   - 使用 `get_logger` 获取日志器
   - 重要事件使用 INFO 级别
   - 错误使用 ERROR 级别

## 📚 相关文档

- `README_V1_4_2.md` - 完整交付说明
- `CURSOR_TASK_PACKAGE.md` - Cursor 任务包
- `V1_4_2_COMPLETE_SUMMARY.md` - 完整总结
- `MAIN_RUN_REPORT.md` - 运行报告

## 🆘 获取帮助

如果遇到问题，请检查：

1. **模块导入错误**：运行 `python3 verify_v1_4_2.py`
2. **测试失败**：运行 `pytest -v` 查看详细错误
3. **运行错误**：查看日志中的 ERROR 标记
4. **功能异常**：检查配置文件是否正确

---

**祝使用愉快！** 🎉















