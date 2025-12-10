# Luna Badge v1.4.3 – 全量 Blueprint（代码骨架规范）

**版本**: v1.4.3  
**创建日期**: 2025-12-05  
**状态**: 📋 待执行

---

## 📋 Blueprint 概述

此 Blueprint 包含九大部分：

1. 目录结构
2. 决策层（Decision Layer）
3. 上下文管理（Context Manager）
4. 决策规则（Decision Rules）
5. 任务链问询系统（Inquiry System）
6. 多模型调度器（Model Scheduler）
7. PlanB 触发模块（PlanB Trigger）
8. 日志模块（Logger）
9. 示例事件流（Cursor 验证专用）

---

## 1. 项目目录结构

```
luna_badge_v1_2/
  decision_layer/
      __init__.py
      decision_core.py
      context_manager.py
      decision_rules.py
      planb_trigger.py
      types.py
      logger.py
  
  task_chain/
      __init__.py
      task_chain_manager.py
      task_node.py
      task_repository.py
  
  inquiry_system/
      __init__.py
      inquiry_manager.py
      inquiry_templates.json
  
  model_scheduler/
      __init__.py
      scheduler.py
      model_registry.py
      health_monitor.py
      router_rules.py
  
  models/
      vision_main/
          __init__.py
          model.py
      vision_fallback/
          __init__.py
          model.py
      semantic_basic/
          __init__.py
          model.py
  
  events/
      __init__.py
      event_bus.py
      event_types.py
  
  shared/
      __init__.py
      system_state.py
      utils.py

  tests/
      test_decision_layer.py
      test_scheduler.py
      test_inquiry_system.py
```

---

## 2. 决策层（decision_layer）Blueprint

### (1) types.py

```python
# -*- coding: utf-8 -*-
"""
决策层类型定义
"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict, Any, Optional


class DecisionAction(Enum):
    """决策动作类型"""
    CONTINUE_TASK = "continue_task"
    INSERT_TASK = "insert_task"
    REPLACE_TASK = "replace_task"
    ASK_USER = "ask_user"
    TRIGGER_PLANB = "trigger_planB"
    NO_OP = "no_op"


class EventType(Enum):
    """事件类型"""
    USER_INTENT = "user_intent"
    TASK_NODE_COMPLETE = "task_node_complete"
    SCENE_UPDATED = "scene_updated"
    MODEL_STATUS = "model_status"
    SYSTEM_ALERT = "system_alert"


@dataclass
class DecisionInput:
    """决策输入"""
    event_type: EventType
    event_payload: Dict[str, Any]
    scene_context: Dict[str, Any]
    task_context: Dict[str, Any]
    user_context: Dict[str, Any]
    model_context: Dict[str, Any]


@dataclass
class DecisionOutput:
    """决策输出"""
    action: DecisionAction
    reason: str
    params: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.params is None:
            self.params = {}
```

### (2) decision_core.py

```python
# -*- coding: utf-8 -*-
"""
决策核心模块
"""

from .types import DecisionInput, DecisionOutput, DecisionAction
from . import context_manager, decision_rules, planb_trigger, logger


class DecisionCore:
    """决策核心类"""
    
    def __init__(self):
        self.logger = logger.get_logger("DecisionCore")
    
    def handle_event(self, decision_input: DecisionInput) -> DecisionOutput:
        """
        处理事件并生成决策
        
        Args:
            decision_input: 决策输入
            
        Returns:
            DecisionOutput: 决策输出
        """
        # 1. 合并上下文
        merged_ctx = context_manager.merge(decision_input)
        
        # 2. PlanB 条件检查
        if planb_trigger.should_trigger(merged_ctx):
            planb_trigger.trigger(merged_ctx)
            return DecisionOutput(
                action=DecisionAction.TRIGGER_PLANB,
                reason="planB_condition_matched",
                params={"context_snapshot": merged_ctx},
            )
        
        # 3. 规则层执行决策
        result = decision_rules.evaluate(merged_ctx)
        
        # 4. 日志
        logger.log_decision(merged_ctx, result)
        
        return result
```

### (3) context_manager.py

```python
# -*- coding: utf-8 -*-
"""
上下文管理器
"""

from .types import DecisionInput
from typing import Dict, Any


def merge(input_obj: DecisionInput) -> Dict[str, Any]:
    """
    将不同来源的信息合并为决策层统一上下文。
    
    Args:
        input_obj: 决策输入对象
        
    Returns:
        dict: 合并后的上下文
    """
    return {
        "event_type": input_obj.event_type,
        "event": input_obj.event_payload,
        "scene": input_obj.scene_context,
        "task": input_obj.task_context,
        "user": input_obj.user_context,
        "models": input_obj.model_context,
    }
```

