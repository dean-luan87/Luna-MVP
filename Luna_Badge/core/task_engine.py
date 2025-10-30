#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Luna 智能任务引擎 v1.0 - 抽象系统原型
基于用户提供的Task Engine架构设计
支持多场景、多角色、多模态交互的任务系统
"""

import logging
import json
import time
import uuid
from typing import Dict, List, Any, Optional, Union, Callable
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime
import os
import threading

logger = logging.getLogger(__name__)

class NodeType(Enum):
    """任务节点类型"""
    NAVIGATION = "navigation"           # 导航相关任务
    INTERACTION = "interaction"         # 与用户对话/问询
    OBSERVATION = "observation"        # 视觉/语音识别
    EXTERNAL_CALL = "external_call"     # 联动外部服务
    MEMORY_ACTION = "memory_action"     # 记忆写入/修改/调取
    CONDITION_CHECK = "condition_check" # 判断环境/状态
    COMPOUND_TASK = "compound_task"     # 嵌套子任务图

class TaskStatus(Enum):
    """任务状态"""
    PENDING = "pending"           # 待执行
    ACTIVE = "active"             # 执行中
    PAUSED = "paused"             # 暂停
    COMPLETED = "completed"       # 已完成
    FAILED = "failed"             # 失败
    CANCELLED = "cancelled"       # 已取消

class FlowControl(Enum):
    """任务流控制机制"""
    SEQUENTIAL = "sequential"         # 顺序执行：A → B → C
    PARALLEL = "parallel"            # 并发执行：A+B+C
    BRANCHING = "branching"          # 条件分支：if A then → B else → C
    LOOP = "loop"                    # 循环执行直到满足条件
    INTERRUPTIBLE = "interruptible"  # 可插入任务
    MEMORY_CONDITIONED = "memory_conditioned"  # 与长期记忆相关

@dataclass
class TaskNode:
    """任务节点定义"""
    id: str
    type: NodeType
    title: str
    description: str
    input_schema: Dict[str, Any]      # 输入数据模式
    output_schema: Dict[str, Any]     # 输出数据模式
    precondition: List[str]          # 前置条件
    postcondition: List[str]         # 后置条件
    executor_config: Dict[str, Any]   # 执行器配置
    timeout: int = 300               # 超时时间（秒）
    retry_count: int = 3             # 重试次数
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type.value,
            "title": self.title,
            "description": self.description,
            "input_schema": self.input_schema,
            "output_schema": self.output_schema,
            "precondition": self.precondition,
            "postcondition": self.postcondition,
            "executor_config": self.executor_config,
            "timeout": self.timeout,
            "retry_count": self.retry_count
        }

@dataclass
class TaskEdge:
    """任务边定义"""
    from_node: str
    to_node: str
    condition: Optional[str] = None   # 条件表达式
    weight: float = 1.0              # 权重
    parallel: bool = False           # 是否并行执行
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "from_node": self.from_node,
            "to_node": self.to_node,
            "condition": self.condition,
            "weight": self.weight,
            "parallel": self.parallel
        }

@dataclass
class TaskGraph:
    """抽象任务图结构"""
    graph_id: str
    scene: str                       # 场景类型
    goal: str                        # 目标描述
    nodes: List[TaskNode]            # 节点列表
    edges: List[TaskEdge]            # 边列表
    flow_control: FlowControl = FlowControl.SEQUENTIAL
    metadata: Dict[str, Any] = None  # 元数据
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "graph_id": self.graph_id,
            "scene": self.scene,
            "goal": self.goal,
            "nodes": [node.to_dict() for node in self.nodes],
            "edges": [edge.to_dict() for edge in self.edges],
            "flow_control": self.flow_control.value,
            "metadata": self.metadata
        }

@dataclass
class TaskExecutionState:
    """任务运行状态结构"""
    graph_id: str
    status: TaskStatus
    current_node: Optional[str] = None
    history: List[str] = None        # 执行历史
    injected_tasks: List[str] = None # 注入的任务
    memory_updated: bool = False     # 记忆是否更新
    context: Dict[str, Any] = None   # 上下文数据
    start_time: float = 0.0
    end_time: Optional[float] = None
    
    def __post_init__(self):
        if self.history is None:
            self.history = []
        if self.injected_tasks is None:
            self.injected_tasks = []
        if self.context is None:
            self.context = {}
        if self.start_time == 0.0:
            self.start_time = time.time()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "graph_id": self.graph_id,
            "status": self.status.value,
            "current_node": self.current_node,
            "history": self.history,
            "injected_tasks": self.injected_tasks,
            "memory_updated": self.memory_updated,
            "context": self.context,
            "start_time": self.start_time,
            "end_time": self.end_time
        }

class NodeExecutor:
    """节点执行器基类"""
    
    def __init__(self, node_type: NodeType):
        self.node_type = node_type
        self.logger = logging.getLogger(f"NodeExecutor.{node_type.value}")
    
    def execute(self, node: TaskNode, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行节点任务
        
        Args:
            node: 任务节点
            context: 执行上下文
            
        Returns:
            Dict[str, Any]: 执行结果
        """
        raise NotImplementedError("子类必须实现execute方法")
    
    def validate_input(self, node: TaskNode, context: Dict[str, Any]) -> bool:
        """验证输入数据"""
        return True
    
    def validate_output(self, node: TaskNode, result: Dict[str, Any]) -> bool:
        """验证输出数据"""
        return True

