#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 主程序 - 集成故障处理、日志持久化和可视化显示
展示如何在主程序中使用这些集成功能
"""

import asyncio
import logging
import time
import numpy as np
from typing import Optional, Dict, Any, List

from core.fault_handler import FaultHandler, FaultType, FaultSeverity, handle_fault
from core.log_manager import LogManager, LogLevel, EventType, log_voice_broadcast, log_path_status, log_ai_detection
from core.visual_display import VisualDisplayManager, DetectionBox, PathRegion, PathStatus, update_display
from core.startup_manager import StartupManager, StartupStage

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

class LunaBadgeIntegratedMain:
    """Luna Badge 集成主程序类"""
    
    def __init__(self):
        """初始化集成主程序"""
        # 核心组件
        self.fault_handler: Optional[FaultHandler] = None
        self.log_manager: Optional[LogManager] = None
        self.visual_display: Optional[VisualDisplayManager] = None
        self.startup_manager: Optional[StartupManager] = None
        
        # 运行状态
        self.is_running = False
        self.startup_complete = False
        
        logger.info("🌟 Luna Badge 集成主程序初始化")
    
    async def initialize_components(self):
        """初始化组件"""
        try:
            logger.info("🔧 开始初始化集成组件")
            
            # 初始化故障处理器
            self.fault_handler = FaultHandler()
            self.fault_handler.add_fault_callback(self.on_fault_occurred)
            logger.info("✅ 故障处理器初始化完成")
            
            # 初始化日志管理器
            self.log_manager = LogManager()
            logger.info("✅ 日志管理器初始化完成")
            
            # 初始化可视化显示管理器
            self.visual_display = VisualDisplayManager(enable_display=True)
            logger.info("✅ 可视化显示管理器初始化完成")
            
            # 初始化启动管理器
            self.startup_manager = StartupManager()
            self.startup_manager.add_status_callback(self.on_startup_status_change)
            logger.info("✅ 启动管理器初始化完成")
            
            return True
        except Exception as e:
            logger.error(f"❌ 组件初始化失败: {e}")
            # 记录故障
            if self.fault_handler:
                handle_fault(FaultType.SOFTWARE, FaultSeverity.CRITICAL, "System", f"组件初始化失败: {e}")
            return False
    
    def on_fault_occurred(self, fault_info):
        """故障发生回调"""
        logger.error(f"🚨 故障发生: {fault_info.fault_id} - {fault_info.error_message}")
        
        # 记录故障日志
        if self.log_manager:
            self.log_manager.log_fault(
                fault_info.fault_type.value,
                fault_info.fault_id,
                fault_info.severity.value,
                fault_info.error_message,
                fault_info.recovery_attempts
            )
        
        # 根据故障严重程度决定处理策略
        if fault_info.severity == FaultSeverity.CRITICAL:
            logger.error("🚨 严重故障，系统可能无法正常工作")
        elif fault_info.severity == FaultSeverity.HIGH:
            logger.warning("⚠️ 高严重程度故障，部分功能可能受影响")
    
    def on_startup_status_change(self, status):
        """启动状态变化回调"""
        logger.info(f"📊 启动状态变化: {status.stage.value} - {status.message}")
        
        # 记录启动状态日志
        if self.log_manager:
            self.log_manager.log(
                LogLevel.INFO,
                EventType.SYSTEM_START,
                "Startup",
                f"启动阶段: {status.stage.value} - {status.message}"
            )
        
        # 根据状态执行相应操作
        if status.stage == StartupStage.START_RECOGNITION and status.success:
            self.startup_complete = True
            logger.info("🔄 开始识别循环，系统进入工作状态")
    
    async def run_startup_sequence(self):
        """运行启动序列"""
        logger.info("🚀 开始运行Luna Badge启动序列")
        
        # 初始化组件
        if not await self.initialize_components():
            logger.error("❌ 组件初始化失败，无法继续启动")
            return False
        
        # 执行启动序列
        if self.startup_manager:
            success = await self.startup_manager.full_startup_sequence()
            
            if success:
                logger.info("🎉 Luna Badge启动序列完成！")
                return True
            else:
                logger.error("❌ Luna Badge启动序列失败！")
                return False
        
        return False
    
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
                
                # 模拟AI检测和处理
                await self.simulate_ai_detection()
                
                # 短暂等待
                await asyncio.sleep(0.1)
                
        except Exception as e:
            logger.error(f"❌ 主循环运行异常: {e}")
            # 记录故障
            if self.fault_handler:
                handle_fault(FaultType.SOFTWARE, FaultSeverity.HIGH, "MainLoop", f"主循环异常: {e}")
        finally:
            logger.info("🔄 主循环结束")
    
    async def simulate_ai_detection(self):
        """模拟AI检测"""
        try:
            # 创建模拟帧
            frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
            
            # 模拟检测结果
            detections = []
            path_status = PathStatus.CLEAR
            broadcast_message = "路径畅通"
            
            # 随机生成检测结果
            import random
            if random.random() < 0.3:  # 30%概率检测到障碍物
                detections = [
                    DetectionBox(100, 100, 200, 300, 0.95, "person", (255, 0, 0)),
                    DetectionBox(300, 150, 400, 250, 0.87, "car", (255, 165, 0))
                ]
                path_status = PathStatus.BLOCKED
                broadcast_message = "前方检测到障碍物，请注意安全"
            
            # 记录AI检测日志
            if self.log_manager:
                log_ai_detection("person", [{"type": "person", "confidence": 0.95}], 0.95, 0.1)
            
            # 记录路径状态日志
            if self.log_manager:
                if path_status == PathStatus.BLOCKED:
                    log_path_status("blocked", len(detections), 0, [det.label for det in detections])
                else:
                    log_path_status("clear", 0, 1, [])
            
            # 记录语音播报日志
            if self.log_manager:
                log_voice_broadcast(broadcast_message, "tts", True, 1.5)
            
            # 更新可视化显示
            if self.visual_display:
                self.visual_display.update_display(
                    frame=frame,
                    detections=detections,
                    path_status=path_status,
                    broadcast_message=broadcast_message,
                    performance_info={"FPS": 30, "Detection Time": "0.05s", "Memory Usage": "256MB"}
                )
            
            # 处理故障（如果有）
            if len(detections) > 2:
                handle_fault(FaultType.AI_MODEL, FaultSeverity.MEDIUM, "AI", "检测到过多障碍物")
                
        except Exception as e:
            logger.error(f"❌ AI检测模拟异常: {e}")
            # 记录故障
            if self.fault_handler:
                handle_fault(FaultType.AI_MODEL, FaultSeverity.HIGH, "AI", f"AI检测异常: {e}")
    
    async def shutdown(self):
        """关闭系统"""
        logger.info("🔄 开始关闭系统")
        
        self.is_running = False
        
        # 关闭可视化显示
        if self.visual_display:
            try:
                self.visual_display.stop()
                logger.info("✅ 可视化显示关闭完成")
            except Exception as e:
                logger.error(f"❌ 可视化显示关闭失败: {e}")
        
        # 关闭日志管理器
        if self.log_manager:
            try:
                self.log_manager.stop()
                logger.info("✅ 日志管理器关闭完成")
            except Exception as e:
                logger.error(f"❌ 日志管理器关闭失败: {e}")
        
        # 关闭故障处理器
        if self.fault_handler:
            try:
                # 清除已解决的故障
                self.fault_handler.clear_resolved_faults()
                logger.info("✅ 故障处理器关闭完成")
            except Exception as e:
                logger.error(f"❌ 故障处理器关闭失败: {e}")
        
        logger.info("🏁 系统关闭完成")
    
    async def run(self):
        """运行主程序"""
        logger.info("🌟 开始运行Luna Badge集成主程序")
        
        try:
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
            # 记录故障
            if self.fault_handler:
                handle_fault(FaultType.SOFTWARE, FaultSeverity.CRITICAL, "System", f"程序运行异常: {e}")
            return False
        finally:
            # 确保系统正确关闭
            await self.shutdown()

async def main():
    """主函数"""
    logger.info("🚀 启动Luna Badge集成主程序")
    
    # 创建主程序实例
    app = LunaBadgeIntegratedMain()
    
    try:
        # 运行主程序
        success = await app.run()
        
        if success:
            logger.info("🎉 Luna Badge集成主程序运行成功")
        else:
            logger.error("❌ Luna Badge集成主程序运行失败")
            
    except Exception as e:
        logger.error(f"❌ 主程序异常: {e}")
    finally:
        logger.info("🏁 Luna Badge集成主程序结束")

if __name__ == "__main__":
    # 运行主程序
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("⚠️ 程序被用户中断")
    except Exception as e:
        logger.error(f"❌ 程序异常: {e}")
