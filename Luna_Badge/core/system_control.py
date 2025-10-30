#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Luna Badge - 系统控制模块
状态机、自检、错误日志、状态循环管理
"""

import time
import logging
import threading
from datetime import datetime
from typing import Dict, List, Optional, Callable, Any
from enum import Enum

from .config import SystemMode, config_manager

class SystemState(Enum):
    """系统状态枚举"""
    ACTIVE = "ACTIVE"
    IDLE = "IDLE"
    SLEEP = "SLEEP"
    OFF = "OFF"

class ErrorCode(Enum):
    """错误代码枚举"""
    E100 = "E100"  # 摄像头无响应
    E200 = "E200"  # 网络未连接
    E300 = "E300"  # 麦克风无响应
    E400 = "E400"  # 语音引擎故障
    E500 = "E500"  # AI模型加载失败

class LunaCore:
    """系统控制器"""
    
    def __init__(self):
        """初始化系统控制器"""
        self.current_state = SystemState.OFF
        self.previous_state = SystemState.OFF
        self.error_log: List[Dict[str, str]] = []
        self.is_running = False
        self.state_lock = threading.Lock()
        self.error_lock = threading.Lock()
        
        # 回调函数
        self.state_change_callbacks: List[Callable] = []
        self.error_callbacks: List[Callable] = []
        
        # 配置
        self.config = config_manager.load_config()
        
        # 硬件接口（将在初始化时设置）
        self.hal_interface = None
        
        # 设置日志
        self._setup_logging()
    
    def _setup_logging(self):
        """设置日志"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def set_hal_interface(self, hal_interface):
        """设置硬件抽象层接口"""
        self.hal_interface = hal_interface
    
    def add_state_change_callback(self, callback: Callable):
        """添加状态变化回调"""
        self.state_change_callbacks.append(callback)
    
    def add_error_callback(self, callback: Callable):
        """添加错误回调"""
        self.error_callbacks.append(callback)
    
    def change_state(self, new_state: SystemState) -> bool:
        """
        改变系统状态
        
        Args:
            new_state: 新状态
            
        Returns:
            状态改变是否成功
        """
        with self.state_lock:
            if self.current_state == new_state:
                return True
            
            self.previous_state = self.current_state
            self.current_state = new_state
            
            # 记录状态变化
            self.logger.info(f"系统状态变化: {self.previous_state.value} -> {self.current_state.value}")
            
            # 触发回调
            for callback in self.state_change_callbacks:
                try:
                    callback(self.previous_state, self.current_state)
                except Exception as e:
                    self.logger.error(f"状态变化回调执行失败: {e}")
            
            return True
    
    def power_on(self) -> bool:
        """
        系统开机
        
        Returns:
            开机是否成功
        """
        try:
            self.logger.info("系统开机中...")
            
            # 执行自检
            if not self.self_diagnose():
                self.logger.error("自检失败，系统启动中止")
                return False
            
            # 改变状态为活跃
            self.change_state(SystemState.ACTIVE)
            
            # 语音播报
            if self.hal_interface:
                self.hal_interface.speak("Luna已启动，正在检查系统状态")
            
            self.logger.info("系统开机成功")
            return True
            
        except Exception as e:
            self.logger.error(f"系统开机失败: {e}")
            self.log_error(ErrorCode.E500, f"系统开机失败: {e}")
            return False
    
    def power_off(self) -> bool:
        """
        系统关机
        
        Returns:
            关机是否成功
        """
        try:
            self.logger.info("系统关机中...")
            
            # 改变状态为关闭
            self.change_state(SystemState.OFF)
            
            # 语音播报
            if self.hal_interface:
                self.hal_interface.speak("系统已关闭，再见")
            
            self.logger.info("系统关机成功")
            return True
            
        except Exception as e:
            self.logger.error(f"系统关机失败: {e}")
            return False
    
    def enter_idle(self) -> bool:
        """
        进入空闲状态
        
        Returns:
            状态改变是否成功
        """
        try:
            self.change_state(SystemState.IDLE)
            
            if self.hal_interface:
                self.hal_interface.speak("我会保持安静，有需要随时叫我")
            
            return True
            
        except Exception as e:
            self.logger.error(f"进入空闲状态失败: {e}")
            return False
    
    def enter_sleep(self) -> bool:
        """
        进入睡眠状态
        
        Returns:
            状态改变是否成功
        """
        try:
            self.change_state(SystemState.SLEEP)
            
            if self.hal_interface:
                self.hal_interface.speak("进入待机状态，等待唤醒信号")
            
            return True
            
        except Exception as e:
            self.logger.error(f"进入睡眠状态失败: {e}")
            return False
    
    def wake_up(self) -> bool:
        """
        唤醒系统
        
        Returns:
            唤醒是否成功
        """
        try:
            if self.current_state in [SystemState.IDLE, SystemState.SLEEP]:
                self.change_state(SystemState.ACTIVE)
                
                if self.hal_interface:
                    self.hal_interface.speak("我在呢，继续为你导航")
                
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"系统唤醒失败: {e}")
            return False
    
    def self_diagnose(self) -> bool:
        """
        系统自检
        
        Returns:
            自检是否通过
        """
        try:
            self.logger.info("开始系统自检...")
            
            if not self.hal_interface:
                self.logger.error("硬件接口未初始化")
                return False
            
            # 检查硬件组件
            errors = []
            
            # 检查摄像头
            if not self._check_camera():
                errors.append(ErrorCode.E100)
            
            # 检查麦克风
            if not self._check_microphone():
                errors.append(ErrorCode.E300)
            
            # 检查网络
            if not self._check_network():
                errors.append(ErrorCode.E200)
            
            # 检查语音引擎
            if not self._check_voice_engine():
                errors.append(ErrorCode.E400)
            
            if errors:
                # 记录错误
                for error in errors:
                    self.log_error(error, f"{error.value} 硬件检测失败")
                
                # 尝试修复
                self.attempt_repair(errors)
                
                self.logger.warning("自检发现问题，已尝试修复")
                if self.hal_interface:
                    self.hal_interface.speak("检测到系统异常，我会尝试修复")
                
                return True  # 即使有错误也继续启动，但会尝试修复
            else:
                self.logger.info("系统自检完成，一切正常")
                if self.hal_interface:
                    self.hal_interface.speak("系统检测完成，一切正常")
                return True
                
        except Exception as e:
            self.logger.error(f"系统自检异常: {e}")
            return False
    
    def _check_camera(self) -> bool:
        """检查摄像头"""
        try:
            if self.hal_interface and hasattr(self.hal_interface, 'check_camera'):
                return self.hal_interface.check_camera()
            return True  # 如果没有硬件接口，假设正常
        except Exception as e:
            self.logger.error(f"摄像头检查失败: {e}")
            return False
    
    def _check_microphone(self) -> bool:
        """检查麦克风"""
        try:
            if self.hal_interface and hasattr(self.hal_interface, 'check_microphone'):
                return self.hal_interface.check_microphone()
            return True
        except Exception as e:
            self.logger.error(f"麦克风检查失败: {e}")
            return False
    
    def _check_network(self) -> bool:
        """检查网络连接"""
        try:
            if self.hal_interface and hasattr(self.hal_interface, 'check_network'):
                return self.hal_interface.check_network()
            return True
        except Exception as e:
            self.logger.error(f"网络检查失败: {e}")
            return False
    
    def _check_voice_engine(self) -> bool:
        """检查语音引擎"""
        try:
            if self.hal_interface and hasattr(self.hal_interface, 'check_voice_engine'):
                return self.hal_interface.check_voice_engine()
            return True
        except Exception as e:
            self.logger.error(f"语音引擎检查失败: {e}")
            return False
    
    def attempt_repair(self, errors: List[ErrorCode]) -> bool:
        """
        尝试修复错误
        
        Args:
            errors: 错误列表
            
        Returns:
            修复是否成功
        """
        try:
            self.logger.info("开始尝试修复系统错误...")
            
            for error in errors:
                if error == ErrorCode.E200:
                    self.logger.info("尝试重新连接网络...")
                    if self.hal_interface:
                        self.hal_interface.speak("正在重新连接网络")
                
                elif error == ErrorCode.E100:
                    self.logger.info("尝试重启摄像模块...")
                    if self.hal_interface:
                        self.hal_interface.speak("尝试重启摄像模块")
                
                elif error == ErrorCode.E300:
                    self.logger.info("重启语音模块...")
                    if self.hal_interface:
                        self.hal_interface.speak("重启语音模块中")
                
                elif error == ErrorCode.E400:
                    self.logger.info("重启语音引擎...")
                    if self.hal_interface:
                        self.hal_interface.speak("重启语音引擎中")
            
            self.logger.info("系统修复完成")
            if self.hal_interface:
                self.hal_interface.speak("修复完成，请再次确认状态")
            
            return True
            
        except Exception as e:
            self.logger.error(f"系统修复失败: {e}")
            return False
    
    def log_error(self, error_code: ErrorCode, message: str) -> None:
        """
        记录错误日志
        
        Args:
            error_code: 错误代码
            message: 错误信息
        """
        with self.error_lock:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            error_entry = {
                "timestamp": timestamp,
                "code": error_code.value,
                "message": message
            }
            self.error_log.append(error_entry)
            
            # 限制错误日志长度
            if len(self.error_log) > 1000:
                self.error_log = self.error_log[-500:]
            
            # 触发错误回调
            for callback in self.error_callbacks:
                try:
                    callback(error_entry)
                except Exception as e:
                    self.logger.error(f"错误回调执行失败: {e}")
            
            self.logger.error(f"[{error_code.value}] {message}")
    
    def get_error_log(self) -> List[Dict[str, str]]:
        """获取错误日志"""
        with self.error_lock:
            return self.error_log.copy()
    
    def clear_error_log(self) -> None:
        """清空错误日志"""
        with self.error_lock:
            self.error_log.clear()
    
    def system_loop(self) -> None:
        """系统主循环"""
        try:
            self.is_running = True
            self.logger.info("系统主循环启动")
            
            idle_timer = 0
            idle_threshold = self.config.get("system", {}).get("idle_threshold", 300)
            
            while self.is_running:
                try:
                    if self.current_state == SystemState.ACTIVE:
                        idle_timer += 1
                        if idle_timer > idle_threshold:
                            self.enter_idle()
                            idle_timer = 0
                    
                    elif self.current_state == SystemState.IDLE:
                        # 检测语音唤醒词
                        if self._detect_wake_word():
                            self.wake_up()
                    
                    elif self.current_state == SystemState.SLEEP:
                        # 等待硬件中断信号
                        if self._detect_wake_word():
                            self.wake_up()
                    
                    elif self.current_state == SystemState.OFF:
                        break
                    
                    time.sleep(1)
                    
                except Exception as e:
                    self.logger.error(f"系统循环异常: {e}")
                    time.sleep(1)
            
            self.logger.info("系统主循环结束")
            
        except Exception as e:
            self.logger.error(f"系统循环启动失败: {e}")
        finally:
            self.is_running = False
    
    def _detect_wake_word(self) -> bool:
        """
        检测语音唤醒词
        
        Returns:
            是否检测到唤醒词
        """
        try:
            if self.hal_interface and hasattr(self.hal_interface, 'detect_wake_word'):
                return self.hal_interface.detect_wake_word()
            return False  # 如果没有硬件接口，返回False
        except Exception as e:
            self.logger.error(f"唤醒词检测失败: {e}")
            return False
    
    def stop(self) -> None:
        """停止系统"""
        self.is_running = False
        self.logger.info("系统停止")
    
    def get_status(self) -> Dict[str, Any]:
        """获取系统状态"""
        return {
            "current_state": self.current_state.value,
            "previous_state": self.previous_state.value,
            "is_running": self.is_running,
            "error_count": len(self.error_log),
            "platform": config_manager.get_platform_config()
        }