class NavigationExecutor(NodeExecutor):
    """导航执行器"""
    
    def __init__(self):
        super().__init__(NodeType.NAVIGATION)
    
    def execute(self, node: TaskNode, context: Dict[str, Any]) -> Dict[str, Any]:
        """执行导航任务"""
        try:
            destination = context.get("destination", "")
            transport_mode = context.get("transport_mode", "walking")
            
            # 模拟导航执行
            self.logger.info(f"🚗 导航到: {destination}, 方式: {transport_mode}")
            
            return {
                "success": True,
                "route": f"导航路线到{destination}",
                "estimated_time": 30,
                "distance": 2.5,
                "transport_mode": transport_mode
            }
        except Exception as e:
            self.logger.error(f"❌ 导航执行失败: {e}")
            return {"success": False, "error": str(e)}

class InteractionExecutor(NodeExecutor):
    """交互执行器"""
    
    def __init__(self):
        super().__init__(NodeType.INTERACTION)
    
    def execute(self, node: TaskNode, context: Dict[str, Any]) -> Dict[str, Any]:
        """执行交互任务"""
        try:
            question = node.executor_config.get("question", "请确认")
            options = node.executor_config.get("options", [])
            
            self.logger.info(f"💬 用户交互: {question}")
            
            # 模拟用户响应
            response = "是"  # 实际应该通过语音识别获取
            
            return {
                "success": True,
                "question": question,
                "response": response,
                "options": options
            }
        except Exception as e:
            self.logger.error(f"❌ 交互执行失败: {e}")
            return {"success": False, "error": str(e)}

class ObservationExecutor(NodeExecutor):
    """观察执行器"""
    
    def __init__(self):
        super().__init__(NodeType.OBSERVATION)
    
    def execute(self, node: TaskNode, context: Dict[str, Any]) -> Dict[str, Any]:
        """执行观察任务"""
        try:
            observation_type = node.executor_config.get("type", "ocr")
            target = node.executor_config.get("target", "signboard")
            
            self.logger.info(f"👁️ 观察任务: {observation_type} - {target}")
            
            # 模拟观察结果
            result = {
                "success": True,
                "observation_type": observation_type,
                "target": target,
                "detected_objects": ["医院", "入口", "挂号处"],
                "confidence": 0.95
            }
            
            return result
        except Exception as e:
            self.logger.error(f"❌ 观察执行失败: {e}")
            return {"success": False, "error": str(e)}