### (4) decision_rules.py

```python
# -*- coding: utf-8 -*-
"""
决策规则模块
"""

from .types import DecisionOutput, DecisionAction, EventType
from typing import Dict, Any


def evaluate(ctx: Dict[str, Any]) -> DecisionOutput:
    """
    根据上下文评估并生成决策
    
    Args:
        ctx: 合并后的上下文
        
    Returns:
        DecisionOutput: 决策输出
    """
    et = ctx["event_type"]
    
    if et == EventType.USER_INTENT:
        return _handle_user_intent(ctx)
    
    if et == EventType.TASK_NODE_COMPLETE:
        return _handle_task_node_complete(ctx)
    
    if et == EventType.SCENE_UPDATED:
        return _handle_scene_change(ctx)
    
    if et == EventType.MODEL_STATUS:
        return _handle_model_status(ctx)
    
    return DecisionOutput(
        action=DecisionAction.NO_OP,
        reason="no_rule_matched",
        params={}
    )


def _handle_user_intent(ctx: Dict[str, Any]) -> DecisionOutput:
    """处理用户意图事件"""
    # TODO: 实现用户意图处理逻辑
    return DecisionOutput(
        action=DecisionAction.NO_OP,
        reason="user_intent_not_implemented",
        params={}
    )


def _handle_task_node_complete(ctx: Dict[str, Any]) -> DecisionOutput:
    """处理任务节点完成事件"""
    task = ctx.get("task", {})
    active_node = task.get("active_node", {})
    
    # 检查是否需要用户确认
    if active_node.get("requires_user_confirmation", False):
        return DecisionOutput(
            action=DecisionAction.ASK_USER,
            reason="node_requires_confirmation",
            params={
                "node_id": active_node.get("id"),
                "question_type": "confirm_completion"
            }
        )
    
    # 检查是否有下一个节点
    next_node = task.get("next_node")
    if next_node:
        return DecisionOutput(
            action=DecisionAction.CONTINUE_TASK,
            reason="next_node_available",
            params={"next_node": next_node}
        )
    
    return DecisionOutput(
        action=DecisionAction.NO_OP,
        reason="task_complete",
        params={}
    )


def _handle_scene_change(ctx: Dict[str, Any]) -> DecisionOutput:
    """处理场景变化事件"""
    # TODO: 实现场景变化处理逻辑
    return DecisionOutput(
        action=DecisionAction.NO_OP,
        reason="scene_change_not_implemented",
        params={}
    )


def _handle_model_status(ctx: Dict[str, Any]) -> DecisionOutput:
    """处理模型状态事件"""
    # TODO: 实现模型状态处理逻辑
    return DecisionOutput(
        action=DecisionAction.NO_OP,
        reason="model_status_not_implemented",
        params={}
    )
```

### (5) planb_trigger.py

```python
# -*- coding: utf-8 -*-
"""
PlanB 触发模块
"""

from typing import Dict, Any
from . import logger


def should_trigger(ctx: Dict[str, Any]) -> bool:
    """
    检查是否应该触发 PlanB
    
    Args:
        ctx: 上下文
        
    Returns:
        bool: 是否触发 PlanB
    """
    models = ctx.get("models", {})
    
    # 检查主模型和备用模型是否都不可用
    vision_main = models.get("vision_main")
    vision_fallback = models.get("vision_fallback")
    
    if vision_main == "down" and vision_fallback == "down":
        return True
    
    return False


def trigger(ctx: Dict[str, Any]) -> None:
    """
    触发 PlanB 应急方案
    
    Args:
        ctx: 上下文
    """
    logger.get_logger("PlanBTrigger").warning(
        "[PlanB Trigger] Emergency detected: %s", ctx
    )
    # TODO: 实现 PlanB 实际逻辑
    print("[PlanB Trigger] Emergency detected:", ctx)
```

### (6) logger.py

