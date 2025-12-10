"""
日志分析器
用于分析测试过程中的日志，验证预期行为
"""
import re
from pathlib import Path
from typing import List, Dict, Any, Optional


class LogAnalyzer:
    """日志分析器"""
    
    def __init__(self, log_file: Optional[str] = None):
        """
        初始化日志分析器
        
        Args:
            log_file: 日志文件路径，None 表示使用默认路径
        """
        if log_file is None:
            from core.config.config_center import ConfigCenter
            ConfigCenter.init(env="dev")
            log_file = ConfigCenter.get("logging.file_path", "logs/runtime.log")
        
        self.log_file = Path(log_file)
    
    def search_pattern(self, pattern: str) -> List[str]:
        """
        搜索匹配模式的行
        
        Args:
            pattern: 正则表达式模式
        
        Returns:
            匹配的行列表
        """
        if not self.log_file.exists():
            return []
        
        matches = []
        with open(self.log_file, 'r', encoding='utf-8') as f:
            for line in f:
                if re.search(pattern, line):
                    matches.append(line.strip())
        
        return matches
    
    def count_occurrences(self, pattern: str) -> int:
        """
        统计模式出现次数
        
        Args:
            pattern: 正则表达式模式
        
        Returns:
            出现次数
        """
        return len(self.search_pattern(pattern))
    
    def check_emergency_events(self) -> Dict[str, Any]:
        """
        检查应急事件日志
        
        Returns:
            包含应急事件统计信息的字典
        """
        return {
            "emergency_mode_entered": self.count_occurrences(r"Enter EMERGENCY mode"),
            "degraded_mode_entered": self.count_occurrences(r"Enter DEGRADED mode"),
            "reset_to_normal": self.count_occurrences(r"Reset to NORMAL mode"),
            "emergency_voice_calls": self.count_occurrences(r"\[EmergencyVoice\]"),
        }
    
    def check_health_events(self) -> Dict[str, int]:
        """
        检查健康事件日志
        
        Returns:
            包含各类型健康事件计数的字典
        """
        from core.failsafe.health_events import HealthEvent
        
        events = {}
        for event_type in HealthEvent.all_events():
            events[event_type] = self.count_occurrences(f"Event: {event_type}")
        
        return events
    
    def check_model_switches(self) -> Dict[str, int]:
        """
        检查模型切换日志
        
        Returns:
            包含模型切换统计信息的字典
        """
        return {
            "switch_to_light": self.count_occurrences(r"Switch to LIGHT model"),
            "switch_to_heavy": self.count_occurrences(r"Switch to HEAVY model"),
            "forced_to_lightweight": self.count_occurrences(r"Forced to LIGHTWEIGHT model"),
        }
    
    def get_recent_errors(self, limit: int = 10) -> List[str]:
        """
        获取最近的错误日志
        
        Args:
            limit: 返回的最大行数
        
        Returns:
            错误日志行列表
        """
        errors = self.search_pattern(r"\[ERROR\]|\[CRITICAL\]")
        return errors[-limit:] if len(errors) > limit else errors