class ContextTracker:
    """语义上下文与状态监控器"""
    
    def __init__(self):
        self.context_history: List[Dict[str, Any]] = []
        self.current_context: Dict[str, Any] = {}
        self.logger = logging.getLogger("ContextTracker")
    
    def update_context(self, key: str, value: Any, source: str = "system"):
        """更新上下文"""
        self.current_context[key] = {
            "value": value,
            "timestamp": time.time(),
            "source": source
        }
        
        # 记录历史
        self.context_history.append({
            "key": key,
            "value": value,
            "timestamp": time.time(),
            "source": source
        })
        
        self.logger.debug(f"📝 上下文更新: {key} = {value}")
    
    def get_context(self, key: str, default: Any = None) -> Any:
        """获取上下文值"""
        if key in self.current_context:
            return self.current_context[key]["value"]
        return default
    
    def clear_context(self):
        """清空上下文"""
        self.current_context.clear()
        self.logger.info("🧹 上下文已清空")

class MemoryBridge:
    """任务与记忆系统双向通道"""
    
    def __init__(self, memory_store):
        self.memory_store = memory_store
        self.logger = logging.getLogger("MemoryBridge")
    
    def save_task_experience(self, graph_id: str, execution_state: TaskExecutionState, result: Dict[str, Any]):
        """保存任务执行经验"""
        try:
            experience = {
                "graph_id": graph_id,
                "execution_time": execution_state.end_time - execution_state.start_time if execution_state.end_time else 0,
                "success": result.get("success", False),
                "nodes_completed": len(execution_state.history),
                "context": execution_state.context,
                "timestamp": time.time()
            }
            
            self.memory_store.add_memory(
                title=f"任务经验: {graph_id}",
                content=f"任务执行经验记录: {json.dumps(experience, ensure_ascii=False)}",
                memory_type="note",
                tags=["task_experience", graph_id],
                priority="normal"
            )
            
            self.logger.info(f"💾 任务经验已保存: {graph_id}")
        except Exception as e:
            self.logger.error(f"❌ 保存任务经验失败: {e}")
    
    def load_task_preferences(self, graph_id: str) -> Dict[str, Any]:
        """加载任务偏好"""
        try:
            memories = self.memory_store.search_memories(["task_experience", graph_id])
            if memories:
                # 解析最新的经验记录
                latest_memory = memories[0]
                # 这里应该解析content中的JSON数据
                return {"loaded": True, "preferences": latest_memory.content}
            return {"loaded": False}
        except Exception as e:
            self.logger.error(f"❌ 加载任务偏好失败: {e}")
            return {"loaded": False}

class TriggerRouter:
    """用户/系统行为触发器"""
    
    def __init__(self):
        self.triggers: Dict[str, List[Callable]] = {}
        self.logger = logging.getLogger("TriggerRouter")
    
    def register_trigger(self, event_type: str, callback: Callable):
        """注册触发器"""
        if event_type not in self.triggers:
            self.triggers[event_type] = []
        self.triggers[event_type].append(callback)
        self.logger.debug(f"🔗 注册触发器: {event_type}")
    
    def trigger_event(self, event_type: str, data: Dict[str, Any]):
        """触发事件"""
        if event_type in self.triggers:
            for callback in self.triggers[event_type]:
                try:
                    callback(data)
                except Exception as e:
                    self.logger.error(f"❌ 触发器执行失败: {e}")

class FallbackManager:
    """容错与中断机制"""
    
    def __init__(self):
        self.fallback_strategies: Dict[str, Callable] = {}
        self.logger = logging.getLogger("FallbackManager")
    
    def register_fallback(self, error_type: str, strategy: Callable):
        """注册容错策略"""
        self.fallback_strategies[error_type] = strategy
        self.logger.debug(f"🛡️ 注册容错策略: {error_type}")
    
    def handle_error(self, error: Exception, context: Dict[str, Any]) -> Dict[str, Any]:
        """处理错误"""
        error_type = type(error).__name__
        
        if error_type in self.fallback_strategies:
            try:
                return self.fallback_strategies[error_type](error, context)
            except Exception as e:
                self.logger.error(f"❌ 容错策略执行失败: {e}")
        
        # 默认容错策略
        return {
            "success": False,
            "error": str(error),
            "fallback": "default",
            "message": "任务执行失败，请重试"
        }

