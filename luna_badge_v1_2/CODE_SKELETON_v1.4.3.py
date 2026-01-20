# -*- coding: utf-8 -*-
"""
Luna Badge v1.4.3 - 关键代码骨架模板
给 Cursor 当起步代码
"""

# ============================================================
# 1) /core/intent_schema.py
# ============================================================

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class ParsedIntent:
    intent_name: str          # e.g. INSERT_TASK, CHANGE_DESTINATION, CONFIRM, REJECT, RESUME_MAIN_TASK, AMBIGUOUS, UNKNOWN
    slots: Dict = None        # structured args, like {"task_type": "toilet"}
    source: str = "inquiry"   # "inquiry" | "asr" | "system"
    need_confirm: bool = False
    raw: str = ""
    
    def __post_init__(self):
        if self.slots is None:
            self.slots = {}


# ============================================================
# 2) /core/decision_actions.py
# ============================================================

from enum import Enum


class DecisionAction(Enum):
    CONTINUE_TASK = "continue_task"
    INSERT_TASK = "insert_task"
    REPLACE_TASK = "replace_task"
    RESUME_MAIN_TASK = "resume_main_task"
    NO_OP = "no_op"
    ASK_USER = "ask_user"
    TRIGGER_PLANB = "trigger_planB"


# ============================================================
# 3) /core/decision_output.py
# ============================================================

from dataclasses import dataclass
from typing import Dict
from .decision_actions import DecisionAction


@dataclass
class DecisionOutput:
    action: DecisionAction
    params: Dict
    narration: str = ""
    
    def __post_init__(self):
        if self.params is None:
            self.params = {}


# ============================================================
# 4) /core/task_result.py
# ============================================================

from dataclasses import dataclass


@dataclass
class TaskResult:
    status: str          # "ok" | "failed" | "cancelled"
    reason: str
    task_id: str
    task_type: str


# ============================================================
# 5) /core/events.py
# ============================================================

from enum import Enum


class EventType(Enum):
    TASK_NODE_COMPLETE = "task_node_complete"
    USER_INTENT = "user_intent"
    INQUIRY_RESPONSE = "inquiry_response"
    SYSTEM_ALERT = "system_alert"
    USER_INACTIVE = "user_inactive"
    MODEL_STATUS = "model_status"
    TASK_NODE_START = "task_node_start"


# ============================================================
# 6) /taskchain/manager.py（骨架）
# ============================================================

from typing import List, Dict, Optional
from core.decision_output import DecisionOutput
from core.decision_actions import DecisionAction
from core.task_result import TaskResult


class TaskChainManager:
    def __init__(self):
        self.main_task: Optional[Dict] = None
        self.sub_task_stack: List[Dict] = []
        self.active_task: Optional[Dict] = None
        self.active_node: Optional[Dict] = None
        self.main_task_state: Optional[Dict] = None

    def start_main_task(self, task_spec: Dict):
        """启动主任务"""
        self.main_task = task_spec
        self.active_task = task_spec
        # TODO: init active_node, main_task_state
        if task_spec.get("nodes"):
            self.active_node = task_spec["nodes"][0]

    def advance(self):
        """推进到下一节点"""
        # TODO: move to next node
        if self.active_task and self.active_task.get("nodes"):
            current_index = 0
            for i, node in enumerate(self.active_task["nodes"]):
                if node.get("id") == self.active_node.get("id"):
                    current_index = i
                    break
            
            if current_index + 1 < len(self.active_task["nodes"]):
                self.active_node = self.active_task["nodes"][current_index + 1]
            else:
                # 任务完成
                self.active_node = None

    def complete_active_node(self) -> TaskResult:
        """完成当前节点"""
        # TODO: mark node complete, decide if task finished
        if self.active_task:
            return TaskResult(
                status="ok",
                reason="",
                task_id=self.active_task.get("task_id", ""),
                task_type=self.active_task.get("type", "")
            )
        return TaskResult(status="failed", reason="no_active_task", task_id="", task_type="")

    def insert_task(self, task_spec: Dict, resume_strategy: str = "auto"):
        """插入子任务"""
        # TODO: push current main task state and switch to sub task
        # 1. 保存主任务状态
        if self.main_task and self.active_task == self.main_task:
            self.main_task_state = {
                "task": self.main_task,
                "node": self.active_node,
                "timestamp": time.time()
            }
        
        # 2. 压入子任务栈
        self.sub_task_stack.append({
            "task": task_spec,
            "resume_strategy": resume_strategy
        })
        
        # 3. 切换活动任务
        self.active_task = task_spec
        if task_spec.get("nodes"):
            self.active_node = task_spec["nodes"][0]
        
        return {"status": "ok", "task": task_spec}

    def _replace_task(self, new_task_spec: Dict):
        """替换任务"""
        # TODO: clear stack and switch main_task
        # 1. 清空子任务栈
        self.sub_task_stack.clear()
        
        # 2. 替换主任务
        self.main_task = new_task_spec
        self.active_task = new_task_spec
        self.main_task_state = None
        
        # 3. 重置节点
        if new_task_spec.get("nodes"):
            self.active_node = new_task_spec["nodes"][0]
        
        return {"status": "replaced", "task": new_task_spec}

    def complete_active_task(self) -> Dict:
        """完成当前活动任务"""
        # TODO: pop from sub_task_stack and resume
        if not self.sub_task_stack:
            # 主任务完成
            return {"status": "main_task_complete", "task": self.main_task}
        
        # 弹出完成的子任务
        finished = self.sub_task_stack.pop()
        
        if finished["resume_strategy"] == "auto":
            return self.resume_main_task()
        elif finished["resume_strategy"] == "ask":
            return {
                "action": "ASK_USER",
                "question": "是否继续之前的任务？",
                "resume_context": self.main_task_state
            }
        
        return {"status": "completed", "task": finished["task"]}

    def resume_main_task(self):
        """恢复主任务"""
        # TODO: restore main_task_state
        if not self.main_task or not self.main_task_state:
            return {
                "status": "error",
                "reason": "no_main_task_to_resume"
            }
        
        # 恢复主任务状态
        self.active_task = self.main_task
        self.active_node = self.main_task_state["node"]
        
        return {
            "status": "resumed",
            "task": self.main_task,
            "node": self.active_node
        }

    def apply_decision(self, decision_output: DecisionOutput):
        """统一执行决策输出"""
        if decision_output.action == DecisionAction.CONTINUE_TASK:
            self.advance()
        elif decision_output.action == DecisionAction.INSERT_TASK:
            self.insert_task(
                decision_output.params["insert_task_spec"],
                decision_output.params.get("resume_strategy", "auto"),
            )
        elif decision_output.action == DecisionAction.REPLACE_TASK:
            self._replace_task(decision_output.params["new_task_spec"])
        # ASK_USER / TRIGGER_PLANB / NO_OP handled by upper layer


