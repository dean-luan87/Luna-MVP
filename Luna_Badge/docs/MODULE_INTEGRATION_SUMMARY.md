# 模块间调用集成总结

## 📋 实现目标

实现模块间调用需求：
1. `path_evaluator.py` → 调用 `speech_style_manager.py` 获取播报风格
2. 所有模块 → 通过事件总线调用TTS播报系统
3. `user_feedback_handler.py` → 持久化到JSON文件

## ✅ 实现的调用关系

### 1. 路径评估 → 播报风格

**调用链**: `path_evaluator.py` → `speech_style_manager.py`

**实现方式**:
- 在 `path_evaluator.py` 中添加延迟导入机制
- 提供 `get_speech_style_manager()` 函数获取播报风格管理器
- 支持根据路径状态自动获取播报风格

**使用示例**:
```python
from core.path_evaluator import evaluate_path
from core.speech_style_manager import get_speech_style

# 评估路径
result = evaluate_path(crowd_density={'level': 'very_crowded'})

# 获取播报风格
style = get_speech_style(result.status.value)
```

**输出示例**:
```json
{
  "speech_style": "empathetic",
  "tts_config": {
    "voice": "zh-CN-XiaoxiaoNeural",
    "style": "empathetic",
    "rate": 0.9,
    "pitch": 0.9,
    "volume": 1.0
  }
}
```

### 2. 事件总线 → TTS播报

**调用链**: `所有模块` → `event_bus.py` → `TTS系统`

**实现方式**:
- 创建 `event_bus.py` 模块，实现事件总线系统
- 支持事件订阅和发布
- 专门的TTS播报接口 `broadcast_tts()`

**使用示例**:
```python
from core.event_bus import get_event_bus

bus = get_event_bus()
bus.start()

# 定义TTS处理器
def tts_handler(data):
    print(f'TTS播报: {data["text"]}')

bus.set_tts_handler(tts_handler)

# 播报消息
bus.broadcast_tts('测试播报', style='empathetic')
```

**事件类型**:
- `TTS_BROADCAST` - TTS播报事件
- `NAVIGATION_UPDATE` - 导航更新
- `VISION_DETECTED` - 视觉检测
- `USER_FEEDBACK` - 用户反馈
- `SYSTEM_LOG` - 系统日志

### 3. 用户反馈 → 持久化

**调用链**: `user_feedback_handler.py` → `JSON文件`

**实现方式**:
- 自动创建 `data/` 目录
- 支持加载和保存
- 文件：
  - `location_corrections.json` - 地点纠错记录
  - `speech_preferences.json` - 语音偏好

**使用示例**:
```python
from core.user_feedback_handler import UserFeedbackHandler

handler = UserFeedbackHandler()

# 处理纠错（自动保存到文件）
result = handler.process_voice_feedback(
    '这不是电梯，这是扶梯',
    {'target': 'signboard_label', 'original_value': '电梯'}
)

# 更新偏好（自动保存到文件）
handler._update_preference('broadcast_frequency', 'low')
```

**文件格式**:

`location_corrections.json`:
```json
{
  "corrections": [
    {
      "original": "电梯",
      "correction": "这不是电梯，这是扶梯",
      "target": "elevator",
      "timestamp": 1698475200.0,
      "verified": false
    }
  ]
}
```

`speech_preferences.json`:
```json
{
  "allow_crowded_passage": true,
  "broadcast_frequency": "low",
  "tone_preference": "default",
  "auto_confirm_silence": true,
  "max_repeat_count": 3
}
```

## ✅ 测试结果

### 测试1: 路径评估 → 播报风格
- ✅ 路径评估: `reroute`
- ✅ 播报风格: `empathetic`
- ✅ TTS配置获取成功

### 测试2: 事件总线 → TTS播报
- ✅ 事件总线启动成功
- ✅ TTS处理器注册成功
- ✅ 播报消息分发成功

### 测试3: 用户反馈 → 持久化
- ✅ 纠错记录已保存到文件
- ✅ 语音偏好已保存到文件
- ✅ 文件读写正常

## 🎯 架构优势

1. **解耦合**: 使用事件总线避免模块间直接依赖
2. **可扩展**: 轻松添加新的事件类型和处理器
3. **持久化**: 自动保存重要数据，断电不丢失
4. **异步**: 事件总线使用队列和线程，不阻塞主流程

---

**实现日期**: 2025年10月27日  
**版本**: v1.0  
**状态**: ✅ 所有调用关系测试通过