class TaskEngine:
    """任务中心核心调度器"""
    
    def __init__(self, memory_store=None):
        self.task_graphs: Dict[str, TaskGraph] = {}
        self.execution_states: Dict[str, TaskExecutionState] = {}
        self.executors: Dict[NodeType, NodeExecutor] = {}
        
        # 核心组件
        self.context_tracker = ContextTracker()
        self.memory_bridge = MemoryBridge(memory_store) if memory_store else None
        self.trigger_router = TriggerRouter()
        self.fallback_manager = FallbackManager()
        
        # 初始化执行器
        self._initialize_executors()
        
        # 注册默认触发器
        self._register_default_triggers()
        
        self.logger = logging.getLogger("TaskEngine")
        self.logger.info("🚀 Luna智能任务引擎初始化完成")
    
    def _initialize_executors(self):
        """初始化执行器"""
        self.executors[NodeType.NAVIGATION] = NavigationExecutor()
        self.executors[NodeType.INTERACTION] = InteractionExecutor()
        self.executors[NodeType.OBSERVATION] = ObservationExecutor()
        
        self.logger.info(f"✅ 已初始化 {len(self.executors)} 个执行器")
    
    def _register_default_triggers(self):
        """注册默认触发器"""
        self.trigger_router.register_trigger("task_started", self._on_task_started)
        self.trigger_router.register_trigger("task_completed", self._on_task_completed)
        self.trigger_router.register_trigger("task_failed", self._on_task_failed)
    
    def create_task(self, task_graph: TaskGraph) -> str:
        """创建任务流程"""
        self.task_graphs[task_graph.graph_id] = task_graph
        
        # 初始化执行状态
        execution_state = TaskExecutionState(
            graph_id=task_graph.graph_id,
            status=TaskStatus.PENDING
        )
        self.execution_states[task_graph.graph_id] = execution_state
        
        self.logger.info(f"📋 创建任务图: {task_graph.graph_id}")
        return task_graph.graph_id
    
    def start_task(self, graph_id: str) -> bool:
        """开始任务"""
        if graph_id not in self.task_graphs:
            self.logger.error(f"❌ 任务图不存在: {graph_id}")
            return False
        
        execution_state = self.execution_states[graph_id]
        execution_state.status = TaskStatus.ACTIVE
        execution_state.start_time = time.time()
        
        # 触发开始事件
        self.trigger_router.trigger_event("task_started", {"graph_id": graph_id})
        
        # 开始执行第一个节点
        self._execute_next_node(graph_id)
        
        self.logger.info(f"🚀 任务已启动: {graph_id}")
        return True
    
    def pause_task(self, graph_id: str) -> bool:
        """暂停任务"""
        if graph_id not in self.execution_states:
            return False
        
        execution_state = self.execution_states[graph_id]
        execution_state.status = TaskStatus.PAUSED
        
        self.logger.info(f"⏸️ 任务已暂停: {graph_id}")
        return True
    
    def resume_task(self, graph_id: str) -> bool:
        """恢复任务"""
        if graph_id not in self.execution_states:
            return False
        
        execution_state = self.execution_states[graph_id]
        execution_state.status = TaskStatus.ACTIVE
        
        # 继续执行当前节点
        self._execute_next_node(graph_id)
        
        self.logger.info(f"▶️ 任务已恢复: {graph_id}")
        return True
    
    def inject_task(self, graph_id: str, new_graph: TaskGraph, return_point: str) -> bool:
        """临时插入任务"""
        if graph_id not in self.execution_states:
            return False
        
        execution_state = self.execution_states[graph_id]
        execution_state.injected_tasks.append(new_graph.graph_id)
        
        # 创建新任务
        self.create_task(new_graph)
        self.start_task(new_graph.graph_id)
        
        self.logger.info(f"💉 注入任务: {new_graph.graph_id} -> {graph_id}")
        return True
    
    def update_node_state(self, node_id: str, status: str, context: Dict[str, Any] = None):
        """外部更新节点状态"""
        # 更新上下文
        if context:
            for key, value in context.items():
                self.context_tracker.update_context(key, value, "external")
        
        self.logger.info(f"🔄 节点状态更新: {node_id} -> {status}")
    
    def recall_task(self, graph_id: str) -> Optional[TaskGraph]:
        """调用历史任务"""
        if graph_id in self.task_graphs:
            return self.task_graphs[graph_id]
        
        # 从记忆中恢复
        if self.memory_bridge:
            preferences = self.memory_bridge.load_task_preferences(graph_id)
            if preferences.get("loaded"):
                # 这里应该根据记忆重建任务图
                pass
        
        return None
    
    def save_to_memory(self, graph_id: str) -> bool:
        """记忆化保存"""
        if graph_id not in self.execution_states:
            return False
        
        execution_state = self.execution_states[graph_id]
        
        if self.memory_bridge:
            self.memory_bridge.save_task_experience(graph_id, execution_state, {"success": True})
            execution_state.memory_updated = True
        
        self.logger.info(f"💾 任务已保存到记忆: {graph_id}")
        return True
    
    def _execute_next_node(self, graph_id: str):
        """执行下一个节点"""
        task_graph = self.task_graphs[graph_id]
        execution_state = self.execution_states[graph_id]
        
        # 找到下一个要执行的节点
        next_node_id = self._find_next_node(task_graph, execution_state)
        if not next_node_id:
            # 任务完成
            execution_state.status = TaskStatus.COMPLETED
            execution_state.end_time = time.time()
            self.trigger_router.trigger_event("task_completed", {"graph_id": graph_id})
            return
        
        # 执行节点
        next_node = self._get_node_by_id(task_graph, next_node_id)
        if next_node:
            self._execute_node(graph_id, next_node)
    
    def _find_next_node(self, task_graph: TaskGraph, execution_state: TaskExecutionState) -> Optional[str]:
        """找到下一个要执行的节点"""
        if not execution_state.current_node:
            # 找到第一个节点（没有前置条件的节点）
            for node in task_graph.nodes:
                if not node.precondition:
                    return node.id
        
        # 根据边找到下一个节点
        for edge in task_graph.edges:
            if edge.from_node == execution_state.current_node:
                # 检查条件
                if edge.condition:
                    if self._evaluate_condition(edge.condition, execution_state.context):
                        return edge.to_node
                else:
                    return edge.to_node
        
        return None
    
    def _get_node_by_id(self, task_graph: TaskGraph, node_id: str) -> Optional[TaskNode]:
        """根据ID获取节点"""
        for node in task_graph.nodes:
            if node.id == node_id:
                return node
        return None
    
    def _execute_node(self, graph_id: str, node: TaskNode):
        """执行节点"""
        execution_state = self.execution_states[graph_id]
        execution_state.current_node = node.id
        execution_state.history.append(node.id)
        
        try:
            # 获取执行器
            executor = self.executors.get(node.type)
            if not executor:
                raise ValueError(f"未找到执行器: {node.type}")
            
            # 执行节点
            result = executor.execute(node, execution_state.context)
            
            # 更新上下文
            if result.get("success"):
                for key, value in result.items():
                    if key != "success":
                        self.context_tracker.update_context(key, value, f"node_{node.id}")
            
            self.logger.info(f"✅ 节点执行完成: {node.id}")
            
            # 继续执行下一个节点
            self._execute_next_node(graph_id)
            
        except Exception as e:
            self.logger.error(f"❌ 节点执行失败: {node.id}: {e}")
            execution_state.status = TaskStatus.FAILED
            self.trigger_router.trigger_event("task_failed", {"graph_id": graph_id, "error": str(e)})
    
    def _evaluate_condition(self, condition: str, context: Dict[str, Any]) -> bool:
        """评估条件表达式"""
        # 简单的条件评估实现
        try:
            # 这里应该实现更复杂的条件评估逻辑
            return True
        except Exception as e:
            self.logger.error(f"❌ 条件评估失败: {e}")
            return False
    
    def _on_task_started(self, data: Dict[str, Any]):
        """任务开始回调"""
        self.logger.info(f"🎬 任务开始: {data['graph_id']}")
    
    def _on_task_completed(self, data: Dict[str, Any]):
        """任务完成回调"""
        graph_id = data['graph_id']
        self.logger.info(f"🎉 任务完成: {graph_id}")
        
        # 自动保存到记忆
        self.save_to_memory(graph_id)
    
    def _on_task_failed(self, data: Dict[str, Any]):
        """任务失败回调"""
        self.logger.error(f"💥 任务失败: {data['graph_id']}: {data['error']}")
    
    def get_task_status(self, graph_id: str) -> Optional[Dict[str, Any]]:
        """获取任务状态"""
        if graph_id not in self.execution_states:
            return None
        
        execution_state = self.execution_states[graph_id]
        task_graph = self.task_graphs[graph_id]
        
        return {
            "graph_id": graph_id,
            "status": execution_state.status.value,
            "current_node": execution_state.current_node,
            "progress": len(execution_state.history) / len(task_graph.nodes) * 100,
            "history": execution_state.history,
            "context": execution_state.context
        }


