#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模拟数据生成器
用于无摄像头时模拟测试整套流程
"""

import random
import time
import json
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class DummyDataGenerator:
    """模拟数据生成器"""
    
    def __init__(self):
        """初始化模拟数据生成器"""
        self.scenarios = {
            "normal": self._generate_normal_scenario,
            "crowded": self._generate_crowded_scenario,
            "obstacle": self._generate_obstacle_scenario,
            "clear": self._generate_clear_scenario,
            "approaching": self._generate_approaching_scenario,
            "vehicle": self._generate_vehicle_scenario,
            "person": self._generate_person_scenario,
            "mixed": self._generate_mixed_scenario
        }
        
        # 模拟数据配置
        self.config = {
            "frame_width": 640,
            "frame_height": 480,
            "detection_confidence": 0.8,
            "tracking_confidence": 0.7,
            "max_objects": 10
        }
        
        logger.info("✅ 模拟数据生成器初始化完成")
    
    def _generate_normal_scenario(self) -> Dict[str, Any]:
        """生成正常场景数据"""
        return {
            "detections": [],
            "tracks": [],
            "path_prediction": {
                "obstructed": False,
                "path_width": 300.0,
                "confidence": 0.9
            },
            "scenario": "normal"
        }
    
    def _generate_crowded_scenario(self) -> Dict[str, Any]:
        """生成拥挤场景数据"""
        detections = []
        tracks = []
        
        # 生成多个人员检测
        for i in range(random.randint(3, 6)):
            x1 = random.randint(200, 400)
            y1 = random.randint(150, 350)
            x2 = x1 + random.randint(50, 100)
            y2 = y1 + random.randint(100, 150)
            
            detection = {
                "bbox": [x1, y1, x2, y2],
                "confidence": random.uniform(0.7, 0.95),
                "class_id": 0,
                "class_name": "person"
            }
            detections.append(detection)
            
            track = {
                "track_id": i + 1,
                "bbox": [x1, y1, x2, y2],
                "confidence": random.uniform(0.6, 0.9)
            }
            tracks.append(track)
        
        return {
            "detections": detections,
            "tracks": tracks,
            "path_prediction": {
                "obstructed": True,
                "path_width": 150.0,
                "confidence": 0.8
            },
            "scenario": "crowded"
        }
    
    def _generate_obstacle_scenario(self) -> Dict[str, Any]:
        """生成障碍物场景数据"""
        detections = []
        tracks = []
        
        # 生成障碍物检测
        for i in range(random.randint(1, 3)):
            x1 = random.randint(250, 350)
            y1 = random.randint(200, 300)
            x2 = x1 + random.randint(80, 120)
            y2 = y1 + random.randint(80, 120)
            
            detection = {
                "bbox": [x1, y1, x2, y2],
                "confidence": random.uniform(0.8, 0.95),
                "class_id": random.choice([1, 2, 3]),  # car, bicycle, motorcycle
                "class_name": random.choice(["car", "bicycle", "motorcycle"])
            }
            detections.append(detection)
            
            track = {
                "track_id": i + 1,
                "bbox": [x1, y1, x2, y2],
                "confidence": random.uniform(0.7, 0.9)
            }
            tracks.append(track)
        
        return {
            "detections": detections,
            "tracks": tracks,
            "path_prediction": {
                "obstructed": True,
                "path_width": 100.0,
                "confidence": 0.7
            },
            "scenario": "obstacle"
        }
    
    def _generate_clear_scenario(self) -> Dict[str, Any]:
        """生成路径畅通场景数据"""
        return {
            "detections": [],
            "tracks": [],
            "path_prediction": {
                "obstructed": False,
                "path_width": 400.0,
                "confidence": 0.95
            },
            "scenario": "clear"
        }
    
    def _generate_approaching_scenario(self) -> Dict[str, Any]:
        """生成靠近场景数据"""
        detections = []
        tracks = []
        
        # 生成正在靠近的目标
        for i in range(random.randint(1, 2)):
            x1 = random.randint(300, 400)
            y1 = random.randint(250, 350)
            x2 = x1 + random.randint(60, 80)
            y2 = y1 + random.randint(120, 150)
            
            detection = {
                "bbox": [x1, y1, x2, y2],
                "confidence": random.uniform(0.8, 0.95),
                "class_id": 0,
                "class_name": "person"
            }
            detections.append(detection)
            
            track = {
                "track_id": i + 1,
                "bbox": [x1, y1, x2, y2],
                "confidence": random.uniform(0.7, 0.9)
            }
            tracks.append(track)
        
        return {
            "detections": detections,
            "tracks": tracks,
            "path_prediction": {
                "obstructed": True,
                "path_width": 200.0,
                "confidence": 0.8
            },
            "scenario": "approaching"
        }
    
    def _generate_vehicle_scenario(self) -> Dict[str, Any]:
        """生成车辆场景数据"""
        detections = []
        tracks = []
        
        # 生成车辆检测
        for i in range(random.randint(1, 2)):
            x1 = random.randint(200, 400)
            y1 = random.randint(150, 250)
            x2 = x1 + random.randint(120, 180)
            y2 = y1 + random.randint(80, 120)
            
            detection = {
                "bbox": [x1, y1, x2, y2],
                "confidence": random.uniform(0.8, 0.95),
                "class_id": 1,
                "class_name": "car"
            }
            detections.append(detection)
            
            track = {
                "track_id": i + 1,
                "bbox": [x1, y1, x2, y2],
                "confidence": random.uniform(0.7, 0.9)
            }
            tracks.append(track)
        
        return {
            "detections": detections,
            "tracks": tracks,
            "path_prediction": {
                "obstructed": True,
                "path_width": 150.0,
                "confidence": 0.8
            },
            "scenario": "vehicle"
        }
    
    def _generate_person_scenario(self) -> Dict[str, Any]:
        """生成人员场景数据"""
        detections = []
        tracks = []
        
        # 生成人员检测
        for i in range(random.randint(1, 3)):
            x1 = random.randint(250, 350)
            y1 = random.randint(200, 300)
            x2 = x1 + random.randint(50, 80)
            y2 = y1 + random.randint(120, 150)
            
            detection = {
                "bbox": [x1, y1, x2, y2],
                "confidence": random.uniform(0.7, 0.9),
                "class_id": 0,
                "class_name": "person"
            }
            detections.append(detection)
            
            track = {
                "track_id": i + 1,
                "bbox": [x1, y1, x2, y2],
                "confidence": random.uniform(0.6, 0.8)
            }
            tracks.append(track)
        
        return {
            "detections": detections,
            "tracks": tracks,
            "path_prediction": {
                "obstructed": True,
                "path_width": 200.0,
                "confidence": 0.8
            },
            "scenario": "person"
        }
    
    def _generate_mixed_scenario(self) -> Dict[str, Any]:
        """生成混合场景数据"""
        detections = []
        tracks = []
        
        # 生成混合目标
        objects = [
            {"class_id": 0, "class_name": "person"},
            {"class_id": 1, "class_name": "car"},
            {"class_id": 2, "class_name": "bicycle"}
        ]
        
        for i, obj in enumerate(random.sample(objects, random.randint(2, 3))):
            x1 = random.randint(200, 400)
            y1 = random.randint(150, 300)
            x2 = x1 + random.randint(60, 120)
            y2 = y1 + random.randint(80, 140)
            
            detection = {
                "bbox": [x1, y1, x2, y2],
                "confidence": random.uniform(0.7, 0.9),
                "class_id": obj["class_id"],
                "class_name": obj["class_name"]
            }
            detections.append(detection)
            
            track = {
                "track_id": i + 1,
                "bbox": [x1, y1, x2, y2],
                "confidence": random.uniform(0.6, 0.8)
            }
            tracks.append(track)
        
        return {
            "detections": detections,
            "tracks": tracks,
            "path_prediction": {
                "obstructed": True,
                "path_width": 180.0,
                "confidence": 0.8
            },
            "scenario": "mixed"
        }
    
    def generate_scenario_data(self, scenario: str) -> Dict[str, Any]:
        """
        生成指定场景的模拟数据
        
        Args:
            scenario: 场景名称
            
        Returns:
            Dict[str, Any]: 模拟数据
        """
        try:
            if scenario not in self.scenarios:
                logger.warning(f"⚠️ 未知场景: {scenario}")
                return self._generate_normal_scenario()
            
            data = self.scenarios[scenario]()
            
            # 添加时间戳
            data["timestamp"] = datetime.now().isoformat()
            data["frame_count"] = random.randint(1, 1000)
            
            logger.info(f"✅ 生成场景数据: {scenario}")
            return data
            
        except Exception as e:
            logger.error(f"❌ 生成场景数据失败: {e}")
            return self._generate_normal_scenario()
    
    def generate_random_scenario(self) -> Dict[str, Any]:
        """
        生成随机场景数据
        
        Returns:
            Dict[str, Any]: 模拟数据
        """
        scenario = random.choice(list(self.scenarios.keys()))
        return self.generate_scenario_data(scenario)
    
    def generate_scenario_sequence(self, scenarios: List[str], duration: int = 10) -> List[Dict[str, Any]]:
        """
        生成场景序列数据
        
        Args:
            scenarios: 场景列表
            duration: 持续时间（秒）
            
        Returns:
            List[Dict[str, Any]]: 场景序列数据
        """
        try:
            sequence = []
            scenario_count = len(scenarios)
            
            for i in range(duration):
                scenario_index = i % scenario_count
                scenario = scenarios[scenario_index]
                data = self.generate_scenario_data(scenario)
                sequence.append(data)
                time.sleep(0.1)  # 模拟帧间隔
            
            logger.info(f"✅ 生成场景序列: {len(sequence)} 帧")
            return sequence
            
        except Exception as e:
            logger.error(f"❌ 生成场景序列失败: {e}")
            return []
    
    def get_available_scenarios(self) -> List[str]:
        """
        获取可用场景列表
        
        Returns:
            List[str]: 场景列表
        """
        return list(self.scenarios.keys())
    
    def get_scenario_description(self, scenario: str) -> str:
        """
        获取场景描述
        
        Args:
            scenario: 场景名称
            
        Returns:
            str: 场景描述
        """
        descriptions = {
            "normal": "正常场景 - 无检测目标",
            "crowded": "拥挤场景 - 多人聚集",
            "obstacle": "障碍物场景 - 车辆或障碍物",
            "clear": "路径畅通场景 - 无障碍物",
            "approaching": "靠近场景 - 目标正在靠近",
            "vehicle": "车辆场景 - 检测到车辆",
            "person": "人员场景 - 检测到人员",
            "mixed": "混合场景 - 多种目标混合"
        }
        
        return descriptions.get(scenario, "未知场景")
    
    def export_scenario_data(self, data: Dict[str, Any], filename: str):
        """
        导出场景数据
        
        Args:
            data: 场景数据
            filename: 文件名
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"✅ 场景数据已导出: {filename}")
            
        except Exception as e:
            logger.error(f"❌ 场景数据导出失败: {e}")

