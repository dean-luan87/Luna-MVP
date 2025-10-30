#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Luna Badge v1.4 - 任务节点执行器
根据节点type调用对应功能模块，支持状态更新、错误处理、fallback机制
"""

import logging
import time
from typing import Dict, Any, Optional, List
from datetime import datetime

logger = logging.getLogger(__name__)


class TaskNodeExecutor:
    """任务节点执行器 - 负责执行任务图中的每个节点"""
    
    def __init__(self, state_manager=None, report_uploader=None):
        """
        初始化节点执行器
        
        Args:
            state_manager: 状态管理器实例（可选）
            report_uploader: 报告上传器实例（可选）
        """
        # 节点类型到执行函数的映射
        self.executors = {
            "navigation": self._execute_navigation,
            "interaction": self._execute_interaction,
            "observation": self._execute_observation,
            "condition_check": self._execute_condition_check,
            "external_call": self._execute_external_call,
            "memory_action": self._execute_memory_action,
            "environmental_state": self._execute_environmental_state,
            "scene_entry": self._execute_scene_entry,
            "decision": self._execute_decision,
        }
        
        self.state_manager = state_manager
        self.report_uploader = report_uploader
        self.logger = logging.getLogger("TaskNodeExecutor")
        
        # 尝试导入实际模块（如果存在）
        self._import_modules()
        
        # 事件总线（预留）
        self.event_bus = None  # TODO: 实现event_bus
    
    def _import_modules(self):
        """尝试导入实际功能模块"""
        self.modules = {}
        self.mock_modules = {}
        
        # 定义模块映射
        module_map = {
            "ai_navigation": "core.ai_navigation",
            "voice_interaction": "core.voice_interaction",
            "condition_checker": "core.condition_checker",
            "external_services": "core.external_services",
            "environment_checker": "core.environment_checker",
            "scene_controller": "core.scene_controller",
            "decision_router": "core.decision_router",
            "memory_manager": "core.memory_store",
        }
        
        for module_name, module_path in module_map.items():
            try:
                module = __import__(module_path, fromlist=[module_name])
                self.modules[module_name] = module
                self.logger.debug(f"✅ 成功导入模块: {module_name}")
            except ImportError:
                self.mock_modules[module_name] = True
                self.logger.debug(f"⚠️ 模块未实现，使用mock: {module_name}")
    
    def execute_node(self, node: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        执行单个任务节点
        
        Args:
            node: 节点定义字典，包含id, type, config等字段
            context: 执行上下文（可选）
            
        Returns:
            Dict[str, Any]: 执行结果，包含node_id, status, output等字段
            
        Raises:
            ValueError: 节点类型未知
            Exception: 执行过程中的任何异常
        """
        if context is None:
            context = {}
        
        node_id = node.get("id", "unknown")
        node_type = node.get("type", "unknown")
        
        self.logger.info(f"🔧 执行节点: {node_id} (type: {node_type})")
        
        # 状态更新：pending → running
        self._update_node_status(node_id, "running")
        
        start_time = time.time()
        timestamp = datetime.now().isoformat()
        
        try:
            # 获取执行器
            executor = self.executors.get(node_type)
            if not executor:
                raise ValueError(f"未知节点类型: {node_type}")
            
            # 执行节点
            result = executor(node, context)
            
            # 确保result是字典
            if not isinstance(result, dict):
                result = {"output": result, "success": True}
            
            # 添加元数据
            duration = time.time() - start_time
            result.update({
                "node_id": node_id,
                "node_type": node_type,
                "status": "complete",
                "success": result.get("success", True),
                "duration": duration,
                "timestamp": timestamp
            })
            
            # 状态更新：running → complete
            self._update_node_status(node_id, "complete")
            
            # 广播事件（预留）
            self._broadcast_event("node_complete", result)
            
            self.logger.info(f"✅ 节点执行完成: {node_id} (耗时{duration:.2f}秒)")
            return result
            
        except Exception as e:
            self.logger.error(f"❌ 节点执行失败: {node_id}: {e}")
            
            duration = time.time() - start_time
            
            # 状态更新：running → failed
            self._update_node_status(node_id, "failed")
            
            # 尝试fallback
            fallback_result = self._handle_fallback(node, e)
            
            result = {
                "node_id": node_id,
                "node_type": node_type,
                "status": "failed",
                "success": False,
                "error": str(e),
                "duration": duration,
                "timestamp": timestamp,
                "fallback": fallback_result
            }
            
            # 广播事件
            self._broadcast_event("node_failed", result)
            
            return result
    
    def _update_node_status(self, node_id: str, status: str):
        """
        更新节点状态
        
        Args:
            node_id: 节点ID
            status: 新状态
        """
        if self.state_manager:
            self.state_manager.update_current_node(node_id, status)
        
        self.logger.debug(f"📊 节点状态更新: {node_id} -> {status}")
    
    def _handle_fallback(self, node: Dict[str, Any], error: Exception) -> Optional[Dict[str, Any]]:
        """
        处理fallback逻辑
        
        Args:
            node: 节点定义
            error: 发生的错误
            
        Returns:
            Optional[Dict]: fallback执行结果，或None
        """
        fallback = node.get("fallback")
        if not fallback:
            return None
        
        self.logger.info(f"🔄 执行fallback: {fallback}")
        
        # 这里可以根据fallback类型执行不同的逻辑
        # 例如：执行备用节点、调用备用服务等
        return {
            "fallback_action": fallback,
            "executed": True,
            "message": f"fallback已执行: {fallback}"
        }
    
    def _broadcast_event(self, event_type: str, data: Dict[str, Any]):
        """
        广播事件（预留功能）
        
        Args:
            event_type: 事件类型
            data: 事件数据
        """
        if self.event_bus:
            self.event_bus.publish(event_type, data)
    
    # ========== 节点类型执行函数 ==========
    
    def _execute_navigation(self, node: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行导航节点
        
        调用模块: ai_navigation.navigate_to()
        """
        config = node.get("config", {})
        destination = config.get("destination", "未知目的地")
        transport_mode = config.get("transport_mode", "walking")
        
        self.logger.info(f"🧭 导航任务: {destination}")
        
        # 尝试调用实际模块
        if "ai_navigation" in self.modules:
            try:
                from core.ai_navigation import AINavigator
                navigator = AINavigator()
                result = navigator.navigate_to(destination, mode=transport_mode)
                return {"success": True, **result}
            except Exception as e:
                self.logger.warning(f"调用ai_navigation失败，使用mock: {e}")
        
        # Mock实现
        return {
            "success": True,
            "destination": destination,
            "transport_mode": transport_mode,
            "estimated_time": 30,
            "distance": 2.5,
            "message": f"正在导航到{destination}",
            "mock": True
        }
    
    def _execute_interaction(self, node: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行交互节点
        
        调用模块: voice_interaction.ask_user()
        """
        config = node.get("config", {})
        question = config.get("question", "请确认")
        options = config.get("options", ["是", "否"])
        
        self.logger.info(f"💬 用户交互: {question}")
        
        # 尝试调用实际模块
        if "voice_interaction" in self.modules:
            try:
                from core.voice_interaction import VoiceInteraction
                interaction = VoiceInteraction()
                result = interaction.ask_user(question, options)
                return {"success": True, **result}
            except Exception as e:
                self.logger.warning(f"调用voice_interaction失败，使用mock: {e}")
        
        # Mock实现
        return {
            "success": True,
            "question": question,
            "response": "是",  # 模拟响应
            "options": options,
            "message": "用户响应: 是",
            "mock": True
        }
    
    def _execute_observation(self, node: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行观察节点
        
        调用模块: vision + OCR
        """
        config = node.get("config", {})
        observation_type = config.get("type", "ocr")
        target = config.get("target", "signboard")
        
        self.logger.info(f"👁️ 观察任务: {observation_type} - {target}")
        
        # Mock实现
        return {
            "success": True,
            "observation_type": observation_type,
            "target": target,
            "detected_objects": ["医院", "入口", "指示牌"],
            "confidence": 0.95,
            "message": f"观察到{len(['医院', '入口', '指示牌'])}个对象",
            "mock": True
        }
    
    def _execute_condition_check(self, node: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行条件检查节点
        
        调用模块: condition_checker.check()
        """
        config = node.get("config", {})
        condition = config.get("condition", "true")
        required_items = config.get("required_items", [])
        
        self.logger.info(f"🔍 条件检查: {condition}")
        
        # 尝试调用实际模块
        if "condition_checker" in self.modules:
            try:
                result = self.modules["condition_checker"].check(condition, required_items)
                return {"success": True, **result}
            except Exception as e:
                self.logger.warning(f"调用condition_checker失败，使用mock: {e}")
        
        # Mock实现
        passed = True  # 默认通过
        return {
            "success": passed,
            "condition": condition,
            "passed": passed,
            "required_items": required_items,
            "message": f"条件检查{'通过' if passed else '失败'}",
            "mock": True
        }
    
    def _execute_external_call(self, node: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行外部服务调用节点
        
        调用模块: external_services.call()
        """
        config = node.get("config", {})
        service = config.get("service", "unknown")
        service_type = config.get("service_type", "")
        
        self.logger.info(f"🔌 外部服务调用: {service}")
        
        # 尝试调用实际模块
        if "external_services" in self.modules:
            try:
                result = self.modules["external_services"].call(service, service_type)
                return {"success": True, **result}
            except Exception as e:
                self.logger.warning(f"调用external_services失败，使用mock: {e}")
        
        # Mock实现
        return {
            "success": True,
            "service": service,
            "service_type": service_type,
            "result": f"{service}调用成功",
            "data": {},
            "mock": True
        }
    
    def _execute_memory_action(self, node: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行记忆操作节点
        
        调用模块: memory_manager.write() / read()
        """
        config = node.get("config", {})
        action = config.get("action", "save")
        memory_type = config.get("memory_type", "default")
        fields = config.get("fields", [])
        
        self.logger.info(f"🧠 记忆操作: {action}")
        
        # 尝试调用实际模块
        if "memory_manager" in self.modules:
            try:
                if action == "save":
                    result = self.modules["memory_manager"].write(memory_type, fields)
                elif action == "read":
                    result = self.modules["memory_manager"].read(memory_type)
                else:
                    result = {"success": False, "error": f"未知操作: {action}"}
                return {"success": True, **result}
            except Exception as e:
                self.logger.warning(f"调用memory_manager失败，使用mock: {e}")
        
        # Mock实现
        return {
            "success": True,
            "action": action,
            "memory_type": memory_type,
            "fields": fields,
            "message": f"记忆已{action}",
            "mock": True
        }
    
    def _execute_environmental_state(self, node: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行环境状态节点
        
        调用模块: environment_checker.observe()
        """
        config = node.get("config", {})
        trigger = node.get("trigger", "")
        
        self.logger.info(f"🌍 环境状态检查: {trigger}")
        
        # 尝试调用实际模块
        if "environment_checker" in self.modules:
            try:
                result = self.modules["environment_checker"].observe(trigger)
                return {"success": True, **result}
            except Exception as e:
                self.logger.warning(f"调用environment_checker失败，使用mock: {e}")
        
        # Mock实现
        return {
            "success": True,
            "trigger": trigger,
            "state": "active",
            "message": "环境状态正常",
            "mock": True
        }
    
    def _execute_scene_entry(self, node: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行场景进入节点
        
        调用模块: scene_controller.enter()
        """
        config = node.get("config", {})
        scene_id = config.get("scene_id", "")
        
        self.logger.info(f"🚪 场景进入: {scene_id}")
        
        # 尝试调用实际模块
        if "scene_controller" in self.modules:
            try:
                result = self.modules["scene_controller"].enter(scene_id)
                return {"success": True, **result}
            except Exception as e:
                self.logger.warning(f"调用scene_controller失败，使用mock: {e}")
        
        # Mock实现
        return {
            "success": True,
            "scene_id": scene_id,
            "message": f"已进入场景: {scene_id}",
            "mock": True
        }
    
    def _execute_decision(self, node: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行决策节点
        
        调用模块: decision_router.route()
        """
        config = node.get("config", {})
        options = node.get("options", [])
        priority = node.get("priority", [])
        
        self.logger.info(f"🤔 决策路由: {len(options)}个选项")
        
        # 尝试调用实际模块
        if "decision_router" in self.modules:
            try:
                result = self.modules["decision_router"].route(options, priority)
                return {"success": True, **result}
            except Exception as e:
                self.logger.warning(f"调用decision_router失败，使用mock: {e}")
        
        # Mock实现 - 选择优先级最高的选项
        selected = priority[0] if priority else options[0] if options else ""
        
        return {
            "success": True,
            "options": options,
            "priority": priority,
            "selected": selected,
            "message": f"选择方案: {selected}",
            "mock": True
        }


# 向后兼容的方法名
TaskNodeExecutor.execute = TaskNodeExecutor.execute_node


if __name__ == "__main__":
    # 测试节点执行器
    print("🔧 TaskNodeExecutor测试")
    print("=" * 60)
    
    executor = TaskNodeExecutor()
    
    # 测试不同类型的节点
    test_nodes = [
        {
            "id": "test_nav",
            "type": "navigation",
            "config": {"destination": "虹口医院", "transport_mode": "walking"}
        },
        {
            "id": "test_int",
            "type": "interaction",
            "config": {"question": "准备好了吗？", "options": ["是", "否"]}
        },
        {
            "id": "test_obs",
            "type": "observation",
            "config": {"type": "ocr", "target": "signboard"}
        },
        {
            "id": "test_dec",
            "type": "decision",
            "options": ["方案A", "方案B"],
            "priority": ["方案A"]
        }
    ]
    
    for node in test_nodes:
        print(f"\n📝 测试节点: {node['id']} ({node['type']})")
        result = executor.execute_node(node)
        print(f"   状态: {result.get('status')}")
        print(f"   成功: {result.get('success')}")
        print(f"   消息: {result.get('message', '完成')}")
    
    print("\n🎉 TaskNodeExecutor测试完成！")