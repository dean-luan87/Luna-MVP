# core/flow_engine/flow_types.py
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Any, List, Optional, Callable


class FlowNodeType(str, Enum):
    QUERY_USER = "query_user"
    NAVIGATE = "navigate"
    OCR_READ = "ocr_read"
    VISION_SCAN = "vision_scan"
    WAIT_EVENT = "wait_event"
    LOGIC_DECISION = "logic_decision"
    CUSTOM = "custom"


@dataclass
class FlowNode:
    id: str
    node_type: FlowNodeType
    params: Dict[str, Any] = field(default_factory=dict)
    executor: Optional[Callable[['FlowContext', Dict[str, Any]], Any]] = None


@dataclass
class FlowEdge:
    source_id: str
    target_id: str
    condition: Optional[str] = None  # e.g. "success", "failure", None


@dataclass
class FlowContext:
    task_id: str
    user_id: str
    scene_type: str
    intent: str
    data: Dict[str, Any] = field(default_factory=dict)

    def append_prompt(self, text: str) -> None:
        prompts = self.data.get("prompts")
        if prompts is None:
            prompts = []
            self.data["prompts"] = prompts
        prompts.append(text)


@dataclass
class FlowDefinition:
    id: str
    nodes: Dict[str, FlowNode]
    edges: List[FlowEdge]
    entry_node_id: str
    # Hook 点映射：{hook_point: node_id}，用于 CompositionEngine 定位插入点
    hook_points: Dict[str, str] = field(default_factory=dict)
    # 元信息，用于存放 hook_points 列表等扩展信息
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FlowInstance:
    definition: FlowDefinition
    context: FlowContext
    current_node_id: str
    finished: bool = False
    paused: bool = False
    parent_task_id: Optional[str] = None


@dataclass
class PlanningInput:
    user_id: str
    intent: str
    scene_type: str
    raw_utterance: str
    extra: Optional[Dict[str, Any]] = None
