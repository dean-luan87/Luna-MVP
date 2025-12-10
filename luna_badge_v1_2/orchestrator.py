# -*- coding: utf-8 -*-
"""
Luna Badge v1.4.4 - 集成层 Orchestrator

将 Command Layer → Inquiry → DecisionCore → TaskChain 打通，提供统一的集成接口。
"""

from typing import Dict, Any, Optional
from inquiry.inquiry_manager import InquiryManager
from decision.decision_core import DecisionCore
from taskchain.manager import TaskChainManager
from core.events import EventType
from core.intent_schema import ParsedIntent
# v1.4.4: Command Layer 集成
from command_layer.prefix_detector import detect_prefix
from command_layer.non_command_handler import handle_non_command
from command_layer.semantic_normalizer import normalize_command, NormalizedCommand
from command_layer.help_center_stub import handle_help_center
from command_layer.ecs_resolver import resolve_slots, FakeMemoryClient, FakePOIClient
from command_layer.mapping import normalized_to_parsed_intent


class Orchestrator:
    """
    集成层 Orchestrator
    
    职责：
    - 连接 Inquiry、DecisionCore、TaskChain 三个模块
    - 提供统一的集成接口
    - 处理完整的用户输入 → 决策 → 任务执行流程
    """
    
    def __init__(self):
        """初始化集成层"""
        self.inquiry_manager = InquiryManager()
        self.decision_core = DecisionCore()
        self.taskchain = TaskChainManager()
        # v1.4.4: Command Layer 客户端（使用 Fake 实现）
        self.memory_client = FakeMemoryClient()
        self.poi_client = FakePOIClient()
    
    def simulate_user_input(self, user_text: str, question_type: str = "resume_main_task") -> Dict[str, Any]:
        """
        模拟用户输入
        
        v1.4.4 完整流程：
        1. 用户输入文本 → CommandPrefixDetector → CommandEnvelope
        2. 非命令 → NonCommandHandler → 直接返回
        3. 命令 → SemanticNormalizer → NormalizedCommand (Phase 3)
        4. NormalizedCommand → ECSv1 → ResolutionResult (Phase 4)
        5. NormalizedCommand + ResolutionResult → ParsedIntent
        6. ParsedIntent → DecisionCore.handle_event → DecisionOutput
        7. DecisionOutput → TaskChainManager.apply_decision → 更新任务状态
        
        Args:
            user_text: 用户输入的文本
            question_type: 问句类型（用于选择模板，v1.4.3 兼容）
        
        Returns:
            Dict: 执行结果
        """
        # v1.4.4: Step 1 - 检测命令前缀
        envelope = detect_prefix(user_text)
        
        # 非命令路径：直接返回提示，不进入 Inquiry/Decision/TaskChain
        if not envelope.is_command:
            return handle_non_command(user_text)
        
        # 帮助中心路径
        if envelope.mode == "HELP_CENTER":
            return handle_help_center(envelope.command_text or "")
        
        # 命令为空（只有 "Luna" 无后续内容）
        if not envelope.command_text:
            return {
                "type": "EMPTY_COMMAND",
                "message": "请给出明确指令，例如：Luna，带我去医院",
                "raw_text": user_text
            }
        
        # v1.4.4: Phase 3 - 语义归一化
        normalized = normalize_command(envelope.command_text)
        
        # 如果无法识别意图，回退到 v1.4.3 流程
        if normalized.intent_type == "UNKNOWN":
            parsed_intent = self.inquiry_manager.handle_user_response(question_type, envelope.command_text)
        else:
            # v1.4.4: Phase 4 - 参数补全（ECSv1）
            resolution = resolve_slots(
                normalized,
                memory_client=self.memory_client,
                poi_client=self.poi_client
            )
            
            # v1.4.4: Phase 6 - 映射为 ParsedIntent
            parsed_intent = normalized_to_parsed_intent(normalized, resolution)
            
            # 如果参数未补全，需要用户澄清
            if not resolution.resolved:
                # 返回澄清提示，不进入决策流程
                return {
                    "type": "NEED_CLARIFICATION",
                    "message": f"请说出具体的 {normalized.slots.get('place_category', '地点')} 名称。",
                    "parsed_intent": parsed_intent,
                    "resolution": {
                        "resolved": False,
                        "reason": resolution.reason
                    }
                }
        
        # Step 2: 生成决策
        payload = {"parsed_intent": parsed_intent}
        context = {
            "task_context": {
                "task_id": self.taskchain.active_task.get("task_id", "") if self.taskchain.active_task else "",
                "task_type": self.taskchain.active_task.get("type", "") if self.taskchain.active_task else ""
            },
            "model_context": {"vision_main": "ok", "vision_fallback": "ok"}
        }
        
        decision_output = self.decision_core.handle_event(
            EventType.USER_INTENT,
            payload,
            context
        )
        
        # Step 3: 应用决策到 TaskChain
        self.taskchain.apply_decision(decision_output)
        
        return {
            "parsed_intent": parsed_intent,
            "decision_output": decision_output,
            "taskchain_state": {
                "active_task": self.taskchain.active_task,
                "active_node": self.taskchain.active_node,
                "sub_task_stack_size": len(self.taskchain.sub_task_stack)
            }
        }
    
    def simulate_node_complete(self, node_id: str, requires_confirmation: bool = False) -> Dict[str, Any]:
        """
        模拟节点完成
        
        Args:
            node_id: 节点 ID
            requires_confirmation: 是否需要用户确认
        
        Returns:
            Dict: 执行结果
        """
        # Step 1: 生成决策
        payload = {"node_id": node_id}
        context = {
            "task_context": {
                "task_id": self.taskchain.active_task.get("task_id", "") if self.taskchain.active_task else "",
                "task_type": self.taskchain.active_task.get("type", "") if self.taskchain.active_task else "",
                "active_node": {
                    "id": node_id,
                    "requires_user_confirmation": requires_confirmation
                }
            },
            "model_context": {"vision_main": "ok", "vision_fallback": "ok"}
        }
        
        decision_output = self.decision_core.handle_event(
            EventType.TASK_NODE_COMPLETE,
            payload,
            context
        )
        
        # Step 2: 应用决策到 TaskChain
        self.taskchain.apply_decision(decision_output)
        
        return {
            "decision_output": decision_output,
            "taskchain_state": {
                "active_task": self.taskchain.active_task,
                "active_node": self.taskchain.active_node,
                "sub_task_stack_size": len(self.taskchain.sub_task_stack)
            }
        }


