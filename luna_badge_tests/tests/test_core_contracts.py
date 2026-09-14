# -*- coding: utf-8 -*-
"""
Luna Badge v1.4.3 - 核心契约层单元测试

测试阶段 1 创建的所有核心契约结构。
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest
from core.intent_schema import ParsedIntent
from core.decision_actions import DecisionAction
from core.decision_output import DecisionOutput
from core.task_result import TaskResult
from core.events import EventType


class TestParsedIntent:
    """测试 ParsedIntent 结构"""
    
    def test_basic_creation(self):
        """测试基本创建"""
        intent = ParsedIntent(
            intent_name="INSERT_TASK",
            slots={"task_type": "toilet"},
            source="asr",
            need_confirm=True,
            raw="我先去厕所"
        )
        assert intent.intent_name == "INSERT_TASK"
        assert intent.slots == {"task_type": "toilet"}
        assert intent.source == "asr"
        assert intent.need_confirm is True
        assert intent.raw == "我先去厕所"
    
    def test_default_values(self):
        """测试默认值"""
        intent = ParsedIntent(intent_name="UNKNOWN")
        assert intent.intent_name == "UNKNOWN"
        assert intent.slots == {}  # 应该被 __post_init__ 初始化为空字典
        assert intent.source == "inquiry"
        assert intent.need_confirm is False
        assert intent.raw == ""
    
    def test_repr(self):
        """测试字符串表示"""
        intent = ParsedIntent(
            intent_name="CONFIRM",
            raw="好的"
        )
        repr_str = repr(intent)
        assert "ParsedIntent" in repr_str
        assert "CONFIRM" in repr_str


class TestDecisionAction:
    """测试 DecisionAction 枚举"""
    
    def test_all_actions_exist(self):
        """测试所有动作都存在"""
        assert DecisionAction.CONTINUE_TASK
        assert DecisionAction.INSERT_TASK
        assert DecisionAction.REPLACE_TASK
        assert DecisionAction.RESUME_MAIN_TASK
        assert DecisionAction.NO_OP
        assert DecisionAction.ASK_USER
        assert DecisionAction.TRIGGER_PLANB
    
    def test_action_values(self):
        """测试动作值"""
        assert DecisionAction.CONTINUE_TASK.value == "continue_task"
        assert DecisionAction.INSERT_TASK.value == "insert_task"
        assert DecisionAction.ASK_USER.value == "ask_user"
    
    def test_str_representation(self):
        """测试字符串表示"""
        assert str(DecisionAction.CONTINUE_TASK) == "continue_task"


class TestDecisionOutput:
    """测试 DecisionOutput 结构"""
    
    def test_basic_creation(self):
        """测试基本创建"""
        output = DecisionOutput(
            action=DecisionAction.INSERT_TASK,
            params={"insert_task_spec": {"task_id": "test"}},
            narration="好的，我先带你去厕所。"
        )
        assert output.action == DecisionAction.INSERT_TASK
        assert output.params == {"insert_task_spec": {"task_id": "test"}}
        assert output.narration == "好的，我先带你去厕所。"
    
    def test_default_values(self):
        """测试默认值"""
        output = DecisionOutput(action=DecisionAction.NO_OP)
        assert output.action == DecisionAction.NO_OP
        assert output.params == {}  # 应该被 __post_init__ 初始化为空字典
        assert output.narration == ""
    
    def test_repr(self):
        """测试字符串表示"""
        output = DecisionOutput(
            action=DecisionAction.CONTINUE_TASK,
            narration="继续执行"
        )
        repr_str = repr(output)
        assert "DecisionOutput" in repr_str
        assert "continue_task" in repr_str


class TestTaskResult:
    """测试 TaskResult 结构"""
    
    def test_success_result(self):
        """测试成功结果"""
        result = TaskResult(
            status="ok",
            reason="任务完成",
            task_id="task_123",
            task_type="navigation"
        )
        assert result.status == "ok"
        assert result.is_success() is True
        assert result.is_failed() is False
        assert result.is_cancelled() is False
    
    def test_failed_result(self):
        """测试失败结果"""
        result = TaskResult(
            status="failed",
            reason="模型错误",
            task_id="task_456",
            task_type="detection"
        )
        assert result.status == "failed"
        assert result.is_success() is False
        assert result.is_failed() is True
    
    def test_cancelled_result(self):
        """测试取消结果"""
        result = TaskResult(
            status="cancelled",
            reason="用户取消",
            task_id="task_789",
            task_type="navigation"
        )
        assert result.status == "cancelled"
        assert result.is_success() is False
        assert result.is_cancelled() is True
    
    def test_repr(self):
        """测试字符串表示"""
        result = TaskResult(
            status="ok",
            reason="完成",
            task_id="test",
            task_type="test"
        )
        repr_str = repr(result)
        assert "TaskResult" in repr_str
        assert "ok" in repr_str


class TestEventType:
    """测试 EventType 枚举"""
    
    def test_all_events_exist(self):
        """测试所有事件类型都存在"""
        assert EventType.TASK_NODE_COMPLETE
        assert EventType.TASK_NODE_START
        assert EventType.USER_INTENT
        assert EventType.INQUIRY_RESPONSE
        assert EventType.SYSTEM_ALERT
        assert EventType.USER_INACTIVE
        assert EventType.MODEL_STATUS
    
    def test_event_values(self):
        """测试事件值"""
        assert EventType.TASK_NODE_COMPLETE.value == "task_node_complete"
        assert EventType.USER_INTENT.value == "user_intent"
        assert EventType.MODEL_STATUS.value == "model_status"
    
    def test_str_representation(self):
        """测试字符串表示"""
        assert str(EventType.USER_INTENT) == "user_intent"


class TestImports:
    """测试模块导入"""
    
    def test_all_modules_importable(self):
        """测试所有模块都可以导入"""
        from core.intent_schema import ParsedIntent
        from core.decision_actions import DecisionAction
        from core.decision_output import DecisionOutput
        from core.task_result import TaskResult
        from core.events import EventType
        
        # 如果导入成功，这些类应该存在
        assert ParsedIntent
        assert DecisionAction
        assert DecisionOutput
        assert TaskResult
        assert EventType
    
    def test_circular_imports(self):
        """测试循环导入（DecisionOutput 导入 DecisionAction）"""
        from core.decision_output import DecisionOutput
        from core.decision_actions import DecisionAction
        
        # 应该能正常创建
        output = DecisionOutput(action=DecisionAction.NO_OP)
        assert output.action == DecisionAction.NO_OP


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