```python
# -*- coding: utf-8 -*-
"""
决策层日志模块
"""

import logging
from typing import Dict, Any
from .types import DecisionOutput


_loggers = {}


def get_logger(name: str) -> logging.Logger:
    """
    获取日志器
    
    Args:
        name: 日志器名称
        
    Returns:
        logging.Logger: 日志器实例
    """
    if name not in _loggers:
        _loggers[name] = logging.getLogger(f"decision_layer.{name}")
    return _loggers[name]


def log_decision(ctx: Dict[str, Any], result: DecisionOutput) -> None:
    """
    记录决策日志
    
    Args:
        ctx: 上下文
        result: 决策输出
    """
    logger = get_logger("DecisionLogger")
    logger.info(
        "[Decision] ctx=%s → action=%s reason=%s",
        ctx,
        result.action.value,
        result.reason
    )
```

### (7) __init__.py

```python
# -*- coding: utf-8 -*-
"""
决策层模块
"""

from .decision_core import DecisionCore
from .types import DecisionInput, DecisionOutput, DecisionAction, EventType

__all__ = [
    "DecisionCore",
    "DecisionInput",
    "DecisionOutput",
    "DecisionAction",
    "EventType",
]
```

---

## 3. 任务链问询系统（inquiry_system）Blueprint

### inquiry_manager.py

```python
# -*- coding: utf-8 -*-
"""
问询系统管理器
"""

import json
import os
from typing import Dict, Any, Optional


class InquiryManager:
    """问询管理器"""
    
    def __init__(self, templates_path: Optional[str] = None):
        """
        初始化问询管理器
        
        Args:
            templates_path: 问询模板文件路径
        """
        if templates_path is None:
            templates_path = os.path.join(
                os.path.dirname(__file__),
                "inquiry_templates.json"
            )
        self.templates_path = templates_path
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict[str, Any]:
        """加载问询模板"""
        if os.path.exists(self.templates_path):
            with open(self.templates_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}
    
    def ask(self, question_type: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        返回问询结构，等待用户回答。
        
        Args:
            question_type: 问题类型
            context: 上下文信息
            
        Returns:
            dict: 问询结构
        """
        # 从模板加载问句
        template = self.templates.get(question_type, {})
        question = template.get("question", "请确认")
        options = template.get("options", ["是", "否"])
        
        return {
            "type": "inquiry",
            "question_type": question_type,
            "question": question,
            "options": options,
            "context": context
        }
    
    def parse_response(self, user_text: str) -> Dict[str, Any]:
        """
        将用户回答解析为结构化意图。
        
        示例输出：
        { "intent_type": "CONFIRM" }
        
        Args:
            user_text: 用户回答文本
            
        Returns:
            dict: 解析后的意图
        """
        # 简易解析（1.4.3 不需要 NLP）
        user_text_lower = user_text.lower().strip()
        
        # 确认类回答
        confirm_keywords = ["是", "是的", "对", "确认", "ok", "yes", "y"]
        if any(keyword in user_text_lower for keyword in confirm_keywords):
            return {"intent_type": "CONFIRM"}
        
        # 否定类回答
        deny_keywords = ["否", "不是", "不对", "取消", "no", "n"]
        if any(keyword in user_text_lower for keyword in deny_keywords):
            return {"intent_type": "DENY"}
        
        # 默认返回未知
        return {"intent_type": "UNKNOWN"}
```

### inquiry_templates.json

```json
{
  "confirm_completion": {
    "question": "您已完成当前任务节点，是否继续？",
    "options": ["是", "否"]
  },
  "confirm_location": {
    "question": "您是否已到达目标位置？",
    "options": ["是", "否"]
  },
  "confirm_action": {
    "question": "是否执行此操作？",
    "options": ["是", "否"]
  }
}
```

### __init__.py

```python
# -*- coding: utf-8 -*-
"""
问询系统模块
"""

from .inquiry_manager import InquiryManager

__all__ = ["InquiryManager"]
```

---

## 4. 多模型调度器（model_scheduler）Blueprint

### scheduler.py

