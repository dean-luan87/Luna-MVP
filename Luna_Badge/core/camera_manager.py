"""
Luna Badge 摄像头管理模块
提供统一的摄像头管理接口，支持多种关闭方式：
1. 语音关闭
2. 双击关闭（硬件）
3. 任务结束后问询关闭
4. 长时间禁止不动超过3分钟自动关闭
"""

import logging
import time
import threading
from typing import Optional, Callable, Dict, Any
from enum import Enum
from dataclasses import dataclass

logger = logging.getLogger(__name__)


class CameraCloseReason(Enum):
    """摄像头关闭原因"""
    VOICE_COMMAND = "voice_command"           # 语音关闭
    HARDWARE_DOUBLE_CLICK = "hardware_double_click"  # 双击关闭
    TASK_COMPLETE = "task_complete"           # 任务完成
    IDLE_TIMEOUT = "idle_timeout"            # 空闲超时
    MANUAL = "manual"                        # 手动关闭
    PRIVACY_LOCK = "privacy_lock"            # 隐私锁定
    ERROR = "error"                          # 错误关闭


@dataclass
class CameraState:
    """摄像头状态"""
    is_open: bool = False
    is_recording: bool = False
    last_activity_time: float = 0.0
    open_count: int = 0
    close_reason: Optional[CameraCloseReason] = None
    idle_start_time: Optional[float] = None


class CameraManager:
    """摄像头管理器"""
    
    def __init__(self, camera_interface=None, idle_timeout: int = 180):
        """
        初始化摄像头管理器
        
        Args:
            camera_interface: 摄像头接口对象（hal_mac/hal_embedded）
            idle_timeout: 空闲超时时间（秒），默认3分钟
        """
        self.camera_interface = camera_interface
        self.idle_timeout = idle_timeout
        
        self.state = CameraState()
        self.monitor_thread: Optional[threading.Thread] = None
        self.monitor_running = False
        
        # 硬件双击检测
        self.last_click_time = 0.0
        self.double_click_interval = 0.5  # 0.5秒内双击有效
        
        # 回调函数
        self.on_close_callback: Optional[Callable] = None
        
        logger.info("📷 摄像头管理器初始化完成")
    
    def set_camera_interface(self, camera_interface):
        """设置摄像头接口"""
        self.camera_interface = camera_interface
        logger.info("📷 摄像头接口已设置")
    
    def open_camera(self) -> bool:
        """
        打开摄像头
        
        Returns:
            bool: 是否成功打开
        """
        if self.state.is_open:
            logger.warning("⚠️ 摄像头已经打开")
            return True
        
        try:
            if not self.camera_interface:
                logger.error("❌ 摄像头接口未设置")
                return False
            
            # 检查隐私锁定
            try:
                from core.privacy_protection import is_camera_locked
                if is_camera_locked():
                    logger.warning("⚠️ 摄像头被隐私锁定，无法打开")
                    return False
            except ImportError:
                pass
            
            # 初始化摄像头
            if hasattr(self.camera_interface, 'camera'):
                camera = self.camera_interface.camera
                if hasattr(camera, 'initialize'):
                    if not camera.initialize():
                        logger.error("❌ 摄像头初始化失败")
                        return False
                if hasattr(camera, 'start_camera'):
                    if not camera.start_camera():
                        logger.error("❌ 摄像头启动失败")
                        return False
            
            self.state.is_open = True
            self.state.last_activity_time = time.time()
            self.state.open_count += 1
            self.state.close_reason = None
            self.state.idle_start_time = time.time()
            
            # 启动监控线程
            self._start_monitor()
            
            logger.info("✅ 摄像头已打开")
            return True
            
        except Exception as e:
            logger.error(f"❌ 打开摄像头失败: {e}")
            return False
    
    def close_camera(self, reason: CameraCloseReason = CameraCloseReason.MANUAL) -> bool:
        """
        关闭摄像头
        
        Args:
            reason: 关闭原因
        
        Returns:
            bool: 是否成功关闭
        """
        if not self.state.is_open:
            logger.warning("⚠️ 摄像头已经关闭")
            return True
        
        try:
            # 停止监控
            self._stop_monitor()
            
            # 关闭摄像头
            if self.camera_interface and hasattr(self.camera_interface, 'camera'):
                camera = self.camera_interface.camera
                if hasattr(camera, 'stop_camera'):
                    camera.stop_camera()
                if hasattr(camera, 'cleanup'):
                    camera.cleanup()
            
            self.state.is_open = False
            self.state.is_recording = False
            self.state.close_reason = reason
            self.state.idle_start_time = None
            
            # 触发关闭回调
            if self.on_close_callback:
                try:
                    self.on_close_callback(reason)
                except Exception as e:
                    logger.error(f"❌ 关闭回调执行失败: {e}")
            
            reason_text = {
                CameraCloseReason.VOICE_COMMAND: "语音命令",
                CameraCloseReason.HARDWARE_DOUBLE_CLICK: "硬件双击",
                CameraCloseReason.TASK_COMPLETE: "任务完成",
                CameraCloseReason.IDLE_TIMEOUT: "空闲超时",
                CameraCloseReason.MANUAL: "手动关闭",
                CameraCloseReason.PRIVACY_LOCK: "隐私锁定",
                CameraCloseReason.ERROR: "错误关闭"
            }.get(reason, "未知原因")
            
            logger.info(f"✅ 摄像头已关闭（原因：{reason_text}）")
            return True
            
        except Exception as e:
            logger.error(f"❌ 关闭摄像头失败: {e}")
            return False
    
    def handle_voice_command(self, command: str) -> bool:
        """
        处理语音命令关闭
        
        Args:
            command: 语音命令文本
        
        Returns:
            bool: 是否成功处理
        """
        close_keywords = ["关闭摄像头", "关闭相机", "关闭镜头", "摄像头关闭", "停止录制"]
        
        command_lower = command.lower()
        for keyword in close_keywords:
            if keyword in command_lower:
                logger.info(f"🎤 收到语音关闭命令: {command}")
                return self.close_camera(CameraCloseReason.VOICE_COMMAND)
        
        return False
    
    def handle_hardware_double_click(self) -> bool:
        """
        处理硬件双击关闭
        
        Returns:
            bool: 是否成功处理
        """
        current_time = time.time()
        
        # 检测双击
        if current_time - self.last_click_time < self.double_click_interval:
            logger.info("🖱️ 检测到硬件双击，关闭摄像头")
            self.last_click_time = 0.0  # 重置
            return self.close_camera(CameraCloseReason.HARDWARE_DOUBLE_CLICK)
        else:
            self.last_click_time = current_time
            return False
    
    def handle_task_complete(self, ask_before_close: bool = True) -> bool:
        """
        任务完成后问询关闭
        
        Args:
            ask_before_close: 是否在关闭前询问用户
        
        Returns:
            bool: 是否成功关闭
        """
        if ask_before_close:
            logger.info("❓ 任务完成，询问是否关闭摄像头...")
            # TODO: 实现语音询问逻辑
            # 这里可以先自动关闭，后续可扩展为语音交互
            return self.close_camera(CameraCloseReason.TASK_COMPLETE)
        else:
            return self.close_camera(CameraCloseReason.TASK_COMPLETE)
    
    def update_activity(self):
        """更新活动时间"""
        self.state.last_activity_time = time.time()
        self.state.idle_start_time = None
    
    def check_idle_timeout(self) -> bool:
        """
        检查空闲超时
        
        Returns:
            bool: 是否超时
        """
        if not self.state.is_open:
            return False
        
        current_time = time.time()
        
        # 计算空闲时间
        if self.state.idle_start_time is None:
            self.state.idle_start_time = current_time
        
        idle_duration = current_time - self.state.idle_start_time
        
        if idle_duration >= self.idle_timeout:
            logger.warning(f"⏰ 摄像头空闲超时（{idle_duration:.1f}秒），自动关闭")
            self.close_camera(CameraCloseReason.IDLE_TIMEOUT)
            return True
        
        return False
    
    def _start_monitor(self):
        """启动监控线程"""
        if self.monitor_running:
            return
        
        self.monitor_running = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        logger.debug("📷 摄像头监控线程已启动")
    
    def _stop_monitor(self):
        """停止监控线程"""
        self.monitor_running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2)
        logger.debug("📷 摄像头监控线程已停止")
    
    def _monitor_loop(self):
        """监控循环（检查空闲超时）"""
        while self.monitor_running:
            try:
                if self.state.is_open:
                    self.check_idle_timeout()
                time.sleep(10)  # 每10秒检查一次
            except Exception as e:
                logger.error(f"❌ 监控循环错误: {e}")
                break
    
    def set_close_callback(self, callback: Callable):
        """设置关闭回调函数"""
        self.on_close_callback = callback
    
    def get_state(self) -> Dict[str, Any]:
        """获取摄像头状态"""
        return {
            "is_open": self.state.is_open,
            "is_recording": self.state.is_recording,
            "last_activity_time": self.state.last_activity_time,
            "open_count": self.state.open_count,
            "close_reason": self.state.close_reason.value if self.state.close_reason else None,
            "idle_duration": time.time() - self.state.idle_start_time if self.state.idle_start_time else 0
        }
    
    def __del__(self):
        """析构函数，确保摄像头关闭"""
        if self.state.is_open:
            self.close_camera(CameraCloseReason.MANUAL)


