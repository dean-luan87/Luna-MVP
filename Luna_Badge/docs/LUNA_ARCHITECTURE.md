# Luna Badge 系统架构

## 📐 架构总览

```
┌─────────────────────────────────────────────────────┐
│                  Luna Badge 系统                     │
└─────────────────────────────────────────────────────┘

┌─────────────────┐
│  视觉感知层      │ ← YOLO+DeepSort / OCR / SLAM
│  Vision Layer   │
└────────┬────────┘
         ↓
┌─────────────────┐
│  路径判断层      │ ← 人群密度 / 方向一致性 / 障碍阻挡
│  Path Layer     │
└────────┬────────┘
         ↓
┌─────────────────┐
│  播报策略层      │ ← 情绪播报风格切换 + 内容模板
│  Speech Layer   │
└────────┬────────┘
         ↓
┌─────────────────┐
│  用户交互层      │ ← 语音反馈 / 纠错 / 路线确认
│  User Layer     │
└─────────────────┘
```

## 🏗️ 架构分层详解

### 1. 视觉感知层 (Vision Layer)

**职责**: 视觉信息采集、识别和理解

#### 核心模块
```python
# 物体检测与追踪
- YOLO: 物体检测 (行人、车辆、障碍物)
- DeepSort: 目标追踪 (轨迹预测)

# OCR识别
- OCR文档识别: ocr_advanced_reader.py
- 商品信息识别: product_info_checker.py
- 门牌识别: doorplate_reader.py

# SLAM地图生成
- 局部地图生成: local_map_generator.py
```

#### 输出数据
```json
{
  "event": "vision_detection",
  "level": "medium",
  "data": {
    "objects": [
      {"type": "person", "position": [100, 200], "confidence": 0.9},
      {"type": "vehicle", "position": [300, 400], "confidence": 0.8}
    ],
    "signboards": [
      {"type": "toilet", "text": "洗手间", "position": [50, 100]}
    ],
    "hazards": [
      {"type": "water", "severity": "high", "position": [200, 300]}
    ]
  },
  "timestamp": "..."
}
```

---

### 2. 路径判断层 (Path Layer)

**职责**: 分析路径状态、人群行为、障碍物

#### 核心模块
```python
# 人群行为分析
- 排队检测: queue_detector.py
- 人群密度: crowd_density_detector.py
- 人流方向: flow_direction_analyzer.py

# 路径状态判断
- 门牌推理: doorplate_inference.py
- 危险环境: hazard_detector.py
```

#### 输出数据
```json
{
  "event": "path_analysis",
  "level": "medium",
  "data": {
    "crowd_density": "crowded",
    "flow_direction": "counter",
    "queue_detected": true,
    "hazards": [
      {"type": "water", "severity": "high"}
    ]
  },
  "timestamp": "..."
}
```

---

### 3. 播报策略层 (Speech Layer)

**职责**: 智能语音播报、风格切换

#### 核心模块
```python
# TTS管理
- TTS管理器: tts_manager.py
- 语音风格切换: TTSStyle

# 内容生成
- 语音内容模板
- 情绪化播报
```

#### 输出数据
```json
{
  "event": "speech_broadcast",
  "level": "high",
  "data": {
    "text": "前方人群密集，请注意安全",
    "style": "urgent",
    "voice": "zh-CN-XiaoxiaoNeural",
    "rate": 1.5,
    "pitch": 1.3
  },
  "timestamp": "..."
}
```

---

### 4. 用户交互层 (User Layer)

**职责**: 用户交互、反馈处理

#### 核心模块
```python
# 用户管理
- 用户管理器: user_manager.py
- 短信验证: 验证码服务

# 记忆系统
- 记忆存储: memory_store.py
- 记忆调用: memory_caller.py

# 语音交互
- 语音识别: voice_recognition.py
- 语音唤醒: voice_wakeup.py
```

#### 输出数据
```json
{
  "event": "user_interaction",
  "level": "medium",
  "data": {
    "type": "voice_command",
    "intent": "forward",
    "confidence": 0.9,
    "user_response": "..."
  },
  "timestamp": "..."
}
```

## 🔄 数据流转

### 完整流程示例

```json
{
  "event": "navigation_cycle",
  "level": "high",
  "data": {
    "step_1_vision": {
      "detects": ["person", "vehicle", "signboard"],
      "count": {"persons": 3, "vehicles": 1}
    },
    "step_2_path": {
      "crowd_density": "crowded",
      "flow_direction": "counter",
      "queue_detected": false
    },
    "step_3_decision": {
      "action": "slow_down_and_warn",
      "style": "urgent"
    },
    "step_4_speech": {
      "text": "前方人群密集且存在逆向人流，请减速并靠右行走"
    }
  },
  "timestamp": "..."
}
```

## 📊 模块映射表

| 架构层 | 模块文件 | 功能 |
|--------|---------|------|
| **视觉感知层** | `ocr_advanced_reader.py` | OCR文档识别 |
|  | `product_info_checker.py` | 商品成分识别 |
|  | `doorplate_reader.py` | 门牌识别 |
|  | `signboard_detector.py` | 标识牌识别 |
|  | `facility_detector.py` | 公共设施识别 |
|  | `hazard_detector.py` | 危险环境识别 |
|  | `local_map_generator.py` | 局部地图生成 |
| **路径判断层** | `queue_detector.py` | 排队检测 |
|  | `crowd_density_detector.py` | 人群密度 |
|  | `flow_direction_analyzer.py` | 人流方向 |
|  | `doorplate_inference.py` | 门牌推理 |
| **播报策略层** | `tts_manager.py` | TTS管理 |
| **用户交互层** | `user_manager.py` | 用户管理 |
|  | `memory_store.py` | 记忆存储 |
|  | `memory_caller.py` | 记忆调用 |
|  | `voice_recognition.py` | 语音识别 |
|  | `voice_wakeup.py` | 语音唤醒 |
|  | `mcp_controller.py` | 设备控制 |

## 🎯 核心特性

### 1. 数据驱动
- 所有输出统一为JSON格式
- 结构化数据便于处理和扩展
- 标准化接口

### 2. 分层设计
- 清晰的职责划分
- 模块间低耦合
- 易于维护和扩展

### 3. 智能化
- AI驱动的视觉识别
- 智能路径分析
- 情感化语音播报
- 自适应用户交互

---

**版本**: v1.2  
**更新日期**: 2025年10月27日  
**状态**: ✅ 架构完整，生产就绪
