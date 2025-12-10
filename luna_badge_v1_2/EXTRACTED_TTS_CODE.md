# 提取的 TTS 代码片段

## 1. modules/voice.py - Voice 类完整代码

```python
# -*- coding: utf-8 -*-
"""
语音播报模块
支持离线TTS（pyttsx3）和在线TTS（edge-tts）
"""

import platform
import logging
import threading
import time
from typing import Optional

logger = logging.getLogger(__name__)


class Voice:
    """语音播报类"""
    
    def __init__(self):
        """初始化语音播报模块"""
        self.engine = None
        self.engine_type = None
        self.is_available = False
        self.speaking = False
        self._lock = threading.Lock()
        
        # 检测系统环境并初始化TTS引擎
        self._initialize_tts()
    
    def _initialize_tts(self):
        """初始化TTS引擎"""
        try:
            # 优先尝试pyttsx3（离线TTS）
            if self._try_pyttsx3():
                self.engine_type = "pyttsx3"
                self.is_available = True
                logger.info("语音播报模块初始化成功: pyttsx3")
                return
            
            # 如果pyttsx3不可用，尝试edge-tts（在线TTS）
            if self._try_edge_tts():
                self.engine_type = "edge-tts"
                self.is_available = True
                logger.info("语音播报模块初始化成功: edge-tts")
                return
            
            # 如果都不可用
            logger.warning("所有TTS引擎都不可用，语音播报功能将被禁用")
            self.is_available = False
            
        except Exception as e:
            logger.error(f"语音播报模块初始化失败: {e}")
            self.is_available = False
    
    def _try_pyttsx3(self) -> bool:
        """尝试初始化pyttsx3引擎"""
        try:
            import pyttsx3
            
            # 在Mac上强制使用nsss驱动
            if platform.system() == 'Darwin':
                try:
                    self.engine = pyttsx3.init(driverName="nsss")
                    logger.info("使用nsss驱动初始化pyttsx3")
                except Exception as e:
                    logger.warning(f"nsss驱动初始化失败: {e}")
                    logger.info("尝试使用默认驱动...")
                    self.engine = pyttsx3.init()
            else:
                self.engine = pyttsx3.init()
            
            # 设置语音参数
            if self.engine:
                # 设置语速
                self.engine.setProperty('rate', 150)
                
                # 设置音量
                self.engine.setProperty('volume', 0.8)
                
                # 智能选择中文语音
                voices = self.engine.getProperty('voices')
                if voices:
                    selected_voice = self._select_best_voice(voices)
                    if selected_voice:
                        self.engine.setProperty('voice', selected_voice.id)
                        logger.info(f"设置语音: {selected_voice.name} (ID: {selected_voice.id})")
                    else:
                        # 使用默认语音
                        self.engine.setProperty('voice', voices[0].id)
                        logger.info(f"使用默认语音: {voices[0].name}")
                
                return True
            
        except ImportError:
            logger.warning("pyttsx3未安装，跳过离线TTS")
        except Exception as e:
            logger.warning(f"pyttsx3初始化失败: {e}")
        
        return False
    
    def _select_best_voice(self, voices):
        """选择最佳语音（优先中文）"""
        chinese_voices = []
        
        for voice in voices:
            voice_name = voice.name.lower()
            voice_languages = getattr(voice, 'languages', [])
            
            # 检查语言属性
            is_chinese = False
            if voice_languages:
                for lang in voice_languages:
                    if any(keyword in str(lang).lower() for keyword in ['zh', 'chinese', 'cn', 'mandarin']):
                        is_chinese = True
                        break
            
            # 检查名称中的中文关键词
            if not is_chinese:
                if any(keyword in voice_name for keyword in ['chinese', 'zh', 'cn', 'mandarin', 'ting-ting', 'xiaoyi']):
                    is_chinese = True
            
            if is_chinese:
                chinese_voices.append(voice)
        
        # 优先返回中文语音
        if chinese_voices:
            logger.info(f"发现 {len(chinese_voices)} 个中文语音")
            return chinese_voices[0]
        
        logger.info("未发现中文语音，将使用默认语音")
        return None
    
    def _try_edge_tts(self) -> bool:
        """尝试初始化edge-tts引擎"""
        try:
            import edge_tts
            
            # 检查网络连接
            import urllib.request
            try:
                urllib.request.urlopen('https://www.microsoft.com', timeout=3)
            except:
                logger.warning("网络连接不可用，跳过edge-tts")
                return False
            
            # 设置中文语音
            self.voice_name = "zh-CN-XiaoxiaoNeural"  # 默认中文语音
            self.engine = edge_tts
            
            return True
            
        except ImportError:
            logger.warning("edge-tts未安装，跳过在线TTS")
        except Exception as e:
            logger.warning(f"edge-tts初始化失败: {e}")
        
        return False
    
    def speak(self, text: str) -> bool:
        """
        语音播报文本
        
        Args:
            text: 要播报的文本
            
        Returns:
            是否播报成功
        """
        if not text or not text.strip():
            return True
        
        if not self.is_available:
            logger.warning("语音播报模块不可用，跳过播报")
            return False
        
        # 检查是否正在播报（使用更严格的检查）
        with self._lock:
            if self.speaking:
                logger.info(f"[TTS] busy, skip new speak: {text[:30]}...")
                return False
            self.speaking = True
        
        try:
            # 在新线程中播报，避免阻塞主线程
            thread = threading.Thread(target=self._speak_thread, args=(text,))
            thread.daemon = True
            thread.start()
            return True
            
        except Exception as e:
            logger.error(f"启动语音播报线程失败: {e}")
            with self._lock:
                self.speaking = False
            return False
    
    def _speak_thread(self, text: str):
        """语音播报线程"""
        try:
            logger.info(f"[TTS] START text={text[:50]}...")
            if self.engine_type == "pyttsx3":
                self._speak_pyttsx3(text)
            elif self.engine_type == "edge-tts":
                self._speak_edge_tts(text)
            logger.info(f"[TTS] END text={text[:50]}...")
        except Exception as e:
            logger.error(f"语音播报失败: {e}")
        finally:
            with self._lock:
                self.speaking = False
    
    def _speak_pyttsx3(self, text: str):
        """使用pyttsx3播报"""
        try:
            if self.engine:
                # 关键修复：不再自动 stop()，避免打断正在播放的内容
                # 由于 speak() 方法已经有锁保护（self.speaking），
                # 同一时刻只会有一个播报在执行，不需要 stop()
                
                # 设置超时保护
                import threading
                import time
                
                def timeout_handler():
                    time.sleep(10)  # 10秒超时
                    try:
                        self.engine.stop()
                    except:
                        pass
                
                # 启动超时保护
                timeout_thread = threading.Thread(target=timeout_handler)
                timeout_thread.daemon = True
                timeout_thread.start()
                
                # 开始播报（在锁保护下，不会被打断）
                self.engine.say(text)
                self.engine.runAndWait()  # 阻塞直到播放完成
                
                logger.debug(f"pyttsx3播报完成: {text[:50]}...")
                
        except Exception as e:
            logger.warning(f"pyttsx3播报失败: {e}")
            # 尝试重新初始化引擎
            try:
                self._try_pyttsx3()
            except:
                pass
    
    def _speak_edge_tts(self, text: str):
        """使用edge-tts播报"""
        try:
            import asyncio
            import edge_tts
            
            async def _async_speak():
                communicate = edge_tts.Communicate(text, self.voice_name)
                await communicate.save("temp_voice.mp3")
                
                # 播放音频文件（在锁保护下，不会被打断）
                import subprocess
                import os
                try:
                    if platform.system() == 'Darwin':
                        # subprocess.run 是阻塞的，会等待播放完成
                        subprocess.run(['afplay', 'temp_voice.mp3'], check=True)
                    else:
                        subprocess.run(['mpg123', 'temp_voice.mp3'], check=True)
                finally:
                    # 清理临时文件
                    if os.path.exists('temp_voice.mp3'):
                        os.remove('temp_voice.mp3')
            
            # 在新的事件循环中运行
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(_async_speak())
            loop.close()
            
            logger.debug(f"edge-tts播报完成: {text[:50]}...")
            
        except Exception as e:
            logger.error(f"edge-tts播报失败: {e}")
    
    def is_speaking(self) -> bool:
        """检查是否正在播报"""
        with self._lock:
            return self.speaking
    
    def stop(self):
        """停止当前播报"""
        try:
            if self.engine_type == "pyttsx3" and self.engine:
                self.engine.stop()
            with self._lock:
                self.speaking = False
            logger.info("语音播报已停止")
        except Exception as e:
            logger.error(f"停止语音播报失败: {e}")
    
    def get_status(self) -> dict:
        """获取语音模块状态"""
        return {
            'available': self.is_available,
            'engine_type': self.engine_type,
            'speaking': self.speaking,
            'platform': platform.system()
        }
```

