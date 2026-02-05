"""
Luna Badge v1.6 - 完整真实唤醒测试（兼容Python 3.9）
"""
import sys
import os

# 检查Python版本
if sys.version_info < (3, 8):
    print("需要Python 3.8或更高版本")
    sys.exit(1)

# 添加路径
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

try:
    import pvporcupine
    import pyaudio
    print("✅ 所有依赖已安装")
    
    import asyncio
    from core.complete_voice_wakeup import CompleteVoiceWakeup
    
    async def main():
        """测试唤醒"""
        print("=" * 70)
        print("Luna Badge v1.6 - 真实唤醒测试")
        print("=" * 70)
        
        # 创建唤醒系统
        wakeup = CompleteVoiceWakeup()
        
        if not wakeup.engine:
            print("❌ 唤醒引擎未初始化")
            return
        
        # 添加回调
        async def on_wakeup(wake_word: str):
            print(f"\n🎉 检测到唤醒词: {wake_word}")
            from core.tts_manager import speak
            speak("你好")
        
        wakeup.add_wakeup_callback(on_wakeup)
        
        print("\n🎧 开始监听...")
        print("唤醒词: 'Hey Porcupine'")
        print("按Ctrl+C退出")
        
        try:
            await wakeup.start_listening()
        except KeyboardInterrupt:
            print("\n停止")
            wakeup.stop_listening()
    
    # 运行
    asyncio.run(main())
    
except ImportError as e:
    print(f"❌ 缺少依赖: {e}")
    print("\n请安装依赖:")
    print("pip3 install pvporcupine pyaudio")
except Exception as e:
    print(f"❌ 错误: {e}")
    import traceback
    traceback.print_exc()