# ============================================================
# 7) /inquiry/parser.py（骨架）
# ============================================================

from core.intent_schema import ParsedIntent


class InquiryParser:
    def parse(self, text: str, tpl: dict) -> ParsedIntent:
        normalized = text.strip().lower()

        # 1. synonyms
        for key, syns in tpl.get("synonyms", {}).items():
            for s in syns:
                if s in normalized:
                    intent_name = tpl["map"][key]
                    return ParsedIntent(
                        intent_name=intent_name,
                        slots={},
                        source="inquiry",
                        need_confirm=False,
                        raw=text
                    )

        # 2. direct options
        for opt in tpl.get("options", []):
            if opt in normalized:
                intent_name = tpl["map"][opt]
                return ParsedIntent(
                    intent_name=intent_name,
                    slots={},
                    source="inquiry",
                    need_confirm=False,
                    raw=text
                )

        # 3. special intents
        special = self._parse_special_intents(normalized)
        if special:
            return ParsedIntent(
                intent_name=special["intent_name"],
                slots=special.get("slots", {}),
                source="inquiry",
                need_confirm=True,
                raw=text
            )

        # 4. unknown
        return ParsedIntent(
            intent_name="UNKNOWN",
            slots={},
            source="inquiry",
            need_confirm=False,
            raw=text
        )

    def _parse_special_intents(self, text: str):
        """解析特殊指令"""
        if "厕所" in text:
            return {"intent_name": "INSERT_TASK", "slots": {"task_type": "toilet"}}
        if "换" in text or "改" in text:
            return {"intent_name": "CHANGE_DESTINATION", "slots": {}}
        if "买" in text:
            return {"intent_name": "INSERT_TASK", "slots": {"task_type": "buy"}}
        return None


# ============================================================
# 8) /decision/decision_core.py（骨架）
# ============================================================

from core.decision_output import DecisionOutput
from core.decision_actions import DecisionAction
from core.intent_schema import ParsedIntent
from core.events import EventType


