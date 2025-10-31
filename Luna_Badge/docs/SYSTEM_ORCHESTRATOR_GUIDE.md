# 🧠 Luna Badge 系统控制中枢使用指南

## 📋 概述

系统控制中枢（System Orchestrator）是 Luna Badge 的"大脑"，统一调度语音、视觉、地图、TTS等子系统，实现"一个指令，多模态响应"。

### 🎯 核心功能

- **🎤 语音控制**：Whisper语音识别 → 意图解析 → 动作执行
- **👁️ 视觉反馈**：YOLO物体检测 → 事件触发 → 语音提醒
- **🧭 路径导航**：目的地提取 → 路径规划 → 实时播报
- **💾 记忆记录**：路径记忆、节点情绪、用户行为
- **🔄 事件驱动**：异步事件处理、状态管理、任务调度

---

## 🧩 架构设计

### 模块关系

```
                    SystemOrchestrator
                    (控制中枢)
                         |
        +----------------+----------------+
        |                |                |
    语音输入         视觉检测        导航记忆
        |                |                |
   Whisper          YOLO/OCR       Navigator
   Recognizer      VisionEngine    Memory/TTS
```

### 核心类

- **SystemOrchestrator**：控制中枢主类
- **SystemState**：系统状态枚举
- **UserIntent**：用户意图枚举
- **VisualEvent**：视觉事件枚举
- **IntentMatch**：意图匹配结果
- **SystemEvent**：系统事件

---

## 📚 API 使用

### 1. 基础初始化

```python
from core.system_orchestrator import SystemOrchestrator
from core.whisper_recognizer import WhisperRecognizer
from core.tts_manager import TTSManager
from core.ai_navigation import AINavigation
from core.memory_store import MemoryStore

# 初始化模块
whisper = WhisperRecognizer(model_name="base")
whisper.load_model()

tts = TTSManager()

navigator = AINavigation()
memory = MemoryStore()
camera = CameraManager()

# 创建控制中枢
orchestrator = SystemOrchestrator(
    whisper_recognizer=whisper,
    tts_manager=tts,
    navigator=navigator,
    memory_manager=memory,
    camera_manager=camera
)

# 启动
orchestrator.start()
```

### 2. 语音输入处理

```python
# 用户说话
orchestrator.handle_voice_input()

# 系统自动完成：
# 1. Whisper识别语音
# 2. 解析用户意图
# 3. 执行对应动作
# 4. 播报反馈
```

#### 支持的意图

| 用户指令 | 意图 | 执行动作 |
|---------|------|---------|
| "我要去厕所" | FIND_TOILET | 调用导航 → 播报路径 |
| "哪里有电梯" | FIND_ELEVATOR | 查找电梯 → 语音指引 |
| "去305号诊室" | FIND_DESTINATION | 路径规划 → 导航播报 |
| "这条路记住" | REMEMBER_PATH | 触发摄像头 → 保存记忆 |
| "开始导航" | START_NAVIGATION | 进入导航状态 |
| "取消" | CANCEL | 中断任务 → 重置状态 |

### 3. 视觉事件处理

```python
# YOLO检测结果
detection_result = {
    "classes": ["stairs", "person"],
    "confidence": 0.95,
    "bbox": [100, 100, 200, 300]
}

# 发送视觉事件
orchestrator.handle_visual_event(detection_result)

# 系统自动完成：
# 1. 解析视觉事件类型
# 2. 生成语音提醒
# 3. 播报反馈
```

#### 视觉事件类型

| 检测结果 | 事件 | 语音反馈 |
|---------|------|---------|
| stairs | STAIRS_DETECTED | "前方有台阶，请小心" |
| elevator | ELEVATOR_DETECTED | "已到达电梯，请注意看标识" |
| toilet | TOILET_SIGN_DETECTED | "左侧有卫生间标识" |
| exit | EXIT_SIGN_DETECTED | "前方有出口标识" |
| obstacle | OBSTACLE_DETECTED | "前方有障碍物，请绕行" |

### 4. 系统状态管理

```python
from core.system_orchestrator import SystemState

# 查看当前状态
print(orchestrator.state)  # SystemState.IDLE

# 手动设置状态
orchestrator.set_state(SystemState.NAVIGATING)

# 状态类型
# IDLE: 空闲
# LISTENING: 监听中
# NAVIGATING: 导航中
# MEMORIZING: 记忆中
# PROCESSING: 处理中
# ERROR: 错误
```

### 5. 日志查询

