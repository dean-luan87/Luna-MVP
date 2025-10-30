#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 用户地点纠错与补全机制
允许用户更正视觉识别结果，系统长期保存
"""

import logging
import json
import time
import os
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import hashlib
from collections import defaultdict

logger = logging.getLogger(__name__)

class CorrectionMethod(Enum):
    """纠错方式"""
    VOICE = "voice"               # 语音输入
    INTERFACE = "interface"       # 界面输入
    GPS_BASED = "gps_based"       # GPS纠正

class TrustLevel(Enum):
    """可信度等级"""
    USER_FEEDBACK = "user_feedback"     # 单次用户反馈
    VERIFIED = "verified"                # 已验证（多次反馈）
    TRUSTED = "trusted"                  # 可信（系统确认）

@dataclass
class LocationCorrection:
    """地点纠错记录"""
    original_name: str                    # 原始识别名称
    corrected_name: str                   # 用户更正名称
    gps_location: Dict[str, float]        # GPS位置
    timestamp: float                      # 纠错时间戳
    correction_method: str                # 纠错方式
    user_id: Optional[str]                # 用户ID（可选）
    trust_level: str                      # 可信度等级
    corrections_count: int                # 纠错次数
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return asdict(self)
    
    def to_json(self) -> str:
        """转换为JSON字符串"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)

@dataclass
class LocationMapping:
    """地点映射关系"""
    location_key: str                     # 地点唯一标识
    original_name: str                    # 原始名称
    corrected_name: str                   # 更正后名称
    gps_center: Dict[str, float]          # GPS中心点
    correction_count: int                 # 纠错次数
    unique_users: int                     # 不同用户数
    trust_level: str                      # 可信度
    last_update: float                    # 最后更新时间
    active: bool                          # 是否有效
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return asdict(self)