class DecisionCore:
    def handle_event(self, event_type: EventType, payload: dict, context: dict) -> DecisionOutput:
        """处理事件并生成决策"""
        if event_type == EventType.USER_INTENT:
            parsed_intent = payload.get("parsed_intent")
            return self.handle_user_intent(parsed_intent, context)
        elif event_type == EventType.TASK_NODE_COMPLETE:
            return self.handle_task_node_complete(payload, context)
        elif event_type == EventType.MODEL_STATUS:
            return self.handle_model_status(payload, context)
        else:
            return DecisionOutput(
                action=DecisionAction.NO_OP,
                params={},
                narration=""
            )
    
    def handle_user_intent(self, parsed_intent: ParsedIntent, context: dict) -> DecisionOutput:
        """处理用户意图"""
        name = parsed_intent.intent_name

        if name == "INSERT_TASK":
            task_spec = self._build_task_from_slots(parsed_intent.slots)
            return DecisionOutput(
                action=DecisionAction.INSERT_TASK,
                params={"insert_task_spec": task_spec, "resume_strategy": "auto"},
                narration="好的，我先帮你处理这件事。"
            )

        if name == "CHANGE_DESTINATION":
            new_task = self._build_task_from_slots(parsed_intent.slots)
            return DecisionOutput(
                action=DecisionAction.REPLACE_TASK,
                params={"new_task_spec": new_task},
                narration="明白了，我帮你更改目的地。"
            )

        if name in ["RESUME_MAIN_TASK", "CONFIRM"]:
            return DecisionOutput(
                action=DecisionAction.CONTINUE_TASK,
                params={},
                narration="好的，我继续执行之前的任务。"
            )

        if name in ["REJECT", "AMBIGUOUS", "UNKNOWN"]:
            return DecisionOutput(
                action=DecisionAction.NO_OP,
                params={},
                narration="那我先保持当前状态。"
            )

        return DecisionOutput(
            action=DecisionAction.NO_OP,
            params={},
            narration="好的。"
        )

    def handle_task_node_complete(self, payload: dict, context: dict) -> DecisionOutput:
        """处理任务节点完成"""
        # TODO: 实现节点完成逻辑
        node = payload.get("node", {})
        if node.get("requires_user_confirmation"):
            return DecisionOutput(
                action=DecisionAction.ASK_USER,
                params={"question_type": "confirm_completion"},
                narration=""
            )
        else:
            return DecisionOutput(
                action=DecisionAction.CONTINUE_TASK,
                params={},
                narration=""
            )

    def handle_model_status(self, payload: dict, context: dict) -> DecisionOutput:
        """处理模型状态"""
        # TODO: 检查 PlanB 触发条件
        models = context.get("models", {})
        if models.get("vision_main") == "down" and models.get("vision_fallback") == "down":
            return DecisionOutput(
                action=DecisionAction.TRIGGER_PLANB,
                params={"context_snapshot": context},
                narration=""
            )
        return DecisionOutput(
            action=DecisionAction.NO_OP,
            params={},
            narration=""
        )

    def _build_task_from_slots(self, slots: dict) -> dict:
        """从 slots 构建任务规格"""
        # TODO: minimal stub for building task_spec from slots
        task_type = slots.get("task_type", "navigation")
        return {
            "task_id": f"{task_type}_{int(time.time())}",
            "type": task_type,
            "target": slots.get("target", {}),
            "priority": 8 if task_type != "navigation" else 5,
            "nodes": [],
            "metadata": {"source": "user_request"}
        }


# ============================================================
# 9) /logging/decision_logger.py
# ============================================================

import time
import json
from typing import Dict, Optional
from core.decision_output import DecisionOutput
from core.intent_schema import ParsedIntent


def log_decision(
    event_type: str,
    parsed_intent: Optional[ParsedIntent],
    decision_output: DecisionOutput,
    task_context: Dict
) -> None:
    """记录决策日志"""
    log_entry = {
        "event_type": event_type,
        "intent_name": parsed_intent.intent_name if parsed_intent else None,
        "action": decision_output.action.value,
        "reason": getattr(decision_output, "reason", ""),
        "task_id": task_context.get("task_id"),
        "task_type": task_context.get("task_type"),
        "need_confirm": parsed_intent.need_confirm if parsed_intent else False,
        "timestamp": time.time()
    }
    
    print(f"[Decision] {json.dumps(log_entry, ensure_ascii=False)}")


# ============================================================
# 10) /inquiry/inquiry_manager.py（骨架）
# ============================================================

import json
import os
from typing import Dict, Optional
from .parser import InquiryParser
from core.intent_schema import ParsedIntent


class InquiryManager:
    def __init__(self, template_path: Optional[str] = None):
        if template_path is None:
            template_path = os.path.join(
                os.path.dirname(__file__),
                "inquiry_templates.json"
            )
        self.template_path = template_path
        self.templates = self._load_templates()
        self.parser = InquiryParser()
        self._unknown_count = 0  # 连续 UNKNOWN 计数
    
    def _load_templates(self) -> Dict:
        """加载问询模板"""
        try:
            with open(self.template_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    
    def build_question(self, question_type: str, context: Dict = None) -> Dict:
        """构建问句"""
        if context is None:
            context = {}
        
        tpl = self.templates.get(question_type)
        if not tpl:
            return {
                "type": "inquiry",
                "question": "请再说一遍，我没有听清。",
                "options": ["是", "否"],
                "internal_type": "fallback"
            }
        
        question = tpl["question"]
        if "{intent_desc}" in question and "intent_desc" in context:
            question = question.replace("{intent_desc}", context["intent_desc"])
        
        return {
            "type": "inquiry",
            "question": question,
            "options": tpl["options"],
            "internal_type": question_type,
            "context": context
        }
    
    def handle_user_response(self, question_type: str, user_text: str) -> ParsedIntent:
        """处理用户回答"""
        tpl = self.templates.get(question_type, {})
        parsed = self.parser.parse(user_text, tpl)
        
        # 降级策略：连续 UNKNOWN
        if parsed.intent_name == "UNKNOWN":
            self._unknown_count += 1
            if self._unknown_count >= 2:
                # 触发降级
                self._unknown_count = 0
                # 返回 UNKNOWN，由决策层处理降级
        else:
            self._unknown_count = 0
        
        return parsed













