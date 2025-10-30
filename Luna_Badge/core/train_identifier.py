"""
列车识别模块 - 地铁共用线路判断
识别驶入站台的列车是否属于目标线路
"""

import logging
import re
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class TrainStatus(Enum):
    """列车状态"""
    MATCHED = "matched"           # 匹配目标线路
    WRONG_LINE = "wrong_line"     # 线路不匹配
    SHARED_TRACK = "shared_track" # 共用轨道
    UNCERTAIN = "uncertain"       # 无法确定


@dataclass
class TrainInfo:
    """列车信息"""
    line_number: str              # 线路号（如"2号线"）
    destination: str              # 终点站
    train_id: Optional[str] = None  # 列车编号
    shared_tracks: List[str] = None  # 共用轨道线路列表


class TrainIdentifier:
    """列车识别器"""
    
    def __init__(self):
        """初始化列车识别器"""
        self.logger = logging.getLogger(__name__)
        
        # 共用轨道配置（示例）
        self.shared_track_config = {
            "2号线": ["浦东专线", "张江高科专线"],
            "10号线": [],
            "1号线": []
        }
        
        self.logger.info("🚇 列车识别器初始化完成")
    
    def identify_train(self,
                      detected_text: str,
                      target_line: str,
                      target_station: str) -> Dict[str, Any]:
        """
        识别列车是否匹配目标
        
        Args:
            detected_text: 识别到的列车信息文字（如"2号线 往中山公园"）
            target_line: 目标线路（如"2号线"）
            target_station: 目标站点
        
        Returns:
            Dict[str, Any]: 识别结果
        """
        # 提取线路号和终点站
        train_info = self._parse_train_info(detected_text)
        
        if not train_info:
            return {
                "status": TrainStatus.UNCERTAIN.value,
                "matched": False,
                "message": None,
                "confidence": 0.5
            }
        
        # 检查线路号是否匹配
        line_matched = train_info.line_number == target_line
        
        # 检查是否为共用轨道
        is_shared = train_info.line_number in self.shared_track_config.get(target_line, [])
        
        # 检查是否经过目标站点（简化：假设线路匹配即经过）
        passes_target = line_matched
        
        if not line_matched and not is_shared:
            return {
                "status": TrainStatus.WRONG_LINE.value,
                "matched": False,
                "message": f"这趟{train_info.line_number}不经过{target_station}，请等待下一班{target_line}列车。",
                "confidence": 0.9,
                "train_line": train_info.line_number,
                "target_line": target_line
            }
        
        if is_shared:
            return {
                "status": TrainStatus.SHARED_TRACK.value,
                "matched": True,
                "message": f"这趟列车与{target_line}共用轨道，可以乘坐。",
                "confidence": 0.85,
                "train_line": train_info.line_number,
                "target_line": target_line
            }
        
        if not passes_target:
            return {
                "status": TrainStatus.WRONG_LINE.value,
                "matched": False,
                "message": f"这趟列车不经过{target_station}，请等待下一班列车。",
                "confidence": 0.8,
                "train_line": train_info.line_number,
                "target_line": target_line
            }
        
        return {
            "status": TrainStatus.MATCHED.value,
            "matched": True,
            "message": None,  # 匹配成功，无需播报
            "confidence": 0.95,
            "train_line": train_info.line_number,
            "target_line": target_line
        }
    
    def _parse_train_info(self, text: str) -> Optional[TrainInfo]:
        """
        从文字中解析列车信息
        
        Args:
            text: OCR识别的文字
        
        Returns:
            Optional[TrainInfo]: 解析的列车信息
        """
        # 匹配线路号模式
        line_patterns = [
            r'(\d+)号线',
            r'Line\s*(\d+)',
            r'L(\d+)'
        ]
        
        line_number = None
        for pattern in line_patterns:
            match = re.search(pattern, text)
            if match:
                line_number = f"{match.group(1)}号线"
                break
        
        if not line_number:
            return None
        
        # 提取终点站（简化处理）
        destination = "未知"
        destination_patterns = [
            r'往([^，,。\s]+)',
            r'至([^，,。\s]+)',
            r'开往([^，,。\s]+)'
        ]
        
        for pattern in destination_patterns:
            match = re.search(pattern, text)
            if match:
                destination = match.group(1).strip()
                break
        
        return TrainInfo(
            line_number=line_number,
            destination=destination,
            shared_tracks=self.shared_track_config.get(line_number, [])
        )


# 全局列车识别器实例
_global_train_identifier: Optional[TrainIdentifier] = None


def get_train_identifier() -> TrainIdentifier:
    """获取全局列车识别器实例"""
    global _global_train_identifier
    if _global_train_identifier is None:
        _global_train_identifier = TrainIdentifier()
    return _global_train_identifier


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("=" * 70)
    print("🚇 列车识别器测试")
    print("=" * 70)
    
    identifier = get_train_identifier()
    
    # 测试1: 线路匹配
    print("\n1. 测试线路匹配...")
    result1 = identifier.identify_train("2号线 往中山公园", "2号线", "虹口医院")
    print(f"   状态: {result1['status']}")
    if result1['message']:
        print(f"   消息: {result1['message']}")
    
    # 测试2: 线路不匹配
    print("\n2. 测试线路不匹配...")
    result2 = identifier.identify_train("10号线 往新江湾城", "2号线", "虹口医院")
    print(f"   状态: {result2['status']}")
    if result2['message']:
        print(f"   消息: {result2['message']}")
    
    print("\n" + "=" * 70)