```python
# -*- coding: utf-8 -*-
"""
模型调度器
"""

from typing import Dict, Any, Optional, List
from .model_registry import ModelRegistry
from .health_monitor import HealthMonitor
from .router_rules import RouterRules


class ModelScheduler:
    """模型调度器"""
    
    def __init__(self):
        self.registry = ModelRegistry()
        self.health_monitor = HealthMonitor()
        self.router_rules = RouterRules()
        self.models = {}
    
    def load_models(self) -> None:
        """加载所有模型"""
        self.models = self.registry.load_all()
        self.health_monitor.register_models(self.models)
    
    def select_model(self, task_type: str, context: Dict[str, Any] = None) -> Optional[Any]:
        """
        根据任务类型选择模型
        
        Args:
            task_type: 任务类型
            context: 上下文信息
            
        Returns:
            模型实例或 None
        """
        if context is None:
            context = {}
        
        # 使用路由规则选择模型
        model_name = self.router_rules.select(task_type, context)
        
        # 检查模型健康状态
        if not self.health_monitor.is_healthy(model_name):
            # 尝试备用模型
            model_name = self.router_rules.select_fallback(task_type, context)
        
        return self.models.get(model_name)
    
    def infer(self, model: Any, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行推理，并返回统一格式
        
        Args:
            model: 模型实例
            input_data: 输入数据
            
        Returns:
            dict: 推理结果
        """
        try:
            output = model.infer(input_data)
            return {
                "success": True,
                "data": output,
                "model_used": model.name if hasattr(model, "name") else "unknown"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "model_used": model.name if hasattr(model, "name") else "unknown"
            }
    
    def fallback_strategy(self, task_type: str) -> Optional[Any]:
        """
        主模型失败后的备选策略
        
        Args:
            task_type: 任务类型
            
        Returns:
            备用模型实例或 None
        """
        return self.models.get("vision_fallback")
```

### model_registry.py

```python
# -*- coding: utf-8 -*-
"""
模型注册表
"""

from typing import Dict, Any


class ModelRegistry:
    """模型注册表"""
    
    def __init__(self):
        self._models = {}
    
    def register(self, name: str, model: Any) -> None:
        """
        注册模型
        
        Args:
            name: 模型名称
            model: 模型实例
        """
        self._models[name] = model
    
    def load_all(self) -> Dict[str, Any]:
        """
        加载所有模型
        
        Returns:
            dict: 模型字典
        """
        # TODO: 实际加载模型
        return self._models
    
    def get(self, name: str) -> Any:
        """
        获取模型
        
        Args:
            name: 模型名称
            
        Returns:
            模型实例或 None
        """
        return self._models.get(name)
```

### health_monitor.py

```python
# -*- coding: utf-8 -*-
"""
模型健康监控
"""

from typing import Dict, Any, Set


class HealthMonitor:
    """模型健康监控器"""
    
    def __init__(self):
        self._models: Dict[str, Any] = {}
        self._health_status: Dict[str, str] = {}
    
    def register_models(self, models: Dict[str, Any]) -> None:
        """
        注册模型
        
        Args:
            models: 模型字典
        """
        self._models = models
        # 初始化所有模型为健康状态
        for name in models.keys():
            self._health_status[name] = "ok"
    
    def is_healthy(self, model_name: str) -> bool:
        """
        检查模型是否健康
        
        Args:
            model_name: 模型名称
            
        Returns:
            bool: 是否健康
        """
        status = self._health_status.get(model_name, "unknown")
        return status == "ok"
    
    def update_status(self, model_name: str, status: str) -> None:
        """
        更新模型状态
        
        Args:
            model_name: 模型名称
            status: 状态（"ok" 或 "down"）
        """
        self._health_status[model_name] = status
```

### router_rules.py

```python
# -*- coding: utf-8 -*-
"""
路由规则
"""

from typing import Dict, Any, Optional


class RouterRules:
    """路由规则"""
    
    def select(self, task_type: str, context: Dict[str, Any] = None) -> str:
        """
        根据任务类型选择模型
        
        Args:
            task_type: 任务类型
            context: 上下文信息
            
        Returns:
            str: 模型名称
        """
        # 默认路由规则
        if task_type == "vision":
            return "vision_main"
        elif task_type == "semantic":
            return "semantic_basic"
        else:
            return "vision_main"
    
    def select_fallback(self, task_type: str, context: Dict[str, Any] = None) -> str:
        """
        选择备用模型
        
        Args:
            task_type: 任务类型
            context: 上下文信息
            
        Returns:
            str: 备用模型名称
        """
        if task_type == "vision":
            return "vision_fallback"
        else:
            return "vision_fallback"
```

### __init__.py

```python
# -*- coding: utf-8 -*-
"""
模型调度器模块
"""

from .scheduler import ModelScheduler
from .model_registry import ModelRegistry
from .health_monitor import HealthMonitor
from .router_rules import RouterRules

__all__ = [
    "ModelScheduler",
    "ModelRegistry",
    "HealthMonitor",
    "RouterRules",
]
```

---

## 5. 任务链（task_chain）Blueprint

### task_node.py

