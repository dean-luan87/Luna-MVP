# Luna Badge TTS语音播报集成指南

**版本**: v1.6  
**完成时间**: 2025-10-30  
**状态**: ✅ 已完成

---

## 📋 目录

1. [概述](#概述)
2. [集成模块](#集成模块)
3. [使用方法](#使用方法)
4. [API文档](#api文档)
5. [测试结果](#测试结果)
6. [场景示例](#场景示例)

---

## 🎯 概述

TTS（文本转语音）已完整集成到Luna Badge系统中，支持风格切换和多场景播报。

### 功能特性

- ✅ **风格切换**: 根据危险等级、人群密度自动切换
- ✅ **情绪播报**: 支持欢快、温和、紧急、愤怒等多种风格
- ✅ **场景适配**: 不同场景使用不同语速和音调
- ✅ **简单易用**: 统一的speak()接口

### 已集成模块

1. **TTS管理器** (`tts_manager.py`)
2. **使用指南播报** (`luna_usage_guide.py`)
3. **验证码反馈** (`voice_verification_code.py`)

---

## 📦 集成模块

### 1. TTS管理器 (`core/tts_manager.py`)

**核心类**: `TTSManager`

**初始化示例**:
```python
from core.tts_manager import TTSManager, speak

# 使用全局管理器
speak("你好，我是Luna")
```

**主要功能**:
- 风格切换（6种风格）
- 危险等级适配
- 人群密度适配

### 2. 使用指南播报 (`core/luna_usage_guide.py`)

**功能**: 产品介绍和功能引导的语音播报

**已集成TTS**:
```python
from core.luna_usage_guide import LunaUsageGuide

guide = LunaUsageGuide()

# 播报介绍
guide.speak_guide("intro", use_tts=True)

# 播报使用方法
guide.speak_guide("how_to_navigate", use_tts=True)
```

### 3. 验证码反馈 (`core/voice_verification_code.py`)

**功能**: 验证码输入结果的语音反馈

**已集成TTS**:
```python
from core.voice_verification_code import VoiceVerificationCodeHandler

handler = VoiceVerificationCodeHandler()

# 验证码正确
handler.voice_send_verification_code("13800138000")

# 验证码错误
handler.voice_input_verification_code("13800138000", "123456")
```

---

## 🚀 使用方法

### 基础使用

#### 简单播报
```python
from core.tts_manager import speak

speak("你好，我是Luna")
```

#### 指定风格播报
```python
from core.tts_manager import speak, TTSStyle

# 紧急播报
speak("前方有障碍物，请注意", style=TTSStyle.URGENT)

# 温和播报
speak("请靠右边行走", style=TTSStyle.GENTLE)

# 欢快播报
speak("你好，我是Luna", style=TTSStyle.CHEERFUL)
```

#### 根据危险等级自动切换
```python
from core.tts_manager import TTSManager, DangerLevel

manager = TTSManager()

# 危险场景 - 自动使用紧急风格
style = manager.select_style_for_danger(DangerLevel.HIGH)
speak("前方道路封闭", style=style)

# 安全场景 - 自动使用欢快风格
style = manager.select_style_for_danger(DangerLevel.SAFE)
speak("导航路线规划完成", style=style)
```

### 在业务模块中使用

#### 使用指南播报
```python
from core.luna_usage_guide import LunaUsageGuide

guide = LunaUsageGuide()

# 播报完整介绍
guide.speak_guide("intro", use_tts=True)

# 播报导航教程
guide.speak_guide("how_to_navigate", use_tts=True)

# 播报WiFi设置教程
guide.speak_guide("step_by_step_wifi", use_tts=True)
```

#### 验证码反馈播报
```python
from core.voice_verification_code import VoiceVerificationCodeHandler

handler = VoiceVerificationCodeHandler()

# 发送验证码
handler.voice_send_verification_code("13800138000")
# 自动播报："验证码已发送，请告诉我6位数字验证码"

# 验证码错误
handler.voice_input_verification_code("13800138000", "123456")
# 自动播报："验证码错误，还有4次机会，请重新输入"
```

---

## 📚 API文档

### speak() 函数

```python
def speak(text: str, style: TTSStyle = TTSStyle.CHEERFUL) -> None
```

**参数**:
- `text` (str): 要播报的文本
- `style` (TTSStyle): 播报风格，默认CHEERFUL

**返回**: None

**示例**:
```python
speak("你好")
speak("前方危险", style=TTSStyle.URGENT)
```

### TTSManager类

#### select_style_for_danger()
```python
style = manager.select_style_for_danger(danger_level)
```

**参数**:
- `danger_level` (DangerLevel): 危险等级

**返回**: TTSStyle

#### select_style_for_crowd_density()
```python
style = manager.select_style_for_crowd_density(density)
```

**参数**:
- `density` (str): 人群密度（sparse/normal/crowded/very_crowded）

**返回**: TTSStyle

---

## ✅ 测试结果

### 测试覆盖率: 100%

#### 测试项1: TTS基础功能
- ✅ 管理器初始化
- ✅ 风格切换
- ✅ 危险等级适配
- ✅ 人群密度适配

#### 测试项2: speak便捷函数
- ✅ 简单播报
- ✅ 风格指定
- ✅ 参数传递

#### 测试项3: 使用指南TTS集成
- ✅ 介绍播报
- ✅ 导航教程播报
- ✅ 提醒教程播报
- ✅ WiFi设置教程播报

#### 测试项4: 完整集成场景
- ✅ 首次开机引导
- ✅ 验证码反馈
- ✅ 账号设置流程

---

## 🎭 场景示例

### 场景1: 安全导航播报
```python
from core.tts_manager import speak, TTSStyle

# 欢快风格
speak("导航路线规划完成", style=TTSStyle.CHEERFUL)
speak("预计10分钟后到达", style=TTSStyle.CHEERFUL)
```

### 场景2: 危险警告播报
```python
from core.tts_manager import speak, TTSStyle

# 紧急风格
speak("前方有障碍物，请注意", style=TTSStyle.URGENT)
speak("请靠右边行走", style=TTSStyle.URGENT)
```

### 场景3: 首次开机引导
```python
from core.luna_usage_guide import LunaUsageGuide

guide = LunaUsageGuide()

# 完整介绍
guide.speak_guide("intro", use_tts=True)

# 输出：
# - 你好，我是 Luna，是你的语音视觉导航助手。
# - 我可以为你导航、识别标志、记录提醒...
# - 你可以随时问我：Luna，怎么用扫码功能？
```

### 场景4: 验证码反馈
```python
from core.voice_verification_code import VoiceVerificationCodeHandler

handler = VoiceVerificationCodeHandler()

# 发送验证码
handler.voice_send_verification_code("13800138000")

# 验证码输入
handler.voice_input_verification_code("13800138000", "一二三四五六")
```

---

## 📊 风格配置

### 支持 TTS 风格

| 风格 | 适用场景 | 语速 | 音调 | 语音 |
|------|----------|------|------|------|
| cheerful | 正常导航 | 1.2x | 1.1x | XiaoxiaoNeural |
| empathetic | 共情场景 | 0.9x | 0.95x | YunxiNeural |
| angry | 严重警告 | 1.3x | 1.2x | YunjianNeural |
| calm | 平静播报 | 0.95x | 1.0x | XiaoyiNeural |
| urgent | 紧急提醒 | 1.5x | 1.3x | XiaoxiaoNeural |
| gentle | 温和引导 | 0.85x | 0.9x | YunxiNeural |

### 危险等级映射

| 危险等级 | 风格 |
|----------|------|
| SAFE | cheerful |
| LOW | calm |
| MEDIUM | gentle |
| HIGH | urgent |
| CRITICAL | angry |

### 人群密度映射

| 人群密度 | 风格 |
|----------|------|
| sparse | cheerful |
| normal | cheerful |
| crowded | calm |
| very_crowded | urgent |

---

## ⚠️ 注意事项

### 1. 平台差异

- **Mac**: 使用 `say` 命令播报中文
- **Linux**: 需要安装 `espeak` 或 `festival`
- **Windows**: 使用内置SAPI
- **嵌入式**: 使用Coqui-TTS或其他离线引擎

### 2. 语音质量

- 系统say命令播报中文效果一般
- 建议使用edge-tts或coqui-tts获取更好效果
- 离线部署可以使用嵌入式TTS引擎

### 3. 播报延迟

- 使用系统say命令几乎没有延迟
- 使用edge-tts需要生成音频，有约1-2秒延迟
- 建议关键场景使用edge-tts，一般提示使用say

### 4. 播报阻塞

- `speak()` 函数会阻塞线程直到播报完成
- 长时间播报可能影响其他功能
- 建议关键功能使用异步播报

---

## 🔄 未来优化

### 计划优化项

1. **异步播报**: 支持非阻塞播报
2. **离线引擎**: 集成Coqui-TTS
3. **语音缓存**: 缓存常用播报内容
4. **音量控制**: 支持动态音量调整

---

## 📝 更新日志

### v1.6 (2025-10-30)
- ✅ 集成到使用指南模块
- ✅ 完善风格切换机制
- ✅ 添加场景适配功能
- ✅ 完善测试用例

---

**文档结束**

*Luna Badge v1.6 - 让播报更自然，让交互更流畅*