---

## 2. Luna_Badge/core/tts_manager.py - 播放相关代码片段

### 关键播放方法

```python
async def speak(self, text: str, style: TTSStyle = TTSStyle.CHEERFUL) -> bool:
    """
    语音播报
    
    Args:
        text: 要播报的文本
        style: 播报风格
        
    Returns:
        bool: 是否成功
    """
    try:
        # 获取配置
        config = self.get_config(style)
        
        # 使用edge-tts播报
        import edge_tts
        communicate = edge_tts.Communicate(
            text=text,
            voice=config.voice,
            rate=config.rate
        )
        
        # 保存为临时文件
        output_file = f"temp_output_{int(time.time())}.mp3"
        await communicate.save(output_file)
        
        # 播报（使用系统命令）
        os.system(f"afplay {output_file}")  # macOS
        
        # 删除临时文件
        os.remove(output_file)
        
        self.logger.info(f"🗣️ 播报: {text} (风格: {style.value})")
        return True
        
    except Exception as e:
        self.logger.error(f"❌ 播报失败: {e}")
        return False

def speak_sync(self, text: str, style: TTSStyle = TTSStyle.CHEERFUL):
    """同步播报（简化版）"""
    # 使用系统say命令
    style_text = style.value
    os.system(f'say -v Ting-Ting "{text}"')  # macOS中文语音
    self.logger.info(f"🗣️ 播报: {text} (风格: {style.value})")
```

