# Luna Badge 核心模块目录结构

## 📂 核心模块（core/）

```
core/
├── path_evaluator.py              # 路径评估决策
├── speech_style_manager.py        # 播报风格控制
├── user_feedback_handler.py       # 用户反馈响应处理
└── event_bus.py                   # 事件总线（辅助模块）
```

## ✅ 模块说明

### 1. path_evaluator.py
**功能**: 聚合多个感知模块输出，判断当前路径是否安全通行

**主要类**:
- `PathStatus`: 路径状态枚举（normal, caution, reroute, stop）
- `ReasonType`: 原因类型枚举
- `PathEvaluation`: 路径评估结果
- `PathEvaluator`: 路径评估器

**调用关系**: 
- 调用 `speech_style_manager.py` 获取播报风格

### 2. speech_style_manager.py
**功能**: 根据路径评估结果和环境场景，控制TTS播报的风格（语气/情绪）

**主要类**:
- `SpeechStyle`: 播报风格枚举（cheerful, gentle, empathetic, serious, urgent）
- `PathStatus`: 路径状态枚举（与path_evaluator一致）
- `TTSConfig`: TTS配置
- `SpeechStyleOutput`: 播报风格输出
- `SpeechStyleManager`: 播报策略控制器

**映射关系**:
- normal → cheerful（轻松提示）
- caution → gentle（温和引导）
- reroute → empathetic（关切建议）
- stop → urgent（紧急指令）

### 3. user_feedback_handler.py
**功能**: 接收用户的语音反馈、静默行为等信号，对导航/播报逻辑进行微调

**主要类**:
- `FeedbackType`: 反馈类型枚举
- `FeedbackAction`: 反馈动作枚举
- `UserFeedback`: 用户反馈
- `FeedbackResponse`: 反馈响应
- `UserPreference`: 用户偏好
- `UserFeedbackHandler`: 用户反馈处理器

**持久化**:
- `location_corrections.json` - 地点纠错记录
- `speech_preferences.json` - 语音偏好

### 4. event_bus.py
**功能**: 模块间消息传递和事件调度，特别是TTS播报

**主要类**:
- `EventType`: 事件类型枚举
- `Event`: 事件
- `EventBus`: 事件总线

**事件类型**:
- TTS_BROADCAST - TTS播报事件
- NAVIGATION_UPDATE - 导航更新
- VISION_DETECTED - 视觉检测
- USER_FEEDBACK - 用户反馈
- SYSTEM_LOG - 系统日志

## 🔗 调用关系图

```
path_evaluator.py
    ↓
speech_style_manager.py
    ↓
    ├→ event_bus.py (TTS播报)
    └→ user_feedback_handler.py (用户偏好)

user_feedback_handler.py
    ↓
    location_corrections.json
    speech_preferences.json
```

## ✅ 验证状态

所有核心模块已按要求放置在 `core/` 目录下：
- ✅ path_evaluator.py
- ✅ speech_style_manager.py
- ✅ user_feedback_handler.py
- ✅ event_bus.py

---

**更新日期**: 2025年10月27日  
**版本**: v1.0  
**状态**: ✅ 目录结构符合要求
