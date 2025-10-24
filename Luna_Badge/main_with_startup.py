#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 主程序 - 集成启动流程封装
展示如何在主程序中使用启动流程管理器
"""

import asyncio
import logging
import signal
import sys
from typing import Optional

from core.startup_manager import StartupManager, StartupStage
from hal_mac.hardware_mac import MacHAL
from core.ai_navigation import AINavigation
from core.system_control import SystemControl

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

class LunaBadgeMain:
    """Luna Badge 主程序类"""
    
    def __init__(self):
        """初始化主程序"""
        self.hardware_interface: Optional[MacHAL] = None
        self.ai_navigation: Optional[AINavigation] = None
        self.system_control: Optional[SystemControl] = None
        self.startup_manager: Optional[StartupManager] = None
        
        # 运行状态
        self.is_running = False
        self.startup_complete = False
        
        logger.info("🌟 Luna Badge 主程序初始化")
    
    async def initialize_components(self):
        """初始化组件"""
        try:
            logger.info("🔧 开始初始化组件")
            
            # 初始化硬件接口
            self.hardware_interface = MacHAL()
            logger.info("✅ 硬件接口初始化完成")
            
            # 初始化AI导航
            self.ai_navigation = AINavigation()
            logger.info("✅ AI导航初始化完成")
            
            # 初始化系统控制
            self.system_control = SystemControl()
            logger.info("✅ 系统控制初始化完成")
            
            return True
        except Exception as e:
            logger.error(f"❌ 组件初始化失败: {e}")
            return False
    
    def create_startup_manager(self):
        """创建启动管理器"""
        if not self.hardware_interface:
            raise RuntimeError("硬件接口未初始化")
        
        self.startup_manager = StartupManager(
            hardware_interface=self.hardware_interface,
            voice_interface=self.hardware_interface.tts
        )
        
        # 设置启动配置
        config = {
            "enable_voice_feedback": True,
            "enable_status_broadcast": True,
            "welcome_message": "Luna Badge 启动完成，准备为您服务",
            "personality_style": "friendly",
            "check_intervals": {
                "hardware_check": 2.0,
                "network_check": 3.0,
                "module_init": 1.0
            }
        }
        self.startup_manager.set_config(config)
        
        # 添加状态回调
        self.startup_manager.add_status_callback(self.on_startup_status_change)
        
        logger.info("✅ 启动管理器创建完成")
    
    def on_startup_status_change(self, status):
        """启动状态变化回调"""
        logger.info(f"📊 启动状态变化: {status.stage.value} - {status.message}")
        
        # 根据状态执行相应操作
        if status.stage == StartupStage.HARDWARE_CHECK and status.success:
            logger.info("🎥 摄像头已就绪，可以开始视觉识别")
        
        elif status.stage == StartupStage.NETWORK_CHECK and status.success:
            logger.info("🌐 网络已连接，可以访问云端服务")
        
        elif status.stage == StartupStage.WELCOME_MESSAGE and status.success:
            logger.info("👋 欢迎语播报完成，用户已收到问候")
        
        elif status.stage == StartupStage.START_RECOGNITION and status.success:
            logger.info("🔄 开始识别循环，系统进入工作状态")
            self.startup_complete = True
    
    async def run_startup_sequence(self):
        """运行启动序列"""
        logger.info("🚀 开始运行Luna Badge启动序列")
        
        # 初始化组件
        if not await self.initialize_components():
            logger.error("❌ 组件初始化失败，无法继续启动")
            return False
        
        # 创建启动管理器
        self.create_startup_manager()
        
        # 执行完整启动序列
        success = await self.startup_manager.full_startup_sequence()
        
        if success:
            logger.info("🎉 Luna Badge启动序列完成！")
            
            # 显示启动总结
            summary = self.startup_manager.get_startup_summary()
            self.display_startup_summary(summary)
            
            return True
        else:
            logger.error("❌ Luna Badge启动序列失败！")
            return False
    
    def display_startup_summary(self, summary):
        """显示启动总结"""
        logger.info("📊 启动总结:")
        logger.info(f"  - 启动完成: {summary['startup_complete']}")
        logger.info(f"  - 总阶段数: {summary['total_stages']}")
        logger.info(f"  - 成功阶段数: {summary['successful_stages']}")
        logger.info(f"  - 成功率: {summary['success_rate']:.2%}")
        logger.info(f"  - 启动耗时: {summary['startup_duration']:.2f}秒")
    
    async def run_main_loop(self):
        """运行主循环"""
        logger.info("🔄 开始运行主循环")
        
        try:
            while self.is_running:
                # 检查启动状态
                if not self.startup_complete:
                    logger.warning("⚠️ 启动未完成，等待启动完成...")
                    await asyncio.sleep(1)
                    continue
                
                # 运行AI导航
                if self.ai_navigation:
                    try:
                        await self.ai_navigation.run_cycle()
                    except Exception as e:
                        logger.error(f"❌ AI导航运行异常: {e}")
                
                # 运行系统控制
                if self.system_control:
                    try:
                        await self.system_control.run_cycle()
                    except Exception as e:
                        logger.error(f"❌ 系统控制运行异常: {e}")
                
                # 短暂等待
                await asyncio.sleep(0.1)
                
        except Exception as e:
            logger.error(f"❌ 主循环运行异常: {e}")
        finally:
            logger.info("🔄 主循环结束")
    
    async def shutdown(self):
        """关闭系统"""
        logger.info("🔄 开始关闭系统")
        
        self.is_running = False
        
        # 关闭AI导航
        if self.ai_navigation:
            try:
                await self.ai_navigation.shutdown()
                logger.info("✅ AI导航关闭完成")
            except Exception as e:
                logger.error(f"❌ AI导航关闭失败: {e}")
        
        # 关闭系统控制
        if self.system_control:
            try:
                await self.system_control.shutdown()
                logger.info("✅ 系统控制关闭完成")
            except Exception as e:
                logger.error(f"❌ 系统控制关闭失败: {e}")
        
        # 关闭硬件接口
        if self.hardware_interface:
            try:
                await self.hardware_interface.shutdown()
                logger.info("✅ 硬件接口关闭完成")
            except Exception as e:
                logger.error(f"❌ 硬件接口关闭失败: {e}")
        
        logger.info("🏁 系统关闭完成")
    
    def setup_signal_handlers(self):
        """设置信号处理器"""
        def signal_handler(signum, frame):
            logger.info(f"📡 收到信号 {signum}，开始关闭系统")
            asyncio.create_task(self.shutdown())
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    async def run(self):
        """运行主程序"""
        logger.info("🌟 开始运行Luna Badge主程序")
        
        try:
            # 设置信号处理器
            self.setup_signal_handlers()
            
            # 运行启动序列
            startup_success = await self.run_startup_sequence()
            
            if not startup_success:
                logger.error("❌ 启动失败，程序退出")
                return False
            
            # 设置运行状态
            self.is_running = True
            
            # 运行主循环
            await self.run_main_loop()
            
            return True
            
        except KeyboardInterrupt:
            logger.info("⚠️ 用户中断程序")
            return False
        except Exception as e:
            logger.error(f"❌ 程序运行异常: {e}")
            return False
        finally:
            # 确保系统正确关闭
            await self.shutdown()

async def main():
    """主函数"""
    logger.info("🚀 启动Luna Badge主程序")
    
    # 创建主程序实例
    app = LunaBadgeMain()
    
    try:
        # 运行主程序
        success = await app.run()
        
        if success:
            logger.info("🎉 Luna Badge主程序运行成功")
        else:
            logger.error("❌ Luna Badge主程序运行失败")
            
    except Exception as e:
        logger.error(f"❌ 主程序异常: {e}")
    finally:
        logger.info("🏁 Luna Badge主程序结束")

if __name__ == "__main__":
    # 运行主程序
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("⚠️ 程序被用户中断")
    except Exception as e:
        logger.error(f"❌ 程序异常: {e}")
    finally:
        sys.exit(0)
