"""
导航策略基类 (Navigation Strategy Base) v1.2.0
所有视觉导航子策略必须实现的接口
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Protocol


@dataclass
class FrameContext:
    """
    当前帧的视觉上下文信息（给所有策略共用）。
    
    注意：这里不要引入 heavy 依赖，只放结构。
    真正的 image_np 由调用方传入，类型保持 Any。
    """
    image_np: Any  # numpy.ndarray
    detections: List[Dict[str, Any]]  # YOLO / VisionEngine 检测结果
    ocr_results: List[Dict[str, Any]]  # OCR 文本结果
    env_meta: Dict[str, Any]  # 环境元信息（时间/室内室外等，可选）


@dataclass
class StrategyResult:
    """
    每个策略返回的结果统一结构。
    """
    active: bool                       # 是否触发了策略
    severity: str                      # "info" | "warning" | "critical"
    message: str                       # 给用户的提示文案（可选）
    code: str                          # 错误码 / 策略码（例如 NAV_STRAT_LOW_LIGHT）
    extra: Dict[str, Any]              # 额外元数据（给调试用）


class NavigationStrategy(Protocol):
    """
    所有导航视觉子策略必须实现的接口。
    """
    
    name: str
    
    def analyze(self, ctx: FrameContext) -> Optional[StrategyResult]:
        """
        输入一帧视觉上下文，输出一个策略结果。
        如果该帧不需要策略介入，可以返回 None。
        """
        ...


class StrategyRegistry:
    """
    策略注册器：NavigationManager 只跟这个打交道。
    """
    
    def __init__(self) -> None:
        self._strategies: List[NavigationStrategy] = []
    
    def register(self, strategy: NavigationStrategy) -> None:
        """注册策略"""
        self._strategies.append(strategy)
    
    def analyze(self, ctx: FrameContext) -> List[StrategyResult]:
        """
        依次执行所有策略，收集结果（可能有多个同时触发）。
        """
        results: List[StrategyResult] = []
        
        for strat in self._strategies:
            try:
                res = strat.analyze(ctx)
                if res is not None and res.active:
                    results.append(res)
            except Exception as e:
                # 这里不抛异常，避免单个策略拖垮整体导航
                # 真正的错误日志由上层去打（NavigationManager / LogManager）
                results.append(
                    StrategyResult(
                        active=True,
                        severity="warning",
                        message=f"策略 {strat.name} 执行异常",
                        code="NAV_STRAT_INTERNAL_ERROR",
                        extra={"strategy": strat.name, "error": str(e)},
                    )
                )
        
        return results



