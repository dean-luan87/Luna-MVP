#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Luna Badge v1.4 - 故障安全与强制恢复模块
负责在系统异常、卡死、执行中断等问题时执行强制恢复或系统重启
"""

import logging
import time
import threading
from typing import Dict, Any, Optional, List
from datetime import datetime
from dataclasses import dataclass, asdict
import json
import os

logger = logging.getLogger(__name__)


@dataclass
class FailsafeRecord:
    """故障记录"""
    timestamp: str
    reason: str
    active_task_id: Optional[str] = None
    last_known_node: Optional[str] = None
    recovery_available: bool = True
    module_name: Optional[str] = None
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()


class HeartbeatMonitor:
    """心跳监测器"""
    
    def __init__(self, timeout: int = 10, interval: int = 5):
        """
        初始化心跳监测器
        
        Args:
            timeout: 超时时间（秒）
            interval: 检查间隔（秒）
        """
        self.timeout = timeout
        self.interval = interval
        self.heartbeats: Dict[str, float] = {}  # module_name -> last_heartbeat
        self.monitoring = False
        self.monitor_thread: Optional[threading.Thread] = None
        self.on_timeout_callback = None
        self.logger = logging.getLogger("HeartbeatMonitor")
    
    def register_module(self, module_name: str):
        """注册模块"""
        self.heartbeats[module_name] = time.time()
        self.logger.debug(f"💓 模块已注册: {module_name}")
    
    def heartbeat(self, module_name: str):
        """接收心跳"""
        self.heartbeats[module_name] = time.time()
        self.logger.debug(f"💓 收到心跳: {module_name}")
    
    def start_monitoring(self, on_timeout=None):
        """启动监控"""
        if self.monitoring:
            self.logger.warning("⚠️ 监控已在运行")
            return
        
        self.monitoring = True
        self.on_timeout_callback = on_timeout
        
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        
        self.logger.info(f"👁️ 心跳监控已启动 (超时={self.timeout}s, 间隔={self.interval}s)")
    
    def stop_monitoring(self):
        """停止监控"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2)
        self.logger.info("🛑 心跳监控已停止")
    
    def _monitor_loop(self):
        """监控循环"""
        while self.monitoring:
            try:
                current_time = time.time()
                
                for module_name, last_heartbeat in list(self.heartbeats.items()):
                    elapsed = current_time - last_heartbeat
                    
                    if elapsed > self.timeout:
                        self.logger.error(f"❌ 模块心跳超时: {module_name} ({int(elapsed)}s)")
                        
                        if self.on_timeout_callback:
                            self.on_timeout_callback(module_name, elapsed)
                
                time.sleep(self.interval)
                
            except Exception as e:
                self.logger.error(f"❌ 监控循环异常: {e}")
                time.sleep(self.interval)


