"""
Calibration Hint Store (v1.4.8 Step 10)

Hint 存储：管理 CalibrationHint 的内存存储

存储策略：
- MAX_HINTS = 100
- FIFO RingBuffer
- 超限丢弃最旧 Hint
"""

from typing import List
from navigation.calibration_hint import CalibrationHint


class CalibrationHintStore:
    """
    校准提示存储：内存存储管理器
    
    职责：
    - 管理 CalibrationHint 的内存存储
    - 提供只读查询能力
    """
    
    def __init__(self, max_hints: int = 100):
        """
        初始化存储
        
        Args:
            max_hints: 最大 Hint 数（默认 100）
        """
        self.max_hints = max_hints
        self._hints: List[CalibrationHint] = []
    
    def add_hint(self, hint: CalibrationHint) -> None:
        """
        添加 Hint
        
        如果超过 max_hints，自动丢弃最旧的 Hint
        
        Args:
            hint: 校准提示
        """
        self._hints.append(hint)
        
        # 如果超过上限，移除最旧的 Hint
        if len(self._hints) > self.max_hints:
            self._hints.pop(0)
    
    def get_all(self) -> List[CalibrationHint]:
        """
        获取所有 Hint
        
        Returns:
            所有 Hint 的列表（拷贝）
        """
        return self._hints.copy()
    
    def get_by_type(self, hint_type: str) -> List[CalibrationHint]:
        """
        按类型查询
        
        Args:
            hint_type: Hint 类型
            
        Returns:
            匹配的 Hint 列表（拷贝）
        """
        filtered = [
            hint for hint in self._hints
            if hint.hint_type == hint_type
        ]
        return filtered.copy()
    
    def get_by_authority(self, authority: str) -> List[CalibrationHint]:
        """
        按主权查询
        
        Args:
            authority: 主权名称（"VISUAL", "MAP_VISION", "GPS"）
            
        Returns:
            匹配的 Hint 列表（拷贝）
        """
        filtered = [
            hint for hint in self._hints
            if hint.authority == authority
        ]
        return filtered.copy()
    
    def size(self) -> int:
        """获取当前 Hint 数"""
        return len(self._hints)
    
    def clear(self) -> None:
        """清空存储"""
        self._hints.clear()
    
    def get_stats(self) -> dict:
        """获取统计信息"""
        if not self._hints:
            return {
                "hint_count": 0,
                "type_count": {},
                "authority_count": {}
            }
        
        # 统计不同类型的数量
        type_count = {}
        for hint in self._hints:
            hint_type = hint.hint_type
            type_count[hint_type] = type_count.get(hint_type, 0) + 1
        
        # 统计不同 authority 的数量
        authority_count = {}
        for hint in self._hints:
            auth = hint.authority
            authority_count[auth] = authority_count.get(auth, 0) + 1
        
        return {
            "hint_count": len(self._hints),
            "type_count": type_count,
            "authority_count": authority_count
        }