```python
# -*- coding: utf-8 -*-
"""
任务节点
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional, List


@dataclass
class TaskNode:
    """任务节点"""
    id: str
    name: str
    description: str
    requires_user_confirmation: bool = False
    next_node_id: Optional[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
```

### task_chain_manager.py

```python
# -*- coding: utf-8 -*-
"""
任务链管理器
"""

from typing import Dict, Any, Optional, List
from .task_node import TaskNode
from .task_repository import TaskRepository


class TaskChainManager:
    """任务链管理器"""
    
    def __init__(self):
        self.repository = TaskRepository()
        self.current_node: Optional[TaskNode] = None
        self.chain: List[TaskNode] = []
    
    def load_chain(self, chain_id: str) -> None:
        """
        加载任务链
        
        Args:
            chain_id: 任务链 ID
        """
        self.chain = self.repository.get_chain(chain_id)
        if self.chain:
            self.current_node = self.chain[0]
    
    def get_current_node(self) -> Optional[TaskNode]:
        """
        获取当前节点
        
        Returns:
            当前节点或 None
        """
        return self.current_node
    
    def move_to_next(self) -> bool:
        """
        移动到下一个节点
        
        Returns:
            bool: 是否成功移动
        """
        if not self.current_node:
            return False
        
        next_id = self.current_node.next_node_id
        if not next_id:
            return False
        
        # 查找下一个节点
        for node in self.chain:
            if node.id == next_id:
                self.current_node = node
                return True
        
        return False
```

### task_repository.py

```python
# -*- coding: utf-8 -*-
"""
任务仓库
"""

from typing import Dict, Any, List
from .task_node import TaskNode


class TaskRepository:
    """任务仓库"""
    
    def __init__(self):
        self._chains: Dict[str, List[TaskNode]] = {}
    
    def get_chain(self, chain_id: str) -> List[TaskNode]:
        """
        获取任务链
        
        Args:
            chain_id: 任务链 ID
            
        Returns:
            任务节点列表
        """
        return self._chains.get(chain_id, [])
    
    def save_chain(self, chain_id: str, chain: List[TaskNode]) -> None:
        """
        保存任务链
        
        Args:
            chain_id: 任务链 ID
            chain: 任务节点列表
        """
        self._chains[chain_id] = chain
```

### __init__.py

```python
# -*- coding: utf-8 -*-
"""
任务链模块
"""

from .task_chain_manager import TaskChainManager
from .task_node import TaskNode
from .task_repository import TaskRepository

__all__ = [
    "TaskChainManager",
    "TaskNode",
    "TaskRepository",
]
```

---

## 6. 事件系统（events）Blueprint

### event_types.py

```python
# -*- coding: utf-8 -*-
"""
事件类型定义
"""

from enum import Enum


class EventType(Enum):
    """事件类型"""
    USER_INTENT = "user_intent"
    TASK_NODE_COMPLETE = "task_node_complete"
    SCENE_UPDATED = "scene_updated"
    MODEL_STATUS = "model_status"
    SYSTEM_ALERT = "system_alert"
```

### event_bus.py

```python
# -*- coding: utf-8 -*-
"""
事件总线
"""

from typing import Dict, Any, List, Callable
from .event_types import EventType


class EventBus:
    """事件总线"""
    
    def __init__(self):
        self._handlers: Dict[EventType, List[Callable]] = {}
    
    def subscribe(self, event_type: EventType, handler: Callable) -> None:
        """
        订阅事件
        
        Args:
            event_type: 事件类型
            handler: 处理函数
        """
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)
    
    def publish(self, event_type: EventType, payload: Dict[str, Any]) -> None:
        """
        发布事件
        
        Args:
            event_type: 事件类型
            payload: 事件负载
        """
        handlers = self._handlers.get(event_type, [])
        for handler in handlers:
            try:
                handler(payload)
            except Exception as e:
                print(f"Error in event handler: {e}")
```

### __init__.py

```python
# -*- coding: utf-8 -*-
"""
事件系统模块
"""

from .event_bus import EventBus
from .event_types import EventType

__all__ = ["EventBus", "EventType"]
```

---

## 7. 共享模块（shared）Blueprint

### system_state.py

```python
# -*- coding: utf-8 -*-
"""
系统状态
"""

from typing import Dict, Any
from dataclasses import dataclass, field


@dataclass
class SystemState:
    """系统状态"""
    current_task: str = ""
    current_node: str = ""
    user_location: str = ""
    model_status: Dict[str, str] = field(default_factory=dict)
    system_mode: str = "normal"  # normal, planB, emergency
```

