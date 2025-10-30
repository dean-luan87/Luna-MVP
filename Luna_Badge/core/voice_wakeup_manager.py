"""
Luna Badge v1.6 - 语音交互增强：真实语音唤醒与待机管理
实现文件：core/voice_wakeup_manager.py
"""
import os
import json
import asyncio
from typing import Optional, Callable, Dict, Any
from enum import Enum
from datetime import datetime
from core.tts_manager import speak


class SystemState(Enum):
    """系统状态"""
    OFF = "off"                    # 关机
    SLEEP = "sleep"                # 待机/睡眠
    IDLE = "idle"                  # 空闲
    LISTENING = "listening"        # 监听中
    ACTIVE = "active"              # 活跃/对话中
    PROCESSING = "processing"      # 处理中


class VoiceWakeupManager:
    """
    语音唤醒与待机管理器
    功能：管理系统待机状态、真实唤醒词检测、状态切换
    """
    
    def __init__(self):
        self.current_state = SystemState.SLEEP
        self.wakeup_callbacks: list[Callable] = []
        self.last_wakeup_time: Optional[datetime] = None
        self.sleep_timeout = 300  # 5分钟无活动进入待机
        self.wake_words = ["你好Luna", "Luna你好", "小智小智", "嘿Luna"]
        self.wakeup_enabled = True
        
        # 读取配置
        self._load_config()
    
    def _load_config(self):
        """加载配置"""
        config_path = "data/wakeup_config.json"
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config = json.load(f)
                self.sleep_timeout = config.get('sleep_timeout', 300)
                self.wake_words = config.get('wake_words', self.wake_words)
    
    async def start_continuous_listening(self):
        """
        启动连续监听（用于真实唤醒词检测）
        
        实际实现应该：
        1. 持续从麦克风采集音频
        2. 调用唤醒词检测引擎（PicoVoice/Porcupine）
        3. 检测到唤醒词后触发回调
        """
        if not self.wakeup_enabled:
            return
        
        # 在待机状态下启动监听
        if self.current_state == SystemState.SLEEP:
            self.current_state = SystemState.LISTENING
            print("🎧 开始监听唤醒词...")
            
            # TODO: 集成真实唤醒词检测
            # while True:
            #     audio = await capture_audio()
            #     wake_word = await detect_wake_word(audio)
            #     if wake_word:
            #         await self._on_wakeup_detected(wake_word)
    
    async def _on_wakeup_detected(self, wake_word: str):
        """唤醒词检测回调"""
        if self.current_state != SystemState.LISTENING:
            return
        
        self.current_state = SystemState.ACTIVE
        self.last_wakeup_time = datetime.now()
        
        print(f"✅ 检测到唤醒词: {wake_word}")
        
        # 语音反馈（轻柔提示音或简短回复）
        speak("嗯")
        
        # 触发回调
        for callback in self.wakeup_callbacks:
            try:
                await callback(wake_word)
            except Exception as e:
                print(f"回调执行失败: {e}")
    
    def enter_sleep_mode(self):
        """
        进入待机模式
        - 停止连续监听
        - 降低功耗
        - 保持唤醒词检测活跃
        """
        if self.current_state in [SystemState.SLEEP, SystemState.OFF]:
            return
        
        self.current_state = SystemState.SLEEP
        print("💤 进入待机模式")
        
        # 保持唤醒词检测活跃（需要事件循环）
        # 在实际运行时，应该在异步环境中调用
        # try:
        #     asyncio.create_task(self.start_continuous_listening())
        # except RuntimeError:
        #     # 如果没有运行中的事件循环，跳过
        #     pass
    
    def enter_idle_mode(self):
        """
        进入空闲模式
        - 系统已唤醒但未在处理任务
        - 等待用户指令
        """
        self.current_state = SystemState.IDLE
        print("⏸️ 进入空闲模式")
        
        # 开始倒计时，如果超时则进入待机
        # TODO: 实现倒计时逻辑
    
    def enter_active_mode(self):
        """
        进入活跃模式
        - 正在处理用户请求
        - 需要语音反馈
        """
        self.current_state = SystemState.ACTIVE
        print("🎤 进入活跃模式")
    
    def enter_processing_mode(self):
        """
        进入处理模式
        - 正在执行复杂任务
        - 可能需要较长时间
        """
        self.current_state = SystemState.PROCESSING
        print("⚙️ 进入处理模式")
    
    def add_wakeup_callback(self, callback: Callable):
        """
        添加唤醒回调
        
        Args:
            callback: 唤醒时调用的函数
        """
        self.wakeup_callbacks.append(callback)
    
    def get_current_state(self) -> SystemState:
        """获取当前状态"""
        return self.current_state
    
    def is_ready(self) -> bool:
        """系统是否准备好接收指令"""
        return self.current_state in [SystemState.IDLE, SystemState.ACTIVE]


class IdleTimeoutManager:
    """
    待机超时管理器
    功能：检测无活动时间，自动进入待机
    """
    
    def __init__(self, timeout_seconds: int = 300):
        self.timeout_seconds = timeout_seconds
        self.last_activity_time = datetime.now()
        self.timeout_handlers: list[Callable] = []
    
    def update_activity(self):
        """更新活动时间"""
        self.last_activity_time = datetime.now()
    
    def check_timeout(self) -> bool:
        """检查是否超时"""
        now = datetime.now()
        elapsed = (now - self.last_activity_time).total_seconds()
        
        return elapsed >= self.timeout_seconds
    
    def add_timeout_handler(self, handler: Callable):
        """添加超时处理函数"""
        self.timeout_handlers.append(handler)
    
    async def run_timeout_checker(self):
        """运行超时检查器"""
        while True:
            await asyncio.sleep(10)  # 每10秒检查一次
            
            if self.check_timeout():
                print("⏰ 检测到超时，进入待机")
                for handler in self.timeout_handlers:
                    try:
                        await handler()
                    except Exception as e:
                        print(f"超时处理失败: {e}")
                
                self.update_activity()


def setup_wakeup_manager() -> VoiceWakeupManager:
    """
    设置并启动唤醒管理器
    
    Returns:
        唤醒管理器实例
    """
    manager = VoiceWakeupManager()
    
    # 添加超时管理器
    timeout_manager = IdleTimeoutManager(timeout_seconds=300)
    
    # 超时时进入待机
    timeout_manager.add_timeout_handler(manager.enter_sleep_mode)
    
    # 启动超时检查
    asyncio.create_task(timeout_manager.run_timeout_checker())
    
    # 启动监听
    asyncio.create_task(manager.start_continuous_listening())
    
    return manager


async def test_wakeup_flow():
    """测试唤醒流程"""
    print("=" * 60)
    print("语音唤醒与待机管理测试")
    print("=" * 60)
    
    manager = setup_wakeup_manager()
    
    # 添加唤醒回调
    async def on_wakeup(wake_word: str):
        print(f"\n🎉 用户唤醒了系统: {wake_word}")
        speak("你好，我在这里")
        
        # 模拟处理用户请求
        await asyncio.sleep(2)
        
        # 进入空闲
        manager.enter_idle_mode()
    
    manager.add_wakeup_callback(on_wakeup)
    
    print("\n系统已启动，等待唤醒...")
    print("（在实际设备上，说出唤醒词即可唤醒）")
    print("（按Ctrl+C退出）")
    
    # 保持运行
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\n测试结束")


if __name__ == "__main__":
    asyncio.run(test_wakeup_flow())
