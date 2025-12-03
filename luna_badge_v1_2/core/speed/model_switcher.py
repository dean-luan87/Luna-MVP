"""
Model Switcher
1.4.1-speed.4: YOLO 模型动态切换器
基于推理耗时自动在 heavy/light 模型间切换
"""
import time
from typing import Optional, Any

from core.logging.log_manager import LogManager
from core.config.config_center import ConfigCenter
from core.health.metrics_collector import MetricsCollector


class ModelSwitcher:
    """
    YOLO 模型切换器
    
    功能：
    - 维护 heavy_model / light_model
    - 基于最近若干次推理耗时自动切换
    - 避免频繁抖动（双阈值 + 最小样本数）
    """
    
    def __init__(self, heavy_model: Any, light_model: Optional[Any] = None):
        """
        初始化模型切换器
        
        Args:
            heavy_model: 重型模型（高精度，可能较慢）
            light_model: 轻型模型（快速，可能精度略低），可选
        """
        self.logger = LogManager.get_logger("ModelSwitcher")
        self.heavy_model = heavy_model
        self.light_model = light_model
        self.active_model = heavy_model
        self.active_name = "heavy"
        
        self.history_latency: list[float] = []
        self.max_history = 20
        
        # 阈值从配置读取，可进一步调参
        self.heavy_to_light_ms = ConfigCenter.get("speed.model_switcher.heavy_to_light_ms", 80)
        self.light_to_heavy_ms = ConfigCenter.get("speed.model_switcher.light_to_heavy_ms", 40)
        self.min_samples = ConfigCenter.get("speed.model_switcher.min_samples", 5)
        
        if light_model is None:
            self.logger.info("ModelSwitcher: 未提供 light_model，将仅使用 heavy_model")
        else:
            self.logger.info(f"ModelSwitcher: 已初始化 (heavy_to_light={self.heavy_to_light_ms}ms, light_to_heavy={self.light_to_heavy_ms}ms)")

    def record_latency(self, elapsed_ms: float) -> None:
        """
        记录推理耗时
        
        Args:
            elapsed_ms: 推理耗时（毫秒）
        """
        self.history_latency.append(elapsed_ms)
        if len(self.history_latency) > self.max_history:
            self.history_latency.pop(0)

    def get_avg_latency(self) -> float:
        """
        获取平均推理耗时
        
        Returns:
            平均耗时（毫秒）
        """
        if not self.history_latency:
            return 0.0
        return sum(self.history_latency) / len(self.history_latency)

    def maybe_switch(self) -> None:
        """
        根据历史延迟决定是否切换模型
        """
        if not self.history_latency or len(self.history_latency) < self.min_samples:
            return
        
        avg = self.get_avg_latency()
        
        # 当前是 heavy，且均值超阈值 → 尝试切 light
        if self.active_name == "heavy" and self.light_model is not None:
            if avg > self.heavy_to_light_ms:
                self.active_model = self.light_model
                self.active_name = "light"
                self.logger.warning(f"[ModelSwitcher] Switch to LIGHT model, avg={avg:.1f}ms")
                MetricsCollector.incr("model_switcher.switch_to_light")
        
        # 当前是 light，且均值低于回切阈值 → 尝试切回 heavy
        elif self.active_name == "light":
            if avg < self.light_to_heavy_ms:
                self.active_model = self.heavy_model
                self.active_name = "heavy"
                self.logger.info(f"[ModelSwitcher] Switch to HEAVY model, avg={avg:.1f}ms")
                MetricsCollector.incr("model_switcher.switch_to_heavy")

    def infer(self, frame: Any) -> Any:
        """
        推理入口
        
        Args:
            frame: 输入图像帧
        
        Returns:
            推理结果
        """
        start = time.perf_counter()
        
        # 支持多种模型接口
        if hasattr(self.active_model, 'detect'):
            # YoloDetector 接口
            result = self.active_model.detect(frame)
        elif hasattr(self.active_model, '__call__'):
            # 直接调用接口（如 ultralytics YOLO）
            result = self.active_model(frame)
        else:
            self.logger.error("Unsupported model interface")
            return None
        
        elapsed_ms = (time.perf_counter() - start) * 1000
        
        MetricsCollector.add_timing("vision_infer.yolo_ms", elapsed_ms / 1000.0)  # 转换为秒
        MetricsCollector.incr(f"model_switcher.{self.active_name}_inferences")
        
        self.record_latency(elapsed_ms)
        self.maybe_switch()
        
        return result

    def force_to_lightweight(self) -> bool:
        """
        强制切换到轻量级模型（1.4.1-failsafe.3）
        
        用于降级模式，强制使用最轻量的模型
        
        Returns:
            True 如果成功切换，False 如果 light 模型不存在
        """
        if self.light_model is None:
            self.logger.warning("[ModelSwitcher] Cannot force to lightweight: light_model not available")
            return False
        
        if self.active_name == "light":
            # 已经在使用 light 模型
            return True
        
        self.active_model = self.light_model
        self.active_name = "light"
        self.logger.warning("[ModelSwitcher] Forced to LIGHTWEIGHT model (degraded mode)")
        MetricsCollector.incr("model_switcher.forced_to_light")
        return True

    def get_stats(self) -> dict:
        """
        获取统计信息
        
        Returns:
            包含当前模型、平均延迟等统计信息的字典
        """
        return {
            "active_model": self.active_name,
            "avg_latency_ms": self.get_avg_latency(),
            "history_count": len(self.history_latency),
            "has_light_model": self.light_model is not None,
        }

