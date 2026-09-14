# -*- coding: utf-8 -*-
"""
v1.8.4: Risk 调试快照单元测试

测试目标：
1. dynamic inactive 的对象必须出现在 snapshot 中，但不参与 risk
2. 快照包含所有必要信息
3. 快照不影响原有逻辑
"""

import unittest
import datetime
from core.risk.risk_registry import RiskRegistry
from core.risk.risk_object_factory import RiskObjectFactory
from core.risk.risk_advisory_service import RiskAdvisoryService
from core.risk.risk_object import DynamicProfile


class TestDebugSnapshot(unittest.TestCase):
    """调试快照功能测试"""
    
    def setUp(self):
        """测试前置设置"""
        self.registry = RiskRegistry()
        self.factory = RiskObjectFactory()
        self.service = RiskAdvisoryService(self.registry, enable_debug=True)
    
    def test_dynamic_inactive_object_in_snapshot(self):
        """
        Test: dynamic inactive 的对象必须出现在 snapshot 中，但不参与 risk
        
        断言：
        - snapshot.objects 包含该 risk_id
        - dynamic_active == False
        - risk_level == 0
        - advisory_triggered == False
        """
        # 创建 TIME_WINDOW 动态区域（只在 7-9 点激活）
        crowd_area = self.factory.make_area(
            risk_id="test_crowd_debug",
            risk_type="CROWD",
            polygon=[(0, 0), (10, 0), (10, 5), (0, 5)],
            confidence=0.9,
        )
        
        crowd_area.dynamic_profile = DynamicProfile(
            mode="TIME_WINDOW",
            active_windows=[(7, 9)],  # 只在 7-9 点激活
            hazard_multiplier=1.3,
            ignore_when_inactive=True  # 非激活时完全忽略
        )
        
        self.registry.upsert(crowd_area)
        
        # 测试时间：12:00（不在激活窗口内）
        test_time = datetime.datetime(2024, 1, 1, 12, 0)
        ts = test_time.timestamp()
        user_xy = (5.0, 2.0)  # 用户在风险区域内
        
        # 调用 tick()
        advisory_text = self.service.tick(user_xy, ts=ts)
        
        # Assert: 不应该返回 advisory_text
        self.assertIsNone(advisory_text, "非激活时间不应该触发警告")
        
        # Assert: 应该生成调试快照
        snapshot = self.service.get_last_debug_snapshot()
        self.assertIsNotNone(snapshot, "应该生成调试快照")
        
        # Assert: snapshot.objects 包含该 risk_id
        crowd_snapshot = next(
            (obj for obj in snapshot.objects if obj.risk_id == "test_crowd_debug"),
            None
        )
        self.assertIsNotNone(crowd_snapshot, "快照应该包含 crowd 对象")
        
        # Assert: dynamic_active == False
        self.assertFalse(
            crowd_snapshot.dynamic_active,
            "非激活时间 dynamic_active 应该为 False"
        )
        
        # Assert: risk_level == 0
        self.assertEqual(
            crowd_snapshot.risk_level,
            0.0,
            "非激活对象 risk_level 应该为 0"
        )
        
        # Assert: advisory_triggered == False
        self.assertFalse(
            snapshot.advisory_triggered,
            "不应该触发 ADVISORY"
        )
        
        # Assert: reason 应该说明原因
        self.assertEqual(
            crowd_snapshot.reason,
            "dynamic_inactive",
            "应该说明未参与计算的原因"
        )
    
    def test_snapshot_contains_all_active_objects(self):
        """
        Test: 快照包含所有 active 对象的信息
        """
        # 创建一个静态风险对象（永远激活）
        lake = self.factory.make_line(
            risk_id="test_lake_debug",
            risk_type="WATER_EDGE",
            polyline=[(0.0, 0.0), (30.0, 0.0)],
            confidence=0.95,
        )
        
        self.registry.upsert(lake)
        
        # 测试时间：8:00（任意时间）
        test_time = datetime.datetime(2024, 1, 1, 8, 0)
        ts = test_time.timestamp()
        user_xy = (5.0, 2.0)  # 用户接近湖边
        
        # 调用 tick()
        self.service.tick(user_xy, ts=ts)
        
        # Assert: 应该生成调试快照
        snapshot = self.service.get_last_debug_snapshot()
        self.assertIsNotNone(snapshot, "应该生成调试快照")
        
        # Assert: snapshot.objects 包含该 risk_id
        lake_snapshot = next(
            (obj for obj in snapshot.objects if obj.risk_id == "test_lake_debug"),
            None
        )
        self.assertIsNotNone(lake_snapshot, "快照应该包含 lake 对象")
        
        # Assert: 包含所有必要字段
        self.assertIsNotNone(lake_snapshot.risk_id)
        self.assertIsNotNone(lake_snapshot.risk_type)
        self.assertIsNotNone(lake_snapshot.dynamic_active)  # 可能是 True 或 False
        self.assertIsNotNone(lake_snapshot.hazard_level)
        self.assertIsNotNone(lake_snapshot.distance_m)
        self.assertIsNotNone(lake_snapshot.trend)
        self.assertIsNotNone(lake_snapshot.risk_level)
        self.assertIsNotNone(lake_snapshot.delta_risk)
        self.assertIsNotNone(lake_snapshot.state)
    
    def test_snapshot_to_dict(self):
        """
        Test: 快照可以转换为字典（用于 JSON 序列化）
        """
        # 创建一个风险对象
        lake = self.factory.make_line(
            risk_id="test_lake_dict",
            risk_type="WATER_EDGE",
            polyline=[(0.0, 0.0), (30.0, 0.0)],
            confidence=0.95,
        )
        
        self.registry.upsert(lake)
        
        # 调用 tick()
        test_time = datetime.datetime(2024, 1, 1, 8, 0)
        ts = test_time.timestamp()
        user_xy = (5.0, 2.0)
        
        self.service.tick(user_xy, ts=ts)
        
        # Assert: 可以转换为字典
        snapshot = self.service.get_last_debug_snapshot()
        self.assertIsNotNone(snapshot, "应该生成调试快照")
        
        snapshot_dict = snapshot.to_dict()
        self.assertIsInstance(snapshot_dict, dict, "应该返回字典")
        
        # Assert: 字典包含必要字段
        self.assertIn("ts", snapshot_dict)
        self.assertIn("user_xy", snapshot_dict)
        self.assertIn("objects", snapshot_dict)
        self.assertIn("advisory_triggered", snapshot_dict)
        self.assertIn("advisory_text", snapshot_dict)
    
    def test_snapshot_does_not_affect_logic(self):
        """
        Test: 快照不影响原有逻辑（启用调试 vs 不启用调试应该行为一致）
        """
        # 创建两个服务：一个启用调试，一个不启用
        service_debug = RiskAdvisoryService(self.registry, enable_debug=True)
        service_no_debug = RiskAdvisoryService(RiskRegistry(), enable_debug=False)
        
        # 创建相同的风险对象
        lake1 = self.factory.make_line(
            risk_id="test_lake_1",
            risk_type="WATER_EDGE",
            polyline=[(0.0, 0.0), (30.0, 0.0)],
            confidence=0.95,
        )
        lake2 = self.factory.make_line(
            risk_id="test_lake_2",
            risk_type="WATER_EDGE",
            polyline=[(0.0, 0.0), (30.0, 0.0)],
            confidence=0.95,
        )
        
        service_debug.registry.upsert(lake1)
        service_no_debug.registry.upsert(lake2)
        
        # 相同的输入
        test_time = datetime.datetime(2024, 1, 1, 8, 0)
        ts = test_time.timestamp()
        user_xy = (5.0, 10.0)  # 用户从远处接近
        
        # 调用 tick()
        advisory_text_1 = service_debug.tick(user_xy, ts=ts)
        advisory_text_2 = service_no_debug.tick(user_xy, ts=ts)
        
        # Assert: 行为应该一致（advisory_text 应该相同）
        # 注意：由于状态机的随机性，可能不完全相同，但主要逻辑应该一致
        # 这里我们主要验证：启用调试不会导致额外的警告或遗漏警告
        # 如果两个都返回 None，说明行为一致
        # 如果两个都返回文本，说明行为一致
        # 如果一个返回文本另一个返回 None，说明行为不一致（这是问题）
        
        # 简化验证：至少验证不会因为启用调试而多触发警告
        if advisory_text_1 is None and advisory_text_2 is not None:
            self.fail("启用调试不应该导致遗漏警告")
        if advisory_text_1 is not None and advisory_text_2 is None:
            self.fail("启用调试不应该导致额外警告")


if __name__ == "__main__":
    unittest.main()


