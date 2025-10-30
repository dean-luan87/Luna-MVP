#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Luna Badge 任务中心对话接口
支持用户通过语音对话创建、修改、管理任务链
"""

import logging
import re
import time
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

from .task_center import TaskCenter, TaskChain, Task, TaskType, TaskStatus, TaskChainStatus, get_task_center
from .memory_store import MemoryStore, get_memory_store, MemoryType, Priority

logger = logging.getLogger(__name__)

class ConversationIntent(Enum):
    """对话意图"""
    CREATE_TASK_CHAIN = "create_task_chain"      # 创建任务链
    MODIFY_TASK_CHAIN = "modify_task_chain"      # 修改任务链
    START_TASK_CHAIN = "start_task_chain"        # 启动任务链
    PAUSE_TASK_CHAIN = "pause_task_chain"        # 暂停任务链
    RESUME_TASK_CHAIN = "resume_task_chain"       # 恢复任务链
    CHECK_STATUS = "check_status"                 # 检查状态
    LIST_TEMPLATES = "list_templates"            # 列出模板
    HELP = "help"                                 # 帮助
    UNKNOWN = "unknown"                           # 未知意图

@dataclass
class ConversationContext:
    """对话上下文"""
    user_id: str
    current_chain_id: Optional[str] = None
    last_intent: Optional[ConversationIntent] = None
    pending_modifications: Dict[str, Any] = None
    conversation_history: List[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.pending_modifications is None:
            self.pending_modifications = {}
        if self.conversation_history is None:
            self.conversation_history = []

class TaskConversationManager:
    """任务对话管理器"""
    
    def __init__(self):
        """初始化任务对话管理器"""
        self.task_center = get_task_center()
        self.memory_store = get_memory_store()
        self.conversation_contexts: Dict[str, ConversationContext] = {}
        
        # 意图识别模式
        self.intent_patterns = {
            ConversationIntent.CREATE_TASK_CHAIN: [
                r"创建.*任务链", r"新建.*任务", r"开始.*流程", r"我要.*流程",
                r"帮我.*任务", r"制定.*计划", r"规划.*流程"
            ],
            ConversationIntent.MODIFY_TASK_CHAIN: [
                r"修改.*任务", r"更改.*任务", r"调整.*任务", r"更新.*任务",
                r"编辑.*任务", r"改一下", r"调整一下"
            ],
            ConversationIntent.START_TASK_CHAIN: [
                r"开始.*任务", r"启动.*任务", r"执行.*任务", r"运行.*任务",
                r"开始.*流程", r"启动.*流程"
            ],
            ConversationIntent.PAUSE_TASK_CHAIN: [
                r"暂停.*任务", r"停止.*任务", r"暂停.*流程", r"等一下",
                r"先停一下", r"暂停一下"
            ],
            ConversationIntent.RESUME_TASK_CHAIN: [
                r"继续.*任务", r"恢复.*任务", r"继续.*流程", r"恢复.*流程",
                r"继续", r"恢复"
            ],
            ConversationIntent.CHECK_STATUS: [
                r"任务.*状态", r"进度.*如何", r"现在.*什么", r"当前.*任务",
                r"任务.*进度", r"状态.*如何"
            ],
            ConversationIntent.LIST_TEMPLATES: [
                r"有哪些.*模板", r"模板.*列表", r"可用.*模板", r"任务.*模板",
                r"流程.*模板", r"模板.*有哪些"
            ],
            ConversationIntent.HELP: [
                r"帮助", r"怎么用", r"如何使用", r"功能.*介绍",
                r"能做什么", r"有什么.*功能"
            ]
        }
        
        # 实体提取模式
        self.entity_patterns = {
            "hospital": [r"医院", r"诊所", r"医疗", r"看病", r"就诊"],
            "shopping": [r"购物", r"商场", r"超市", r"买东西", r"购物中心"],
            "transport": [r"出行", r"交通", r"坐车", r"地铁", r"公交"],
            "department": [r"内科", r"外科", r"儿科", r"妇科", r"眼科", r"耳鼻喉科"],
            "time": [r"明天", r"后天", r"下周", r"上午", r"下午", r"晚上"],
            "location": [r"虹口医院", r"中山医院", r"瑞金医院", r"华山医院"]
        }
        
        logger.info("💬 任务对话管理器初始化完成")
    
    def process_user_input(self, user_id: str, user_input: str) -> Dict[str, Any]:
        """
        处理用户输入
        
        Args:
            user_id: 用户ID
            user_input: 用户输入文本
            
        Returns:
            Dict[str, Any]: 处理结果
        """
        # 获取或创建对话上下文
        if user_id not in self.conversation_contexts:
            self.conversation_contexts[user_id] = ConversationContext(user_id=user_id)
        
        context = self.conversation_contexts[user_id]
        
        # 记录对话历史
        context.conversation_history.append({
            "timestamp": time.time(),
            "user_input": user_input,
            "intent": None,
            "response": None
        })
        
        # 识别意图
        intent = self._recognize_intent(user_input)
        context.last_intent = intent
        
        # 更新对话历史
        context.conversation_history[-1]["intent"] = intent.value
        
        # 根据意图处理
        response = self._handle_intent(context, intent, user_input)
        
        # 更新对话历史
        context.conversation_history[-1]["response"] = response
        
        # 保存到长期记忆
        self._save_to_memory(user_id, user_input, intent, response)
        
        return response
    
    def _recognize_intent(self, user_input: str) -> ConversationIntent:
        """识别用户意图"""
        user_input = user_input.lower()
        
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, user_input):
                    return intent
        
        return ConversationIntent.UNKNOWN
    
    def _handle_intent(self, context: ConversationContext, intent: ConversationIntent, user_input: str) -> Dict[str, Any]:
        """根据意图处理用户输入"""
        try:
            if intent == ConversationIntent.CREATE_TASK_CHAIN:
                return self._handle_create_task_chain(context, user_input)
            elif intent == ConversationIntent.MODIFY_TASK_CHAIN:
                return self._handle_modify_task_chain(context, user_input)
            elif intent == ConversationIntent.START_TASK_CHAIN:
                return self._handle_start_task_chain(context, user_input)
            elif intent == ConversationIntent.PAUSE_TASK_CHAIN:
                return self._handle_pause_task_chain(context, user_input)
            elif intent == ConversationIntent.RESUME_TASK_CHAIN:
                return self._handle_resume_task_chain(context, user_input)
            elif intent == ConversationIntent.CHECK_STATUS:
                return self._handle_check_status(context, user_input)
            elif intent == ConversationIntent.LIST_TEMPLATES:
                return self._handle_list_templates(context, user_input)
            elif intent == ConversationIntent.HELP:
                return self._handle_help(context, user_input)
            else:
                return self._handle_unknown_intent(context, user_input)
        except Exception as e:
            logger.error(f"❌ 处理意图失败: {e}")
            return {
                "success": False,
                "message": "抱歉，处理您的请求时出现了错误，请重试。",
                "error": str(e)
            }
    
    def _handle_create_task_chain(self, context: ConversationContext, user_input: str) -> Dict[str, Any]:
        """处理创建任务链意图"""
        # 提取实体信息
        entities = self._extract_entities(user_input)
        
        # 确定模板类型
        template_id = self._determine_template(entities)
        
        if not template_id:
            # 提供模板选择
            templates = self.task_center.get_available_templates()
            return {
                "success": False,
                "message": "请选择您要创建的任务类型：",
                "options": [
                    {"id": template["template_id"], "name": template["name"], "description": template["description"]}
                    for template in templates
                ],
                "requires_selection": True
            }
        
        # 创建任务链
        customizations = self._extract_customizations(entities)
        chain_id = self.task_center.create_task_chain_from_template(template_id, customizations)
        
        context.current_chain_id = chain_id
        
        return {
            "success": True,
            "message": f"已为您创建{self.task_center.task_templates[template_id].name}任务链",
            "chain_id": chain_id,
            "next_action": "是否现在启动这个任务链？"
        }
    
    def _handle_modify_task_chain(self, context: ConversationContext, user_input: str) -> Dict[str, Any]:
        """处理修改任务链意图"""
        if not context.current_chain_id:
            return {
                "success": False,
                "message": "请先创建一个任务链，或者告诉我您要修改哪个任务链。"
            }
        
        # 提取修改信息
        modifications = self._extract_modifications(user_input)
        
        if not modifications:
            return {
                "success": False,
                "message": "请告诉我您要修改什么内容，比如任务名称、时间、地点等。"
            }
        
        # 应用修改
        success = self.task_center.modify_task_chain(context.current_chain_id, modifications)
        
        if success:
            return {
                "success": True,
                "message": "任务链已成功修改",
                "modifications": modifications
            }
        else:
            return {
                "success": False,
                "message": "修改任务链失败，请重试"
            }
    
    def _handle_start_task_chain(self, context: ConversationContext, user_input: str) -> Dict[str, Any]:
        """处理启动任务链意图"""
        chain_id = context.current_chain_id
        
        if not chain_id:
            return {
                "success": False,
                "message": "请先创建一个任务链"
            }
        
        success = self.task_center.start_task_chain(chain_id)
        
        if success:
            return {
                "success": True,
                "message": "任务链已启动，开始执行第一个任务",
                "chain_id": chain_id
            }
        else:
            return {
                "success": False,
                "message": "启动任务链失败，请检查任务链状态"
            }
    
    def _handle_pause_task_chain(self, context: ConversationContext, user_input: str) -> Dict[str, Any]:
        """处理暂停任务链意图"""
        chain_id = context.current_chain_id
        
        if not chain_id:
            return {
                "success": False,
                "message": "没有正在运行的任务链可以暂停"
            }
        
        success = self.task_center.pause_task_chain(chain_id, "用户主动暂停")
        
        if success:
            return {
                "success": True,
                "message": "任务链已暂停，您可以随时说'继续'来恢复"
            }
        else:
            return {
                "success": False,
                "message": "暂停任务链失败"
            }
    
    def _handle_resume_task_chain(self, context: ConversationContext, user_input: str) -> Dict[str, Any]:
        """处理恢复任务链意图"""
        chain_id = context.current_chain_id
        
        if not chain_id:
            return {
                "success": False,
                "message": "没有暂停的任务链可以恢复"
            }
        
        success = self.task_center.resume_task_chain(chain_id)
        
        if success:
            return {
                "success": True,
                "message": "任务链已恢复，继续执行"
            }
        else:
            return {
                "success": False,
                "message": "恢复任务链失败"
            }
    
    def _handle_check_status(self, context: ConversationContext, user_input: str) -> Dict[str, Any]:
        """处理检查状态意图"""
        chain_id = context.current_chain_id
        
        if not chain_id:
            return {
                "success": False,
                "message": "没有正在运行的任务链"
            }
        
        status = self.task_center.get_task_chain_status(chain_id)
        
        if status:
            return {
                "success": True,
                "message": f"任务链'{status['name']}'当前状态：{status['status']}，进度：{status['progress']:.1f}%",
                "status": status
            }
        else:
            return {
                "success": False,
                "message": "无法获取任务链状态"
            }
    
    def _handle_list_templates(self, context: ConversationContext, user_input: str) -> Dict[str, Any]:
        """处理列出模板意图"""
        templates = self.task_center.get_available_templates()
        
        if not templates:
            return {
                "success": False,
                "message": "当前没有可用的任务模板"
            }
        
        template_list = []
        for template in templates:
            template_list.append(f"• {template['name']}: {template['description']}")
        
        return {
            "success": True,
            "message": "可用的任务模板：\n" + "\n".join(template_list),
            "templates": templates
        }
    
    def _handle_help(self, context: ConversationContext, user_input: str) -> Dict[str, Any]:
        """处理帮助意图"""
        help_text = """
