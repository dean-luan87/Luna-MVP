#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Luna 智能任务引擎 - 系统集成适配器
将TaskEngine与现有Luna Badge系统集成
"""

import logging
import time
from typing import Dict, List, Any, Optional
from .task_engine import TaskEngine, TaskGraph, TaskNode, TaskEdge, NodeType, FlowControl, get_task_engine
from .task_graph_templates import TaskGraphTemplates
from .memory_store import get_memory_store
from .task_conversation import get_conversation_manager

logger = logging.getLogger(__name__)

class LunaTaskEngineAdapter:
    """Luna任务引擎适配器"""
    
    def __init__(self):
        """初始化适配器"""
        self.task_engine = get_task_engine(get_memory_store())
        self.conversation_manager = get_conversation_manager()
        self.templates = TaskGraphTemplates.get_all_templates()
        
        # 注册自定义执行器
        self._register_custom_executors()
        
        # 注册事件处理器
        self._register_event_handlers()
        
        self.logger = logging.getLogger("LunaTaskEngineAdapter")
        self.logger.info("🔗 Luna任务引擎适配器初始化完成")
    
    def _register_custom_executors(self):
        """注册自定义执行器"""
        # 这里可以注册更多自定义执行器
        pass
    
    def _register_event_handlers(self):
        """注册事件处理器"""
        # 注册任务引擎事件到对话管理器
        self.task_engine.trigger_router.register_trigger(
            "task_started", 
            self._on_task_started
        )
        self.task_engine.trigger_router.register_trigger(
            "task_completed", 
            self._on_task_completed
        )
        self.task_engine.trigger_router.register_trigger(
            "task_failed", 
            self._on_task_failed
        )
    
    def create_task_from_template(self, template_name: str, customizations: Dict[str, Any] = None) -> str:
        """
        从模板创建任务
        
        Args:
            template_name: 模板名称
            customizations: 自定义配置
            
        Returns:
            str: 任务图ID
        """
        if template_name not in self.templates:
            raise ValueError(f"模板不存在: {template_name}")
        
        # 获取模板
        template = self.templates[template_name]
        
        # 应用自定义配置
        if customizations:
            template = self._apply_customizations(template, customizations)
        
        # 创建任务
        graph_id = f"{template_name}_{int(time.time() * 1000)}"
        template.graph_id = graph_id
        
        self.task_engine.create_task(template)
        
        self.logger.info(f"📋 从模板创建任务: {template_name} -> {graph_id}")
        return graph_id
    
    def _apply_customizations(self, template: TaskGraph, customizations: Dict[str, Any]) -> TaskGraph:
        """应用自定义配置"""
        # 更新节点配置
        for node in template.nodes:
            if node.id in customizations:
                node.executor_config.update(customizations[node.id])
        
        # 更新元数据
        if "metadata" in customizations:
            template.metadata.update(customizations["metadata"])
        
        return template
    
    def start_task(self, graph_id: str) -> bool:
        """启动任务"""
        return self.task_engine.start_task(graph_id)
    
    def pause_task(self, graph_id: str) -> bool:
        """暂停任务"""
        return self.task_engine.pause_task(graph_id)
    
    def resume_task(self, graph_id: str) -> bool:
        """恢复任务"""
        return self.task_engine.resume_task(graph_id)
    
    def get_task_status(self, graph_id: str) -> Optional[Dict[str, Any]]:
        """获取任务状态"""
        return self.task_engine.get_task_status(graph_id)
    
    def process_user_input(self, user_id: str, user_input: str) -> Dict[str, Any]:
        """
        处理用户输入（集成对话管理器）
        
        Args:
            user_id: 用户ID
            user_input: 用户输入
            
        Returns:
            Dict[str, Any]: 处理结果
        """
        # 使用对话管理器处理输入
        response = self.conversation_manager.process_user_input(user_id, user_input)
        
        # 如果对话管理器识别出任务相关意图，执行相应操作
        if response.get("success") and "task" in response.get("message", "").lower():
            # 这里可以添加任务相关的特殊处理逻辑
            pass
        
        return response
    
    def inject_emergency_task(self, current_graph_id: str, emergency_type: str) -> bool:
        """
        注入紧急任务
        
        Args:
            current_graph_id: 当前任务图ID
            emergency_type: 紧急任务类型
            
        Returns:
            bool: 是否成功注入
        """
        # 创建紧急任务图
        emergency_graph = self._create_emergency_task_graph(emergency_type)
        
        # 注入任务
        return self.task_engine.inject_task(current_graph_id, emergency_graph, "emergency_return")
    
    def _create_emergency_task_graph(self, emergency_type: str) -> TaskGraph:
        """创建紧急任务图"""
        if emergency_type == "toilet":
            return TaskGraph(
                graph_id=f"emergency_toilet_{int(time.time() * 1000)}",
                scene="emergency",
                goal="寻找洗手间",
                nodes=[
                    TaskNode(
                        id="find_toilet",
                        type=NodeType.OBSERVATION,
                        title="寻找洗手间",
                        description="识别洗手间位置",
                        input_schema={},
                        output_schema={"toilet_found": "boolean", "location": "string"},
                        precondition=[],
                        postcondition=["toilet_found"],
                        executor_config={"type": "ocr", "target": "toilet_signs"},
                        timeout=120
                    ),
                    TaskNode(
                        id="navigate_to_toilet",
                        type=NodeType.NAVIGATION,
                        title="导航到洗手间",
                        description="导航到洗手间",
                        input_schema={"location": "string"},
                        output_schema={"arrived": "boolean"},
                        precondition=["toilet_found"],
                        postcondition=["arrived_toilet"],
                        executor_config={"mode": "urgent_navigation"},
                        timeout=300
                    )
                ],
                edges=[
                    TaskEdge(from_node="find_toilet", to_node="navigate_to_toilet")
                ],
                flow_control=FlowControl.SEQUENTIAL,
                metadata={"priority": "high", "estimated_duration": 5}
            )
        
        # 默认紧急任务
        return TaskGraph(
            graph_id=f"emergency_default_{int(time.time() * 1000)}",
            scene="emergency",
            goal="处理紧急情况",
            nodes=[
                TaskNode(
                    id="emergency_response",
                    type=NodeType.INTERACTION,
                    title="紧急响应",
                    description="处理紧急情况",
                    input_schema={},
                    output_schema={"handled": "boolean"},
                    precondition=[],
                    postcondition=["emergency_handled"],
                    executor_config={"question": "需要什么帮助？", "options": ["安全", "医疗", "其他"]},
                    timeout=60
                )
            ],
            edges=[],
            flow_control=FlowControl.SEQUENTIAL,
            metadata={"priority": "high", "estimated_duration": 2}
        )
    
    def get_available_templates(self) -> List[Dict[str, Any]]:
        """获取可用模板列表"""
        template_list = []
        for name, template in self.templates.items():
            template_list.append({
                "name": name,
                "scene": template.scene,
                "goal": template.goal,
                "node_count": len(template.nodes),
                "estimated_duration": template.metadata.get("estimated_duration", 0),
                "complexity": template.metadata.get("complexity", "unknown"),
                "description": f"{template.scene}场景的{template.goal}"
            })
        return template_list
    
    def create_custom_task(self, scene: str, goal: str, 
                          node_descriptions: List[Dict[str, Any]]) -> str:
        """
        创建自定义任务
        
        Args:
            scene: 场景类型
            goal: 目标描述
            node_descriptions: 节点描述列表
            
        Returns:
            str: 任务图ID
        """
        # 创建节点
        nodes = []
        for i, desc in enumerate(node_descriptions):
            node = TaskNode(
                id=desc.get("id", f"node_{i}"),
                type=NodeType(desc.get("type", "interaction")),
                title=desc.get("title", f"任务节点{i+1}"),
                description=desc.get("description", ""),
                input_schema=desc.get("input_schema", {}),
                output_schema=desc.get("output_schema", {}),
                precondition=desc.get("precondition", []),
                postcondition=desc.get("postcondition", []),
                executor_config=desc.get("executor_config", {}),
                timeout=desc.get("timeout", 300)
            )
            nodes.append(node)
        
        # 创建边（简单的顺序连接）
        edges = []
        for i in range(len(nodes) - 1):
            edge = TaskEdge(
                from_node=nodes[i].id,
                to_node=nodes[i+1].id
            )
            edges.append(edge)
        
        # 创建任务图
        graph_id = f"custom_{scene}_{int(time.time() * 1000)}"
        custom_graph = TaskGraph(
            graph_id=graph_id,
            scene=scene,
            goal=goal,
            nodes=nodes,
            edges=edges,
            flow_control=FlowControl.SEQUENTIAL,
            metadata={"type": "custom", "created_by": "user"}
        )
        
        # 创建任务
        self.task_engine.create_task(custom_graph)
        
        self.logger.info(f"🎨 创建自定义任务: {graph_id}")
        return graph_id
    
    def _on_task_started(self, data: Dict[str, Any]):
        """任务开始回调"""
        graph_id = data["graph_id"]
        self.logger.info(f"🎬 任务开始: {graph_id}")
        
        # 可以在这里添加语音播报
        # self.speak(f"任务已开始：{graph_id}")
    
    def _on_task_completed(self, data: Dict[str, Any]):
        """任务完成回调"""
        graph_id = data["graph_id"]
        self.logger.info(f"🎉 任务完成: {graph_id}")
        
        # 可以在这里添加语音播报
        # self.speak(f"任务已完成：{graph_id}")
    
    def _on_task_failed(self, data: Dict[str, Any]):
        """任务失败回调"""
        graph_id = data["graph_id"]
        error = data["error"]
        self.logger.error(f"💥 任务失败: {graph_id} - {error}")
        
        # 可以在这里添加错误处理和语音播报
        # self.speak(f"任务执行遇到问题：{error}")


# 全局适配器实例
_global_adapter: Optional[LunaTaskEngineAdapter] = None

def get_luna_task_adapter() -> LunaTaskEngineAdapter:
    """获取全局Luna任务适配器实例"""
    global _global_adapter
    if _global_adapter is None:
        _global_adapter = LunaTaskEngineAdapter()
    return _global_adapter


if __name__ == "__main__":
    # 测试适配器
    print("🔗 Luna任务引擎适配器测试")
    print("=" * 60)
    
    adapter = get_luna_task_adapter()
    
    # 测试1: 获取可用模板
    print("\n1. 获取可用模板...")
    templates = adapter.get_available_templates()
    for template in templates:
        print(f"   📋 {template['name']}: {template['description']}")
    
    # 测试2: 从模板创建任务
    print("\n2. 从模板创建任务...")
    graph_id = adapter.create_task_from_template(
        "hospital_visit",
        {"plan_route": {"destination": "虹口医院"}}
    )
    print(f"   ✅ 任务创建成功: {graph_id}")
    
    # 测试3: 启动任务
    print("\n3. 启动任务...")
    success = adapter.start_task(graph_id)
    print(f"   ✅ 任务启动: {success}")
    
    # 测试4: 检查状态
    print("\n4. 检查任务状态...")
    status = adapter.get_task_status(graph_id)
    if status:
        print(f"   📊 状态: {status['status']}")
        print(f"   📈 进度: {status['progress']:.1f}%")
        print(f"   🎯 当前节点: {status['current_node']}")
    
    # 测试5: 用户输入处理
    print("\n5. 用户输入处理...")
    response = adapter.process_user_input("test_user", "创建医院任务链")
    print(f"   💬 响应: {response['message'][:50]}...")
    
    print("\n🎉 Luna任务引擎适配器测试完成！")