class LocationCorrectionManager:
    """地点纠错管理器"""
    
    def __init__(self, storage_file: str = "data/location_corrections.json"):
        """
        初始化地点纠错管理器
        
        Args:
            storage_file: 数据存储文件
        """
        self.storage_file = storage_file
        self.corrections: List[LocationCorrection] = []
        self.location_mappings: Dict[str, LocationMapping] = {}
        
        # 按GPS区域存储纠错记录（用于快速查找）
        self.gps_index: Dict[str, List[LocationCorrection]] = defaultdict(list)
        
        # 可信修正阈值
        self.trust_threshold = 3  # 需要3次不同用户反馈
        
        self.logger = logging.getLogger(__name__)
        self._load_data()
        self.logger.info("📍 地点纠错管理器初始化完成")
    
    def submit_correction(self, original_name: str, corrected_name: str,
                         latitude: float, longitude: float,
                         correction_method: str = "voice",
                         user_id: Optional[str] = None) -> LocationCorrection:
        """
        提交地点纠错
        
        Args:
            original_name: 原始识别名称
            corrected_name: 用户更正名称
            latitude: 纬度
            longitude: 经度
            correction_method: 纠错方式
            user_id: 用户ID
            
        Returns:
            LocationCorrection: 纠错记录
        """
        # 创建纠错记录
        correction = LocationCorrection(
            original_name=original_name,
            corrected_name=corrected_name,
            gps_location={"latitude": latitude, "longitude": longitude},
            timestamp=time.time(),
            correction_method=correction_method,
            user_id=user_id,
            trust_level=TrustLevel.USER_FEEDBACK.value,
            corrections_count=1
        )
        
        # 添加到记录列表
        self.corrections.append(correction)
        
        # 更新地点映射
        location_key = self._generate_location_key(original_name, latitude, longitude)
        self._update_location_mapping(location_key, correction)
        
        # 添加到GPS索引
        gps_key = self._round_gps(latitude, longitude)
        self.gps_index[gps_key].append(correction)
        
        # 检查是否需要提升可信度
        self._update_trust_level(location_key)
        
        # 保存数据
        self._save_data()
        
        self.logger.info(f"✅ 地点纠错已记录: {original_name} -> {corrected_name}")
        
        return correction
    
    def get_corrected_name(self, original_name: str, latitude: float, longitude: float) -> Optional[str]:
        """
        获取更正后的地点名称
        
        Args:
            original_name: 原始识别名称
            latitude: 纬度
            longitude: 经度
            
        Returns:
            str: 更正后的名称，如果没有则返回None
        """
        location_key = self._generate_location_key(original_name, latitude, longitude)
        
        if location_key in self.location_mappings:
            mapping = self.location_mappings[location_key]
            
            # 优先使用可信修正
            if mapping.trust_level in [TrustLevel.VERIFIED.value, TrustLevel.TRUSTED.value]:
                return mapping.corrected_name
            
            # 其次使用有多次反馈的
            if mapping.correction_count >= 2:
                return mapping.corrected_name
        
        return None
    
    def get_nearby_corrections(self, latitude: float, longitude: float, 
                               radius: float = 0.001) -> List[LocationCorrection]:
        """
        获取附近的纠错记录
        
        Args:
            latitude: 纬度
            longitude: 经度
            radius: 搜索半径（度）
            
        Returns:
            List[LocationCorrection]: 附近的纠错记录
        """
        nearby_corrections = []
        
        # 搜索附近的GPS网格
        gps_key = self._round_gps(latitude, longitude)
        search_keys = [
            gps_key,
            f"{float(gps_key.split(',')[0]) + 0.001:.3f},{float(gps_key.split(',')[1]) + 0.001:.3f}",
            f"{float(gps_key.split(',')[0]) - 0.001:.3f},{float(gps_key.split(',')[1]) - 0.001:.3f}"
        ]
        
        for key in search_keys:
            if key in self.gps_index:
                nearby_corrections.extend(self.gps_index[key])
        
        # 过滤距离
        filtered = []
        for correction in nearby_corrections:
            dist = self._calculate_distance(
                latitude, longitude,
                correction.gps_location["latitude"],
                correction.gps_location["longitude"]
            )
            # 转换为米
            dist_meters = dist * 111000  # 大约1度=111km
            
            # 检查是否在半径内（默认100米）
            if dist_meters < 100:
                filtered.append(correction)
        
        return filtered
    
    def _update_location_mapping(self, location_key: str, correction: LocationCorrection):
        """更新地点映射"""
        if location_key not in self.location_mappings:
            # 创建新映射
            self.location_mappings[location_key] = LocationMapping(
                location_key=location_key,
                original_name=correction.original_name,
                corrected_name=correction.corrected_name,
                gps_center=correction.gps_location,
                correction_count=1,
                unique_users=1 if correction.user_id else 0,
                trust_level=TrustLevel.USER_FEEDBACK.value,
                last_update=correction.timestamp,
                active=True
            )
        else:
            # 更新现有映射
            mapping = self.location_mappings[location_key]
            mapping.correction_count += 1
            mapping.last_update = correction.timestamp
            mapping.active = True
            
            # 更新GPS中心（取平均值）
            lat1, lon1 = mapping.gps_center["latitude"], mapping.gps_center["longitude"]
            lat2, lon2 = correction.gps_location["latitude"], correction.gps_location["longitude"]
            n = mapping.correction_count
            
            mapping.gps_center = {
                "latitude": (lat1 * (n-1) + lat2) / n,
                "longitude": (lon1 * (n-1) + lon2) / n
            }
            
            # 更新不同用户数
            if correction.user_id and correction.user_id not in self._get_user_ids(location_key):
                mapping.unique_users += 1
    
    def _update_trust_level(self, location_key: str):
        """更新可信度等级"""
        if location_key not in self.location_mappings:
            return
        
        mapping = self.location_mappings[location_key]
        
        # 根据纠错次数和不同用户数提升可信度
        if mapping.unique_users >= 3:
            mapping.trust_level = TrustLevel.TRUSTED.value
        elif mapping.correction_count >= self.trust_threshold:
            mapping.trust_level = TrustLevel.VERIFIED.value
        elif mapping.correction_count >= 2:
            mapping.trust_level = TrustLevel.VERIFIED.value
    
    def _get_user_ids(self, location_key: str) -> List[str]:
        """获取该地点的所有用户ID"""
        user_ids = []
        for correction in self.corrections:
            loc_key = self._generate_location_key(
                correction.original_name,
                correction.gps_location["latitude"],
                correction.gps_location["longitude"]
            )
            if loc_key == location_key and correction.user_id:
                user_ids.append(correction.user_id)
        return list(set(user_ids))
    
    def _generate_location_key(self, name: str, latitude: float, longitude: float) -> str:
        """生成地点唯一标识"""
        # 使用名称和GPS的组合生成唯一ID
        rounded_lat = round(latitude, 4)
        rounded_lon = round(longitude, 4)
        key_data = f"{name}_{rounded_lat}_{rounded_lon}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def _round_gps(self, latitude: float, longitude: float) -> str:
        """将GPS坐标四舍五入到0.001度（约100米）"""
        return f"{round(latitude, 3)},{round(longitude, 3)}"
    
    def _calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """计算GPS距离（度）"""
        return ((lat2 - lat1)**2 + (lon2 - lon1)**2) ** 0.5
    
    def _load_data(self):
        """加载数据"""
        try:
            os.makedirs(os.path.dirname(self.storage_file), exist_ok=True)
            if os.path.exists(self.storage_file):
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    # 加载纠错记录
                    for correction_data in data.get('corrections', []):
                        correction = LocationCorrection(**correction_data)
                        self.corrections.append(correction)
                        
                        # 添加到GPS索引
                        gps_key = self._round_gps(
                            correction.gps_location["latitude"],
                            correction.gps_location["longitude"]
                        )
                        self.gps_index[gps_key].append(correction)
                    
                    # 加载地点映射
                    for mapping_data in data.get('mappings', []):
                        mapping = LocationMapping(**mapping_data)
                        self.location_mappings[mapping.location_key] = mapping
                    
                    self.logger.info(f"📂 加载了 {len(self.corrections)} 条纠错记录")
        except Exception as e:
            self.logger.error(f"❌ 加载数据失败: {e}")
    
    def _save_data(self):
        """保存数据"""
        try:
            data = {
                'corrections': [correction.to_dict() for correction in self.corrections[-1000:]],  # 保留最近1000条
                'mappings': [mapping.to_dict() for mapping in self.location_mappings.values()]
            }
            
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            self.logger.info("💾 数据已保存")
        except Exception as e:
            self.logger.error(f"❌ 保存数据失败: {e}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        verified_count = sum(1 for m in self.location_mappings.values() 
                           if m.trust_level == TrustLevel.VERIFIED.value)
        trusted_count = sum(1 for m in self.location_mappings.values() 
                           if m.trust_level == TrustLevel.TRUSTED.value)
        
        return {
            "total_corrections": len(self.corrections),
            "total_mappings": len(self.location_mappings),
            "verified_mappings": verified_count,
            "trusted_mappings": trusted_count,
            "avg_corrections_per_location": len(self.corrections) / len(self.location_mappings) if self.location_mappings else 0
        }
    
    def export_for_training(self) -> List[Dict[str, Any]]:
        """
        导出纠错数据用于聚合训练
        
        Returns:
            List[Dict[str, Any]]: 训练数据
        """
        training_data = []
        
        for mapping in self.location_mappings.values():
            if mapping.trust_level in [TrustLevel.VERIFIED.value, TrustLevel.TRUSTED.value]:
                training_data.append({
                    "original_name": mapping.original_name,
                    "corrected_name": mapping.corrected_name,
                    "gps_location": mapping.gps_center,
                    "correction_count": mapping.correction_count,
                    "trust_level": mapping.trust_level
                })
        
        return training_data


