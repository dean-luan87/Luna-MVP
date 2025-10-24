#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 故障处理机制
系统模块出错时不卡死，提供明确提示和处理策略
"""

import asyncio
import logging
import traceback
import time
from typing import Dict, Any, Optional, Callable, List
from enum import Enum
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor
import functools

logger = logging.getLogger(__name__)

class FaultSeverity(Enum):
    """故障严重程度枚举"""
    LOW = "low"           # 低严重程度，不影响主要功能
    MEDIUM = "medium"     # 中等严重程度，影响部分功能
    HIGH = "high"         # 高严重程度，影响主要功能
    CRITICAL = "critical" # 严重故障，系统无法正常工作

class FaultType(Enum):
    """故障类型枚举"""
    HARDWARE = "hardware"         # 硬件故障
    SOFTWARE = "software"         # 软件故障
    NETWORK = "network"           # 网络故障
    AI_MODEL = "ai_model"         # AI模型故障
    VOICE = "voice"               # 语音故障
    CAMERA = "camera"             # 摄像头故障
    MEMORY = "memory"             # 内存故障
    DISK = "disk"                 # 磁盘故障
    UNKNOWN = "unknown"           # 未知故障

@dataclass
class FaultInfo:
    """故障信息数据类"""
    fault_id: str
    fault_type: FaultType
    severity: FaultSeverity
    module_name: str
    error_message: str
    error_code: str
    timestamp: float
    stack_trace: str
    context: Dict[str, Any]
    recovery_attempts: int = 0
    max_recovery_attempts: int = 3
    is_resolved: bool = False

class FaultHandler:
    """故障处理器"""
    
    def __init__(self):
        """初始化故障处理器"""
        self.faults: Dict[str, FaultInfo] = {}
        self.recovery_strategies: Dict[FaultType, Callable] = {}
        self.fault_callbacks: List[Callable[[FaultInfo], None]] = []
        self.is_handling_fault = False
        
        # 故障统计
        self.fault_stats = {
            "total_faults": 0,
            "resolved_faults": 0,
            "critical_faults": 0,
            "faults_by_type": {},
            "faults_by_severity": {}
        }
        
        # 注册默认恢复策略
        self._register_default_recovery_strategies()
        
        logger.info("🔧 故障处理器初始化完成")
    
    def _register_default_recovery_strategies(self):
        """注册默认恢复策略"""
        self.recovery_strategies[FaultType.HARDWARE] = self._recover_hardware_fault
        self.recovery_strategies[FaultType.SOFTWARE] = self._recover_software_fault
        self.recovery_strategies[FaultType.NETWORK] = self._recover_network_fault
        self.recovery_strategies[FaultType.AI_MODEL] = self._recover_ai_model_fault
        self.recovery_strategies[FaultType.VOICE] = self._recover_voice_fault
        self.recovery_strategies[FaultType.CAMERA] = self._recover_camera_fault
        self.recovery_strategies[FaultType.MEMORY] = self._recover_memory_fault
        self.recovery_strategies[FaultType.DISK] = self._recover_disk_fault
    
    def register_recovery_strategy(self, fault_type: FaultType, strategy: Callable[[FaultInfo], bool]):
        """
        注册故障恢复策略
        
        Args:
            fault_type: 故障类型
            strategy: 恢复策略函数
        """
        self.recovery_strategies[fault_type] = strategy
        logger.info(f"✅ 注册故障恢复策略: {fault_type.value}")
    
    def add_fault_callback(self, callback: Callable[[FaultInfo], None]):
        """
        添加故障回调函数
        
        Args:
            callback: 故障回调函数
        """
        self.fault_callbacks.append(callback)
        logger.info(f"✅ 添加故障回调函数: {callback.__name__}")
    
    def handle_fault(self, fault_type: FaultType, severity: FaultSeverity, 
                    module_name: str, error_message: str, error_code: str = "",
                    context: Dict[str, Any] = None) -> str:
        """
        处理故障
        
        Args:
            fault_type: 故障类型
            severity: 故障严重程度
            module_name: 模块名称
            error_message: 错误消息
            error_code: 错误代码
            context: 上下文信息
            
        Returns:
            str: 故障ID
        """
        if context is None:
            context = {}
        
        # 生成故障ID
        fault_id = f"{fault_type.value}_{int(time.time() * 1000)}"
        
        # 创建故障信息
        fault_info = FaultInfo(
            fault_id=fault_id,
            fault_type=fault_type,
            severity=severity,
            module_name=module_name,
            error_message=error_message,
            error_code=error_code,
            timestamp=time.time(),
            stack_trace=traceback.format_exc(),
            context=context
        )
        
        # 记录故障
        self.faults[fault_id] = fault_info
        
        # 更新统计信息
        self._update_fault_stats(fault_info)
        
        # 记录日志
        self._log_fault(fault_info)
        
        # 调用回调函数
        for callback in self.fault_callbacks:
            try:
                callback(fault_info)
            except Exception as e:
                logger.error(f"❌ 故障回调函数执行失败: {e}")
        
        # 根据严重程度决定处理策略
        if severity == FaultSeverity.CRITICAL:
            logger.error(f"🚨 严重故障: {fault_info.fault_id}")
            # 严重故障立即尝试恢复
            asyncio.create_task(self._attempt_recovery(fault_info))
        elif severity == FaultSeverity.HIGH:
            logger.warning(f"⚠️ 高严重程度故障: {fault_info.fault_id}")
            # 高严重程度故障延迟恢复
            asyncio.create_task(self._delayed_recovery(fault_info, delay=2.0))
        else:
            logger.info(f"ℹ️ 故障记录: {fault_info.fault_id}")
        
        return fault_id
    
    def _update_fault_stats(self, fault_info: FaultInfo):
        """更新故障统计信息"""
        self.fault_stats["total_faults"] += 1
        
        if fault_info.severity == FaultSeverity.CRITICAL:
            self.fault_stats["critical_faults"] += 1
        
        # 按类型统计
        fault_type = fault_info.fault_type.value
        if fault_type not in self.fault_stats["faults_by_type"]:
            self.fault_stats["faults_by_type"][fault_type] = 0
        self.fault_stats["faults_by_type"][fault_type] += 1
        
        # 按严重程度统计
        severity = fault_info.severity.value
        if severity not in self.fault_stats["faults_by_severity"]:
            self.fault_stats["faults_by_severity"][severity] = 0
        self.fault_stats["faults_by_severity"][severity] += 1
    
    def _log_fault(self, fault_info: FaultInfo):
        """记录故障日志"""
        log_message = (
            f"故障ID: {fault_info.fault_id} | "
            f"类型: {fault_info.fault_type.value} | "
            f"严重程度: {fault_info.severity.value} | "
            f"模块: {fault_info.module_name} | "
            f"错误: {fault_info.error_message}"
        )
        
        if fault_info.severity == FaultSeverity.CRITICAL:
            logger.error(log_message)
        elif fault_info.severity == FaultSeverity.HIGH:
            logger.warning(log_message)
        else:
            logger.info(log_message)
        
        # 记录详细堆栈跟踪
        logger.debug(f"故障堆栈跟踪:\n{fault_info.stack_trace}")
    
    async def _attempt_recovery(self, fault_info: FaultInfo):
        """尝试恢复故障"""
        if fault_info.is_resolved:
            return
        
        fault_info.recovery_attempts += 1
        
        logger.info(f"🔄 尝试恢复故障: {fault_info.fault_id} (第{fault_info.recovery_attempts}次)")
        
        # 获取恢复策略
        recovery_strategy = self.recovery_strategies.get(fault_info.fault_type)
        
        if recovery_strategy:
            try:
                success = await recovery_strategy(fault_info)
                if success:
                    fault_info.is_resolved = True
                    self.fault_stats["resolved_faults"] += 1
                    logger.info(f"✅ 故障恢复成功: {fault_info.fault_id}")
                else:
                    logger.warning(f"⚠️ 故障恢复失败: {fault_info.fault_id}")
            except Exception as e:
                logger.error(f"❌ 故障恢复异常: {fault_info.fault_id} - {e}")
        else:
            logger.warning(f"⚠️ 未找到恢复策略: {fault_info.fault_type.value}")
        
        # 如果恢复失败且未达到最大尝试次数，继续尝试
        if not fault_info.is_resolved and fault_info.recovery_attempts < fault_info.max_recovery_attempts:
            await asyncio.sleep(5.0)  # 等待5秒后重试
            await self._attempt_recovery(fault_info)
    
    async def _delayed_recovery(self, fault_info: FaultInfo, delay: float):
        """延迟恢复故障"""
        await asyncio.sleep(delay)
        await self._attempt_recovery(fault_info)
    
    # 默认恢复策略
    async def _recover_hardware_fault(self, fault_info: FaultInfo) -> bool:
        """恢复硬件故障"""
        logger.info(f"🔧 尝试恢复硬件故障: {fault_info.fault_id}")
        # 模拟硬件故障恢复
        await asyncio.sleep(1.0)
        return True
    
    async def _recover_software_fault(self, fault_info: FaultInfo) -> bool:
        """恢复软件故障"""
        logger.info(f"🔧 尝试恢复软件故障: {fault_info.fault_id}")
        # 模拟软件故障恢复
        await asyncio.sleep(1.0)
        return True
    
    async def _recover_network_fault(self, fault_info: FaultInfo) -> bool:
        """恢复网络故障"""
        logger.info(f"🔧 尝试恢复网络故障: {fault_info.fault_id}")
        # 模拟网络故障恢复
        await asyncio.sleep(1.0)
        return True
    
    async def _recover_ai_model_fault(self, fault_info: FaultInfo) -> bool:
        """恢复AI模型故障"""
        logger.info(f"🔧 尝试恢复AI模型故障: {fault_info.fault_id}")
        # 模拟AI模型故障恢复
        await asyncio.sleep(1.0)
        return True
    
    async def _recover_voice_fault(self, fault_info: FaultInfo) -> bool:
        """恢复语音故障"""
        logger.info(f"🔧 尝试恢复语音故障: {fault_info.fault_id}")
        # 模拟语音故障恢复
        await asyncio.sleep(1.0)
        return True
    
    async def _recover_camera_fault(self, fault_info: FaultInfo) -> bool:
        """恢复摄像头故障"""
        logger.info(f"🔧 尝试恢复摄像头故障: {fault_info.fault_id}")
        # 模拟摄像头故障恢复
        await asyncio.sleep(1.0)
        return True
    
    async def _recover_memory_fault(self, fault_info: FaultInfo) -> bool:
        """恢复内存故障"""
        logger.info(f"🔧 尝试恢复内存故障: {fault_info.fault_id}")
        # 模拟内存故障恢复
        await asyncio.sleep(1.0)
        return True
    
    async def _recover_disk_fault(self, fault_info: FaultInfo) -> bool:
        """恢复磁盘故障"""
        logger.info(f"🔧 尝试恢复磁盘故障: {fault_info.fault_id}")
        # 模拟磁盘故障恢复
        await asyncio.sleep(1.0)
        return True
    
    def get_fault_info(self, fault_id: str) -> Optional[FaultInfo]:
        """获取故障信息"""
        return self.faults.get(fault_id)
    
    def get_fault_stats(self) -> Dict[str, Any]:
        """获取故障统计信息"""
        return self.fault_stats.copy()
    
    def get_active_faults(self) -> List[FaultInfo]:
        """获取活跃故障列表"""
        return [fault for fault in self.faults.values() if not fault.is_resolved]
    
    def clear_resolved_faults(self):
        """清除已解决的故障"""
        resolved_faults = [fault_id for fault_id, fault in self.faults.items() if fault.is_resolved]
        for fault_id in resolved_faults:
            del self.faults[fault_id]
        logger.info(f"✅ 清除已解决故障: {len(resolved_faults)}个")
    
    def reset_stats(self):
        """重置统计信息"""
        self.fault_stats = {
            "total_faults": 0,
            "resolved_faults": 0,
            "critical_faults": 0,
            "faults_by_type": {},
            "faults_by_severity": {}
        }
        logger.info("🔄 故障统计信息已重置")


# 故障处理装饰器
def fault_tolerant(module_name: str, fault_type: FaultType = FaultType.SOFTWARE, 
                  severity: FaultSeverity = FaultSeverity.MEDIUM):
    """
    故障容忍装饰器
    
    Args:
        module_name: 模块名称
        fault_type: 故障类型
        severity: 故障严重程度
    """
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            fault_handler = FaultHandler()
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                fault_id = fault_handler.handle_fault(
                    fault_type=fault_type,
                    severity=severity,
                    module_name=module_name,
                    error_message=str(e),
                    error_code=type(e).__name__,
                    context={"function": func.__name__, "args": str(args), "kwargs": str(kwargs)}
                )
                logger.error(f"❌ 函数 {func.__name__} 执行失败，故障ID: {fault_id}")
                return None
        return wrapper
    return decorator


# 全局故障处理器实例
global_fault_handler = FaultHandler()

# 便捷函数
def handle_fault(fault_type: FaultType, severity: FaultSeverity, 
                module_name: str, error_message: str, error_code: str = "",
                context: Dict[str, Any] = None) -> str:
    """处理故障的便捷函数"""
    return global_fault_handler.handle_fault(
        fault_type, severity, module_name, error_message, error_code, context
    )

def get_fault_stats() -> Dict[str, Any]:
    """获取故障统计信息的便捷函数"""
    return global_fault_handler.get_fault_stats()

def get_active_faults() -> List[FaultInfo]:
    """获取活跃故障列表的便捷函数"""
    return global_fault_handler.get_active_faults()


if __name__ == "__main__":
    # 测试故障处理机制
    logging.basicConfig(level=logging.INFO)
    
    async def test_fault_handler():
        """测试故障处理器"""
        fault_handler = FaultHandler()
        
        # 添加故障回调
        def fault_callback(fault_info: FaultInfo):
            print(f"📊 故障回调: {fault_info.fault_id} - {fault_info.error_message}")
        
        fault_handler.add_fault_callback(fault_callback)
        
        # 模拟不同类型的故障
        fault_handler.handle_fault(
            FaultType.HARDWARE, FaultSeverity.HIGH, "Camera", "摄像头初始化失败"
        )
        
        fault_handler.handle_fault(
            FaultType.NETWORK, FaultSeverity.MEDIUM, "Network", "网络连接超时"
        )
        
        fault_handler.handle_fault(
            FaultType.AI_MODEL, FaultSeverity.CRITICAL, "YOLO", "模型加载失败"
        )
        
        # 等待一段时间让恢复策略执行
        await asyncio.sleep(10)
        
        # 显示统计信息
        stats = fault_handler.get_fault_stats()
        print(f"📊 故障统计: {stats}")
    
    # 运行测试
    asyncio.run(test_fault_handler())