class FailsafeTrigger:
    """故障安全触发器"""
    
    def __init__(self, state_manager=None, cache_manager=None, storage_dir: str = "data/failsafe"):
        """
        初始化故障安全模块
        
        Args:
            state_manager: 状态管理器
            cache_manager: 缓存管理器
            storage_dir: 故障记录存储目录
        """
        self.state_manager = state_manager
        self.cache_manager = cache_manager
        self.storage_dir = storage_dir
        self.logger = logging.getLogger("FailsafeTrigger")
        
        os.makedirs(storage_dir, exist_ok=True)
        
        self.heartbeat_monitor = HeartbeatMonitor(timeout=10, interval=5)
        self.failsafe_mode = False
        self.current_record: Optional[FailsafeRecord] = None
        
        # 注册心跳超时回调
        self.heartbeat_monitor.start_monitoring(on_timeout=self._on_module_timeout)
        
        self.logger.info("🔐 FailsafeTrigger 初始化完成")
    
    def monitor_heartbeat(self, module_name: str, interval: int = 5):
        """
        启动心跳监测，检查模块是否正常响应
        
        Args:
            module_name: 模块名称
            interval: 检查间隔（秒）
        """
        self.heartbeat_monitor.register_module(module_name)
        self.logger.info(f"👁️ 开始监控模块: {module_name}")
    
    def record_heartbeat(self, module_name: str):
        """
        记录心跳
        
        Args:
            module_name: 模块名称
        """
        self.heartbeat_monitor.heartbeat(module_name)
    
    def trigger_failsafe(self, reason: str, module_name: str = "unknown") -> None:
        """
        强制触发系统恢复机制
        
        Args:
            reason: 故障原因
            module_name: 故障模块名称
        """
        self.logger.error(f"🚨 触发故障安全机制: {reason}")
        
        # 记录故障事件
        self.log_failsafe_event(reason, module_name)
        
        # 保存当前任务状态
        active_task_id = self._get_active_task_id()
        last_node = self._get_last_known_node()
        
        # 创建故障记录
        record = FailsafeRecord(
            timestamp=datetime.now().isoformat(),
            reason=reason,
            active_task_id=active_task_id,
            last_known_node=last_node,
            recovery_available=True,
            module_name=module_name
        )
        
        self.current_record = record
        self._save_failsafe_record(record)
        
        # 进入故障模式
        self.enter_failsafe_mode(reason)
        
        # 停止心跳监控
        self.heartbeat_monitor.stop_monitoring()
        
        self.logger.error(f"🚨 系统已进入故障安全模式: {reason}")
    
    def prompt_user_for_recovery(self) -> bool:
        """
        重启后提示用户是否恢复任务
        
        Returns:
            bool: 用户是否选择恢复
        """
        self.logger.info("❓ 询问用户是否恢复任务")
        
        # 检查是否有可恢复的记录
        if not self.current_record or not self.current_record.recovery_available:
            return False
        
        # 模拟用户交互（实际应该调用语音或UI）
        # 这里返回True作为示例
        user_choice = True  # 实际应该通过UI/语音获取
        
        if user_choice:
            self.logger.info("✅ 用户选择恢复任务")
        else:
            self.logger.info("❌ 用户选择不恢复")
        
        return user_choice
    
    def restore_task_from_cache(self) -> bool:
        """
        调用 task_state_manager 恢复任务链
        
        Returns:
            bool: 是否成功恢复
        """
        if not self.current_record:
            self.logger.warning("⚠️ 没有可恢复的故障记录")
            return False
        
        if not self.state_manager:
            self.logger.warning("⚠️ 状态管理器未初始化")
            return False
        
        task_id = self.current_record.active_task_id
        if not task_id:
            self.logger.warning("⚠️ 任务ID为空")
            return False
        
        # 尝试恢复任务状态
        try:
            # 这里应该调用state_manager恢复状态
            # 实际实现需要根据具体API
            self.logger.info(f"🔄 恢复任务: {task_id}")
            
            # 清除故障模式
            self.failsafe_mode = False
            self.current_record = None
            
            # 重新启动心跳监控
            self.heartbeat_monitor.start_monitoring(on_timeout=self._on_module_timeout)
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ 恢复任务失败: {e}")
            return False
    
    def enter_failsafe_mode(self, reason: str) -> None:
        """
        切换 UI 或语音为"故障模式"
        
        Args:
            reason: 故障原因
        """
        self.failsafe_mode = True
        
        # 这里应该触发UI/语音提示
        message = f"系统刚才发生异常：{reason}，请稍等..."
        self.logger.info(f"🔐 进入故障模式: {message}")
        
        # 实际应该调用TTS播放
        # tts_manager.speak(message)
    
    def log_failsafe_event(self, reason: str, module_name: str = "unknown") -> None:
        """
        写入 failsafe 触发日志
        
        Args:
            reason: 故障原因
            module_name: 模块名称
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"failsafe_{timestamp}.json"
        filepath = os.path.join(self.storage_dir, filename)
        
        data = {
            "timestamp": datetime.now().isoformat(),
            "reason": reason,
            "module_name": module_name,
            "active_task_id": self._get_active_task_id(),
            "last_known_node": self._get_last_known_node(),
            "recovery_available": True
        }
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"📝 故障事件已记录: {filepath}")
            
        except Exception as e:
            self.logger.error(f"❌ 记录故障事件失败: {e}")
    
    def _on_module_timeout(self, module_name: str, elapsed: float):
        """模块超时回调"""
        reason = f"{module_name}模块心跳超时({int(elapsed)}秒)"
        self.trigger_failsafe(reason, module_name)
    
    def _get_active_task_id(self) -> Optional[str]:
        """获取当前活跃任务ID"""
        # 尝试从状态管理器获取
        if self.state_manager and hasattr(self.state_manager, 'task_states'):
            for task_id in self.state_manager.task_states.keys():
                return task_id
        return None
    
    def _get_last_known_node(self) -> Optional[str]:
        """获取最后已知节点"""
        if not self.current_record:
            return None
        
        # 从故障记录中获取
        return self.current_record.last_known_node
    
    def _save_failsafe_record(self, record: FailsafeRecord):
        """保存故障记录"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"record_{timestamp}.json"
        filepath = os.path.join(self.storage_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(asdict(record), f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"💾 故障记录已保存: {filepath}")
            
        except Exception as e:
            self.logger.error(f"❌ 保存故障记录失败: {e}")
    
    def get_recovery_status(self) -> Dict[str, Any]:
        """
        获取恢复状态
        
        Returns:
            Dict: 恢复状态信息
        """
        return {
            "failsafe_mode": self.failsafe_mode,
            "has_recovery": self.current_record is not None and self.current_record.recovery_available,
            "recovery_info": asdict(self.current_record) if self.current_record else None
        }
    
    def clear_failsafe_mode(self):
        """清除故障模式"""
        self.failsafe_mode = False
        self.current_record = None
        self.logger.info("✅ 故障模式已清除")


if __name__ == "__main__":
    # 测试故障安全模块
    print("🔐 FailsafeTrigger测试")
    print("=" * 60)
    
    # 初始化
    failsafe = FailsafeTrigger()
    
    # 测试1: 注册模块
    print("\n1. 注册并监控模块...")
    failsafe.monitor_heartbeat("ai_navigation")
    failsafe.monitor_heartbeat("voice_recognition")
    print("   ✓ 模块已注册")
    
    # 测试2: 正常心跳
    print("\n2. 发送正常心跳...")
    failsafe.record_heartbeat("ai_navigation")
    failsafe.record_heartbeat("voice_recognition")
    print("   ✓ 心跳正常")
    
    # 测试3: 触发故障
    print("\n3. 模拟触发故障...")
    failsafe.trigger_failsafe("AI导航子系统未响应", module_name="ai_navigation")
    
    # 测试4: 检查恢复状态
    print("\n4. 检查恢复状态...")
    status = failsafe.get_recovery_status()
    print(f"   故障模式: {status['failsafe_mode']}")
    print(f"   可恢复: {status['has_recovery']}")
    if status['recovery_info']:
        print(f"   任务ID: {status['recovery_info']['active_task_id']}")
    
    # 测试5: 询问用户
    print("\n5. 询问用户是否恢复...")
    user_recovery = failsafe.prompt_user_for_recovery()
    print(f"   用户选择: {'恢复' if user_recovery else '不恢复'}")
    
    # 测试6: 执行恢复
    if user_recovery:
        result = failsafe.restore_task_from_cache()
        print(f"   恢复结果: {'成功' if result else '失败'}")
    
    print("\n🎉 FailsafeTrigger测试完成！")

