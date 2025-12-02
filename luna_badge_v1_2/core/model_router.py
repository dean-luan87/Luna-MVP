"""
Model Router (v1.3.0) - 完整版本（含 trace_id 全链路埋点）

模型路由器（Model Router，含埋点）

Luna 1.3.0 版本采用双模型协同架构：
- L1 → 小模型（0.5B / 1.5B）：设备侧/边缘执行，快速、离线、稳定
- L2 → 主模型（3B）：近端服务器/主服务执行，负责复杂语义

模型路由器（Router）是两者之间的调度大脑，负责决定：
"当前输入应该由 L1 处理，还是交给 L2？"

设计原则：
1. 安全优先：危险情况强制用 L1（延迟最小、稳定性最高）
2. 语义分层：简单导航用 L1，复杂语义用 L2
3. 降级原则：L2 异常时自动回退到 L1
"""

import logging
import time
import uuid
from typing import Dict, Any, Optional, Callable

from .tracking import TrackingSystem, EventType, track_event, track_error
from .error_codes import ErrorCode

logger = logging.getLogger(__name__)


class ModelRouter:
    """
    模型路由器（Model Router）

    负责在 L1 和 L2 模型之间进行智能路由
    支持 trace_id 全链路追踪

    路由规则：
    1. 安全优先：critical_flag 或 vision_alert → 强制 L1
    2. 简单导航意图 → L1
    3. 复杂语义意图 → L2
    4. L2 失败 → 降级到 L1
    """

    # 简单导航类意图集合
    SIMPLE_INTENTS = ["simple_nav", "orientation", "confirm", "yes_no"]

    def __init__(
        self,
        l1_model: Optional[Callable] = None,
        l2_model: Optional[Callable] = None,
        tracking: Optional[TrackingSystem] = None,
        auto_load: bool = False,
        l1_model_size: str = "0.5B",
        l2_model_size: str = "3B",
    ):
        """
        初始化模型路由器

        Args:
            l1_model: L1 模型的可调用对象（函数），如果为 None 且 auto_load=True 则自动加载
            l2_model: L2 模型的可调用对象（函数），如果为 None 且 auto_load=True 则自动加载
            tracking: 埋点系统实例（可选）
            auto_load: 是否自动加载模型
            l1_model_size: L1 模型大小（仅 auto_load=True 时有效）
            l2_model_size: L2 模型大小（仅 auto_load=True 时有效）
        """
        self.tracking = tracking
        self.loader = None

        # 自动加载模型
        if auto_load:
            logger.info("🚀 启用自动加载模型模式")
            from .qwen_loader import QwenModelLoader
            self.loader = QwenModelLoader(tracking=tracking)
            
            # 加载 L1
            if l1_model is None:
                logger.info(f"正在自动加载 L1 模型 ({l1_model_size})...")
                if self.loader.load_l1(model_size=l1_model_size):
                    l1_model = self.loader.get_l1_callable()
                else:
                    logger.error("❌ L1 模型自动加载失败")
            
            # 加载 L2
            if l2_model is None:
                logger.info(f"正在自动加载 L2 模型 ({l2_model_size})...")
                if self.loader.load_l2(model_size=l2_model_size):
                    l2_model = self.loader.get_l2_callable()
                else:
                    logger.warning("⚠️ L2 模型自动加载失败，将只能使用 L1")

        self.l1 = l1_model
        self.l2 = l2_model

        if self.l1 is None:
            logger.warning("⚠️ L1 模型未加载，路由功能可能受限")
        if self.l2 is None:
            logger.warning("⚠️ L2 模型未加载，将只能使用 L1")

        logger.info("✅ 模型路由器初始化完成")

    def _handle_task_chain(self, task_manager, trace_id, text, context, result):
        """
        处理任务链（辅助方法，避免重复代码）

        Args:
            task_manager: TaskChainManager 实例
            trace_id: 追踪ID
            text: 用户输入
            context: 上下文
            result: Router 返回结果
        """
        if task_manager is not None:
            try:
                task_manager.handle_router_output(
                    trace_id=trace_id,
                    user_text=text,
                    context=context or {},
                    router_result=result,
                )
            except Exception as e:
                # 任务链错误不影响主流程，只记录
                logger.error(f"TaskChainManager 处理失败: {e}", exc_info=True)
                track_error(
                    phase="task_chain",
                    error_code=ErrorCode.E600.value,
                    error_message=f"TaskChainManager handle_router_output error: {str(e)}",
                    payload={
                        "trace_id": trace_id,
                        "input_text": text,
                    },
                    tracking=self.tracking,
                )

    # -----------------------------------------
    # 主入口：Router 决策（含 trace_id 全链路埋点）
    # -----------------------------------------

    def route(
        self,
        text: str,
        context: Optional[Dict[str, Any]] = None,
        task_manager: Optional[Any] = None,
    ) -> Dict[str, Any]:
        """
        路由主入口：决定使用 L1 还是 L2 处理输入

        Args:
            text: 用户输入的文本
            context: 上下文信息，包含：
                - critical_flag: bool, 系统级危险标识
                - vision_alert: bool, 视觉模型触发的实时危险
                - scene_type: str, 场景类型（"street"/"hospital"/"traffic"等）
                - task_state: str, 任务状态（"navigating"/"paused"/"idle"）
                - user_confused: bool, 用户是否困惑

        Returns:
            Dict[str, Any]: 路由结果，包含：
                - model: str, "L1" 或 "L2"
                - response: dict, 模型响应
                - reason: str, 路由原因
                - intent: str, 意图分类（如果是 L1）
                - trace_id: str, 追踪ID
        """
        if context is None:
            context = {}

        # 生成 trace_id
        trace_id = uuid.uuid4().hex[:12]
        route_start_time = time.time()

        try:
            # 记录 route_start
            track_event(
                phase="router",
                event_name="route_start",
                payload={
                    "trace_id": trace_id,
                    "text": text,
                    "context": context,
                },
                tracking=self.tracking,
            )

            # ① 强制危险场景：只用 L1
            if context.get("critical_flag") or context.get("vision_alert"):
                logger.info("🚨 危险场景检测，强制使用 L1")
                
                l1_start = time.time()
                result = self._call_L1(text, reason="critical", trace_id=trace_id)
                l1_latency = (time.time() - l1_start) * 1000
                
                # 记录 L1 推理
                if "error" not in result:
                    track_event(
                        phase="router",
                        event_name="l1_inference",
                        payload={
                            "trace_id": trace_id,
                            "intent": result.get("intent"),
                            "confidence": result.get("confidence"),
                            "latency": l1_latency,
                            "model": "L1",
                        },
                        tracking=self.tracking,
                    )
                
                # 记录路由决策
                track_event(
                    phase="router",
                    event_name="route_decision",
                    payload={
                        "trace_id": trace_id,
                        "decision": "L1",
                        "reason": "critical",
                    },
                    tracking=self.tracking,
                )
                
                # 记录最终输出
                final_answer = result.get("response", {}).get("text", "") if isinstance(result.get("response"), dict) else ""
                track_event(
                    phase="router",
                    event_name="route_output",
                    payload={
                        "trace_id": trace_id,
                        "final_answer": final_answer,
                    },
                    tracking=self.tracking,
                )
                
                result["trace_id"] = trace_id
                # 处理任务链
                self._handle_task_chain(task_manager, trace_id, text, context, result)
                return result

            # ② 使用 L1 做一次意图分类
            if self.l1 is None:
                logger.warning("L1 模型不可用，直接尝试 L2")
                if self.l2 is None:
                    error_result = {
                        "model": "ERROR",
                        "error": "L1 和 L2 模型都不可用",
                        "reason": "no_model",
                        "trace_id": trace_id,
                    }
                    track_error(
                        phase="router",
                        error_code=ErrorCode.E304.value,
                        error_message="L1 和 L2 模型都不可用",
                        payload={
                            "trace_id": trace_id,
                            "input_text": text,
                        },
                        tracking=self.tracking,
                    )
                    # 处理任务链
                    self._handle_task_chain(task_manager, trace_id, text, context, error_result)
                    return error_result
                
                fallback_l2_result = self._call_L2(text, reason="fallback_no_l1", trace_id=trace_id)
                fallback_l2_result["trace_id"] = trace_id
                # 处理任务链
                self._handle_task_chain(task_manager, trace_id, text, context, fallback_l2_result)
                return fallback_l2_result

            # 使用 L1 做意图分类
            l1_classify_start = time.time()
            l1_intent_result = self._call_L1(text, reason="intent_classify", trace_id=trace_id)
            l1_classify_latency = (time.time() - l1_classify_start) * 1000
            
            # 如果 L1 调用失败，尝试 L2
            if "error" in l1_intent_result:
                logger.warning(f"L1 意图分类失败，尝试 L2: {l1_intent_result.get('error')}")
                if self.l2 is not None:
                    fallback_l2_result = self._call_L2(text, reason="fallback_l1_error", trace_id=trace_id)
                    fallback_l2_result["trace_id"] = trace_id
                    # 处理任务链
                    self._handle_task_chain(task_manager, trace_id, text, context, fallback_l2_result)
                    return fallback_l2_result
                else:
                    l1_intent_result["trace_id"] = trace_id
                    # 处理任务链
                    self._handle_task_chain(task_manager, trace_id, text, context, l1_intent_result)
                    return l1_intent_result

            # 记录 L1 意图分类结果
            track_event(
                phase="router",
                event_name="l1_inference",
                payload={
                    "trace_id": trace_id,
                    "intent": l1_intent_result.get("intent"),
                    "confidence": l1_intent_result.get("confidence"),
                    "latency": l1_classify_latency,
                    "model": "L1",
                    "purpose": "intent_classify",
                },
                tracking=self.tracking,
            )

            intent = l1_intent_result.get("intent", "unknown")

            # ③ 简单导航类意图 → L1
            if intent in self.SIMPLE_INTENTS:
                logger.info(f"检测到简单导航意图: {intent}，使用 L1")
                
                l1_start = time.time()
                result = self._call_L1(text, reason="simple_nav", trace_id=trace_id)
                l1_latency = (time.time() - l1_start) * 1000
                
                # 记录 L1 推理
                if "error" not in result:
                    track_event(
                        phase="router",
                        event_name="l1_inference",
                        payload={
                            "trace_id": trace_id,
                            "intent": result.get("intent"),
                            "confidence": result.get("confidence"),
                            "latency": l1_latency,
                            "model": "L1",
                        },
                        tracking=self.tracking,
                    )
                
                # 记录路由决策
                track_event(
                    phase="router",
                    event_name="route_decision",
                    payload={
                        "trace_id": trace_id,
                        "decision": "L1",
                        "reason": "simple_nav",
                        "intent": intent,
                    },
                    tracking=self.tracking,
                )
                
                # 记录最终输出
                final_answer = result.get("response", {}).get("text", "") if isinstance(result.get("response"), dict) else ""
                track_event(
                    phase="router",
                    event_name="route_output",
                    payload={
                        "trace_id": trace_id,
                        "final_answer": final_answer,
                    },
                    tracking=self.tracking,
                )
                
                result["trace_id"] = trace_id
                # 处理任务链
                self._handle_task_chain(task_manager, trace_id, text, context, result)
                return result

            # ④ 否则交给 L2（主模型）
            if self.l2 is None:
                logger.warning("L2 模型不可用，降级使用 L1")
                result = self._call_L1(text, reason="fallback_no_l2", trace_id=trace_id)
                
                # 记录降级
                track_event(
                    phase="router",
                    event_name="route_decision",
                    payload={
                        "trace_id": trace_id,
                        "decision": "L1",
                        "reason": "fallback_no_l2",
                    },
                    tracking=self.tracking,
                )
                
                result["trace_id"] = trace_id
                # 处理任务链
                self._handle_task_chain(task_manager, trace_id, text, context, result)
                return result

            # 调用 L2
            l2_start = time.time()
            l2_result = self._call_L2(text, reason="complex_semantic", trace_id=trace_id)
            l2_latency = (time.time() - l2_start) * 1000

            # ⑤ 如果 L2 出错 → 降级到 L1
            if "error" in l2_result:
                logger.warning(f"L2 调用失败，降级到 L1: {l2_result.get('error')}")
                
                # 记录 L2 错误
                track_event(
                    phase="router",
                    event_name="l2_inference",
                    payload={
                        "trace_id": trace_id,
                        "latency": l2_latency,
                        "model": "L2",
                        "error": l2_result.get("error"),
                    },
                    tracking=self.tracking,
                )
                
                # 记录降级
                track_event(
                    phase="router",
                    event_name="route_decision",
                    payload={
                        "trace_id": trace_id,
                        "decision": "L1",
                        "reason": "fallback_L2_error",
                    },
                    tracking=self.tracking,
                )
                
                fallback_result = self._call_L1(text, reason="fallback_L2_error", trace_id=trace_id)
                fallback_result["trace_id"] = trace_id
                # 处理任务链
                self._handle_task_chain(task_manager, trace_id, text, context, fallback_result)
                return fallback_result

            # 记录 L2 推理成功
            track_event(
                phase="router",
                event_name="l2_inference",
                payload={
                    "trace_id": trace_id,
                    "latency": l2_latency,
                    "model": "L2",
                    "answer": l2_result.get("response", {}).get("text", "") if isinstance(l2_result.get("response"), dict) else "",
                },
                tracking=self.tracking,
            )

            # 记录路由决策
            track_event(
                phase="router",
                event_name="route_decision",
                payload={
                    "trace_id": trace_id,
                    "decision": "L2",
                    "reason": "complex_semantic",
                    "intent": intent,
                },
                tracking=self.tracking,
            )

            # 记录最终输出
            final_answer = l2_result.get("response", {}).get("text", "") if isinstance(l2_result.get("response"), dict) else ""
            track_event(
                phase="router",
                event_name="route_output",
                payload={
                    "trace_id": trace_id,
                    "final_answer": final_answer,
                },
                tracking=self.tracking,
            )

            l2_result["trace_id"] = trace_id
            # 处理任务链
            self._handle_task_chain(task_manager, trace_id, text, context, l2_result)
            return l2_result

        except Exception as e:
            logger.error(f"Router 运行时异常: {e}", exc_info=True)
            track_error(
                phase="router",
                error_code=ErrorCode.E301.value,
                error_message=f"router runtime error: {str(e)}",
                payload={
                    "trace_id": trace_id,
                    "input_text": text,
                },
                tracking=self.tracking,
            )
            error_result = {
                "model": "ERROR",
                "error": str(e),
                "reason": "exception",
                "trace_id": trace_id,
            }
            # 处理任务链（即使出错也尝试记录）
            self._handle_task_chain(task_manager, trace_id, text, context, error_result)
            return error_result

    # -----------------------------------------
    # L1 调用
    # -----------------------------------------

    def _call_L1(self, text: str, reason: Optional[str] = None, trace_id: Optional[str] = None) -> Dict[str, Any]:
        """
        调用 L1 模型

        Args:
            text: 用户输入文本
            reason: 调用原因
            trace_id: 追踪ID（可选）

        Returns:
            Dict[str, Any]: L1 模型响应
        """
        if self.l1 is None:
            return {
                "model": "L1",
                "error": "L1 模型未加载",
                "reason": reason or "error"
            }

        try:
            result = self.l1(text)

            if "error" in result:
                return {
                    "model": "L1",
                    "error": result["error"],
                    "reason": reason or "error"
                }

            return {
                "model": "L1",
                "response": result,
                "intent": result.get("intent", "unknown"),
                "confidence": result.get("confidence", 0.5),
                "reason": reason or "normal"
            }

        except Exception as e:
            logger.error(f"L1 模型调用异常: {e}")
            return {
                "model": "L1",
                "error": str(e),
                "reason": reason or "exception"
            }

    # -----------------------------------------
    # L2 调用
    # -----------------------------------------

    def _call_L2(self, text: str, reason: Optional[str] = None, trace_id: Optional[str] = None) -> Dict[str, Any]:
        """
        调用 L2 模型

        Args:
            text: 用户输入文本
            reason: 调用原因
            trace_id: 追踪ID（可选）

        Returns:
            Dict[str, Any]: L2 模型响应
        """
        if self.l2 is None:
            return {
                "model": "L2",
                "error": "L2 模型未加载",
                "reason": reason or "error"
            }

        try:
            result = self.l2(text)

            if "error" in result:
                return {
                    "model": "L2",
                    "error": result["error"],
                    "reason": reason or "error"
                }

            return {
                "model": "L2",
                "response": result,
                "reason": reason or "normal"
            }

        except Exception as e:
            logger.error(f"L2 模型调用异常: {e}")
            return {
                "model": "L2",
                "error": str(e),
                "reason": reason or "exception"
            }

