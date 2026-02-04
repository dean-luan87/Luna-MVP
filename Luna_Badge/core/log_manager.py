#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 行为日志记录器 (Behavior Chain Tracker)
实时记录所有用户行为事件，用于分析、调试和用户画像
"""

import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum

logger = logging.getLogger(__name__)


class LogSource(Enum):
    """日志来源"""
    VOICE = "voice"
    VISION = "vision"
    NAVIGATION = "navigation"
    MEMORY = "memory"
    TTS = "tts"
    SYSTEM = "system"
    OBSERVER_MODE = "observer_mode"  # v1.8.1: Observer Mode 专属日志


class LogLevel(Enum):
    """日志级别"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    DEBUG = "debug"


@dataclass
class BehaviorLog:
    """行为日志条目"""
    timestamp: str
    source: str
    intent: Optional[str] = None
    content: Optional[str] = None
    system_response: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    level: str = "info"
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        data = asdict(self)
        # 移除None字段
        return {k: v for k, v in data.items() if v is not None}


class LogManager:
    """行为日志管理器"""
    
    def __init__(self,
                 user_id: str = "anonymous",
                 log_dir: str = "logs/user_behavior"):
        """
        初始化日志管理器
        
        Args:
            user_id: 用户ID
            log_dir: 日志目录
        """
        self.user_id = user_id
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # 当前日志文件
        self.current_log_file = None
        self.log_buffer = []
        self.buffer_size = 50
        
        logger.info(f"📶 行为日志管理器初始化 (用户: {user_id})")
    
    def _get_log_file_path(self, date: Optional[str] = None) -> Path:
        """获取日志文件路径"""
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
        
        filename = f"{date}_{self.user_id}.log"
        return self.log_dir / filename
    
    def _ensure_log_file(self):
        """确保日志文件存在"""
        if not self.current_log_file:
            self.current_log_file = self._get_log_file_path()
    
    def log_voice_intent(self,
                        intent: str,
                        content: str,
                        system_response: str,
                        metadata: Optional[Dict[str, Any]] = None):
        """
        记录语音意图日志
        
        Args:
            intent: 意图
            content: 用户语音内容
            system_response: 系统响应
            metadata: 额外元数据
        """
        log = BehaviorLog(
            timestamp=datetime.now().isoformat(),
            source=LogSource.VOICE.value,
            intent=intent,
            content=content,
            system_response=system_response,
            metadata=metadata,
            level=LogLevel.INFO.value
        )
        
        self._write_log(log)
    
    def log_visual_event(self,
                        event_type: str,
                        detection_result: Dict[str, Any],
                        system_response: Optional[str] = None):
        """
        记录视觉事件日志
        
        Args:
            event_type: 事件类型
            detection_result: 检测结果
            system_response: 系统响应
        """
        log = BehaviorLog(
            timestamp=datetime.now().isoformat(),
            source=LogSource.VISION.value,
            intent=event_type,
            content=str(detection_result),
            system_response=system_response,
            metadata={"detection_result": detection_result},
            level=LogLevel.INFO.value
        )
        
        self._write_log(log)
    
    def log_navigation(self,
                      action: str,
                      destination: Optional[str] = None,
                      path_info: Optional[Dict[str, Any]] = None,
                      system_response: Optional[str] = None):
        """
        记录导航日志
        
        Args:
            action: 导航动作
            destination: 目的地
            path_info: 路径信息
            system_response: 系统响应
        """
        content = f"导航动作: {action}"
        if destination:
            content += f", 目的地: {destination}"
        
        log = BehaviorLog(
            timestamp=datetime.now().isoformat(),
            source=LogSource.NAVIGATION.value,
            intent=action,
            content=content,
            system_response=system_response,
            metadata={"destination": destination, "path_info": path_info},
            level=LogLevel.INFO.value
        )
        
        self._write_log(log)
    
    def log_memory_operation(self,
                            operation: str,
                            data: Optional[Dict[str, Any]] = None,
                            system_response: Optional[str] = None):
        """
        记录记忆操作日志
        
        Args:
            operation: 操作类型
            data: 数据
            system_response: 系统响应
        """
        log = BehaviorLog(
            timestamp=datetime.now().isoformat(),
            source=LogSource.MEMORY.value,
            intent=operation,
            content=str(data) if data else None,
            system_response=system_response,
            metadata={"data": data},
            level=LogLevel.INFO.value
        )
        
        self._write_log(log)
    
    def log_tts_output(self,
                      text: str,
                      success: bool = True,
                      metadata: Optional[Dict[str, Any]] = None):
        """
        记录TTS输出日志
        
        Args:
            text: 播报文本
            success: 是否成功
            metadata: 额外元数据
        """
        log = BehaviorLog(
            timestamp=datetime.now().isoformat(),
            source=LogSource.TTS.value,
            intent="speak",
            content=text,
            system_response="success" if success else "failed",
            metadata=metadata,
            level=LogLevel.INFO.value if success else LogLevel.ERROR.value
        )
        
        self._write_log(log)
    
    def log_system_event(self,
                        event: str,
                        level: LogLevel = LogLevel.INFO,
                        metadata: Optional[Dict[str, Any]] = None):
        """
        记录系统事件日志
        
        Args:
            event: 事件描述
            level: 日志级别
            metadata: 额外元数据
        """
        log = BehaviorLog(
            timestamp=datetime.now().isoformat(),
            source=LogSource.SYSTEM.value,
            content=event,
            metadata=metadata,
            level=level.value
        )
        
        self._write_log(log)
    
    def _write_log(self, log: BehaviorLog):
        """
        写入日志
        
        Args:
            log: 日志条目
        """
        # 确保日志文件存在
        self._ensure_log_file()
        
        # 添加到缓冲区
        self.log_buffer.append(log)
        
        # 缓冲区满了或重要日志立即写入
        if len(self.log_buffer) >= self.buffer_size or log.level in ["error", "warning"]:
            self._flush_buffer()
    
    def _flush_buffer(self):
        """刷新缓冲区到文件"""
        if not self.log_buffer:
            return
        
        try:
            # 追加模式写入
            with open(self.current_log_file, 'a', encoding='utf-8') as f:
                for log in self.log_buffer:
                    f.write(json.dumps(log.to_dict(), ensure_ascii=False) + '\n')
            
            logger.debug(f"📝 写入 {len(self.log_buffer)} 条日志")
            self.log_buffer.clear()
            
        except Exception as e:
            logger.error(f"❌ 写入日志失败: {e}")
    
    def flush(self):
        """手动刷新缓冲区"""
        self._flush_buffer()
    
    def log_observer_mode_event(self,
                                observer_trigger_reason: str,
                                observer_level: str,
                                user_response: Optional[str] = None,
                                intervene_reason: Optional[str] = None,
                                observer_enabled: bool = False,
                                observer_bypass_reason: Optional[str] = None,
                                metadata: Optional[Dict[str, Any]] = None):
        """
        v1.8.1: 记录 Observer Mode 专属日志
        
        硬约束：
        1. observer_mode=false 时，禁止写任何新增字段
        2. 日志写入必须是旁路：失败不影响主流程、可关可删
        
        Args:
            observer_trigger_reason: Observer Mode 触发原因
            observer_level: Observer Mode 级别（background / confirm / intervene）
            user_response: 用户响应（accepted / rejected / ignored，仅 CONFIRM 时使用）
            intervene_reason: 干预原因（仅 INTERVENE 时使用）
            observer_enabled: Observer Mode 是否启用（bool，写死当前是否启用）
            observer_bypass_reason: 记录为何未记录/未触发（string）
            metadata: 额外元数据（应包含 active: bool 字段）
        
        最小日志字段：
        - observer_trigger_reason
        - observer_level
        - observer_user_response
        
        额外字段（内部日志）：
        - observer_enabled
        - observer_bypass_reason
        """
        # 硬约束 1: observer_mode=false 时，禁止写任何新增字段
        if not observer_enabled:
            return  # Observer Mode 未启用时不记录
        
        # 如果 metadata 中 active=False，也不记录
        if metadata and not metadata.get("active", False):
            return  # Observer Mode 未激活时不记录
        
        try:
            log_metadata = metadata or {}
            log_metadata.update({
                "observer_trigger_reason": observer_trigger_reason,
                "observer_level": observer_level,
                "observer_enabled": observer_enabled,
            })
            
            if user_response:
                log_metadata["observer_user_response"] = user_response
            
            if intervene_reason:
                log_metadata["intervene_reason"] = intervene_reason
            
            if observer_bypass_reason:
                log_metadata["observer_bypass_reason"] = observer_bypass_reason
            
            log = BehaviorLog(
                timestamp=datetime.now().isoformat(),
                source=LogSource.OBSERVER_MODE.value,
                content=f"Observer Mode: {observer_level}",
                metadata=log_metadata,
                level=LogLevel.INFO.value
            )
            
            # 硬约束 2: 日志写入必须是旁路，失败不影响主流程
            self._write_log(log)
        except Exception as e:
            # 吞掉异常（或降级到 debug），不影响用户侧流程
            logger.debug(f"[ObserverMode] 日志写入失败（已忽略）: {e}")
            # 不抛出异常，不影响主流程
    
    def read_logs(self,
                  date: Optional[str] = None,
                  limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        读取日志
        
        Args:
            date: 日期
            limit: 限制条数
            
        Returns:
            日志列表
        """
        log_file = self._get_log_file_path(date)
        
        if not log_file.exists():
            return []
        
        try:
            logs = []
            with open(log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        try:
                            log = json.loads(line)
                            logs.append(log)
                        except json.JSONDecodeError:
                            continue
            
            # 限制返回数量
            if limit:
                logs = logs[-limit:]
            
            return logs
            
        except Exception as e:
            logger.error(f"❌ 读取日志失败: {e}")
            return []
    
    def list_available_dates(self) -> List[str]:
        """
        列出所有可用的日志日期
        
        Returns:
            日期列表（格式：YYYY-MM-DD）
        """
        dates = []
        if not self.log_dir.exists():
            return dates
        
        pattern = f"*_{self.user_id}.log"
        for log_file in self.log_dir.glob(pattern):
            # 从文件名提取日期：YYYY-MM-DD_userid.log
            try:
                date_str = log_file.stem.replace(f"_{self.user_id}", "")
                # 验证日期格式
                datetime.strptime(date_str, "%Y-%m-%d")
                dates.append(date_str)
            except ValueError:
                continue
        
        return sorted(dates, reverse=True)  # 最新的在前
    
    def get_latest_logs(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        获取最新的日志（自动查找最近的日志文件）
        
        Args:
            limit: 限制条数
            
        Returns:
            日志列表
        """
        available_dates = self.list_available_dates()
        if not available_dates:
            return []
        
        # 尝试从最新的日期开始读取
        all_logs = []
        for date in available_dates:
            logs = self.read_logs(date=date)
            all_logs.extend(logs)
            if limit and len(all_logs) >= limit:
                break
        
        if limit:
            return all_logs[-limit:]
        return all_logs
    
    def get_statistics(self, date: Optional[str] = None) -> Dict[str, Any]:
        """
        获取统计信息
        
        Args:
            date: 日期
            
        Returns:
            统计信息
        """
        logs = self.read_logs(date)
        
        stats = {
            "total_logs": len(logs),
            "by_source": {},
            "by_level": {},
            "by_intent": {}
        }
        
        for log in logs:
            # 按来源统计
            source = log.get("source", "unknown")
            stats["by_source"][source] = stats["by_source"].get(source, 0) + 1
            
            # 按级别统计
            level = log.get("level", "info")
            stats["by_level"][level] = stats["by_level"].get(level, 0) + 1
            
            # 按意图统计
            intent = log.get("intent", "unknown")
            stats["by_intent"][intent] = stats["by_intent"].get(intent, 0) + 1
        
        return stats


# 全局日志管理器实例
_global_log_manager = None


def get_log_manager(user_id: str = "anonymous") -> LogManager:
    """获取全局日志管理器实例"""
    global _global_log_manager
    
    if _global_log_manager is None:
        _global_log_manager = LogManager(user_id=user_id)
    
    return _global_log_manager


# 测试函数
if __name__ == "__main__":
    import logging
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 创建日志管理器
    log_manager = LogManager(user_id="test_user")
    
    print("=" * 70)
    print("📶 测试行为日志管理器")
    print("=" * 70)
    
    # 测试语音意图日志
    print("\n🎤 测试语音意图日志:")
    log_manager.log_voice_intent(
        intent="find_toilet",
        content="我要去厕所",
        system_response="已开始导航至洗手间"
    )
    
    # 测试视觉事件日志
    print("👁️ 测试视觉事件日志:")
    log_manager.log_visual_event(
        event_type="stairs_detected",
        detection_result={"classes": ["stairs"], "confidence": 0.95},
        system_response="前方有台阶，请小心"
    )
    
    # 测试导航日志
    print("🧭 测试导航日志:")
    log_manager.log_navigation(
        action="start_navigation",
        destination="305号诊室",
        path_info={"distance": 30, "steps": 5},
        system_response="正在为您导航到305号诊室"
    )
    
    # 测试记忆日志
    print("💾 测试记忆日志:")
    log_manager.log_memory_operation(
        operation="save_path",
        data={"path_id": "path_123", "nodes": 5},
        system_response="路径已保存"
    )
    
    # 测试TTS日志
    print("🔊 测试TTS日志:")
    log_manager.log_tts_output(
        text="请直行10米，左转后有洗手间",
        success=True
    )
    
    # 测试系统事件日志
    print("⚙️ 测试系统事件日志:")
    log_manager.log_system_event(
        event="控制中枢启动",
        level=LogLevel.INFO
    )
    
    # 刷新缓冲区
    log_manager.flush()
    
    # 读取日志
    print("\n📖 读取日志:")
    logs = log_manager.read_logs(limit=10)
    print(f"总日志数: {len(logs)}")
    for log in logs[-3:]:
        print(f"  {log['timestamp']}: {log['source']} - {log.get('intent', 'N/A')}")
    
    # 获取统计
    print("\n📊 统计信息:")
    stats = log_manager.get_statistics()
    print(json.dumps(stats, indent=2, ensure_ascii=False))
    
    print("\n✅ 测试完成")
