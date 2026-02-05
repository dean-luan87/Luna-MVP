#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 启动流程测试脚本
测试完整的启动流程封装
"""

import asyncio
import logging
import time
from core.startup_manager import StartupManager, StartupStage, quick_startup

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

class MockHardwareInterface:
    """模拟硬件接口"""
    
    async def initialize(self):
        """初始化硬件接口"""
        await asyncio.sleep(0.5)
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

async def test_startup_manager():
    """测试启动管理器"""
    logger.info("🧪 开始测试启动管理器")
    
    # 创建模拟接口
    hardware_interface = MockHardwareInterface()
    voice_interface = MockVoiceInterface()
    
    # 创建启动管理器
    startup_manager = StartupManager(hardware_interface, voice_interface)
    
    # 添加状态回调
    def status_callback(status):
        logger.info(f"📊 状态回调: {status.stage.value} - {status.success} - {status.message}")
    
    startup_manager.add_status_callback(status_callback)
    
    # 设置启动配置
    config = {
        "enable_voice_feedback": True,
        "enable_status_broadcast": True,
        "welcome_message": "Luna Badge 启动完成，准备为您服务",
        "personality_style": "friendly",
        "check_intervals": {
            "hardware_check": 1.0,  # 缩短测试时间
            "network_check": 1.0,
            "module_init": 0.5
        }
    }
    startup_manager.set_config(config)
    
    # 执行完整启动序列
    logger.info("🚀 开始执行完整启动序列")
    start_time = time.time()
    
    success = await startup_manager.full_startup_sequence()
    
    end_time = time.time()
    duration = end_time - start_time
    
    # 输出结果
    if success:
        logger.info("🎉 启动序列执行成功！")
    else:
        logger.error("❌ 启动序列执行失败！")
    
    # 获取启动总结
    summary = startup_manager.get_startup_summary()
    logger.info(f"📊 启动总结:")
    logger.info(f"  - 启动完成: {summary['startup_complete']}")
    logger.info(f"  - 总阶段数: {summary['total_stages']}")
    logger.info(f"  - 成功阶段数: {summary['successful_stages']}")
    logger.info(f"  - 成功率: {summary['success_rate']:.2%}")
    logger.info(f"  - 启动耗时: {duration:.2f}秒")
    
    # 显示语音队列状态
    voice_status = voice_interface.get_queue_status()
    logger.info(f"🗣️ 语音播报状态:")
    logger.info(f"  - 队列大小: {voice_status['queue_size']}")
    logger.info(f"  - 最近消息: {voice_status['recent_messages']}")
    
    return success

async def test_quick_startup():
    """测试快速启动函数"""
    logger.info("🧪 开始测试快速启动函数")
    
    # 创建模拟接口
    hardware_interface = MockHardwareInterface()
    voice_interface = MockVoiceInterface()
    
    # 设置配置
    config = {
        "enable_voice_feedback": True,
        "enable_status_broadcast": True,
        "welcome_message": "快速启动完成！",
        "personality_style": "professional",
        "check_intervals": {
            "hardware_check": 0.5,
            "network_check": 0.5,
            "module_init": 0.3
        }
    }
    
    # 执行快速启动
    start_time = time.time()
    success = await quick_startup(hardware_interface, voice_interface, config)
    end_time = time.time()
    duration = end_time - start_time
    
    if success:
        logger.info(f"🎉 快速启动成功！耗时: {duration:.2f}秒")
    else:
        logger.error("❌ 快速启动失败！")
    
    return success

async def test_individual_stages():
    """测试各个启动阶段"""
    logger.info("🧪 开始测试各个启动阶段")
    
    # 创建模拟接口
    hardware_interface = MockHardwareInterface()
    voice_interface = MockVoiceInterface()
    
    # 创建启动管理器
    startup_manager = StartupManager(hardware_interface, voice_interface)
    
    # 测试各个阶段
    stages = [
        (startup_manager.power_on, "设备上电"),
        (startup_manager.system_init, "系统初始化"),
        (startup_manager.module_init, "模块初始化"),
        (startup_manager.hardware_check, "硬件检查"),
        (startup_manager.network_check, "网络检查"),
        (startup_manager.welcome_message, "欢迎语播报"),
        (startup_manager.ready_to_serve, "准备就绪"),
        (startup_manager.start_recognition, "开始识别循环")
    ]
    
    for stage_func, stage_name in stages:
        logger.info(f"🔄 测试阶段: {stage_name}")
        try:
            success = await stage_func()
            if success:
                logger.info(f"✅ {stage_name}测试成功")
            else:
                logger.error(f"❌ {stage_name}测试失败")
        except Exception as e:
            logger.error(f"❌ {stage_name}测试异常: {e}")
        
        # 短暂等待
        await asyncio.sleep(0.5)

async def main():
    """主测试函数"""
    logger.info("🚀 开始Luna Badge启动流程测试")
    
    # 测试1: 启动管理器
    logger.info("=" * 50)
    logger.info("测试1: 启动管理器")
    logger.info("=" * 50)
    success1 = await test_startup_manager()
    
    # 测试2: 快速启动函数
    logger.info("=" * 50)
    logger.info("测试2: 快速启动函数")
    logger.info("=" * 50)
    success2 = await test_quick_startup()
    
    # 测试3: 各个启动阶段
    logger.info("=" * 50)
    logger.info("测试3: 各个启动阶段")
    logger.info("=" * 50)
    await test_individual_stages()
    
    # 总结
    logger.info("=" * 50)
    logger.info("测试总结")
    logger.info("=" * 50)
    logger.info(f"启动管理器测试: {'✅ 通过' if success1 else '❌ 失败'}")
    logger.info(f"快速启动函数测试: {'✅ 通过' if success2 else '❌ 失败'}")
    logger.info("各个启动阶段测试: ✅ 完成")
    
    if success1 and success2:
        logger.info("🎉 所有测试通过！启动流程封装正常工作")
    else:
        logger.error("❌ 部分测试失败！请检查启动流程")

if __name__ == "__main__":
    # 运行测试
    asyncio.run(main())
