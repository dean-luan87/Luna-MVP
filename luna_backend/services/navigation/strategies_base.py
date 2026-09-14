"""
导航策略基类 (BaseStrategy) v1.2.0
所有导航策略的基础类，负责任重试机制、日志、错误码、流控制
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from .context import NavigationContext

# 延迟导入以避免循环依赖
def _get_logger():
    try:
        from luna_backend.utils.logger import log_navigation
        return log_navigation
    except ImportError:
        try:
            from utils.logger import log_navigation
            return log_navigation
        except ImportError:
            def _dummy_log(tag, extra):
                pass
            return _dummy_log

def _get_error_codes():
    try:
        from luna_backend.config.error_codes import ERR
        return ERR
    except ImportError:
        try:
            from config.error_codes import ERR
            return ERR
        except ImportError:
            class DummyERR:
                UNKNOWN_ERROR = 9003
            return DummyERR()


class BaseStrategy(ABC):
    """
    导航策略基类
    
    所有具体策略都应该继承此类，实现should_execute和execute方法
    """
    
    STRATEGY_NAME = "BASE"
    
    def __init__(self, context: NavigationContext):
        """
        初始化策略
        
        Args:
            context: NavigationContext 导航当前状态
        """
        self.ctx = context
    
    @abstractmethod
    def should_execute(self) -> bool:
        """
        判断是否应该执行本策略
        
        Returns:
            是否应该执行
        """
        pass
    
    @abstractmethod
    def execute(self) -> Dict[str, Any]:
        """
        执行策略逻辑
        
        Returns:
            策略执行结果字典，包含success, action, text等
        """
        pass
    
    def log(self, tag: str, extra: Optional[Dict[str, Any]] = None):
        """
        记录日志
        
        Args:
            tag: 日志标签
            extra: 额外信息
        """
        log_navigation = _get_logger()
        log_navigation(tag.upper(), extra or {})
    
    def error(self, code: int, msg: str) -> Dict[str, Any]:
        """
        返回错误结果
        
        Args:
            code: 错误码
            msg: 错误消息
        
        Returns:
            错误结果字典
        """
        self.log("STRATEGY_ERROR", {"code": code, "msg": msg})
        return {
            "success": False,
            "error_code": code,
            "error_msg": msg,
            "action": "ERROR",
            "text": msg,
        }
    
    def name(self) -> str:
        """
        获取策略名称
        
        Returns:
            策略名称
        """
        return self.STRATEGY_NAME
    
    def run(self, ctx: Optional[NavigationContext] = None) -> Optional[Dict[str, Any]]:
        """
        运行策略（兼容旧接口）
        
        Args:
            ctx: 导航上下文（可选，如果提供则临时使用）
        
        Returns:
            策略执行结果，如果不应该执行则返回None
        """
        if ctx:
            old_ctx = self.ctx
            self.ctx = ctx
            try:
                if self.should_execute():
                    return self.execute()
            finally:
                self.ctx = old_ctx
        else:
            if self.should_execute():
                return self.execute()
        return None