# 全局摄像头管理器实例
_global_camera_manager: Optional[CameraManager] = None


def get_camera_manager(camera_interface=None, idle_timeout: int = 180) -> CameraManager:
    """获取全局摄像头管理器实例"""
    global _global_camera_manager
    if _global_camera_manager is None:
        _global_camera_manager = CameraManager(camera_interface, idle_timeout)
    elif camera_interface and not _global_camera_manager.camera_interface:
        _global_camera_manager.set_camera_interface(camera_interface)
    return _global_camera_manager


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("=" * 70)
    print("📷 摄像头管理器测试")
    print("=" * 70)
    
    # 模拟测试
    manager = CameraManager(idle_timeout=5)  # 5秒超时用于测试
    
    # 测试1: 语音命令关闭
    print("\n1. 测试语音命令关闭...")
    result = manager.handle_voice_command("关闭摄像头")
    print(f"   结果: {'成功' if result else '失败（摄像头未打开）'}")
    
    # 测试2: 硬件双击关闭
    print("\n2. 测试硬件双击关闭...")
    manager.handle_hardware_double_click()  # 第一次点击
    time.sleep(0.3)
    result = manager.handle_hardware_double_click()  # 第二次点击（在0.5秒内）
    print(f"   结果: {'成功' if result else '失败'}")
    
    # 测试3: 状态查询
    print("\n3. 测试状态查询...")
    state = manager.get_state()
    print(f"   状态: {state}")
    
    print("\n" + "=" * 70)