### utils.py

```python
# -*- coding: utf-8 -*-
"""
工具函数
"""

from typing import Dict, Any


def merge_dicts(*dicts: Dict[str, Any]) -> Dict[str, Any]:
    """
    合并多个字典
    
    Args:
        *dicts: 多个字典
        
    Returns:
        合并后的字典
    """
    result = {}
    for d in dicts:
        result.update(d)
    return result
```

### __init__.py

```python
# -*- coding: utf-8 -*-
"""
共享模块
"""

from .system_state import SystemState
from .utils import merge_dicts

__all__ = ["SystemState", "merge_dicts"]
```

---

## 8. 示例事件流（Cursor 验证用）

### 示例代码

```python
# -*- coding: utf-8 -*-
"""
示例事件流测试
"""

from decision_layer import DecisionCore, DecisionInput, EventType

# 创建决策核心
decision_core = DecisionCore()

# 任务节点结束 → 决策层 → 问询系统
decision_input = DecisionInput(
    event_type=EventType.TASK_NODE_COMPLETE,
    event_payload={"node_id": "hospital_entrance"},
    scene_context={"location": "hospital_gate"},
    task_context={
        "active_node": {
            "id": "hospital_entrance",
            "requires_user_confirmation": True
        }
    },
    user_context={},
    model_context={"vision_main": "ok", "vision_fallback": "ok"},
)

# 执行决策
result = decision_core.handle_event(decision_input)

# 期望输出：
# DecisionOutput(
#     action=DecisionAction.ASK_USER,
#     reason="node_requires_confirmation",
#     params={"node_id": "hospital_entrance", "question_type": "confirm_completion"}
# )

print(f"Decision: {result.action.value}, Reason: {result.reason}")
```

---

## 9. 测试文件（tests）Blueprint

### test_decision_layer.py

```python
# -*- coding: utf-8 -*-
"""
决策层测试
"""

import unittest
from decision_layer import DecisionCore, DecisionInput, EventType, DecisionAction


class TestDecisionLayer(unittest.TestCase):
    """决策层测试类"""
    
    def setUp(self):
        self.decision_core = DecisionCore()
    
    def test_task_node_complete_with_confirmation(self):
        """测试需要确认的任务节点完成"""
        decision_input = DecisionInput(
            event_type=EventType.TASK_NODE_COMPLETE,
            event_payload={"node_id": "hospital_entrance"},
            scene_context={},
            task_context={
                "active_node": {
                    "id": "hospital_entrance",
                    "requires_user_confirmation": True
                }
            },
            user_context={},
            model_context={},
        )
        
        result = self.decision_core.handle_event(decision_input)
        
        self.assertEqual(result.action, DecisionAction.ASK_USER)
        self.assertEqual(result.reason, "node_requires_confirmation")
```

### test_scheduler.py

```python
# -*- coding: utf-8 -*-
"""
调度器测试
"""

import unittest
from model_scheduler import ModelScheduler


class TestScheduler(unittest.TestCase):
    """调度器测试类"""
    
    def setUp(self):
        self.scheduler = ModelScheduler()
    
    def test_select_model(self):
        """测试模型选择"""
        model = self.scheduler.select_model("vision")
        # TODO: 添加断言
        pass
```

---

## ✅ Blueprint 执行检查清单

### 目录结构

- [ ] 创建所有目录
- [ ] 创建所有 `__init__.py` 文件
- [ ] 验证目录结构正确

### 代码文件

- [ ] 创建所有 Python 文件
- [ ] 实现所有类和方法
- [ ] 添加类型注解
- [ ] 添加文档字符串

### 测试文件

- [ ] 创建测试文件
- [ ] 实现测试用例
- [ ] 运行测试验证

### 配置文件

- [ ] 创建 `inquiry_templates.json`
- [ ] 验证 JSON 格式正确

---

## 📝 执行说明

### 给 Cursor 的指令

```
请按照 BLUEPRINT_v1.4.3.md 中的规范，创建 v1.4.3 版本的完整代码骨架。

要求：
1. 严格按照 Blueprint 中的目录结构创建文件
2. 所有代码必须符合 Python 工程化标准
3. 所有类和方法必须有类型注解和文档字符串
4. 创建完成后运行测试验证
```

---

**Blueprint 状态**: ✅ 已完成  
**可执行状态**: ✅ 可以给 Cursor 执行  
**版本**: v1.4.3


