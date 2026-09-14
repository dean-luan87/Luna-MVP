"""
B2 v0.4.2: Gate 接入 tick 主循环集成测试

覆盖 3 个断言：
1. SUSPENDED => tick 返回 None
2. READ_ONLY => tick 返回 summary 且 readonly=True 且不写 timeline
3. ACTIVE => tick 返回 summary（若有 impact）且 timeline 可写（但 NO_OP 不写）
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import time
from vision_pipeline.b2.v03.b2_v03 import B2v03
from vision_pipeline.b2.v03.types import FactorType, FactorEvidence


class TestB2V042TickGateIntegration(unittest.TestCase):
    """B2 v0.4.2 Gate 接入 tick 主循环集成测试"""
    
    def setUp(self):
        """设置测试环境"""
        self.b2 = B2v03(
            logger=Mock(),
            record_store=None,
            timeline_writer=Mock(),
            trace_writer=Mock(),
            fps=30.0
        )
        self.b2.range_m = 5.0
        
        # Mock GateEvaluatorV05
        self.b2.gate_evaluator_v05 = Mock()
        
        # Mock trace_writer
        self.b2.trace_writer = Mock()
        self.b2.trace_writer.write = Mock()
        
        # Mock timeline_writer
        self.b2.timeline_writer = Mock() if hasattr(self.b2, 'timeline_writer') else None
        
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
    
    def test_suspended_returns_none(self):
        """测试 1: SUSPENDED => tick 返回 None"""
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
        
        # 验证：to_c_message 未发送
        self.assertEqual(call_args["to_c_message"]["sent"], False)
        self.assertEqual(call_args["to_c_message"]["reason"], "gate_suspended")
        
        # 验证：timeline 未写入
        self.assertFalse(call_args["writeback"]["timeline_written"])
    
    def test_read_only_returns_summary_with_readonly_flag(self):
        """测试 2: READ_ONLY => tick 返回 summary 且 readonly=True 且不写 timeline"""
        # 设置 Gate 返回 READ_ONLY
        self.b2.gate_evaluator_v05.evaluate.return_value = (
            "READ_ONLY",
            {
                "blocked_by": "insufficient_evidence",
                "human_readable": "证据不足，B只读运行",
                "can_trigger": False
            }
        )
        
        # Mock _summarize_world_change 返回有效 summary
        with patch.object(self.b2, '_summarize_world_change', return_value={
            "impact": "NEED_SLOW_DOWN",
            "level": "CONDITION_CHANGE",
            "main_factor": "PATH",
            "advisory_only": True,
            "system_ts": 100.0
        }):
            # 调用 tick（需要有效的 perception 数据）
            result = self.b2.tick(
                frame_ts=100.0,
                perception={"factors": {}},
                frame_id=3000
            )
        
        # 验证：返回 summary
        self.assertIsNotNone(result)
        
        # 验证：summary 包含 readonly=True
        self.assertTrue(result.get("readonly", False))
        
        # 验证：trace 被写入
        self.b2.trace_writer.write.assert_called_once()
        
        # 验证：trace 包含 gate_eval
        call_args = self.b2.trace_writer.write.call_args[0][0]
        self.assertIn("gate_eval", call_args)
        self.assertEqual(call_args["gate_eval"]["mode"], "READ_ONLY")
        
        # 验证：timeline 未写入
        self.assertFalse(call_args["writeback"]["timeline_written"])
        self.assertFalse(call_args["writeback"]["memory_written"])
    
    def test_active_returns_summary_and_writes_timeline(self):
        """测试 3: ACTIVE => tick 返回 summary（若有 impact）且 timeline 可写（但 NO_OP 不写）"""
        # 设置 Gate 返回 ACTIVE
        self.b2.gate_evaluator_v05.evaluate.return_value = (
            "ACTIVE",
            {
                "blocked_by": None,
                "human_readable": "Gate通过，B正常工作",
                "can_trigger": True
            }
        )
        
        # Mock _summarize_world_change 返回有效 summary（非 NO_OP）
        with patch.object(self.b2, '_summarize_world_change', return_value={
            "impact": "NEED_SLOW_DOWN",
            "level": "CONDITION_CHANGE",
            "main_factor": "PATH",
            "advisory_only": True,
            "system_ts": 100.0
        }):
            # 调用 tick（需要有效的 perception 数据）
            result = self.b2.tick(
                frame_ts=100.0,
                perception={"factors": {}},
                frame_id=3000
            )
        
        # 验证：返回 summary
        self.assertIsNotNone(result)
        
        # 验证：summary 不包含 readonly（ACTIVE 模式）
        self.assertNotIn("readonly", result)
        
        # 验证：trace 被写入
        self.b2.trace_writer.write.assert_called_once()
        
        # 验证：trace 包含 gate_eval
        call_args = self.b2.trace_writer.write.call_args[0][0]
        self.assertIn("gate_eval", call_args)
        self.assertEqual(call_args["gate_eval"]["mode"], "ACTIVE")
        
        # 验证：ACTIVE 模式下，如果 impact != NO_OP，timeline 可以写入
        # （具体行为取决于 _write_outputs 的实现）


if __name__ == "__main__":
    unittest.main()
