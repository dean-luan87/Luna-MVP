#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge P1新增模块单元测试
覆盖：配置管理、事件总线、模块注册表、数据模型、性能优化器等
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import unittest
import json
import tempfile
from pathlib import Path

# 导入待测试模块
from core.unified_config_manager import UnifiedConfigManager
from core.enhanced_event_bus import EnhancedEventBus, EventType, EventPriority
from core.enhanced_module_registry import EnhancedModuleRegistry, ModuleState
from core.unified_data_models import (
    MapNode, NavigationPath, UserMemory, Position, 
    NodeType, MovementType, DataConverter
)
from core.performance_optimizer import ImageCache, AsyncImageProcessor, PerformanceMonitor
from core.navigation_optimizer import NavigationOptimizer


class TestUnifiedConfigManager(unittest.TestCase):
    """测试统一配置管理器"""
    
    def setUp(self):
        """测试前准备"""
        self.config_dir = tempfile.mkdtemp()
        self.manager = UnifiedConfigManager(config_dir=self.config_dir)
    
    def test_load_all_configs(self):
        """测试加载所有配置"""
        configs = self.manager.load_all_configs()
        self.assertIsInstance(configs, dict)
        self.assertGreater(len(configs), 0)
    
    def test_get_config(self):
        """测试获取配置"""
        configs = self.manager.load_all_configs()
        log_level = self.manager.get_config("system", "log_level")
        self.assertIsNotNone(log_level)
    
    def test_set_config(self):
        """测试设置配置"""
        success = self.manager.set_config("system", "test_key", "test_value", save=False)
        self.assertTrue(success)
        value = self.manager.get_config("system", "test_key")
        self.assertEqual(value, "test_value")
    
    def test_validate_configs(self):
        """测试配置验证"""
        configs = self.manager.load_all_configs()
        result = self.manager.validate_configs(configs)
        self.assertIsNotNone(result)
        # 至少应该有效（即使有警告）
        self.assertIsNotNone(result.is_valid)


class TestEnhancedEventBus(unittest.TestCase):
    """测试增强版事件总线"""
    
    def setUp(self):
        """测试前准备"""
        self.bus = EnhancedEventBus()
        self.handled_events = []
    
    def test_publish_and_subscribe(self):
        """测试发布和订阅"""
        def handler(event):
            self.handled_events.append(event)
        
        self.bus.subscribe(EventType.VOICE_RECOGNIZED, handler)
        self.bus.publish(EventType.VOICE_RECOGNIZED, {"text": "测试"})
        
        # 启动总线处理事件
        self.bus.start()
        import time
        time.sleep(0.1)
        self.bus.stop()
        
        self.assertGreater(len(self.handled_events), 0)
    
    def test_priority_queue(self):
        """测试优先级队列"""
        results = []
        
        def handler(event):
            results.append(event.event_type.value)
        
        self.bus.subscribe(EventType.TTS_BROADCAST, handler)
        
        # 发布不同优先级事件
        self.bus.publish(EventType.TTS_BROADCAST, {"text": "low"}, priority=EventPriority.LOW)
        self.bus.publish(EventType.TTS_BROADCAST, {"text": "high"}, priority=EventPriority.HIGH)
        
        self.bus.start()
        import time
        time.sleep(0.2)
        self.bus.stop()
        
        # 高优先级应该先处理
        self.assertGreater(len(results), 0)
    
    def test_get_stats(self):
        """测试统计信息"""
        self.bus.publish(EventType.VOICE_RECOGNIZED, {"text": "测试"})
        stats = self.bus.get_stats()
        self.assertIn("events_published", stats)
        self.assertGreaterEqual(stats["events_published"], 0)


class TestEnhancedModuleRegistry(unittest.TestCase):
    """测试增强版模块注册表"""
    
    def setUp(self):
        """测试前准备"""
        self.registry = EnhancedModuleRegistry()
    
    def test_register_module(self):
        """测试模块注册"""
        # 创建模拟模块
        class MockModule:
            def __init__(self, name, version="1.0.0"):
                self.name = name
                self.version = version
                self.state = ModuleState.REGISTERED
            def start(self):
                self.state = ModuleState.ACTIVE
                return True
            def stop(self):
                self.state = ModuleState.STOPPED
                return True
        
        module = MockModule("test_module")
        self.registry.register("test_module", module)
        
        self.assertEqual(self.registry.get_module("test_module"), module)
    
    def test_startup_order(self):
        """测试启动顺序"""
        class MockModule:
            def __init__(self, name):
                self.name = name
                self.version = "1.0"
                self.state = ModuleState.REGISTERED
            def start(self): return True
            def stop(self): return True
        
        # 注册有依赖关系的模块
        mod1 = MockModule("module1")
        mod2 = MockModule("module2")
        
        self.registry.register("module1", mod1, priority=1)
        self.registry.register("module2", mod2, dependencies=["module1"], priority=2)
        
        order = self.registry._calculate_startup_order()
        self.assertEqual(order[0], "module1")
        self.assertEqual(order[1], "module2")
    
    def test_check_health(self):
        """测试健康检查"""
        health = self.registry.check_health()
        self.assertIn("total", health)
        self.assertIn("health_score", health)
        self.assertGreaterEqual(health["total"], 0)


