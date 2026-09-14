"""
B2 Integration - 接入点（不控制 C）

B2 的输出应该进入"共享上下文/黑板"，C 可以读取，但 B2 不干预 C 的执行节律。
"""

from typing import Optional
from .b2_types import B2Output


class SharedBlackboard:
    """
    简版黑板：后续可升级到统一后台/可视化系统
    
    B2 的输出写入这里，C 可以读取，但 B2 不干预 C 的执行节律。
    """
    
    def __init__(self):
        """初始化共享黑板"""
        self.latest_b2: Optional[B2Output] = None
    
    def put_b2(self, b2_output: B2Output):
        """
        写入 B2 输出
        
        Args:
            b2_output: B2 输出
        """
        self.latest_b2 = b2_output
    
    def get_b2(self) -> Optional[B2Output]:
        """
        获取最新的 B2 输出
        
        Returns:
            B2Output 或 None
        """
        return self.latest_b2