# 全局模拟数据生成器实例
_global_dummy_generator: Optional[DummyDataGenerator] = None

def get_dummy_generator() -> DummyDataGenerator:
    """获取全局模拟数据生成器实例"""
    global _global_dummy_generator
    if _global_dummy_generator is None:
        _global_dummy_generator = DummyDataGenerator()
    return _global_dummy_generator

def generate_scenario_data(scenario: str) -> Dict[str, Any]:
    """生成场景数据"""
    generator = get_dummy_generator()
    return generator.generate_scenario_data(scenario)

def generate_random_scenario() -> Dict[str, Any]:
    """生成随机场景数据"""
    generator = get_dummy_generator()
    return generator.generate_random_scenario()

# 使用示例
if __name__ == "__main__":
    # 创建模拟数据生成器
    generator = DummyDataGenerator()
    
    # 测试各种场景
    scenarios = generator.get_available_scenarios()
    print(f"可用场景: {scenarios}")
    
    for scenario in scenarios:
        data = generator.generate_scenario_data(scenario)
        description = generator.get_scenario_description(scenario)
        print(f"场景: {scenario} - {description}")
        print(f"检测数量: {len(data['detections'])}")
        print(f"跟踪数量: {len(data['tracks'])}")
        print(f"路径状态: {'阻塞' if data['path_prediction']['obstructed'] else '畅通'}")
        print()
    
    print("✅ 模拟数据生成器测试完成")
