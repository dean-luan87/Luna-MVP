#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 启动流程管理器
负责从设备上电到开始识别循环的完整启动流程
"""

import time
import logging
import asyncio
from typing import Dict, Any, Optional, Callable
from enum import Enum
from dataclasses import dataclass

logger = logging.getLogger(__name__)

class StartupStage(Enum):
    """启动阶段枚举"""
    POWER_ON = "power_on"           # 设备上电
    SYSTEM_INIT = "system_init"     # 系统初始化
    MODULE_INIT = "module_init"     # 模块初始化
    HARDWARE_CHECK = "hardware_check"  # 硬件检查
    NETWORK_CHECK = "network_check"    # 网络检查
    WELCOME_MESSAGE = "welcome_message"  # 欢迎语播报
    READY_TO_SERVE = "ready_to_serve"   # 准备就绪
    START_RECOGNITION = "start_recognition"  # 开始识别循环

@dataclass
class StartupStatus:
    """启动状态数据类"""
    stage: StartupStage
    success: bool
    message: str
    timestamp: float
    details: Dict[str, Any]

class StartupManager:
    """启动流程管理器"""
    
    def __init__(self, hardware_interface=None, voice_interface=None):
        """
        初始化启动管理器
        
        Args:
            hardware_interface: 硬件接口实例
            voice_interface: 语音接口实例
        """
        self.hardware_interface = hardware_interface
        self.voice_interface = voice_interface
        self.startup_status = []
        self.current_stage = None
        self.startup_complete = False
        
        # 启动配置
        self.config = {
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
        
        # 状态回调函数
        self.status_callbacks = []
        
        logger.info("🚀 Luna Badge 启动管理器初始化完成")
    
    def add_status_callback(self, callback: Callable[[StartupStatus], None]):
        """
        添加状态变化回调函数
        
        Args:
            callback: 状态变化回调函数
        """
        self.status_callbacks.append(callback)
        logger.debug(f"✅ 添加状态回调函数: {callback.__name__}")
    
    def _broadcast_status(self, stage: StartupStage, success: bool, message: str, details: Dict[str, Any] = None):
        """
        播报启动状态
        
        Args:
            stage: 启动阶段
            success: 是否成功
            message: 状态消息
            details: 详细信息
        """
        if details is None:
            details = {}
            
        status = StartupStatus(
            stage=stage,
            success=success,
            message=message,
            timestamp=time.time(),
            details=details
        )
        
        # 记录状态
        self.startup_status.append(status)
        self.current_stage = stage
        
        # 播报状态
        if self.config["enable_status_broadcast"] and self.voice_interface:
            try:
                if success:
                    broadcast_message = f"✅ {message}"
                else:
                    broadcast_message = f"❌ {message}"
                
                self.voice_interface.speak_async(broadcast_message)
                logger.info(f"📢 状态播报: {broadcast_message}")
            except Exception as e:
                logger.error(f"❌ 状态播报失败: {e}")
        
        # 调用回调函数
        for callback in self.status_callbacks:
            try:
                callback(status)
            except Exception as e:
                logger.error(f"❌ 状态回调函数执行失败: {e}")
        
        # 记录日志
        if success:
            logger.info(f"✅ {stage.value}: {message}")
        else:
            logger.error(f"❌ {stage.value}: {message}")
    
    def _wait_with_feedback(self, duration: float, message: str):
        """
        等待并播报进度
        
        Args:
            duration: 等待时间（秒）
            message: 等待消息
        """
        if self.voice_interface and self.config["enable_voice_feedback"]:
            self.voice_interface.speak_async(f"⏳ {message}")
        
        time.sleep(duration)
    
    async def power_on(self) -> bool:
        """
        设备上电阶段
        
        Returns:
            bool: 是否成功
        """
        try:
            self._broadcast_status(
                StartupStage.POWER_ON,
                True,
                "设备上电完成",
                {"power_on_time": time.time()}
            )
            return True
        except Exception as e:
            self._broadcast_status(
                StartupStage.POWER_ON,
                False,
                f"设备上电失败: {e}",
                {"error": str(e)}
            )
            return False
    
    async def system_init(self) -> bool:
        """
        系统初始化阶段
        
        Returns:
            bool: 是否成功
        """
        try:
            self._wait_with_feedback(
                self.config["check_intervals"]["module_init"],
                "正在初始化系统..."
            )
            
            # 模拟系统初始化
            if self.hardware_interface:
                await self.hardware_interface.initialize()
            
            self._broadcast_status(
                StartupStage.SYSTEM_INIT,
                True,
                "系统初始化完成",
                {"init_time": time.time()}
            )
            return True
        except Exception as e:
            self._broadcast_status(
                StartupStage.SYSTEM_INIT,
                False,
                f"系统初始化失败: {e}",
                {"error": str(e)}
            )
            return False
    
    async def module_init(self) -> bool:
        """
        模块初始化阶段
        
        Returns:
            bool: 是否成功
        """
        try:
            self._wait_with_feedback(
                self.config["check_intervals"]["module_init"],
                "正在初始化模块..."
            )
            
            # 模拟模块初始化
            modules = ["AI导航", "语音引擎", "视觉识别", "路径预测"]
            for module in modules:
                self._wait_with_feedback(0.5, f"初始化{module}...")
                logger.info(f"✅ {module}初始化完成")
            
            self._broadcast_status(
                StartupStage.MODULE_INIT,
                True,
                "模块初始化完成",
                {"modules": modules}
            )
            return True
        except Exception as e:
            self._broadcast_status(
                StartupStage.MODULE_INIT,
                False,
                f"模块初始化失败: {e}",
                {"error": str(e)}
            )
            return False
    
    async def hardware_check(self) -> bool:
        """
        硬件检查阶段
        
        Returns:
            bool: 是否成功
        """
        try:
            self._wait_with_feedback(
                self.config["check_intervals"]["hardware_check"],
                "正在检查硬件..."
            )
            
            # 模拟硬件检查
            hardware_checks = {
                "摄像头": True,
                "麦克风": True,
                "扬声器": True,
                "传感器": True
            }
            
            for device, status in hardware_checks.items():
                if status:
                    logger.info(f"✅ {device}检查正常")
                else:
                    logger.warning(f"⚠️ {device}检查异常")
            
            self._broadcast_status(
                StartupStage.HARDWARE_CHECK,
                True,
                "摄像头就绪，硬件检查完成",
                {"hardware_status": hardware_checks}
            )
            return True
        except Exception as e:
            self._broadcast_status(
                StartupStage.HARDWARE_CHECK,
                False,
                f"硬件检查失败: {e}",
                {"error": str(e)}
            )
            return False
    
    async def network_check(self) -> bool:
        """
        网络检查阶段
        
        Returns:
            bool: 是否成功
        """
        try:
            self._wait_with_feedback(
                self.config["check_intervals"]["network_check"],
                "正在检查网络连接..."
            )
            
            # 模拟网络检查
            network_status = {
                "wifi": True,
                "internet": True,
                "api_access": True
            }
            
            for service, status in network_status.items():
                if status:
                    logger.info(f"✅ {service}连接正常")
                else:
                    logger.warning(f"⚠️ {service}连接异常")
            
            self._broadcast_status(
                StartupStage.NETWORK_CHECK,
                True,
                "网络已连接",
                {"network_status": network_status}
            )
            return True
        except Exception as e:
            self._broadcast_status(
                StartupStage.NETWORK_CHECK,
                False,
                f"网络检查失败: {e}",
                {"error": str(e)}
            )
            return False
    
    async def welcome_message(self) -> bool:
        """
        欢迎语播报阶段
        
        Returns:
            bool: 是否成功
        """
        try:
            if self.voice_interface and self.config["enable_voice_feedback"]:
                # 根据人格风格生成欢迎语
                if self.config["personality_style"] == "friendly":
                    welcome_msg = "你好！我是Luna，很高兴为您服务！"
                elif self.config["personality_style"] == "professional":
                    welcome_msg = "Luna Badge 系统已就绪，开始为您提供导航服务。"
                else:
                    welcome_msg = self.config["welcome_message"]
                
                self.voice_interface.speak_async(welcome_msg)
                logger.info(f"🗣️ 播报欢迎语: {welcome_msg}")
            
            self._broadcast_status(
                StartupStage.WELCOME_MESSAGE,
                True,
                "欢迎语播报完成",
                {"welcome_message": self.config["welcome_message"]}
            )
            return True
        except Exception as e:
            self._broadcast_status(
                StartupStage.WELCOME_MESSAGE,
                False,
                f"欢迎语播报失败: {e}",
                {"error": str(e)}
            )
            return False
    
    async def ready_to_serve(self) -> bool:
        """
        准备就绪阶段
        
        Returns:
            bool: 是否成功
        """
        try:
            self._broadcast_status(
                StartupStage.READY_TO_SERVE,
                True,
                "系统准备就绪",
                {"ready_time": time.time()}
            )
            return True
        except Exception as e:
            self._broadcast_status(
                StartupStage.READY_TO_SERVE,
                False,
                f"准备就绪失败: {e}",
                {"error": str(e)}
            )
            return False
    
    async def start_recognition(self) -> bool:
        """
        开始识别循环阶段
        
        Returns:
            bool: 是否成功
        """
        try:
            self._broadcast_status(
                StartupStage.START_RECOGNITION,
                True,
                "开始识别循环",
                {"start_time": time.time()}
            )
            return True
        except Exception as e:
            self._broadcast_status(
                StartupStage.START_RECOGNITION,
                False,
                f"开始识别循环失败: {e}",
                {"error": str(e)}
            )
            return False
    
    async def full_startup_sequence(self) -> bool:
        """
        完整启动序列
        
        Returns:
            bool: 是否成功
        """
        logger.info("🚀 开始Luna Badge完整启动序列")
        
        startup_stages = [
            (self.power_on, "设备上电"),
            (self.system_init, "系统初始化"),
            (self.module_init, "模块初始化"),
            (self.hardware_check, "硬件检查"),
            (self.network_check, "网络检查"),
            (self.welcome_message, "欢迎语播报"),
            (self.ready_to_serve, "准备就绪"),
            (self.start_recognition, "开始识别循环")
        ]
        
        for stage_func, stage_name in startup_stages:
            try:
                logger.info(f"🔄 执行阶段: {stage_name}")
                success = await stage_func()
                
                if not success:
                    logger.error(f"❌ 启动阶段失败: {stage_name}")
                    return False
                
                logger.info(f"✅ 启动阶段完成: {stage_name}")
                
            except Exception as e:
                logger.error(f"❌ 启动阶段异常: {stage_name} - {e}")
                return False
        
        self.startup_complete = True
        logger.info("🎉 Luna Badge完整启动序列完成！")
        return True
    
    def get_startup_summary(self) -> Dict[str, Any]:
        """
        获取启动总结
        
        Returns:
            Dict[str, Any]: 启动总结信息
        """
        total_stages = len(self.startup_status)
        successful_stages = len([s for s in self.startup_status if s.success])
        
        return {
            "startup_complete": self.startup_complete,
            "total_stages": total_stages,
            "successful_stages": successful_stages,
            "success_rate": successful_stages / total_stages if total_stages > 0 else 0,
            "current_stage": self.current_stage.value if self.current_stage else None,
            "startup_duration": self.startup_status[-1].timestamp - self.startup_status[0].timestamp if len(self.startup_status) > 1 else 0,
            "stages": [
                {
                    "stage": status.stage.value,
                    "success": status.success,
                    "message": status.message,
                    "timestamp": status.timestamp
                }
                for status in self.startup_status
            ]
        }
    
    def set_config(self, config: Dict[str, Any]):
        """
        设置启动配置
        
        Args:
            config: 配置字典
        """
        self.config.update(config)
        logger.info(f"✅ 启动配置更新: {config}")
    
    def reset(self):
        """重置启动管理器状态"""
        self.startup_status = []
        self.current_stage = None
        self.startup_complete = False
        logger.info("🔄 启动管理器状态已重置")


# 便捷函数
async def quick_startup(hardware_interface=None, voice_interface=None, config: Dict[str, Any] = None) -> bool:
    """
    快速启动函数
    
    Args:
        hardware_interface: 硬件接口实例
        voice_interface: 语音接口实例
        config: 启动配置
    
    Returns:
        bool: 是否启动成功
    """
    startup_manager = StartupManager(hardware_interface, voice_interface)
    
    if config:
        startup_manager.set_config(config)
    
    return await startup_manager.full_startup_sequence()


if __name__ == "__main__":
    # 测试启动管理器
    logging.basicConfig(level=logging.INFO)
    
    async def test_startup():
        """测试启动流程"""
        startup_manager = StartupManager()
        
        # 添加状态回调
        def status_callback(status: StartupStatus):
            print(f"📊 状态更新: {status.stage.value} - {status.message}")
        
        startup_manager.add_status_callback(status_callback)
        
        # 执行完整启动序列
        success = await startup_manager.full_startup_sequence()
        
        if success:
            print("🎉 启动测试成功！")
            summary = startup_manager.get_startup_summary()
            print(f"📊 启动总结: {summary}")
        else:
            print("❌ 启动测试失败！")
    
    # 运行测试
    asyncio.run(test_startup())