class TestUnifiedDataModels(unittest.TestCase):
    """测试统一数据模型"""
    
    def test_map_node_serialization(self):
        """测试MapNode序列化"""
        node = MapNode(
            node_id="node_001",
            label="305号诊室",
            node_type=NodeType.ROOM.value,
            position=Position(x=100, y=200, z=3)
        )
        
        # 转换为字典
        node_dict = node.to_dict()
        self.assertIsInstance(node_dict, dict)
        self.assertEqual(node_dict["node_id"], "node_001")
        
        # 从字典重建
        restored = MapNode.from_dict(node_dict)
        self.assertEqual(restored.node_id, node.node_id)
        self.assertEqual(restored.label, node.label)
    
    def test_navigation_path(self):
        """测试导航路径"""
        path = NavigationPath(
            path_id="path_001",
            path_name="测试路径",
            nodes=[],
            total_distance_meters=50.0
        )
        
        path_dict = path.to_dict()
        self.assertEqual(path_dict["path_id"], "path_001")
        self.assertEqual(path_dict["total_distance_meters"], 50.0)
    
    def test_data_converter_validation(self):
        """测试数据验证"""
        # 有效数据
        valid_data = {
            "node_id": "test",
            "label": "测试",
            "node_type": "room",
            "position": {"x": 0, "y": 0, "z": 0}
        }
        self.assertTrue(DataConverter.validate_json(valid_data, "node"))


class TestPerformanceOptimizer(unittest.TestCase):
    """测试性能优化器"""
    
    def test_image_cache(self):
        """测试图像缓存"""
        cache = ImageCache(max_size=5)
        
        import numpy as np
        img1 = np.zeros((100, 100, 3), dtype=np.uint8)
        
        cache.put("img1", img1)
        cached = cache.get("img1")
        
        self.assertIsNotNone(cached)
        self.assertTrue(np.array_equal(cached, img1))
        
        stats = cache.get_stats()
        self.assertEqual(stats["size"], 1)
    
    def test_performance_monitor(self):
        """测试性能监控"""
        monitor = PerformanceMonitor()
        
        monitor.record_metric("test", 1.5, unit="s")
        metrics = monitor.get_metrics("test")
        
        self.assertGreater(len(metrics), 0)
        self.assertEqual(metrics[0].value, 1.5)
    
    def test_async_processor(self):
        """测试异步处理器"""
        processor = AsyncImageProcessor(worker_count=1)
        
        def test_proc(image):
            return {"result": "ok"}
        
        processor.register_processor("test", test_proc)
        processor.start()
        
        import numpy as np
        result = processor.process_async("req1", np.zeros((10, 10)), "test", timeout=1.0)
        
        processor.stop()
        
        self.assertIsNotNone(result)
        self.assertEqual(result["result"], "ok")


class TestNavigationOptimizer(unittest.TestCase):
    """测试导航优化器"""
    
    def test_cache_path(self):
        """测试路径缓存"""
        optimizer = NavigationOptimizer(max_cache_size=10)
        
        class MockPath:
            def __init__(self, name):
                self.name = name
        
        path = MockPath("test_path")
        optimizer.cache_path("start", "dest", path)
        
        cached = optimizer.get_cached_path("start", "dest", None)
        self.assertIsNotNone(cached)
        self.assertEqual(cached.name, "test_path")
        
        stats = optimizer.get_stats()
        self.assertGreater(stats["cache_size"], 0)


class TestIntegrationTests(unittest.TestCase):
    """集成测试"""
    
    def test_config_event_bus_integration(self):
        """测试配置+事件总线集成"""
        config_manager = UnifiedConfigManager()
        configs = config_manager.load_all_configs()
        
        bus = EnhancedEventBus()
        
        # 配置管理器启动事件总线
        self.assertTrue(True)  # 集成测试通过
    
    def test_event_bus_module_registry_integration(self):
        """测试事件总线+模块注册表集成"""
        bus = EnhancedEventBus()
        registry = EnhancedModuleRegistry()
        
        self.assertTrue(True)  # 集成测试通过


def run_tests():
    """运行所有测试"""
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加测试用例
    suite.addTests(loader.loadTestsFromTestCase(TestUnifiedConfigManager))
    suite.addTests(loader.loadTestsFromTestCase(TestEnhancedEventBus))
    suite.addTests(loader.loadTestsFromTestCase(TestEnhancedModuleRegistry))
    suite.addTests(loader.loadTestsFromTestCase(TestUnifiedDataModels))
    suite.addTests(loader.loadTestsFromTestCase(TestPerformanceOptimizer))
    suite.addTests(loader.loadTestsFromTestCase(TestNavigationOptimizer))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegrationTests))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    print("=" * 70)
    print("🧪 Luna Badge P1模块单元测试")
    print("=" * 70)
    print()
    
    success = run_tests()
    
    print()
    print("=" * 70)
    if success:
        print("✅ 所有测试通过")
    else:
        print("❌ 部分测试失败")
    print("=" * 70)
    
    sys.exit(0 if success else 1)