# 全局任务引擎实例
_global_task_engine: Optional[TaskEngine] = None

def get_task_engine(memory_store=None) -> TaskEngine:
    """获取全局任务引擎实例"""
    global _global_task_engine
    if _global_task_engine is None:
        _global_task_engine = TaskEngine(memory_store)
    return _global_task_engine


if __name__ == "__main__":
    # 测试任务引擎
    print("🚀 Luna智能任务引擎测试")
    print("=" * 60)
    
    # 创建任务引擎
    task_engine = get_task_engine()
    
    # 创建医院就诊任务图
    hospital_graph = TaskGraph(
        graph_id="hospital_visit",
        scene="healthcare",
        goal="完成一次就诊",
        nodes=[
            TaskNode(
                id="plan_route",
                type=NodeType.NAVIGATION,
                title="规划路线",
                description="导航到医院",
                input_schema={"destination": "string"},
                output_schema={"route": "string", "estimated_time": "number"},
                precondition=[],
                postcondition=["route_planned"],
                executor_config={"destination": "虹口医院", "transport_mode": "walking"}
            ),
            TaskNode(
                id="wait_register",
                type=NodeType.INTERACTION,
                title="等待挂号",
                description="等待叫号或确认挂号",
                input_schema={"queue_number": "string"},
                output_schema={"status": "string"},
                precondition=["route_planned"],
                postcondition=["registered"],
                executor_config={"question": "请确认是否已挂号", "options": ["是", "否"]}
            ),
            TaskNode(
                id="observe_signs",
                type=NodeType.OBSERVATION,
                title="观察指示牌",
                description="识别医院内的指示牌",
                input_schema={},
                output_schema={"detected_objects": "array"},
                precondition=["registered"],
                postcondition=["signs_identified"],
                executor_config={"type": "ocr", "target": "signboard"}
            )
        ],
        edges=[
            TaskEdge(from_node="plan_route", to_node="wait_register"),
            TaskEdge(from_node="wait_register", to_node="observe_signs")
        ]
    )
    
    # 创建并启动任务
    print("\n1. 创建任务图...")
    graph_id = task_engine.create_task(hospital_graph)
    print(f"   ✅ 任务图创建成功: {graph_id}")
    
    print("\n2. 启动任务...")
    success = task_engine.start_task(graph_id)
    print(f"   ✅ 任务启动: {success}")
    
    print("\n3. 检查任务状态...")
    status = task_engine.get_task_status(graph_id)
    if status:
        print(f"   📊 状态: {status['status']}")
        print(f"   📈 进度: {status['progress']:.1f}%")
        print(f"   🎯 当前节点: {status['current_node']}")
        print(f"   📝 历史: {status['history']}")
    
    print("\n🎉 Luna智能任务引擎测试完成！")
