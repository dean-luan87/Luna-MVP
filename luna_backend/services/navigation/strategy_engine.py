"""
策略引擎 (StrategyEngine) v1.2.0
Luna导航的灵魂：策略调度器，负责按优先级执行策略
"""

from typing import List, Dict, Any, Optional
from .navigation_context import NavigationContext
from .base_strategy import BaseStrategy

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

def _get_speech_router():
    """延迟导入语音路由"""
    try:
        from luna_backend.services.speech.speech_router import SpeechRouter
        return SpeechRouter()
    except ImportError:
        try:
            from services.speech.speech_router import SpeechRouter
            return SpeechRouter()
        except ImportError:
            return None


class StrategyEngine:
    """
    策略引擎
    
    核心逻辑：依次检查策略 → 执行第一个匹配的策略
    """
    
    def __init__(self, context: NavigationContext, strategies: Optional[List[BaseStrategy]] = None, enable_speech: bool = True):
        """
        初始化策略引擎
        
        Args:
            context: 导航上下文
            strategies: 策略列表（按优先级排序），如果为None则使用默认策略列表
            enable_speech: 是否启用语音播报
        """
        self.ctx = context
        self.strategies: List[BaseStrategy] = strategies or []
        self.last_executed_strategy: Optional[str] = None
        self.enable_speech = enable_speech
        self.speaker = _get_speech_router() if enable_speech else None
    
    def add_strategy(self, strategy: BaseStrategy, priority: Optional[int] = None):
        """
        添加策略
        
        Args:
            strategy: 策略实例
            priority: 优先级（越小越优先），如果为None则添加到末尾
        """
        if priority is not None:
            self.strategies.insert(priority, strategy)
        else:
            self.strategies.append(strategy)
    
    def run(self) -> Dict[str, Any]:
        """
        执行策略引擎
        
        核心逻辑：依次检查策略 → 执行第一个匹配的策略
        
        Returns:
            策略执行结果字典
        """
        if not self.strategies:
            return {
                "success": True,
                "action": "NO_ACTION",
                "text": "当前无需策略执行",
                "strategy": "NONE",
            }
        
        # 依次检查策略
        for strategy in self.strategies:
            try:
                if strategy.should_execute():
                    self.last_executed_strategy = strategy.name()
                    result = strategy.execute()
                    
                    # 确保结果包含必要字段
                    if not isinstance(result, dict):
                        result = {"success": True, "action": "UNKNOWN", "text": str(result)}
                    
                    result.setdefault("success", True)
                    result.setdefault("strategy", strategy.name())
                    
                    # 记录日志
                    log_navigation = _get_logger()
                    log_navigation("STRATEGY_EXECUTED", {
                        "strategy": strategy.name(),
                        "action": result.get("action"),
                        "context": self.ctx.to_dict(),
                    })
                    
                    # 语音播报（如果启用）
                    if self.enable_speech and self.speaker and "text" in result:
                        try:
                            self.speaker.speak_action(result)
                        except Exception as e:
                            log_navigation("SPEECH_ERROR", {
                                "error": str(e),
                                "text": result.get("text")
                            })
                    
                    return result
            except Exception as e:
                # 策略执行异常，记录日志但继续尝试下一个策略
                log_navigation = _get_logger()
                log_navigation("STRATEGY_ERROR", {
                    "strategy": strategy.name(),
                    "error": str(e),
                })
                continue
        
        # 没有策略匹配，返回默认动作
        return {
            "success": True,
            "action": "NO_ACTION",
            "text": "当前无需策略执行",
            "strategy": "NONE",
        }
    
    def get_current_strategy(self) -> Optional[BaseStrategy]:
        """
        获取当前执行的策略
        
        Returns:
            当前策略实例，如果没有则返回None
        """
        if self.last_executed_strategy:
            for s in self.strategies:
                if s.name() == self.last_executed_strategy:
                    return s
        return None
    
    def clear_strategies(self):
        """清空所有策略"""
        self.strategies.clear()
        self.last_executed_strategy = None

