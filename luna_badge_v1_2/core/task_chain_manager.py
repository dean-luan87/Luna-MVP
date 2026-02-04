"""
Task Chain Manager (v1.3.0)

任务链管理器

负责根据 Router 的输出更新和管理任务链
支持任务链的创建、更新和状态追踪
"""

import logging
import time
from typing import Optional, Dict, Any

# 修复导入路径
try:
    from .task.task_chain import TaskChain
    # TaskNode 和 new_task_chain 可能不存在，提供占位
    TaskNode = None
    def new_task_chain():
        return TaskChain("default")
except ImportError:
    # 如果导入失败，提供占位类
    class TaskChain:
        def __init__(self, name="default"):
            self.name = name
    TaskNode = None
    def new_task_chain():
        return TaskChain("default")
from .tracking import track_event, track_error
from .error_codes import ErrorCode

logger = logging.getLogger(__name__)


class TaskChainManager:
    """
    任务链管理器

    负责管理当前活跃的任务链，根据 Router 的输出更新任务链状态
    """

    def __init__(self):
        """初始化任务链管理器"""
        self.current_chain: Optional[TaskChain] = None
        logger.info("任务链管理器初始化完成")

    # -----------------------------------
    # 对外主入口：由 Router 调用
    # -----------------------------------

    def handle_router_output(
        self,
        trace_id: str,
        user_text: str,
        context: Dict[str, Any],
        router_result: Dict[str, Any]
    ) -> None:
        """
        根据 Router 的决策结果，更新任务链

        Args:
            trace_id: 这次对话链路 ID
            user_text: 用户输入
            context: 当次上下文（scene_type、task_state 等）
            router_result: Router.route() 返回的 dict，包含 model, intent, reason 等
        """
        try:
            intent = router_result.get("intent", "unknown")  # L1 给出的意图
            model = router_result.get("model", "UNKNOWN")
            reason = router_result.get("reason", "unknown")

            scene_type = context.get("scene_type", "navigation")

            # 将 trace_id 绑定到当前任务链
            chain = self._get_or_create_chain(scene_type)
            chain.add_trace_id(trace_id)

            # 根据 intent 更新任务结构
            if intent in ["simple_nav", "orientation"]:
                self._update_for_simple_nav(chain, user_text, trace_id, model, reason)
            elif intent in ["hospital", "multi_step", "complex_semantic"]:
                self._update_for_complex_task(chain, user_text, trace_id, model, reason, context)
            else:
                # chat / unknown 等，只记录，不改变结构
                self._log_chain_event(
                    chain, trace_id, "chain_ignore",
                    payload={
                        "intent": intent,
                        "reason": reason,
                        "user_text": user_text,
                    }
                )

        except Exception as e:
            logger.error(f"处理 Router 输出失败: {e}", exc_info=True)
            track_error(
                phase="task_chain",
                error_code=ErrorCode.E600.value,
                error_message=f"TaskChainManager handle_router_output error: {str(e)}",
                payload={
                    "trace_id": trace_id,
                    "user_text": user_text,
                },
                tracking=None,
            )

    # -----------------------------------
    # 内部：获取或创建任务链
    # -----------------------------------

    def _get_or_create_chain(self, scene_type: str) -> TaskChain:
        """
        获取当前任务链，如果不存在或已结束则创建新的

        Args:
            scene_type: 场景类型

        Returns:
            TaskChain: 当前任务链
        """
        if self.current_chain is None or self.current_chain.status in ("completed", "cancelled"):
            self.current_chain = new_task_chain(scene_type)
            self._log_chain_event(
                self.current_chain,
                trace_id="",
                event_name="chain_created",
                payload={"scene_type": scene_type}
            )
            logger.info(f"创建新任务链: {self.current_chain.chain_id}, scene_type={scene_type}")

        return self.current_chain

    # -----------------------------------
    # 更新：简单导航场景（不重建任务，只作为当前节点细化）
    # -----------------------------------

    def _update_for_simple_nav(
        self,
        chain: TaskChain,
        user_text: str,
        trace_id: str,
        model: str,
        reason: str
    ):
        """
        更新简单导航任务

        Args:
            chain: 当前任务链
            user_text: 用户输入
            trace_id: 追踪ID
            model: 使用的模型（L1/L2）
            reason: 路由原因
        """
        node = chain.current_node()

        if node is None:
            # 没有节点，则创建一个基础导航节点
            node = TaskNode(
                node_id=f"node_nav_{int(time.time())}",
                node_type="NAV_STEP",
                status="active",
                description=f"导航：{user_text}",
                extras={
                    "router_model": model,
                    "router_reason": reason,
                }
            )
            chain.add_node(node)
        else:
            # 已有节点，则更新描述和状态
            if node.node_type == "NAV_STEP":
                node.description = f"导航：{user_text}"
                if node.status == "pending":
                    node.update_status("active")
                node.extras.update({
                    "router_model": model,
                    "router_reason": reason,
                })

        self._log_chain_event(
            chain, trace_id, "chain_update_nav",
            payload={
                "user_text": user_text,
                "model": model,
                "reason": reason,
                "node_id": node.node_id,
            }
        )

    # -----------------------------------
    # 更新：复杂任务（医院、多步骤）
    # -----------------------------------

    def _update_for_complex_task(
        self,
        chain: TaskChain,
        user_text: str,
        trace_id: str,
        model: str,
        reason: str,
        context: Dict[str, Any]
    ):
        """
        更新复杂任务

        Args:
            chain: 当前任务链
            user_text: 用户输入
            trace_id: 追踪ID
            model: 使用的模型（L1/L2）
            reason: 路由原因
            context: 上下文信息
        """
        # 判断任务类型
        scene_type = context.get("scene_type", "navigation")
        
        # 根据场景类型确定节点类型
        if "hospital" in scene_type.lower() or "医院" in user_text:
            node_type = "HOSPITAL_STEP"
        elif "711" in user_text or "shop" in user_text.lower() or "商店" in user_text:
            node_type = "SHOP_STEP"
        elif "厕所" in user_text or "toilet" in user_text.lower():
            node_type = "TOILET_STEP"
        else:
            node_type = "COMPLEX_STEP"

        # 追加一个新的 TaskNode
        node = TaskNode(
            node_id=f"node_task_{int(time.time())}",
            node_type=node_type,
            status="active",
            description=f"复杂任务：{user_text}",
            extras={
                "router_model": model,
                "router_reason": reason,
                "scene_type": scene_type,
            }
        )

        chain.add_node(node)

        self._log_chain_event(
            chain, trace_id, "chain_update_complex",
            payload={
                "user_text": user_text,
                "model": model,
                "reason": reason,
                "node_id": node.node_id,
                "node_type": node_type,
            }
        )

    # -----------------------------------
    # 埋点封装
    # -----------------------------------

    def _log_chain_event(
        self,
        chain: TaskChain,
        trace_id: str,
        event_name: str,
        payload: Dict[str, Any]
    ):
        """
        记录任务链事件到埋点系统

        Args:
            chain: 任务链
            trace_id: 追踪ID
            event_name: 事件名称
            payload: 额外数据
        """
        data = {
            "trace_id": trace_id,
            "chain_id": chain.chain_id,
            "scene_type": chain.scene_type,
            "chain_status": chain.status,
            "current_index": chain.current_index,
            "node_count": len(chain.nodes),
        }
        data.update(payload)

        track_event(
            phase="task_chain",
            event_name=event_name,
            payload=data,
            tracking=None,  # 使用全局便捷函数，不需要 tracking 实例
        )

    # -----------------------------------
    # 对外查询接口
    # -----------------------------------

    def get_current_chain_snapshot(self) -> Optional[Dict[str, Any]]:
        """
        获取当前任务链的快照（用于调试/接口）

        Returns:
            Optional[Dict[str, Any]]: 任务链的字典表示，如果不存在则返回 None
        """
        if self.current_chain is None:
            return None
        return self.current_chain.to_dict()

    def get_current_chain(self) -> Optional[TaskChain]:
        """
        获取当前任务链对象

        Returns:
            Optional[TaskChain]: 当前任务链，如果不存在则返回 None
        """
        return self.current_chain

    def complete_current_node(self):
        """
        完成当前节点，推进到下一个节点

        用于显式标记节点完成
        """
        if self.current_chain:
            self.current_chain.advance()
            logger.info(f"节点推进，当前索引: {self.current_chain.current_index}")

    def pause_chain(self):
        """暂停当前任务链"""
        if self.current_chain:
            self.current_chain.pause()
            logger.info(f"任务链已暂停: {self.current_chain.chain_id}")

    def resume_chain(self):
        """恢复当前任务链"""
        if self.current_chain:
            self.current_chain.resume()
            logger.info(f"任务链已恢复: {self.current_chain.chain_id}")

    def cancel_chain(self):
        """取消当前任务链"""
        if self.current_chain:
            self.current_chain.cancel()
            logger.info(f"任务链已取消: {self.current_chain.chain_id}")