# 全局管理器实例
global_location_correction_manager = LocationCorrectionManager()

def submit_correction(original_name: str, corrected_name: str, latitude: float, longitude: float) -> LocationCorrection:
    """提交纠错的便捷函数"""
    return global_location_correction_manager.submit_correction(
        original_name, corrected_name, latitude, longitude
    )


if __name__ == "__main__":
    # 测试地点纠错管理器
    import logging
    logging.basicConfig(level=logging.INFO)
    
    # 创建管理器
    manager = LocationCorrectionManager('data/test_location_corrections.json')
    
    # 模拟用户纠错
    print("=" * 60)
    print("📍 地点纠错测试")
    print("=" * 60)
    
    # 场景1: 用户更正洗手间名称
    print("\n场景1: 更正洗手间名称")
    correction = manager.submit_correction(
        original_name="洗手间",
        corrected_name="商场洗手间A",
        latitude=39.9040,
        longitude=116.4070,
        correction_method="voice",
        user_id="user_001"
    )
    print(f"纠错记录: {correction.original_name} -> {correction.corrected_name}")
    
    # 场景2: 另一个用户也更正相同地点
    print("\n场景2: 第二个用户确认")
    manager.submit_correction(
        original_name="洗手间",
        corrected_name="商场洗手间A",
        latitude=39.9040,
        longitude=116.4070,
        correction_method="voice",
        user_id="user_002"
    )
    
    # 场景3: 第三个用户确认（提升为可信）
    print("\n场景3: 第三个用户确认（提升可信度）")
    manager.submit_correction(
        original_name="洗手间",
        corrected_name="商场洗手间A",
        latitude=39.9040,
        longitude=116.4070,
        correction_method="interface",
        user_id="user_003"
    )
    
    # 获取更正后的名称
    print("\n📋 测试获取更正名称:")
    corrected = manager.get_corrected_name("洗手间", 39.9040, 116.4070)
    print(f"原始: 洗手间 -> 更正后: {corrected}")
    
    # 获取统计信息
    print("\n📊 统计信息:")
    stats = manager.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # 导出训练数据
    print("\n🎓 导出训练数据:")
    training_data = manager.export_for_training()
    print(f"可信修正数据: {len(training_data)} 条")
    for data in training_data:
        print(f"  - {data['original_name']} -> {data['corrected_name']} (信任度: {data['trust_level']})")
    
    print("\n" + "=" * 60)
