"""
Inference Wrapper (v1.3.0)

推理封装（含日志）

对模型推理进行统一封装，提供统一的接口、错误处理和日志记录
"""

import logging
import time
from typing import Dict, Any, Optional, Callable
from functools import wraps

from .error_codes import ErrorCode, create_error_response, create_success_response
from .tracking import TrackingSystem, EventType

logger = logging.getLogger(__name__)


class InferenceWrapper:
    """
    推理封装器

    对模型推理进行统一封装，提供：
    - 统一的输入/输出格式
    - 错误处理和重试机制
    - 性能监控和日志记录
    - 埋点数据记录
    """

    def __init__(
        self,
        model_name: str,
        model_callable: Callable,
        tracking: Optional[TrackingSystem] = None,
        timeout_seconds: float = 30.0,
        max_retries: int = 1,
    ):
        """
        初始化推理封装器

        Args:
            model_name: 模型名称（如 "L1", "L2"）
            model_callable: 模型可调用对象
            tracking: 埋点系统实例（可选）
            timeout_seconds: 超时时间（秒）
            max_retries: 最大重试次数
        """
        self.model_name = model_name
        self.model_callable = model_callable
        self.tracking = tracking
        self.timeout_seconds = timeout_seconds
        self.max_retries = max_retries

        logger.info(f"推理封装器初始化: {model_name}")

    def infer(
        self,
        user_input: str,
        context: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        执行推理

        Args:
            user_input: 用户输入
            context: 上下文信息（可选）
            metadata: 额外元数据（可选）

        Returns:
            Dict[str, Any]: 推理结果
        """
        start_time = time.time()

        # 输入验证
        validation_result = self._validate_input(user_input)
        if not validation_result["success"]:
            return validation_result

        # 记录开始推理
        logger.debug(f"[{self.model_name}] 开始推理: {user_input[:50]}...")

        # 重试机制
        last_error = None
        for attempt in range(self.max_retries + 1):
            try:
                # 执行推理
                result = self._execute_inference(user_input, context)

                # 计算延迟
                latency_ms = (time.time() - start_time) * 1000

                # 验证输出
                if "error" in result:
                    last_error = result["error"]
                    logger.warning(
                        f"[{self.model_name}] 推理失败 (尝试 {attempt + 1}/{self.max_retries + 1}): {last_error}"
                    )
                    continue

                # 记录埋点
                if self.tracking:
                    self.tracking.track_inference(
                        model=self.model_name,
                        user_input=user_input,
                        response=result.get("text", ""),
                        latency_ms=latency_ms,
                        success=True,
                    )

                logger.info(
                    f"[{self.model_name}] 推理成功，延迟: {latency_ms:.2f}ms"
                )

                return create_success_response({
                    "text": result.get("text", ""),
                    "intent": result.get("intent"),
                    "confidence": result.get("confidence"),
                    "latency_ms": latency_ms,
                    "metadata": metadata,
                })

            except TimeoutError:
                error_msg = f"推理超时（>{self.timeout_seconds}秒）"
                logger.error(f"[{self.model_name}] {error_msg}")
                last_error = error_msg

                # 记录埋点
                if self.tracking:
                    self.tracking.track_inference(
                        model=self.model_name,
                        user_input=user_input,
                        response="",
                        latency_ms=(time.time() - start_time) * 1000,
                        success=False,
                        error_code=ErrorCode.E204.value,
                    )

                return create_error_response(ErrorCode.E204, error_msg)

            except Exception as e:
                error_msg = str(e)
                logger.error(
                    f"[{self.model_name}] 推理异常 (尝试 {attempt + 1}/{self.max_retries + 1}): {error_msg}",
                    exc_info=True,
                )
                last_error = error_msg

                # 记录埋点
                if self.tracking:
                    self.tracking.track_inference(
                        model=self.model_name,
                        user_input=user_input,
                        response="",
                        latency_ms=(time.time() - start_time) * 1000,
                        success=False,
                        error_code=ErrorCode.E404.value,
                    )

                if attempt < self.max_retries:
                    time.sleep(0.1 * (attempt + 1))  # 指数退避
                    continue

        # 所有重试都失败
        logger.error(f"[{self.model_name}] 推理最终失败: {last_error}")

        return create_error_response(ErrorCode.E203, last_error or "推理失败")

    def _validate_input(self, user_input: str) -> Dict[str, Any]:
        """
        验证输入

        Args:
            user_input: 用户输入

        Returns:
            Dict[str, Any]: 验证结果
        """
        if not user_input or not isinstance(user_input, str):
            return create_error_response(
                ErrorCode.E401, "输入为空或格式错误"
            )

        if len(user_input) > 10000:  # 限制输入长度
            return create_error_response(
                ErrorCode.E401, f"输入过长（>{10000}字符）"
            )

        return create_success_response()

    def _execute_inference(
        self,
        user_input: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        执行推理（内部方法）

        Args:
            user_input: 用户输入
            context: 上下文信息

        Returns:
            Dict[str, Any]: 推理结果

        Raises:
            TimeoutError: 如果推理超时
            Exception: 其他推理错误
        """
        # 使用超时机制（简化版，实际可以使用 signal 或 threading）
        start_time = time.time()

        # 调用模型
        result = self.model_callable(user_input)

        # 检查超时
        elapsed = time.time() - start_time
        if elapsed > self.timeout_seconds:
            raise TimeoutError(f"推理超时: {elapsed:.2f}秒 > {self.timeout_seconds}秒")

        return result


def wrap_inference(
    model_name: str,
    tracking: Optional[TrackingSystem] = None,
    timeout_seconds: float = 30.0,
):
    """
    装饰器：将模型函数包装为推理封装器

    Args:
        model_name: 模型名称
        tracking: 埋点系统实例
        timeout_seconds: 超时时间

    Returns:
        Callable: 装饰后的函数
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Dict[str, Any]:
            # 创建临时封装器
            wrapper_instance = InferenceWrapper(
                model_name=model_name,
                model_callable=lambda text: func(text, *args, **kwargs),
                tracking=tracking,
                timeout_seconds=timeout_seconds,
            )

            # 提取 user_input（假设是第一个参数）
            user_input = args[0] if args else kwargs.get("text", "")
            return wrapper_instance.infer(user_input)

        return wrapper

    return decorator













