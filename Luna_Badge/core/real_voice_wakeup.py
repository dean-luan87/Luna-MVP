"""
Luna Badge v1.6 - 真实唤醒词检测集成
实现文件：core/real_voice_wakeup.py

⚠️ 注意：此模块需要安装唤醒词检测引擎
对于Mac/开发环境：可以使用PicoVoice或Porcupine
对于嵌入式设备（RV1126）：需要使用RKNN优化的模型
"""

import os
import logging
from typing import Optional, Callable, List
from core.voice_wakeup_manager import SystemState

logger = logging.getLogger(__name__)


class RealVoiceWakeupEngine:
    """
    真实唤醒词检测引擎
    根据平台选择不同的实现
    """
    
    def __init__(self, wake_words: List[str] = None):
        """
        初始化唤醒引擎
        
        Args:
            wake_words: 唤醒词列表
        """
        if wake_words is None:
            wake_words = ["你好Luna", "Luna你好"]
        
        self.wake_words = wake_words
        self.is_running = False
        self.callbacks: List[Callable] = []
        
        # 检测运行平台
        self.platform = self._detect_platform()
        
        # 根据平台加载对应的引擎
        self.engine = self._load_engine()
    
    def _detect_platform(self) -> str:
        """检测运行平台"""
        import platform
        system = platform.system().lower()
        
        if system == "darwin":
            return "mac"
        elif system == "linux":
            # 检查是否在嵌入式设备上
            if "arm" in platform.machine().lower():
                return "embedded"
            else:
                return "linux"
        else:
            return "unknown"
    
    def _load_engine(self):
        """根据平台加载对应的唤醒引擎"""
        if self.platform == "mac":
            return self._load_mac_engine()
        elif self.platform == "embedded":
            return self._load_embedded_engine()
        else:
            logger.warning(f"未识别的平台: {self.platform}，使用模拟引擎")
            return self._load_mock_engine()
    
    def _load_mac_engine(self):
        """加载Mac平台的唤醒引擎（PicoVoice）"""
        try:
            # 尝试加载PicoVoice
            import pvporcupine
            logger.info("✓ 使用PicoVoice Porcupine引擎")
            
            # 创建Porcupine实例
            # 注意：需要有效的Access Key
            porcupine = pvporcupine.create(
                keywords=['hey porcupine']  # 默认关键词
                # access_key=os.getenv('PORCUPINE_ACCESS_KEY')
            )
            
            return porcupine
            
        except ImportError:
            logger.warning("未安装PicoVoice，使用模拟引擎")
            return self._load_mock_engine()
        except Exception as e:
            logger.error(f"PicoVoice初始化失败: {e}")
            return self._load_mock_engine()
    
    def _load_embedded_engine(self):
        """加载嵌入式平台的唤醒引擎（RKNN模型）"""
        logger.info("⚠️ 嵌入式唤醒引擎需要RKNN模型，当前使用模拟引擎")
        return self._load_mock_engine()
    
    def _load_mock_engine(self):
        """加载模拟引擎（用于开发和测试）"""
        logger.info("使用模拟唤醒引擎")
        
        class MockEngine:
            def __init__(self, wake_words):
                self.wake_words = wake_words
                self.frame_length = 512
            
            def process(self, pcm):
                # 模拟检测逻辑
                return -1  # -1表示未检测到
            
            def delete(self):
                pass
        
        return MockEngine(self.wake_words)
    
    def add_wakeup_callback(self, callback: Callable):
        """添加唤醒回调"""
        self.callbacks.append(callback)
    
    async def start_listening(self):
        """启动监听"""
        if self.is_running:
            return
        
        self.is_running = True
        logger.info("🎧 开始真实唤醒词检测...")
        
        # 持续监听
        await self._listen_loop()
    
    def stop_listening(self):
        """停止监听"""
        self.is_running = False
        logger.info("🛑 停止唤醒词检测")
        
        # 清理引擎
        if hasattr(self.engine, 'delete'):
            self.engine.delete()
    
    async def _listen_loop(self):
        """监听循环"""
        import pyaudio
        import asyncio
        
        # 音频参数
        CHUNK = 512
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 16000
        
        # 初始化音频输入
        audio = pyaudio.PyAudio()
        stream = audio.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK
        )
        
        logger.info("开始从麦克风采集音频...")
        
        try:
            while self.is_running:
                # 读取音频数据
                pcm = stream.read(CHUNK, exception_on_overflow=False)
                
                # 处理音频（转换为整数数组）
                import struct
                pcm_int16 = struct.unpack_from('h' * CHUNK, pcm)
                
                # 调用唤醒引擎检测
                if hasattr(self.engine, 'process'):
                    keyword_index = self.engine.process(pcm_int16)
                    
                    # 如果检测到唤醒词
                    if keyword_index >= 0:
                        logger.info(f"🎉 检测到唤醒词: {self.wake_words[keyword_index]}")
                        
                        # 触发回调
                        for callback in self.callbacks:
                            try:
                                await callback(self.wake_words[keyword_index])
                            except Exception as e:
                                logger.error(f"回调执行失败: {e}")
                
                # 避免占用太多CPU
                await asyncio.sleep(0.001)
        
        except KeyboardInterrupt:
            logger.info("收到中断信号")
        finally:
            # 清理资源
            stream.stop_stream()
            stream.close()
            audio.terminate()
            logger.info("音频流已关闭")


