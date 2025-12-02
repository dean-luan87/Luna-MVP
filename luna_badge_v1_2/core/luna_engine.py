"""
Luna Engine (v1.3.0)

对外统一引擎接口（SDK）

将 L1/L2 模型、Router、TaskChain、Tracking 等所有模块封装成一个统一的入口
上层模块（语音模块、导航模块、硬件逻辑）只需要调用这一个接口
"""

import logging
from typing import Dict, Any, Optional

from .config import CONFIG
from .tracking import TrackingSystem, track_event, track_error
from .error_codes import ErrorCode
from .model_router import ModelRouter
from .task_chain_manager import TaskChainManager

logger = logging.getLogger(__name__)


class LunaEngine:
    """
    Luna 引擎

    对外统一的接口，封装所有底层模块（L1/L2、Router、TaskChain、Tracking）
    """

    def __init__(
        self,
        auto_load: bool = True,
        l1_model_size: Optional[str] = None,
        l2_model_size: Optional[str] = None,
        tracking: Optional[TrackingSystem] = None,
    ):
        """
        初始化 Luna 引擎

        Args:
            auto_load: 是否自动加载模型
            l1_model_size: L1 模型大小（"0.5B" 或 "1.5B"），如果为 None 则从配置读取
            l2_model_size: L2 模型大小（"3B"），如果为 None 则从配置读取
            tracking: 埋点系统实例（可选，如果为 None 则自动创建）
        """
        # 从配置读取模型设置
        models_cfg = CONFIG.models
        
        # 使用配置中的模型名称（通过模型大小映射）
        if l1_model_size is None:
            # 从配置读取模型名称，然后映射回大小
            l1_model_name = models_cfg.get("l1_model_name", "Qwen/Qwen2.5-0.5B-Instruct")
            if "0.5B" in l1_model_name:
                l1_model_size = "0.5B"
            elif "1.5B" in l1_model_name:
                l1_model_size = "1.5B"
            else:
                l1_model_size = "0.5B"  # 默认
        
        if l2_model_size is None:
            l2_model_name = models_cfg.get("l2_model_name", "Qwen/Qwen2.5-3B-Instruct")
            if "3B" in l2_model_name:
                l2_model_size = "3B"
            else:
                l2_model_size = "3B"  # 默认

        # 初始化埋点系统
        if tracking is None:
            tracking = TrackingSystem(log_dir="logs/tracking")
            tracking.start_session()
        self.tracking = tracking

        # 记录引擎初始化开始
        track_event(
            phase="engine",
            event_name="engine_init_start",
            payload={
                "l1_model_size": l1_model_size,
                "l2_model_size": l2_model_size,
                "config_env": CONFIG.env,
            },
            tracking=self.tracking,
        )

        try:
            # 从配置读取功能开关
            enable_l1 = models_cfg.get("enable_l1", True)
            enable_l2 = models_cfg.get("enable_l2", True)
            enable_task_chain = CONFIG.features.get("enable_task_chain", True)

            # 初始化 Router（自动加载模型）
            logger.info(f"🚀 初始化 Luna Engine (env={CONFIG.env})...")
            
            # 只有在启用时才自动加载
            actual_auto_load = auto_load and (enable_l1 or enable_l2)
            
            self.router = ModelRouter(
                auto_load=actual_auto_load,
                tracking=self.tracking,
                l1_model_size=l1_model_size if enable_l1 else None,
                l2_model_size=l2_model_size if enable_l2 else None,
            )

            # 根据配置决定是否初始化 TaskChainManager
            if enable_task_chain:
                self.task_manager = TaskChainManager()
                logger.info("✅ TaskChain 已启用")
            else:
                self.task_manager = None
                logger.info("⚠️ TaskChain 已禁用")

            logger.info("✅ Luna Engine 初始化成功")

            # 记录引擎初始化成功
            track_event(
                phase="engine",
                event_name="engine_init_success",
                payload={
                    "l1_model_size": l1_model_size,
                    "l2_model_size": l2_model_size,
                },
                tracking=self.tracking,
            )

        except Exception as e:
            logger.error(f"❌ Luna Engine 初始化失败: {e}", exc_info=True)

            # 记录引擎初始化失败
            track_error(
                phase="engine",
                error_code=ErrorCode.E200.value,
                error_message=f"Engine init failed: {str(e)}",
                payload={
                    "l1_model_size": l1_model_size,
                    "l2_model_size": l2_model_size,
                },
                tracking=self.tracking,
            )

            # 抛出异常，让上层处理
            raise

    # -------------------------------------------------
    # 对外主入口：整个 Luna 能力的统一调用接口
    # -------------------------------------------------

    def handle_user_input(
        self,
        user_text: str,
        sensors_context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        上层（语音模块 / 导航模块 / 硬件逻辑）只需要调用这个接口

        Args:
            user_text: ASR 转写后文本
            sensors_context: 传入当前场景信息，包含：
                - scene_type: str, "street" / "hospital" / ...
                - critical_flag: bool, 系统级危险标识
                - vision_alert: bool, 视觉模型触发的实时危险
                - task_state: str, 任务状态（"navigating"/"paused"/"idle"）

        Returns:
            Dict[str, Any]: 统一返回结构，包含：
                - output_text: str, 给 TTS 播报的文本
                - model: str, "L1" 或 "L2"
                - intent: str, 意图分类结果
                - reason: str, 路由原因
                - trace_id: str, 追踪ID
                - chain_snapshot: dict or None, 当前任务链快照（用于调试/上报）
                - raw: dict, 完整原始结构
        """
        if sensors_context is None:
            sensors_context = {}

        # 引擎级埋点：请求开始
        track_event(
            phase="engine",
            event_name="handle_input_start",
            payload={
                "user_text": user_text,
                "context": sensors_context,
            },
            tracking=self.tracking,
        )

        try:
            # 1. 调用 Router（根据配置决定是否传入 TaskChainManager）
            router_result = self.router.route(
                text=user_text,
                context=sensors_context,
                task_manager=self.task_manager if self.task_manager else None,
            )

            # 2. 获取当前任务链快照（如果启用）
            chain_snapshot = self.task_manager.get_current_chain_snapshot() if self.task_manager else None

            # 3. 提取输出文本
            output_text = self._extract_output_text(router_result)

            # 4. 封装统一返回结构
            result = {
                "output_text": output_text,
                "model": router_result.get("model"),
                "intent": router_result.get("intent", "unknown"),
                "reason": router_result.get("reason", "unknown"),
                "trace_id": router_result.get("trace_id"),
                "chain_snapshot": chain_snapshot,
                "raw": router_result,
            }

            # 引擎级埋点：请求结束
            track_event(
                phase="engine",
                event_name="handle_input_success",
                payload={
                    "trace_id": result.get("trace_id"),
                    "model": result.get("model"),
                    "intent": result.get("intent"),
                    "reason": result.get("reason"),
                },
                tracking=self.tracking,
            )

            return result

        except Exception as e:
            logger.error(f"❌ Engine handle_user_input 错误: {e}", exc_info=True)

            # 引擎级错误
            track_error(
                phase="engine",
                error_code=ErrorCode.E301.value,
                error_message=f"Engine handle_user_input error: {str(e)}",
                payload={
                    "user_text": user_text,
                    "context": sensors_context,
                },
                tracking=self.tracking,
            )

            # 出错时返回一个安全默认结构，避免硬件崩溃
            return {
                "output_text": "",
                "model": None,
                "intent": None,
                "reason": "engine_error",
                "trace_id": None,
                "chain_snapshot": self.task_manager.get_current_chain_snapshot() if self.task_manager else None,
                "raw": {
                    "error": str(e),
                },
            }

    # -------------------------------------------------
    # 内部工具：从 router_result 抽取最终要说的话
    # -------------------------------------------------

    def _extract_output_text(self, router_result: Dict[str, Any]) -> str:
        """
        不同模型可能返回结构不同，这里统一转换为 output_text

        - L1: 可能只返回结构化指令 → 需要转成自然语言提示
        - L2: 直接是自然语言回答

        Args:
            router_result: Router 返回的结果字典

        Returns:
            str: 给 TTS 播报的文本
        """
        model = router_result.get("model")
        resp = router_result.get("response")

        if model == "L1":
            # 对 L1 的结构化结果做一个简单的 humanization
            intent = router_result.get("intent", "unknown")

            if intent == "simple_nav":
                # 真实情况下这里可以基于 extras 生成"请往前走几步"之类的语句
                return "好的，我继续为你导航。"
            elif intent == "orientation":
                return "我在，路没问题，你可以继续往前走。"
            elif intent == "confirm":
                return "好的，我明白了。"
            elif intent == "yes_no":
                return "收到。"
            else:
                # 尝试从 response 中提取文本
                if isinstance(resp, dict):
                    text = resp.get("text", "")
                    if text:
                        return text
                return "我已收到你的指令。"

        elif model == "L2":
            # L2 的 resp 通常是 {"text": "..."} 这样的形式
            if isinstance(resp, dict):
                return resp.get("text", "")
            elif isinstance(resp, str):
                return resp
            else:
                return str(resp or "")

        # 如果有错误，返回空字符串
        if router_result.get("error"):
            return ""

        # 默认兜底
        return ""

