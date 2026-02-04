# 语音克隆集成指南

## 📋 概述

本文档说明如何将 Coqui TTS 语音克隆技术集成到 Luna 系统中，替换现有TTS模块。

## 🎯 方案选择

**推荐：Coqui TTS + XTTS-v2**

- ✅ 中文支持优秀
- ✅ 仅需3-5秒参考音频即可克隆
- ✅ 部署简单，API友好
- ✅ 活跃维护，文档完善

## 📦 安装步骤

### 1. 安装 Coqui TTS

```bash
# 基础安装
pip install TTS

# 如果需要GPU加速（推荐）
pip install TTS torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### 2. 验证安装

```bash
python -c "from TTS.api import TTS; print('✅ TTS安装成功')"
```

## 🎤 准备参考音频

### 要求

- **格式**：WAV、MP3（推荐WAV）
- **时长**：3-10秒（推荐5秒左右）
- **质量**：
  - 清晰、无噪音
  - 单人说话
  - 无背景音乐
- **内容**：中文或英文均可

### 录制建议

```bash
# 使用系统录音工具录制
# macOS: QuickTime Player
# Linux: arecord
# Windows: 录音机

# 示例：使用 ffmpeg 转换格式
ffmpeg -i input.mp3 -ar 22050 -ac 1 reference_voice.wav
```

## 🔧 集成步骤

### 1. 替换现有 TTS 模块

```python
# 在 Luna_Badge/core/tts_manager.py 中

from core.voice_clone_tts import VoiceCloneTTS, create_voice_clone_tts

# 初始化（全局单例）
_voice_clone_tts = None

def init_voice_clone_tts(reference_audio_path: str, use_gpu: bool = False):
    """初始化语音克隆TTS"""
    global _voice_clone_tts
    _voice_clone_tts = create_voice_clone_tts(
        reference_audio_path=reference_audio_path,
        use_gpu=use_gpu
    )
    return _voice_clone_tts

def speak(text: str, language: str = "zh") -> str:
    """生成语音（兼容原有接口）"""
    if _voice_clone_tts is None:
        raise RuntimeError("语音克隆TTS未初始化，请先调用 init_voice_clone_tts()")
    
    return _voice_clone_tts.speak(text=text, language=language)
```

### 2. 配置文件

```yaml
# config/tts_config.yaml

voice_clone:
  enabled: true
  reference_audio: "data/voice/reference_voice.wav"
  model: "tts_models/multilingual/multi-dataset/xtts_v2"
  use_gpu: false  # 如果有GPU，设为true
  output_dir: "data/voice/output"
  default_language: "zh"
  speed: 1.0  # 语速倍数
```

### 3. 系统初始化

```python
# 在系统启动时初始化

from core.voice_clone_tts import init_voice_clone_tts
import yaml

# 加载配置
with open("config/tts_config.yaml", "r") as f:
    tts_config = yaml.safe_load(f)["voice_clone"]

# 初始化语音克隆TTS
if tts_config["enabled"]:
    init_voice_clone_tts(
        reference_audio_path=tts_config["reference_audio"],
        use_gpu=tts_config["use_gpu"]
    )
```

## 📝 使用示例

### 基础使用

```python
from core.voice_clone_tts import VoiceCloneTTS

# 创建实例
tts = VoiceCloneTTS(
    reference_audio_path="reference_voice.wav",
    use_gpu=False
)

# 生成语音
audio_path = tts.speak("你好，这是克隆的语音", language="zh")
print(f"语音已生成: {audio_path}")
```

### 异步生成

```python
def on_complete(output_path):
    if output_path:
        print(f"语音生成完成: {output_path}")
        # 播放音频
        play_audio(output_path)
    else:
        print("语音生成失败")

# 异步生成
tts.speak_async("异步生成语音", language="zh", callback=on_complete)
```

### 集成到现有系统

```python
# 替换原有的 speak 函数调用
from core.tts_manager import speak  # 或 voice_clone_tts

# 原有调用方式不变
audio_path = speak("要说的内容", language="zh")
```

## ⚙️ 性能优化

### 1. GPU加速（推荐）

```python
tts = VoiceCloneTTS(
    reference_audio_path="reference_voice.wav",
    use_gpu=True  # 启用GPU加速
)
```

### 2. 缓存机制

```python
import hashlib
from pathlib import Path

class CachedVoiceCloneTTS(VoiceCloneTTS):
    def __init__(self, *args, cache_dir="data/voice/cache", **kwargs):
        super().__init__(*args, **kwargs)
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def speak(self, text, language="zh", **kwargs):
        # 检查缓存
        cache_key = hashlib.md5(f"{text}_{language}".encode()).hexdigest()
        cache_path = self.cache_dir / f"{cache_key}.wav"
        
        if cache_path.exists():
            logger.debug(f"📦 使用缓存: {cache_path}")
            return str(cache_path)
        
        # 生成并缓存
        output_path = super().speak(text, language, **kwargs)
        import shutil
        shutil.copy(output_path, cache_path)
        return str(cache_path)
```

### 3. 预加载模型

```python
# 在系统启动时预加载模型，避免首次调用延迟
tts = VoiceCloneTTS(...)
tts._initialize()  # 提前初始化
```

## 🔍 故障排查

### 问题1：模型下载失败

```bash
# 手动下载模型
python -c "from TTS.api import TTS; TTS('tts_models/multilingual/multi-dataset/xtts_v2')"
```

### 问题2：内存不足

```python
# 使用CPU模式（速度较慢但内存占用小）
tts = VoiceCloneTTS(..., use_gpu=False)
```

### 问题3：音频质量不佳

- 检查参考音频质量（清晰、无噪音）
- 尝试不同的参考音频
- 调整语速参数

### 问题4：中文发音不准

- 确保参考音频是中文
- 检查 language 参数设为 "zh"
- 尝试更长的参考音频（5-10秒）

## 📊 性能对比

| 指标 | 原TTS | 语音克隆TTS |
|------|-------|------------|
| 语音自然度 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 个性化 | ❌ | ✅ |
| 生成速度 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 资源占用 | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| 中文支持 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

## 🚀 下一步

1. ✅ 安装 Coqui TTS
2. ✅ 准备参考音频
3. ✅ 集成到系统
4. 🔄 测试和优化
5. 🔄 部署到生产环境

## 📚 参考资源

- [Coqui TTS 文档](https://tts.readthedocs.io/)
- [Coqui TTS GitHub](https://github.com/coqui-ai/TTS)
- [XTTS 模型说明](https://github.com/coqui-ai/TTS/blob/dev/TTS/tts/models/xtts.py)
- [语音克隆最佳实践](https://github.com/coqui-ai/TTS/wiki/XTTS-v2)

---

**集成完成后，Luna 将拥有更自然、个性化的语音输出！** 🎉
