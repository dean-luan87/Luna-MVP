# core/model_scheduler/executor.py
from concurrent.futures import ThreadPoolExecutor, Future
from typing import Any, Dict, List, Optional
from .registry import ModelDescriptor


class ParallelExecutionManager:
    """统一管理多模型的并行执行."""

    def __init__(self, max_workers: int = 4) -> None:
        self._pool = ThreadPoolExecutor(max_workers=max_workers)

    def submit(self, model: ModelDescriptor, **inputs: Any) -> Future:
        if model.runner is None:
            raise RuntimeError(f"Model {model.id} has no runner attached")
        return self._pool.submit(model.runner, **inputs)


class FallbackChain:
    """模型故障时的 fallback 策略链."""

    def __init__(self, models: List[ModelDescriptor]) -> None:
        self._models = models

    def run_with_fallback(self, **inputs: Any) -> Dict[str, Any]:
        last_error: Optional[Exception] = None
        for m in self._models:
            try:
                if m.runner is None:
                    continue
                result = m.runner(**inputs)
                return {
                    "model_id": m.id,
                    "success": True,
                    "output": result,
                }
            except Exception as e:
                last_error = e
                continue
        return {
            "model_id": None,
            "success": False,
            "error": str(last_error) if last_error else "no_model_available",
        }


class ModelScheduler:
    """
    对上层暴露的统一接口：执行单模型 / 执行 fallback 链。
    模型选择可以由上层 ContextAwareModelSelector 决定。
    """

    def __init__(self, parallel_manager: Optional[ParallelExecutionManager] = None) -> None:
        self._parallel_manager = parallel_manager or ParallelExecutionManager()

    def run_single_model(self, model: ModelDescriptor, **inputs: Any) -> Dict[str, Any]:
        future = self._parallel_manager.submit(model, **inputs)
        output = future.result()
        return {
            "model_id": model.id,
            "success": True,
            "output": output,
        }

    def run_fallback_chain(self, models: List[ModelDescriptor], **inputs: Any) -> Dict[str, Any]:
        chain = FallbackChain(models)
        return chain.run_with_fallback(**inputs)