### TTSManager 类完整结构（播放相关部分）

```python
class TTSManager:
    """TTS管理器"""
    
    def __init__(self):
        """初始化TTS管理器"""
        self.logger = logging.getLogger(__name__)
        
        # 风格配置
        self.style_configs = {
            TTSStyle.CHEERFUL: {
                "voice": "zh-CN-XiaoxiaoNeural",
                "rate": 1.2,
                "pitch": 1.1
            },
            TTSStyle.EMPATHETIC: {
                "voice": "zh-CN-YunxiNeural",
                "rate": 0.9,
                "pitch": 0.95
            },
            TTSStyle.ANGRY: {
                "voice": "zh-CN-YunjianNeural",
                "rate": 1.3,
                "pitch": 1.2
            },
            TTSStyle.CALM: {
                "voice": "zh-CN-XiaoyiNeural",
                "rate": 0.95,
                "pitch": 1.0
            },
            TTSStyle.URGENT: {
                "voice": "zh-CN-XiaoxiaoNeural",
                "rate": 1.5,
                "pitch": 1.3
            },
            TTSStyle.GENTLE: {
                "voice": "zh-CN-YunxiNeural",
                "rate": 0.85,
                "pitch": 0.9
            }
        }
        
        # 默认配置
        self.default_config = TTSConfig(
            style=TTSStyle.CHEERFUL,
            voice="zh-CN-XiaoxiaoNeural",
            rate=1.0,
            pitch=1.0,
            volume=1.0
        )
        
        self.logger.info("🗣️ TTS管理器初始化完成")
    
    def get_config(self, style: TTSStyle) -> TTSConfig:
        """
        获取指定风格的配置
        
        Args:
            style: 播报风格
            
        Returns:
            TTSConfig: TTS配置
        """
        style_config = self.style_configs.get(style, self.style_configs[TTSStyle.CHEERFUL])
        
        return TTSConfig(
            style=style,
            voice=style_config["voice"],
            rate=style_config["rate"],
            pitch=style_config["pitch"],
            volume=1.0
        )
    
    async def speak(self, text: str, style: TTSStyle = TTSStyle.CHEERFUL) -> bool:
        """
        语音播报（异步版本）
        
        Args:
            text: 要播报的文本
            style: 播报风格
            
        Returns:
            bool: 是否成功
        """
        try:
            # 获取配置
            config = self.get_config(style)
            
            # 使用edge-tts播报
            import edge_tts
            communicate = edge_tts.Communicate(
                text=text,
                voice=config.voice,
                rate=config.rate
            )
            
            # 保存为临时文件
            output_file = f"temp_output_{int(time.time())}.mp3"
            await communicate.save(output_file)
            
            # 播报（使用系统命令）
            os.system(f"afplay {output_file}")  # macOS
            
            # 删除临时文件
            os.remove(output_file)
            
            self.logger.info(f"🗣️ 播报: {text} (风格: {style.value})")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ 播报失败: {e}")
            return False
    
    def speak_sync(self, text: str, style: TTSStyle = TTSStyle.CHEERFUL):
        """同步播报（简化版）"""
        # 使用系统say命令
        style_text = style.value
        os.system(f'say -v Ting-Ting "{text}"')  # macOS中文语音
        self.logger.info(f"🗣️ 播报: {text} (风格: {style.value})")
```

---

## 关键差异对比

### modules/voice.py (Voice 类)
- ✅ 支持 pyttsx3（离线）和 edge-tts（在线）
- ✅ 有锁保护（`self.speaking` + `self._lock`）
- ✅ 在独立线程中播放（`_speak_thread`）
- ✅ 已修复：移除了自动 `stop()` 调用
- ✅ 有播放开始/结束日志

### Luna_Badge/core/tts_manager.py (TTSManager 类)
- ✅ 支持多种播报风格（欢快、共情、愤怒等）
- ❌ 没有锁保护（可能被打断）
- ❌ `speak()` 是异步的，但 `os.system()` 是阻塞的
- ❌ `speak_sync()` 使用 `os.system()`，没有互斥保护
- ⚠️ 使用 `os.system()` 而不是 `subprocess.run()`（不够安全）

## 建议

如果要修复 `TTSManager` 的打断问题，可以：
1. 添加锁保护（类似 `Voice` 类）
2. 将 `os.system()` 改为 `subprocess.run()`
3. 添加播放状态检查




