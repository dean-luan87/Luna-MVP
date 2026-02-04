# -*- coding: utf-8 -*-
"""
Luna Badge v1.4.3 - DecisionCore 实现

决策核心模块，负责根据事件和上下文生成决策输出。
"""

import time
from typing import Dict, Any, Optional
from core.decision_output import DecisionOutput
from core.decision_actions import DecisionAction
from core.intent_schema import ParsedIntent
from core.events import EventType
from decision_logging.decision_logger import log_decision


class DecisionCore:
    """
    决策核心
    
    职责：
    - 根据事件类型和上下文生成决策输出
    - 不直接修改 TaskChain，只返回决策结果
    - 由外部根据 DecisionOutput 调用 TaskChainManager.apply_decision
    """
    
    def __init__(self):
        """初始化决策核心"""
        pass
    
    def handle_event(
        self,
        event_type: EventType,
        payload: Dict[str, Any],
        context: Dict[str, Any]
    ) -> DecisionOutput:
        """
        处理事件并生成决策
        
        Args:
            event_type: 事件类型
            payload: 事件负载
            context: 上下文信息
        
        Returns:
            DecisionOutput: 决策输出
        """
        parsed_intent = None
        decision_output = None
        
        if event_type == EventType.USER_INTENT:
            parsed_intent = payload.get("parsed_intent")
            if isinstance(parsed_intent, dict):
                # 如果传入的是字典，转换为 ParsedIntent
                parsed_intent = ParsedIntent(
                    intent_name=parsed_intent.get("intent_name") or parsed_intent.get("type", "UNKNOWN"),
                    slots=parsed_intent.get("slots", {}),
                    source=parsed_intent.get("source", "inquiry"),
                    need_confirm=parsed_intent.get("need_confirm", False),
                    raw=parsed_intent.get("raw", "")
                )
            decision_output = self.handle_user_intent(parsed_intent, context, payload)
        
        elif event_type == EventType.TASK_NODE_COMPLETE:
            decision_output = self.handle_task_node_complete(payload, context)
        
        elif event_type == EventType.MODEL_STATUS:
            decision_output = self.handle_model_status(payload, context)
        
        elif event_type in [EventType.SYSTEM_ALERT, EventType.USER_INACTIVE]:
            # 一律 NO_OP + 记录日志
            decision_output = DecisionOutput(
                action=DecisionAction.NO_OP,
                params={},
                narration="我保持当前任务不变。"
            )
        
        else:
            # 未知事件类型，返回 NO_OP
            decision_output = DecisionOutput(
                action=DecisionAction.NO_OP,
                params={},
                narration=""
            )
        
        # 记录日志
        task_context = context.get("task_context", {})
        log_decision(
            event_type=event_type.value,
            parsed_intent=parsed_intent,
            decision_output=decision_output,
            task_context=task_context
        )
        
        return decision_output
    
    def handle_user_intent(
        self,
        parsed_intent: Optional[ParsedIntent],
        context: Dict[str, Any],
        payload: Optional[Dict[str, Any]] = None
    ) -> DecisionOutput:
        """
        处理用户意图
        
        Args:
            parsed_intent: 解析后的用户意图
            context: 上下文信息
        
        Returns:
            DecisionOutput: 决策输出
        """
        if not parsed_intent:
            return DecisionOutput(
                action=DecisionAction.NO_OP,
                params={},
                narration="我保持当前任务不变。"
            )
        
        intent_name = parsed_intent.intent_name
        task_context = context.get("task_context", {})
        task_id = task_context.get("task_id", "")
        
        if intent_name == "INSERT_TASK":
            # 如果需要确认，先询问用户
            if parsed_intent.need_confirm:
                return DecisionOutput(
                    action=DecisionAction.ASK_USER,
                    params={
                        "question_type": "confirm_new_intent",
                        "context": {
                            "intent_desc": self._get_intent_description(parsed_intent),
                            "pending_intent": parsed_intent  # 保存待确认的意图
                        }
                    },
                    narration=""
                )
            
            # 不需要确认，直接插入任务
            task_spec = self._build_task_from_slots(parsed_intent.slots)
            return DecisionOutput(
                action=DecisionAction.INSERT_TASK,
                params={
                    "main_task_id": task_id,
                    "insert_task_spec": task_spec,
                    "resume_strategy": "auto"
                },
                narration=self._generate_narration_for_insert_task(parsed_intent.slots)
            )
        
        elif intent_name == "CHANGE_DESTINATION":
            # 如果需要确认，先询问用户
            if parsed_intent.need_confirm:
                return DecisionOutput(
                    action=DecisionAction.ASK_USER,
                    params={
                        "question_type": "confirm_new_intent",
                        "context": {
                            "intent_desc": self._get_intent_description(parsed_intent),
                            "pending_intent": parsed_intent  # 保存待确认的意图
                        }
                    },
                    narration=""
                )
            
            # 不需要确认，直接替换任务
            new_task = self._build_task_from_slots(parsed_intent.slots)
            return DecisionOutput(
                action=DecisionAction.REPLACE_TASK,
                params={
                    "old_task_id": task_id,
                    "new_task_spec": new_task
                },
                narration="明白了，我帮你更改目的地。"
            )
        
        elif intent_name == "RESUME_MAIN_TASK":
            return DecisionOutput(
                action=DecisionAction.CONTINUE_TASK,
                params={
                    "task_id": task_id
                },
                narration="好的，我继续执行之前的任务。"
            )
        
        elif intent_name == "CONFIRM":
            # CONFIRM 需要根据上下文决定是继续任务还是执行特定确认逻辑
            # 检查是否有待确认的意图（从 payload 或 context 中获取）
            # 注意：这里我们需要从上一个 ASK_USER 的 context 中获取 pending_intent
            # 在实际应用中，这应该由上层（如 Orchestrator）管理
            # 这里我们检查 payload 中是否有 pending_intent
            pending_intent = None
            if payload is not None:
                pending_intent = payload.get("pending_intent")
            if not pending_intent:
                # 尝试从 context 中获取
                pending_intent = context.get("pending_intent")
            
            if pending_intent:
                # 如果有待确认的意图，执行该意图
                if isinstance(pending_intent, dict):
                    pending_intent = ParsedIntent(
                        intent_name=pending_intent.get("intent_name", "UNKNOWN"),
                        slots=pending_intent.get("slots", {}),
                        source=pending_intent.get("source", "inquiry"),
                        need_confirm=False,
                        raw=pending_intent.get("raw", "")
                    )
                
                if pending_intent.intent_name == "INSERT_TASK":
                    task_spec = self._build_task_from_slots(pending_intent.slots)
                    return DecisionOutput(
                        action=DecisionAction.INSERT_TASK,
                        params={
                            "main_task_id": task_id,
                            "insert_task_spec": task_spec,
                            "resume_strategy": "auto"
                        },
                        narration=self._generate_narration_for_insert_task(pending_intent.slots)
                    )
                elif pending_intent.intent_name == "CHANGE_DESTINATION":
                    new_task = self._build_task_from_slots(pending_intent.slots)
                    return DecisionOutput(
                        action=DecisionAction.REPLACE_TASK,
                        params={
                            "old_task_id": task_id,
                            "new_task_spec": new_task
                        },
                        narration="明白了，我帮你更改目的地。"
                    )
            
            # 默认：继续任务
            return DecisionOutput(
                action=DecisionAction.CONTINUE_TASK,
                params={
                    "task_id": task_id
                },
                narration="好的，我继续执行之前的任务。"
            )
        
        elif intent_name in ["REJECT", "AMBIGUOUS", "UNKNOWN"]:
            return DecisionOutput(
                action=DecisionAction.NO_OP,
                params={},
                narration="我保持当前任务不变。"
            )
        
        else:
            # 其它未识别意图
            return DecisionOutput(
                action=DecisionAction.NO_OP,
                params={},
                narration="我保持当前任务不变。"
            )
    
    def handle_task_node_complete(
        self,
        payload: Dict[str, Any],
        context: Dict[str, Any]
    ) -> DecisionOutput:
        """
        处理任务节点完成
        
        Args:
            payload: 事件负载
            context: 上下文信息
        
        Returns:
            DecisionOutput: 决策输出
        """
        task_context = context.get("task_context", {})
        task_id = task_context.get("task_id", "")
        active_node = task_context.get("active_node", {})
        
        if not task_id:
            return DecisionOutput(
                action=DecisionAction.NO_OP,
                params={},
                narration=""
            )
        
        # 检查节点是否需要用户确认
        if active_node.get("requires_user_confirmation", False):
            # 根据节点类型决定 question_type
            node_type = active_node.get("type", "default")
            question_type = f"confirm_{node_type}" if node_type != "default" else "confirm_completion"
            
            return DecisionOutput(
                action=DecisionAction.ASK_USER,
                params={
                    "question_type": question_type,
                    "task_id": task_id,
                    "node_id": active_node.get("id", "")
                },
                narration=""
            )
        else:
            # 不需要确认，继续任务
            return DecisionOutput(
                action=DecisionAction.CONTINUE_TASK,
                params={
                    "task_id": task_id
                },
                narration=""
            )
    
    def handle_model_status(
        self,
        payload: Dict[str, Any],
        context: Dict[str, Any]
    ) -> DecisionOutput:
        """
        处理模型状态
        
        Args:
            payload: 事件负载
            context: 上下文信息
        
        Returns:
            DecisionOutput: 决策输出
        """
        model_context = context.get("model_context", {})
        
        # 检查 PlanB 触发条件：主视觉 + 备份均 down
        vision_main = model_context.get("vision_main", "ok")
        vision_fallback = model_context.get("vision_fallback", "ok")
        
        if vision_main == "down" and vision_fallback == "down":
            return DecisionOutput(
                action=DecisionAction.TRIGGER_PLANB,
                params={
                    "context_snapshot": context
                },
                narration=""
            )
        
        # 模型正常，返回 NO_OP
        return DecisionOutput(
            action=DecisionAction.NO_OP,
            params={},
            narration=""
        )
    
    def _build_task_from_slots(self, slots: Dict[str, Any]) -> Dict[str, Any]:
        """
        从 slots 构建任务规格
        
        Args:
            slots: 意图槽位信息
        
        Returns:
            Dict: 任务规格
        """
        task_type = slots.get("task_type", "navigation")
        
        # 根据 task_type 构建不同的任务规格
        if task_type == "toilet":
            return {
                "task_id": f"go_to_toilet_{int(time.time())}",
                "type": "go_to_toilet",
                "target": {"poi_type": "toilet"},
                "priority": 8,
                "nodes": [
                    {"id": "find_toilet", "name": "寻找厕所"},
                    {"id": "toilet_reached", "name": "到达厕所"}
                ],
                "metadata": {
                    "source": "user_request"
                }
            }
        elif task_type == "buy":
            return {
                "task_id": f"buy_item_{int(time.time())}",
                "type": "buy_item",
                "target": {"poi_type": "shop"},
                "priority": 8,
                "nodes": [
                    {"id": "find_shop", "name": "寻找商店"},
                    {"id": "shop_reached", "name": "到达商店"}
                ],
                "metadata": {
                    "source": "user_request"
                }
            }
        else:
            # 默认导航任务
            return {
                "task_id": f"navigation_{int(time.time())}",
                "type": "navigation",
                "target": slots.get("target", {}),
                "priority": 5,
                "nodes": [],
                "metadata": {
                    "source": "user_request"
                }
            }
    
    def _generate_narration_for_insert_task(self, slots: Dict[str, Any]) -> str:
        """
        为插入任务生成播报文案
        
        Args:
            slots: 意图槽位信息
        
        Returns:
            str: 播报文案
        """
        task_type = slots.get("task_type", "")
        
        if task_type == "toilet":
            return "好的，我先带你去厕所。"
        elif task_type == "buy":
            return "好的，我先带你去商店。"
        else:
            return "好的，我先帮你处理这件事。"
    
    def _get_intent_description(self, parsed_intent: ParsedIntent) -> str:
        """
        获取意图描述（用于问句生成）
        
        Args:
            parsed_intent: 解析后的意图
        
        Returns:
            str: 意图描述
        """
        task_type = parsed_intent.slots.get("task_type", "")
        
        if task_type == "toilet":
            return "先去厕所"
        elif task_type == "buy":
            return "先去商店"
        elif parsed_intent.intent_name == "CHANGE_DESTINATION":
            return "更改目的地"
        else:
            return parsed_intent.raw or "这个操作"