```python
# 获取最近的日志
logs = orchestrator.get_logs(limit=100)

for log in logs:
    print(f"{log['timestamp']}: {log['action_type']} - {log['data']}")

# 日志类型
# voice_intent: 语音意图
# tts_speak: TTS播报
# navigation: 导航动作
# memory: 记忆操作
```

---

## 🔄 工作流程

### 语音流程

```
用户说话
    ↓
Whisper识别
    ↓
意图解析
    ↓
执行动作
    ├─ 导航模块：规划路径
    ├─ 记忆模块：保存记录
    └─ TTS模块：播报反馈
```

### 视觉流程

```
摄像头捕获图像
    ↓
YOLO检测
    ↓
解析视觉事件
    ↓
生成语音提醒
    └─ TTS播报
```

### 联合流程

```
1. 用户说："带我去305号诊室"
   → Whisper识别文本
   → 解析为FIND_DESTINATION意图
   → 提取目的地"305号诊室"
   → 调用导航模块规划路径
   → TTS播报："正在为您导航到305号诊室"

2. 途中检测到电梯
   → YOLO识别elevator
   → 触发ELEVATOR_DETECTED事件
   → TTS播报："已到达电梯，请按三楼"

3. 记录导航记忆
   → 保存路径信息
   → 记录目的地和节点
```

---

## 🧪 测试

### 运行测试

```bash
cd Luna_Badge
python3 test_system_orchestrator.py
```

### 测试内容

1. **基础功能**：状态管理、启动/停止
2. **意图解析**：6种意图的识别准确度
3. **视觉事件**：5种视觉事件的解析
4. **模拟集成**：完整流程的端到端测试
5. **Demo场景**：实际使用场景模拟

---

## 🎯 Demo验证

### 验证场景

#### 场景1：语音流程 ✅
```
用户："我要去厕所"
  → 识别：find_toilet
  → 导航：规划到洗手间路径
  → 播报："请直行10米，左转后有洗手间"
```

#### 场景2：视觉流程 ✅
```
检测："stairs"
  → 事件：STAIRS_DETECTED
  → 播报："前方有台阶，请小心"
```

#### 场景3：联合流程 ✅
```
用户："带我去305号诊室"
  → 导航：规划路径
  → 播报：开始导航
  → 视觉：检测到电梯
  → 播报："已到达电梯，请按三楼"
  → 记忆：记录导航过程
```

---

## 🚀 扩展功能

### 自定义意图处理

```python
# 注册自定义事件处理器
def custom_handler(event: SystemEvent):
    print(f"处理事件: {event.event_type}")

orchestrator.register_event_handler("custom_event", custom_handler)
```

### 上下文对话

```python
# 保存上下文
orchestrator.context["last_intent"] = UserIntent.FIND_TOILET

# 后续对话可以使用上下文
if "上次" in text:
    if orchestrator.context.get("last_intent") == UserIntent.FIND_TOILET:
        # 使用上次的洗手间查询结果
        pass
```

### 任务打断

```python
# 取消当前任务
orchestrator.handle_cancel()

# 任务状态重置
orchestrator.current_task = None
orchestrator.context = {}
```

---

## 📊 性能优化

### 异步处理

- 事件队列：非阻塞事件处理
- 多线程：语音识别和视觉检测并行

### 日志管理

- 限制日志长度：最多1000条
- 自动清理：避免内存占用过大

### 状态缓存

- 上下文保留：避免重复查询
- 模块复用：减少重复初始化

---

## 🐛 常见问题

### Q1: 意图识别不准确

**原因**：关键词匹配过于简单  
**解决**：后续接入NER模型或对话系统

### Q2: 视觉事件未触发

**原因**：YOLO模块未初始化或检测结果格式错误  
**解决**：检查vision_engine的检测结果格式

### Q3: TTS播报失败

**原因**：TTS模块未初始化或网络问题  
**解决**：检查tts_manager的配置和网络连接

---

## 📚 相关文档

- `core/system_orchestrator.py` - 控制中枢实现
- `test_system_orchestrator.py` - 测试脚本
- `TASK_STATUS_ANALYSIS.md` - 任务完成情况
- `MEMORY_MODULE_GUIDE.md` - 记忆模块指南

---

## ✅ 总结

系统控制中枢实现了：

- ✅ **统一调度**：协调所有子系统
- ✅ **意图识别**：6种核心意图
- ✅ **视觉反馈**：5种视觉事件
- ✅ **路径导航**：自动规划与播报
- ✅ **记忆记录**：完整的用户行为追踪
- ✅ **事件驱动**：异步非阻塞处理

**准备就绪！**🚀

---

**版本**: v1.0  
**创建时间**: 2025-10-31  
**状态**: ✅ 已完成

