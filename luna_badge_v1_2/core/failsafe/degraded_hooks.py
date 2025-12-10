"""
Degraded Hooks
1.4.1-failsafe.3: 降级行为钩子
在进入降级模式时执行降级行为（模型降级、OCR 暂停等）
"""
from typing import Optional

from core.logging.log_manager import LogManager
from core.speed.speed_context import SpeedContext


class DegradedHooks:
    """
    Degraded 行为钩子 v1
    
    功能：
    - 强制模型降级：启用最轻量模型
    - 暂停 OCR（若系统中存在 OCRManager）
    - 所有操作必须为"非破坏性"
    
    设计原则：
    - 非阻塞
    - 防御性编程（OCR 不存在时不影响）
    - 可恢复
    """
    
    _instance: Optional["DegradedHooks"] = None
    
    def __init__(self):
        """初始化降级钩子"""
        self.logger = LogManager.get_logger("DegradedHooks")
        self.ocr_paused = False
        self.model_forced = False

    @classmethod
    def get_instance(cls) -> "DegradedHooks":
        """
        获取单例实例
        
        Returns:
            DegradedHooks 实例
        """
        if cls._instance is None:
            cls._instance = DegradedHooks()
        return cls._instance

    def apply(self) -> None:
        """
        应用降级行为
        
        包括：
        - 强制切到最轻量模型
        - 暂停 OCR（如果存在）
        """
        self.logger.warning("[DegradedHooks] Applying degraded behaviour")

        # 1. 强制切到最轻量模型
        try:
            # 通过 VisionInferWorker 获取 ModelSwitcher
            # 由于 ModelSwitcher 在 VisionInferWorker 内部，我们需要通过 SpeedContext 访问
            # 或者直接通过 VisionInferWorker 访问
            
            # 方案：通过 SpeedContext 存储的 infer_worker 访问
            # 如果 infer_worker 不存在，则尝试其他方式
            infer_worker = getattr(SpeedContext, 'infer_worker', None)
            
            if infer_worker is not None and hasattr(infer_worker, 'switcher'):
                success = infer_worker.switcher.force_to_lightweight()
                if success:
                    self.model_forced = True
                    self.logger.info("[DegradedHooks] Model switched to lightweight")
                else:
                    self.logger.warning("[DegradedHooks] Model switch to lightweight failed (light model not available)")
            else:
                self.logger.warning("[DegradedHooks] VisionInferWorker not available, cannot force model switch")
        except Exception as e:
            self.logger.error(f"[DegradedHooks] Model switch failed: {e}")

        # 2. 暂停 OCR
        try:
            from core.ocr.ocr_manager import OCRManager
            if hasattr(OCRManager, 'pause'):
                OCRManager.pause()
                self.ocr_paused = True
                self.logger.info("[DegradedHooks] OCR paused")
            else:
                self.logger.debug("[DegradedHooks] OCRManager.pause() not available")
        except (ImportError, AttributeError):
            self.logger.debug("[DegradedHooks] OCRManager not available, skipping OCR pause")

    def restore(self) -> None:
        """
        恢复正常行为
        
        包括：
        - 恢复 OCR（如果之前暂停了）
        - 恢复模型切换（允许自动切换）
        """
        self.logger.info("[DegradedHooks] Restoring normal behaviour")

        # 恢复 OCR
        if self.ocr_paused:
            try:
                from core.ocr.ocr_manager import OCRManager
                if hasattr(OCRManager, 'resume'):
                    OCRManager.resume()
                    self.logger.info("[DegradedHooks] OCR resumed")
            except (ImportError, AttributeError):
                pass
            finally:
                self.ocr_paused = False

        # 恢复模型切换（清除强制标记，允许自动切换）
        self.model_forced = False
        self.logger.debug("[DegradedHooks] Model switch restriction removed")

    def get_stats(self) -> dict:
        """
        获取统计信息
        
        Returns:
            包含当前状态等统计信息的字典
        """
        return {
            "ocr_paused": self.ocr_paused,
            "model_forced": self.model_forced,
        }





