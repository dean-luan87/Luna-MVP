#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 快速启动测试
快速验证启动流程封装功能
"""

import asyncio
import logging
from core.startup_manager import StartupManager, quick_startup

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

class MockHardwareInterface:
    """模拟硬件接口"""
    
    async def initialize(self):
        """初始化硬件接口"""
        await asyncio.sleep(0.2)
        logger.info("🔧 模拟硬件接口初始化完成")
    
    def get_info(self):
        """获取硬件信息"""
        return {
            "camera": "ready",
            "microphone": "ready",
            "speaker": "ready"
        }

class MockVoiceInterface:
    """模拟语音接口"""
    
    def __init__(self):
        self.speech_queue = []
    
    def speak_async(self, text: str):
        """异步语音播报"""
        self.speech_queue.append(text)
        logger.info(f"🗣️ 模拟语音播报: {text}")
    
    def get_queue_status(self):
        """获取语音队列状态"""
        return {
            "queue_size": len(self.speech_queue),
            "recent_messages": self.speech_queue[-3:] if self.speech_queue else []
        }

async def test_quick_startup():
    """测试快速启动功能"""
    logger.info("🧪 开始测试快速启动功能")
    
    # 创建模拟接口
    hardware_interface = MockHardwareInterface()
    voice_interface = MockVoiceInterface()
    
    # 设置快速启动配置
    config = {
        "enable_voice_feedback": True,
        "enable_status_broadcast": True,
        "welcome_message": "快速启动测试完成！",
        "personality_style": "friendly",
        "check_intervals": {
            "hardware_check": 0.5,  # 快速测试
            "network_check": 0.5,
            "module_init": 0.3
        }
    }
    
    # 执行快速启动
    logger.info("🚀 开始快速启动")
    success = await quick_startup(hardware_interface, voice_interface, config)
    
    if success:
        logger.info("🎉 快速启动测试成功！")
        
        # 显示语音播报状态
        voice_status = voice_interface.get_queue_status()
        logger.info(f"🗣️ 语音播报状态:")
        logger.info(f"  - 队列大小: {voice_status['queue_size']}")
        logger.info(f"  - 最近消息: {voice_status['recent_messages']}")
        
        return True
    else:
        logger.error("❌ 快速启动测试失败！")
        return False

async def test_startup_manager():
    """测试启动管理器"""
    logger.info("🧪 开始测试启动管理器")
    
    # 创建模拟接口
    hardware_interface = MockHardwareInterface()
    voice_interface = MockVoiceInterface()
    
    # 创建启动管理器
    startup_manager = StartupManager(hardware_interface, voice_interface)
    
    # 设置配置
    config = {
        "enable_voice_feedback": True,
        "enable_status_broadcast": True,
        "welcome_message": "启动管理器测试完成！",
        "personality_style": "professional",
        "check_intervals": {
            "hardware_check": 0.5,
            "network_check": 0.5,
            "module_init": 0.3
        }
    }
    startup_manager.set_config(config)
    
    # 添加状态回调
    def status_callback(status):
        logger.info(f"📊 状态回调: {status.stage.value} - {status.success} - {status.message}")
    
    startup_manager.add_status_callback(status_callback)
    
    # 执行启动序列
    logger.info("🚀 开始启动序列")
    success = await startup_manager.full_startup_sequence()
    
    if success:
        logger.info("🎉 启动管理器测试成功！")
        
        # 显示启动总结
        summary = startup_manager.get_startup_summary()
        logger.info(f"📊 启动总结:")
        logger.info(f"  - 启动完成: {summary['startup_complete']}")
        logger.info(f"  - 成功率: {summary['success_rate']:.2%}")
        logger.info(f"  - 启动耗时: {summary['startup_duration']:.2f}秒")
        
        return True
    else:
        logger.error("❌ 启动管理器测试失败！")
        return False

async def main():
    """主测试函数"""
    logger.info("🚀 开始Luna Badge快速启动测试")
    
    # 测试1: 快速启动功能
    logger.info("=" * 50)
    logger.info("测试1: 快速启动功能")
    logger.info("=" * 50)
    success1 = await test_quick_startup()
    
    # 测试2: 启动管理器
    logger.info("=" * 50)
    logger.info("测试2: 启动管理器")
    logger.info("=" * 50)
    success2 = await test_startup_manager()
    
    # 总结
    logger.info("=" * 50)
    logger.info("测试总结")
    logger.info("=" * 50)
    logger.info(f"快速启动功能测试: {'✅ 通过' if success1 else '❌ 失败'}")
    logger.info(f"启动管理器测试: {'✅ 通过' if success2 else '❌ 失败'}")
    
    if success1 and success2:
        logger.info("🎉 所有测试通过！启动流程封装正常工作")
        return True
    else:
        logger.error("❌ 部分测试失败！请检查启动流程")
        return False

if __name__ == "__main__":
    # 运行测试
    try:
        success = asyncio.run(main())
        if success:
            print("\n🎉 快速启动测试完成！启动流程封装功能正常")
        else:
            print("\n❌ 快速启动测试失败！请检查启动流程")
    except KeyboardInterrupt:
        print("\n⚠️ 测试被用户中断")
    except Exception as e:
        print(f"\n❌ 测试异常: {e}")