def install_requirements():
    """安装所需的依赖"""
    print("📦 安装唤醒词检测依赖...")
    print("\n1. PicoVoice (Mac/Linux):")
    print("   pip install pvporcupine")
    print("\n2. PyAudio (音频输入):")
    print("   pip install pyaudio")
    print("\n3. 访问Key获取:")
    print("   https://console.picovoice.ai/")
    print("\n⚠️ 嵌入式设备需要RKNN优化模型，请联系开发团队")


async def test_real_wakeup():
    """测试真实唤醒词检测"""
    print("=" * 70)
    print("真实唤醒词检测测试")
    print("=" * 70)
    
    # 检查依赖
    try:
        import pyaudio
        logger.info("✓ PyAudio已安装")
    except ImportError:
        print("❌ 未安装PyAudio，请先安装:")
        print("pip install pyaudio")
        return
    
    # 尝试加载PicoVoice
    try:
        import pvporcupine
        logger.info("✓ PicoVoice已安装")
    except ImportError:
        print("⚠️ 未安装PicoVoice，将使用模拟引擎")
        print("安装命令: pip install pvporcupine")
    
    # 创建唤醒引擎
    engine = RealVoiceWakeupEngine()
    
    # 添加回调
    async def on_wakeup(wake_word: str):
        print(f"\n🎉 唤醒成功: {wake_word}")
        from core.tts_manager import speak
        speak("我在这里")
    
    engine.add_wakeup_callback(on_wakeup)
    
    # 启动监听
    print("\n开始监听唤醒词...")
    print("说出唤醒词：'你好Luna' 或 'Luna你好'")
    print("（按Ctrl+C停止）\n")
    
    try:
        await engine.start_listening()
    except Exception as e:
        print(f"\n错误: {e}")
        print("\n提示：")
        print("1. 检查麦克风权限")
        print("2. 确认PicoVoice已正确安装")
        print("3. 如果是Mac，可能需要处理权限问题")


if __name__ == "__main__":
    import asyncio
    
    print("Luna Badge v1.6 - 真实唤醒词检测")
    print("\n请选择操作：")
    print("1) 测试真实唤醒检测")
    print("2) 查看安装说明")
    
    choice = input("\n请输入选项（1-2）: ").strip()
    
    if choice == "1":
        asyncio.run(test_real_wakeup())
    elif choice == "2":
        install_requirements()
    else:
        print("无效选项")
