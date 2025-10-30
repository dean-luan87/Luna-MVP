"""
Luna Badge v1.6 - 完整真实唤醒词检测实现
实现文件：core/complete_voice_wakeup.py
"""
import os
import asyncio
import struct
from typing import Optional, Callable, List
import logging

logger = logging.getLogger(__name__)


class CompleteVoiceWakeup:
    """
    完整的语音唤醒实现
    集成PicoVoice真实唤醒引擎
    """
    
    def __init__(self, access_key: str = None):
        """
        初始化唤醒系统
        
        Args:
            access_key: PicoVoice Access Key
        """
        self.access_key = access_key or os.getenv('PORCUPINE_ACCESS_KEY')
        self.engine = None
        self.callbacks: List[Callable] = []
        self.is_running = False
        
        # 初始化引擎
        self._initialize_engine()
    
    def _initialize_engine(self):
        """初始化唤醒引擎"""
        try:
            import pvporcupine
            
            # 使用默认关键词
            keywords = ['hey porcupine']
            
            if self.access_key:
                logger.info("使用PicoVoice专业版")
                self.engine = pvporcupine.create(
                    access_key=self.access_key,
                    keywords=keywords
                )
            else:
                logger.info("使用PicoVoice免费版（需要联网）")
                self.engine = pvporcupine.create(keywords=keywords)
            
            logger.info("✓ 唤醒引擎初始化成功")
            
        except ImportError:
            logger.error("❌ 未安装PicoVoice，请运行: pip install pvporcupine")
            self.engine = None
        except Exception as e:
            logger.error(f"❌ PicoVoice初始化失败: {e}")
            self.engine = None
    
    def add_wakeup_callback(self, callback: Callable[[str], None]):
        """添加唤醒回调"""
        self.callbacks.append(callback)
        logger.info(f"✓ 添加唤醒回调: {callback.__name__}")
    
    async def start_listening(self):
        """启动监听"""
        if not self.engine:
            logger.error("唤醒引擎未初始化，无法启动")
            return
        
        if self.is_running:
            logger.warning("监听已在运行中")
            return
        
        self.is_running = True
        logger.info("🎧 开始监听唤醒词...")
        
        # 启动音频流
        await self._audio_stream_loop()
    
    def stop_listening(self):
        """停止监听"""
        self.is_running = False
        logger.info("🛑 停止监听")
    
    async def _audio_stream_loop(self):
        """音频流循环"""
        import pyaudio
        
        try:
            # 音频参数
            sample_rate = self.engine.sample_rate
            frame_length = self.engine.frame_length
            
            # 初始化PyAudio
            audio = pyaudio.PyAudio()
            
            # 打开音频流
            stream = audio.open(
                rate=sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=frame_length
            )
            
            logger.info(f"✓ 音频流已打开 (采样率: {sample_rate}Hz)")
            
            try:
                while self.is_running:
                    # 读取音频数据
                    pcm = stream.read(frame_length, exception_on_overflow=False)
                    
                    # 转换为整数数组
                    pcm_int16 = struct.unpack_from('h' * frame_length, pcm)
                    
                    # 检测唤醒词
                    keyword_index = self.engine.process(pcm_int16)
                    
                    # 如果检测到唤醒词
                    if keyword_index >= 0:
                        wake_word = f"唤醒词{keyword_index}"
                        logger.info(f"🎉 检测到唤醒词: {wake_word}")
                        
                        # 触发所有回调
                        for callback in self.callbacks:
                            try:
                                await callback(wake_word)
                            except Exception as e:
                                logger.error(f"回调执行失败: {e}")
            
            finally:
                # 清理资源
                stream.stop_stream()
                stream.close()
                audio.terminate()
                logger.info("✓ 音频流已关闭")
                
                # 释放引擎
                self.engine.delete()
                
        except Exception as e:
            logger.error(f"音频流错误: {e}")
            self.is_running = False


async def test_complete_wakeup():
    """测试完整唤醒系统"""
    print("=" * 70)
    print("Luna Badge v1.6 - 完整真实唤醒测试")
    print("=" * 70)
    
    # 检查依赖
    print("\n📦 检查依赖...")
    try:
        import pvporcupine
        print("✓ PicoVoice 已安装")
    except ImportError:
        print("❌ 未安装 PicoVoice")
        print("请运行: pip3 install pvporcupine")
        return
    
    try:
        import pyaudio
        print("✓ PyAudio 已安装")
    except ImportError:
        print("❌ 未安装 PyAudio")
        print("请运行: pip3 install pyaudio")
        return
    
    # 创建唤醒系统
    print("\n🚀 初始化唤醒系统...")
    wakeup = CompleteVoiceWakeup()
    
    if not wakeup.engine:
        print("❌ 唤醒引擎初始化失败")
        return
    
    # 添加唤醒回调
    async def on_wakeup(wake_word: str):
        print(f"\n🎉 唤醒成功: {wake_word}")
        from core.tts_manager import speak
        speak("你好，我在这里")
    
    wakeup.add_wakeup_callback(on_wakeup)
    
    # 开始监听
    print("\n🎧 开始监听唤醒词...")
    print("说出唤醒词: 'Hey Porcupine'")
    print("（按Ctrl+C停止）\n")
    
    try:
        await wakeup.start_listening()
    except KeyboardInterrupt:
        print("\n\n收到中断信号，停止监听...")
        wakeup.stop_listening()
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()


async def main():
    """主函数"""
    print("\nLuna Badge v1.6 - 真实唤醒词检测")
    print("\n请确保：")
    print("1. 已安装 pvporcupine 和 pyaudio")
    print("2. 麦克风权限已授予")
    print("3. 麦克风正常工作")
    
    input("\n按Enter开始测试...")
    
    await test_complete_wakeup()


if __name__ == "__main__":
    asyncio.run(main())