我可以帮您管理任务链，支持以下功能：

📋 创建任务链：
• "创建医院任务链"
• "我要去医院看病"
• "帮我制定购物计划"

✏️ 修改任务链：
• "修改任务名称"
• "调整时间"
• "更改地点"

🚀 启动任务链：
• "开始任务"
• "启动流程"

⏸️ 暂停/恢复：
• "暂停任务"
• "继续任务"

📊 查看状态：
• "任务状态如何"
• "当前进度"

📝 查看模板：
• "有哪些模板"
• "可用任务模板"

您想尝试哪个功能？
        """
        
        return {
            "success": True,
            "message": help_text.strip(),
            "help_type": "general"
        }
    
    def _handle_unknown_intent(self, context: ConversationContext, user_input: str) -> Dict[str, Any]:
        """处理未知意图"""
        return {
            "success": False,
            "message": "抱歉，我没有理解您的意思。您可以问我关于任务链的问题，或者说'帮助'查看可用功能。",
            "suggestion": "尝试说：'创建医院任务链' 或 '帮助'"
        }
    
    def _extract_entities(self, user_input: str) -> Dict[str, List[str]]:
        """提取实体信息"""
        entities = {}
        
        for entity_type, patterns in self.entity_patterns.items():
            matches = []
            for pattern in patterns:
                if re.search(pattern, user_input):
                    matches.append(pattern)
            if matches:
                entities[entity_type] = matches
        
        return entities
    
    def _determine_template(self, entities: Dict[str, List[str]]) -> Optional[str]:
        """根据实体确定模板"""
        if "hospital" in entities:
            return "hospital_workflow"
        elif "shopping" in entities:
            return "shopping_workflow"
        elif "transport" in entities:
            return "transport_workflow"
        
        return None
    
    def _extract_customizations(self, entities: Dict[str, List[str]]) -> Dict[str, Any]:
        """提取自定义配置"""
        customizations = {}
        
        if "department" in entities:
            customizations["department"] = entities["department"][0]
        if "location" in entities:
            customizations["location"] = entities["location"][0]
        if "time" in entities:
            customizations["time"] = entities["time"][0]
        
        return customizations
    
    def _extract_modifications(self, user_input: str) -> Dict[str, Any]:
        """提取修改信息"""
        modifications = {}
        
        # 提取任务修改
        task_modifications = []
        
        # 简单的修改提取逻辑
        if "时间" in user_input or "几点" in user_input:
            modifications["time_modification"] = True
        if "地点" in user_input or "哪里" in user_input:
            modifications["location_modification"] = True
        if "科室" in user_input or "部门" in user_input:
            modifications["department_modification"] = True
        
        return modifications
    
    def _save_to_memory(self, user_id: str, user_input: str, intent: ConversationIntent, response: Dict[str, Any]):
        """保存到长期记忆"""
        try:
            memory_content = f"用户意图：{intent.value}，输入：{user_input}，响应：{response.get('message', '')}"
            
            self.memory_store.add_memory(
                title=f"任务对话: {intent.value}",
                content=memory_content,
                memory_type=MemoryType.NOTE,
                tags=["task_conversation", intent.value],
                priority=Priority.NORMAL
            )
        except Exception as e:
            logger.error(f"❌ 保存到记忆失败: {e}")


# 全局对话管理器实例
_global_conversation_manager: Optional[TaskConversationManager] = None

def get_conversation_manager() -> TaskConversationManager:
    """获取全局对话管理器实例"""
    global _global_conversation_manager
    if _global_conversation_manager is None:
        _global_conversation_manager = TaskConversationManager()
    return _global_conversation_manager


if __name__ == "__main__":
    # 测试对话管理器
    print("💬 任务对话管理器测试")
    print("=" * 50)
    
    conversation_manager = get_conversation_manager()
    
    # 测试用例
    test_cases = [
        "我要去医院看病",
        "创建购物任务链",
        "任务状态如何",
        "有哪些模板",
        "帮助"
    ]
    
    for i, test_input in enumerate(test_cases, 1):
        print(f"\n{i}. 测试输入: {test_input}")
        response = conversation_manager.process_user_input("test_user", test_input)
        print(f"   响应: {response['message']}")
        print(f"   成功: {response['success']}")
    
    print("\n🎉 任务对话管理器测试完成！")
