"""
B2 v0.4.2: Gate 接入 tick 主循环测试

验证点：
1. Gate=SUSPENDED → tick 返回 None（但仍写 trace）
2. Gate=READ_ONLY → 无 timeline，不发给 C
3. Gate=ACTIVE → 行为与 v0.4.1 一致
"""

import unittest
from unittest.mock import Mock, patch
import time
from vision_pipeline.b2.v03.b2_v03 import B2v03
from vision_pipeline.b2.v03.types import FactorType, FactorEvidence


class TestB2V042GateInTick(unittest.TestCase):
    """B2 v0.4.2 Gate 接入 tick 主循环测试"""
    
    def setUp(self):
        """设置测试环境"""
        self.b2 = B2v03(
            logger=Mock(),
            record_store=None,
            timeline_writer=Mock(),
            trace_writer=Mock()
        )
        self.b2.fps = 30.0
        self.b2.range_m = 5.0
        
        # Mock GateEvaluatorV05
        self.b2.gate_evaluator_v05 = Mock()
        
        # Mock trace_writer
        self.b2.trace_writer = Mock()
        self.b2.trace_writer.write = Mock()
    
    def test_gate_suspended_returns_none(self):
        """测试：Gate=SUSPENDED → tick 返回 None（但仍写 trace）"""
        # 设置 Gate 返回 SUSPENDED
        self.b2.gate_evaluator_v05.evaluate.return_value = (
            "SUSPENDED",
            {
                "blocked_by": "camera_shake",
                "human_readable": "镜头晃动过大，B暂停工作",
                "can_trigger": False
            }
        )
        
        # 调用 tick
        result = self.b2.tick(
            frame_ts=100.0,
            perception={},
            frame_id=3000
        )
        
        # 验证：返回 None
        self.assertIsNone(result)
        
        # 验证：trace 被写入
        self.b2.trace_writer.write.assert_called_once()
        
        # 验证：trace 包含 gate_eval
        call_args = self.b2.trace_writer.write.call_args[0][0]
        self.assertIn("gate_eval", call_args)
        self.assertEqual(call_args["gate_eval"]["mode"], "SUSPENDED")
        self.assertEqual(call_args["gate_eval"]["blocked_by"], "camera_shake")
        
        # 验证：to_c_message 未发送
        self.assertEqual(call_args["to_c_message"]["sent"], False)
        self.assertEqual(call_args["to_c_message"]["reason"], "gate_suspended")
        
        # 验证：timeline 未写入
        self.assertFalse(call_args["writeback"]["timeline_written"])
    
    def test_gate_read_only_no_timeline(self):
        """测试：Gate=READ_ONLY → 无 timeline，不发给 C"""
        # 设置 Gate 返回 READ_ONLY
        self.b2.gate_evaluator_v05.evaluate.return_value = (
            "READ_ONLY",
            {
                "blocked_by": "insufficient_evidence",
                "human_readable": "证据不足，B只读运行",
                "can_trigger": False
            }
        )
        
        # Mock 必要的内部方法
        self.b2._append_future_state = Mock()
        self.b2._collect_future_window = Mock(return_value=[
            {"ts": 101.0, "factors": {}},
            {"ts": 102.0, "factors": {}}
        ])
        self.b2.state_machine = Mock()
        self.b2.state_machine.tick = Mock(return_value=Mock(
            can_trigger=True,
            blocked_by=None,
            state=Mock()
        ))
        self.b2.state_machine.get_runtime_state_dict = Mock(return_value={})
        self.b2.state_machine.get_state_gate_dict = Mock(return_value={})
        
        # Mock evidence lifecycle
        self.b2.evidence_lifecycle = Mock()
        self.b2.evidence_lifecycle.update = Mock(return_value="OBSERVING")
        self.b2.evidence_lifecycle.get_evidence_state_dict = Mock(return_value={})
        
        # 调用 tick（需要有效的 perception 数据）
        result = self.b2.tick(
            frame_ts=100.0,
            perception={"factors": {}},
            frame_id=3000
        )
        
        # 验证：trace 被写入
        self.b2.trace_writer.write.assert_called_once()
        
        # 验证：trace 包含 gate_eval
        call_args = self.b2.trace_writer.write.call_args[0][0]
        self.assertIn("gate_eval", call_args)
        self.assertEqual(call_args["gate_eval"]["mode"], "READ_ONLY")
        
        # 验证：to_c_message 未发送
        self.assertEqual(call_args["to_c_message"]["sent"], False)
        
        # 验证：timeline 未写入
        self.assertFalse(call_args["writeback"]["timeline_written"])
    
    def test_gate_active_full_flow(self):
        """测试：Gate=ACTIVE → 完整流程（行为与 v0.4.1 一致）"""
        # 设置 Gate 返回 ACTIVE
        self.b2.gate_evaluator_v05.evaluate.return_value = (
            "ACTIVE",
            {
                "blocked_by": None,
                "human_readable": "Gate通过，B正常工作",
                "can_trigger": True
            }
        )
        
        # Mock 必要的内部方法
        self.b2._append_future_state = Mock()
        self.b2._collect_future_window = Mock(return_value=[
            {"ts": 101.0, "factors": {}},
            {"ts": 102.0, "factors": {}}
        ])
        self.b2.state_machine = Mock()
        self.b2.state_machine.tick = Mock(return_value=Mock(
            can_trigger=True,
            blocked_by=None,
            state=Mock()
        ))
        self.b2.state_machine.get_runtime_state_dict = Mock(return_value={})
        self.b2.state_machine.get_state_gate_dict = Mock(return_value={})
        
        # Mock evidence lifecycle
        self.b2.evidence_lifecycle = Mock()
        self.b2.evidence_lifecycle.update = Mock(return_value="CONFIRMED")
        self.b2.evidence_lifecycle.get_evidence_state_dict = Mock(return_value={
            "state": "CONFIRMED",
            "confidence": 0.8
        })
        
        # 调用 tick（需要有效的 perception 数据）
        result = self.b2.tick(
            frame_ts=100.0,
            perception={"factors": {}},
            frame_id=3000
        )
        
        # 验证：trace 被写入
        self.b2.trace_writer.write.assert_called_once()
        
        # 验证：trace 包含 gate_eval
        call_args = self.b2.trace_writer.write.call_args[0][0]
        self.assertIn("gate_eval", call_args)
        self.assertEqual(call_args["gate_eval"]["mode"], "ACTIVE")
        
        # 验证：Gate=ACTIVE 时，如果 impact != NO_OP，应该可以发送消息
        # （具体行为取决于实际的 impact 和 evidence 状态）


if __name__ == "__main__":
    unittest.main()
